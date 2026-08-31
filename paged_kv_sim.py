import json
import random

# Step 1: KV Cost & Block Constants
def kv_kb_per_token(layers=28, kv_heads=2, head_dim=128, dbytes=2):
  return 2 * layers * kv_heads * head_dim * dbytes / 1024  # ~28 KB for Qwen2.5-1.5B


KB_PER_TOKEN = kv_kb_per_token()
BLOCK_TOKENS = 16
BLOCK_KB = BLOCK_TOKENS * KB_PER_TOKEN
print(f"KB per token: {KB_PER_TOKEN}   KB per block: {BLOCK_KB}")


# Step 2: The Naive Slab Allocator
class SlabAllocator:

  def __init__(self, budget_kb, max_len=4096):
    self.budget_kb = budget_kb
    self.max_len = max_len
    self.used_kb = 0
    self.resident = {}  # seq_id -> reserved_kb

  def admit(self, seq_id):
    need = self.max_len * KB_PER_TOKEN
    if self.used_kb + need > self.budget_kb:
      return False
    self.used_kb += need
    self.resident[seq_id] = need
    return True

  def complete(self, seq_id):
    self.used_kb -= self.resident.pop(seq_id)


# Step 3: The Block-Pool Allocator (Mini-PagedAttention)
class BlockPoolAllocator:

  def __init__(self, budget_kb, block_kb=BLOCK_KB):
    self.block_kb = block_kb
    self.total_blocks = int(budget_kb // block_kb)
    self.free_blocks = self.total_blocks
    self.block_tables = {}  # seq_id -> list of block ids (count only here)

  def admit(self, seq_id):
    if self.free_blocks < 1:
      return False
    self.free_blocks -= 1
    self.block_tables[seq_id] = 1
    return True

  def grow(self, seq_id, current_len_tokens):
    needed_blocks = -(-current_len_tokens // BLOCK_TOKENS)  # ceiling division
    held = self.block_tables[seq_id]
    if needed_blocks > held:
      extra = needed_blocks - held
      if self.free_blocks < extra:
        return False  # Blocked: pool is full
      self.free_blocks -= extra
      self.block_tables[seq_id] = needed_blocks
    return True

  def complete(self, seq_id):
    self.free_blocks += self.block_tables.pop(seq_id)


# Step 4: Synthetic Workload Generation
random.seed(7)


def make_workload(n_sequences=60, max_len=4096):
  lengths = []
  for _ in range(n_sequences):
    if random.random() < 0.85:
      lengths.append(random.randint(50, 400))  # Common case
    else:
      lengths.append(random.randint(2000, max_len))  # Occasional straggler
  return lengths


WORKLOAD = make_workload()
print(
    f"mean length: {sum(WORKLOAD) / len(WORKLOAD):.1f}  max: {max(WORKLOAD)}"
)


# Step 5: Simulation Execution
def simulate_slab(budget_kb, workload):
  alloc = SlabAllocator(budget_kb)
  admitted, rejected = 0, 0
  for i, length in enumerate(workload):
    if alloc.admit(seq_id=i):
      admitted += 1
    else:
      rejected += 1
  return {"peak_concurrent": admitted, "admitted": admitted, "rejected": rejected}


def simulate_blockpool(budget_kb, workload):
  alloc = BlockPoolAllocator(budget_kb)
  admitted, rejected = 0, 0
  for i, length in enumerate(workload):
    if not alloc.admit(seq_id=i):
      rejected += 1
      continue
    grew = True
    for step_len in range(BLOCK_TOKENS, length + BLOCK_TOKENS, BLOCK_TOKENS):
      if not alloc.grow(seq_id=i, current_len_tokens=min(step_len, length)):
        grew = False
        break
    if grew:
      admitted += 1
    else:
      alloc.complete(seq_id=i)
      rejected += 1
  return {"peak_concurrent": admitted, "admitted": admitted, "rejected": rejected}


BUDGET_KB = 2 * 1024 * 1024  # 2 GB in KB
slab_result = simulate_slab(BUDGET_KB, WORKLOAD)
blockpool_result = simulate_blockpool(BUDGET_KB, WORKLOAD)

print("slab:      ", slab_result)
print("block-pool:", blockpool_result)


# Step 6: Write Report
report = {
    "kb_per_token": KB_PER_TOKEN,
    "block_tokens": BLOCK_TOKENS,
    "budget_kb": BUDGET_KB,
    "workload_mean_len": sum(WORKLOAD) / len(WORKLOAD),
    "slab": slab_result,
    "blockpool": blockpool_result,
    "blockpool_advantage": round(
        blockpool_result["peak_concurrent"] / slab_result["peak_concurrent"], 2
    ),
}

with open("kv_sim_report.json", "w") as f:
  json.dump(report, f, indent=2)

print(json.dumps(report, indent=2))
