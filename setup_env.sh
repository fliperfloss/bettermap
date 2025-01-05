#!/bin/bash

# Set up Python virtual environment and install dependencies
echo "Setting up Python virtual environment..."

# Step 1: Create virtual environment
python3 -m venv venv

# Step 2: Activate virtual environment (Linux/macOS)
# For Windows, use .\venv\Scripts\activate
source venv/bin/activate

# Step 3: Install dependencies from requirements.txt
echo "Installing dependencies..."
pip install -r requirements.txt

# Step 4: Run the setup script (if you have one)
python3 setup.py install

echo "Setup complete. Your environment is ready!"
