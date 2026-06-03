#!/bin/bash
cd "$(dirname "$0")"
chmod +x serve.sh 2>/dev/null
exec ./serve.sh
