FROM nvidia/cuda:12.3.2-cudnn9-devel-ubuntu22.04

RUN apt-get update && \
    apt-get install pip wget git -y

RUN git clone https://github.com/hpcaitech/ColossalAI.git && \
    cd ColossalAI && \
    pip install --no-cache-dir . && \
    BUILD_EXT=1 pip install --no-cache-dir .

RUN cd examples/language/grok-1 && \
    pip install -r requirements.txt --no-cache-dir && \
    mkdir -p hpcaitech/grok-1

RUN wget https://github.com/xai-org/grok-1/raw/main/tokenizer.model
