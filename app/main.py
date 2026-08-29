import os
import sys
import time
import uuid
import logging
import torch
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from transformers import AutoModelForCausalLM, AutoTokenizer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("serving")

MODEL_ID = os.environ.get("MODEL_ID", "Qwen/Qwen2.5-0.5B-Instruct")
API_KEY = os.environ.get("API_KEY", "")
MAX_TOKENS = int(os.environ.get("MAX_TOKENS", "256"))

if not API_KEY:
    logger.warning("WARNING: API_KEY is unset. Running unauthenticated (open).")

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"loading {MODEL_ID} on {DEVICE} ...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
    device_map="auto" if DEVICE == "cuda" else None
)
if DEVICE == "cpu":
    model.to("cpu")
print("model ready")

app = FastAPI(title="aidc-serving")

def verify_api_key(authorization: Optional[str] = Header(None)):
    if not API_KEY:
        return
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized: Missing or invalid Bearer token")
    token = authorization.split(" ")[1]
    if token != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API key")

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: Optional[str] = MODEL_ID
    messages: List[ChatMessage]
    max_tokens: Optional[int] = Field(default=16)
    temperature: Optional[float] = 0.7

@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL_ID}

@app.get("/v1/models", dependencies=[Depends(verify_api_key)])
def list_models():
    return {
        "object": "list",
        "data": [
            {
                "id": MODEL_ID,
                "object": "model",
                "created": int(time.time()),
                "owned_by": "aidc"
            }
        ]
    }

@app.post("/v1/chat/completions", dependencies=[Depends(verify_api_key)])
def chat_completions(req: ChatCompletionRequest):
    clamped_tokens = min(req.max_tokens if req.max_tokens else 16, MAX_TOKENS)

    text = tokenizer.apply_chat_template(
        [m.model_dump() for m in req.messages],
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(DEVICE)

    with torch.no_grad():
        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=clamped_tokens,
            do_sample=False if req.temperature == 0 else True,
            temperature=req.temperature if req.temperature > 0 else None
        )

    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    response_text = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return {
        "id": f"chatcmpl-{uuid.uuid4().hex[:8]}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": req.model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response_text
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": len(model_inputs.input_ids[0]),
            "completion_tokens": len(generated_ids[0]),
            "total_tokens": len(model_inputs.input_ids[0]) + len(generated_ids[0])
        }
    }
