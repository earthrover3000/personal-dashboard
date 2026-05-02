#!/bin/bash
python3 "$(dirname "$0")/../../src/push.py" "$@"
echo "Script location: $(realpath "$0")"
read -rp "Press Enter to continue..."
