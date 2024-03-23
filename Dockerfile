FROM hpcaitech/colossalai:0.3.0

WORKDIR /

RUN apt-get update && \
    apt-get install pip wget git -y

RUN git clone https://github.com/hpcaitech/ColossalAI.git && \
    cd ColossalAI/examples/language/grok-1 && \
    pip install -r requirements.txt --no-cache-dir && \
    mkdir -p hpcaitech/grok-1

RUN wget https://github.com/xai-org/grok-1/raw/main/tokenizer.model
