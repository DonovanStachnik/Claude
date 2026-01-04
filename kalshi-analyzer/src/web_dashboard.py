"""
Web Dashboard for Kalshi Opportunities
Clean interface showing best bets in real-time
"""

from flask import Flask, render_template, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
import glob

app = Flask(__name__)
CORS(app)

DATA_DIR = '../data'

def get_latest_opportunities():
    """Load most recent opportunities from data directory"""
    try:
        # Find most recent opportunities file
        files = glob.glob(f'{DATA_DIR}/opportunities_*.json')
        if not files:
            return {
                'timestamp': None,
                'opportunities': [],
                'total': 0
            }

        latest_file = max(files, key=os.path.getctime)

        with open(latest_file, 'r') as f:
            data = json.load(f)

        return data

    except Exception as e:
        print(f"Error loading opportunities: {e}")
        return {
            'timestamp': None,
            'opportunities': [],
            'total': 0,
            'error': str(e)
        }

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/opportunities')
def get_opportunities():
    """API endpoint for opportunities data"""
    data = get_latest_opportunities()
    return jsonify(data)

@app.route('/api/stats')
def get_stats():
    """API endpoint for summary statistics"""
    data = get_latest_opportunities()

    if not data['opportunities']:
        return jsonify({
            'total_markets': 0,
            'total_opportunities': 0,
            'strong_buy': 0,
            'buy': 0,
            'avg_edge': 0,
            'categories': {}
        })

    opportunities = data['opportunities']

    # Calculate stats
    strong_buy = sum(1 for o in opportunities if o['analysis']['recommendation'] == 'STRONG_BUY')
    buy = sum(1 for o in opportunities if o['analysis']['recommendation'] == 'BUY')

    edges = [o['analysis']['edge'] for o in opportunities]
    avg_edge = sum(edges) / len(edges) if edges else 0

    # Category breakdown
    categories = {}
    for o in opportunities:
        cat = o['analysis'].get('category', 'other')
        categories[cat] = categories.get(cat, 0) + 1

    return jsonify({
        'total_opportunities': len(opportunities),
        'strong_buy': strong_buy,
        'buy': buy,
        'avg_edge': round(avg_edge, 2),
        'categories': categories,
        'last_update': data.get('timestamp')
    })

if __name__ == '__main__':
    # Create templates directory
    os.makedirs('templates', exist_ok=True)

    print("=" * 60)
    print("KALSHI DASHBOARD STARTING")
    print("=" * 60)
    print("\nOpen your browser to: http://localhost:5000")
    print("\nPress Ctrl+C to stop")
    print("=" * 60)

    app.run(host='0.0.0.0', port=5000, debug=False)
