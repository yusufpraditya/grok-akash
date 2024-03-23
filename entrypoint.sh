#!/bin/bash

huggingface-cli download hpcai-tech/grok-1 --repo-type model --local-dir hpcaitech/grok-1 --local-dir-use-symlinks False
pip install accelerate

gotty -w "python entrypoint.py"
