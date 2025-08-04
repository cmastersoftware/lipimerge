#!/bin/bash

# ============================================================
# Setup Script for LipiMerge Project
#
# Sets up a Python virtual environment and installs dependencies.
# ============================================================

# Sanity check: Ensure the script is run from the project root directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ The pyproject.toml root configuration file not found. Please run this script from the project root directory."
    exit 1
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 to proceed."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip is not installed. Please install pip to proceed."
    exit 1
fi

# Create virtual environment
if [ -d ".venv" ]; then

    read -p "A virtual environment already exists. Do you want to recreate it? (y/n): " choice
    if [[ "$choice" != "y" && "$choice" != "Y" ]]; then
        echo "Exiting without changes."
        exit 0
    fi

    rm -rf .venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to remove existing virtual environment. Please check permissions."
        exit 1
    fi

    echo "Existing virtual environment removed."
fi

echo "Creating a new virtual environment..."
python3 -m venv .venv

if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment."
    exit 1
fi

# Activate it
source .venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment."
    exit 1
fi

# Install dependencies
python3 -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies. Please check your internet connection and/or requirements.txt."
    exit 1
fi

# Done
echo "✅ Environment setup complete."
