import torch
from transformers import AutoModelForCausalLM
from sentencepiece import SentencePieceProcessor
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

print("It will take 5-10 minutes to load checkpoints.")

torch.set_default_dtype(torch.bfloat16)
model = AutoModelForCausalLM.from_pretrained(
    "grok-1",
    trust_remote_code=True,
    device_map="auto",
    torch_dtype=torch.bfloat16,
)
sp = SentencePieceProcessor(model_file="tokenizer.model")

app = FastAPI()

app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/infer_t5")
def t5(text):
  try:
    input_ids = sp.encode(text)
    input_ids = torch.tensor([input_ids]).cuda()
    attention_mask = torch.ones_like(input_ids)

    generate_kwargs = {
      "max_new_tokens": 64
    }

    inputs = {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        **generate_kwargs,
    }
    outputs = model.generate(**inputs)

    decoded_output = sp.decode(outputs[0].cpu().tolist())

    return { "output": decoded_output }
  except:
    return { "output": "Error. Try again!" }

@app.get("/")
def index() -> FileResponse:
  return FileResponse(path="/app/static/index.html", media_type="text/html")