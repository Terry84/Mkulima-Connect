import json
import requests
from flask import Blueprint, render_template, current_app
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    market_prices = []
    # Try to fetch from external API (example API URL)
    api_url = 'https://api.example.com/market_prices'  # Placeholder URL, will fallback to local JSON
    try:
        response = requests.get(api_url, timeout=3)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            market_prices = data
        else:
            market_prices = []
    except Exception:
        # Load from static JSON fallback
        try:
            static_path = os.path.join(current_app.root_path, 'static', 'market_prices.json')
            with open(static_path, 'r', encoding='utf-8') as f:
                market_prices = json.load(f)
        except Exception:
            market_prices = []

    return render_template('index.html', market_prices=market_prices)
