#!/bin/bash
cd /home/adam/av-app/temp/arc_simulation
echo "🚀 Starting Artifact Virtual Multi-ARC Network Dashboard..."
venv/bin/streamlit run streamlit_dashboard.py --server.port 8501 --server.address 0.0.0.0
