#!/bin/bash

echo "Installing dependencies"
pip install --upgrade -r requirements.txt
echo "Dependencies installed."
cd knapsackbench
echo "Starting server..."
uvicorn main:app --reload