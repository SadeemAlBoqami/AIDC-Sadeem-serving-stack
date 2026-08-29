FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir torch==2.4.1 --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir \
    fastapi==0.115.0 \
    uvicorn==0.30.6 \
    transformers==4.45.1 \
    accelerate==0.34.2

COPY app/ ./app/

ENV MODEL_ID="Qwen/Qwen2.5-0.5B-Instruct"
ENV HOST_PORT=8000
ENV MAX_TOKENS=256

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]