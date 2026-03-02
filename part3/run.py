#!/usr/bin/env python3
"""Entry point for the HBnB application."""
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)  # Different port
