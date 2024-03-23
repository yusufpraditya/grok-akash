#!/bin/bash

huggingface-cli download hpcai-tech/grok-1 --repo-type model --local-dir hpcaitech/grok-1 --local-dir-use-symlinks False

pip install accelerate

cd /ColossalAI/examples/language/grok-1

gotty -w "python entrypoint.py"
