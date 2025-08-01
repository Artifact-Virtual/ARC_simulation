#!/bin/bash
cd /home/adam/av-app/temp/arc_simulation
echo "🔴 Starting Live Multi-ARC Stream Dashboard..."
./venv/bin/streamlit run live_stream.py --server.port 8502 --server.address 0.0.0.0
