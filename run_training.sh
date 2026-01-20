#!/bin/bash
cd /Users/armanshaik/Documents/ECO-Q-Net/ECO-Q-Net
/Users/armanshaik/Documents/ECO-Q-Net/.venv/bin/python training/train.py > training.log 2>&1
echo "Training completed. Exit code: $?"
