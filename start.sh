#!/bin/bash
# Start script for TimeComplexity Analyzer
cd "$(dirname "$0")"
source venv/bin/activate
cd backend
python main.py
