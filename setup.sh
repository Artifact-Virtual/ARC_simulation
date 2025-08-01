#!/bin/bash
# Setup script for Constitutional Simulation Suite


# Create and/or activate virtual environment
if [ -d ".venv" ]; then
    echo "Activating existing virtual environment (.venv)."
    source .venv/bin/activate
else
    echo "Creating virtual environment (.venv)."
    python3 -m venv .venv
    source .venv/bin/activate
fi

# Install requirements
pip install --upgrade pip --break-system-packages
pip install --break-system-packages -r requirements.txt

echo "Setup complete. To activate the environment later, run: source venv/bin/activate"
