#!/bin/bash
python3 "$(dirname "$0")/../../src/serve.py"
echo "Script location: $(realpath "$0")"
read -rp "Press Enter to continue..."
