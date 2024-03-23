FROM ubuntu:22.04

WORKDIR /grok

RUN apt-get update && \
    apt-get install pip wget -y && \
    mkdir -p hpcaitech/grok-1

RUN wget https://github.com/xai-org/grok-1/raw/main/tokenizer.model

COPY . /grok

RUN pip install --no-cache-dir -r /grok/requirements.txt

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]