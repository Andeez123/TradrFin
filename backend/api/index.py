"""
Vercel Serverless Function Handler
This file adapts the FastAPI app for Vercel's serverless environment.
"""
import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app

# Vercel expects a handler variable
handler = app
