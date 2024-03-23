#!/bin/bash

huggingface-cli download hpcai-tech/grok-1 --repo-type model --local-dir hpcaitech/grok-1 --local-dir-use-symlinks False

uvicorn main:app --host 0.0.0.0 --port 8080