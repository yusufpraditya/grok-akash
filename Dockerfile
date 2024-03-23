FROM ubuntu:22.04

WORKDIR /

RUN apt-get update && \
    apt-get install pip wget git -y

RUN wget https://github.com/yudai/gotty/releases/download/v2.0.0-alpha.3/gotty_2.0.0-alpha.3_linux_amd64.tar.gz && tar -zxvf gotty_2.0.0-alpha.3_linux_amd64.tar.gz && chmod +x gotty && rm -rf gotty_2.0.0-alpha.3_linux_amd64.tar.gz

RUN git clone https://github.com/hpcaitech/ColossalAI.git && \
    cd ColossalAI/examples/language/grok-1 && \
    pip install -r requirements.txt --no-cache-dir && \
    mkdir -p hpcaitech/grok-1

RUN wget https://github.com/xai-org/grok-1/raw/main/tokenizer.model

WORKDIR /ColossalAI/examples/language/grok-1

ADD entrypoint.sh
ADD entrypoint.py

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
