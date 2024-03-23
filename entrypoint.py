import torch
from transformers import AutoModelForCausalLM

torch.set_default_dtype(torch.bfloat16)
model = AutoModelForCausalLM.from_pretrained(
    "hpcaitech/grok-1",
    trust_remote_code=True,
    device_map="auto",
    torch_dtype=torch.bfloat16,
)
sp = SentencePieceProcessor(model_file="tokenizer.model")

while True:
  text = input("Enter the text you want to process: ")
  input_ids = sp.encode(text)
  input_ids = torch.tensor([input_ids]).cuda()
  attention_mask = torch.ones_like(input_ids)
  generate_kwargs = {}  # Add any additional args if you want
  inputs = {
      "input_ids": input_ids,
      "attention_mask": attention_mask,
      **generate_kwargs,
  }
  outputs = model.generate(**inputs)
