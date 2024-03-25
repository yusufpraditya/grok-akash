import torch
from transformers import AutoModelForCausalLM
from sentencepiece import SentencePieceProcessor
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from huggingface_hub import snapshot_download
import os
import time

MAX_NEW_TOKENS = int(os.environ.get("MAX_NEW_TOKENS", 100))

is_downloaded = False

while not is_downloaded:
  try:
    snapshot_download(repo_id="hpcai-tech/grok-1", local_dir="hpcai-tech/grok-1", local_dir_use_symlinks=False, resume_download=True, max_workers=64, revision="d34f045119ab9a385517721dbdb40ba2036a5d60")

    bin_files = [file for file in os.listdir("./hpcai-tech/grok-1") if file.lower().endswith('.bin')]

    if len(bin_files) == 65:
      is_downloaded = True
      print("Download finished. Checkpoints will be loaded and takes about 10 minutes.")
      print("If after 10 minutes it still looks 'stuck', try reloading Cloudmos.")
  except Exception as error:
    print(error)
    print("Retrying..")
    time.sleep(5)

torch.set_default_dtype(torch.bfloat16)
model = AutoModelForCausalLM.from_pretrained(
    "./hpcai-tech/grok-1",
    trust_remote_code=True,
    device_map="auto",
    torch_dtype=torch.bfloat16,
    local_files_only=True
)
sp = SentencePieceProcessor(model_file="tokenizer.model")

app = FastAPI()

@app.get("/infer")
def inference(input):
  try:
    input_ids = sp.encode(input)
    input_ids = torch.tensor([input_ids]).cuda()
    attention_mask = torch.ones_like(input_ids)

    generate_kwargs = {
      "max_new_tokens": MAX_NEW_TOKENS
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

app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
def index() -> FileResponse:
  return FileResponse(path="/app/static/index.html", media_type="text/html")