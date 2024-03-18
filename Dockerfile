FROM nvidia/cuda:12.3.2-cudnn9-runtime-ubuntu22.04

RUN apt-get -y update && apt-get upgrade -y
RUN apt-get install pip

RUN pip install dm_haiku==0.0.12
RUN pip install -U "jax[cuda12_pip]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
RUN pip install numpy==1.26.4
RUN pip install sentencepiece==0.2.0
