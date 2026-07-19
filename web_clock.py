#!/usr/bin/env python3
"""
JARVIS Web Clock Interface
Beautiful web dashboard for the digital clock
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from clock import DigitalClock
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Initialize clock
clock = DigitalClock()

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('clock_dashboard.html')

@app.route('/api/clock/all')
def get_all_times():
    """Get times for all timezones"""
    format_24h = request.args.get('format', '12h') == '24h'
    times = clock.get_all_times(format_24h)
    return jsonify(times)

@app.route('/api/clock/<city>')
def get_city_time(city):
    """Get time for specific city"""
    format_24h = request.args.get('format', '12h') == '24h'
    data = clock.get_time_for_city(city, format_24h)
    return jsonify(data)

@app.route('/api/clock/compare')
def compare_times():
    """Compare times between two cities"""
    city1 = request.args.get('city1')
    city2 = request.args.get('city2')
    format_24h = request.args.get('format', '12h') == '24h'
    
    if not city1 or not city2:
        return jsonify({'error': 'Missing city parameters'}), 400
    
    data1 = clock.get_time_for_city(city1, format_24h)
    data2 = clock.get_time_for_city(city2, format_24h)
    diff = clock.time_difference(city1, city2)
    
    return jsonify({
        'city1': data1,
        'city2': data2,
        'difference': diff
    })

@app.route('/api/clock/utc')
def get_utc():
    """Get UTC time"""
    utc_time = clock.get_utc_time()
    return jsonify({
        'time': utc_time.strftime('%H:%M:%S'),
        'date': utc_time.strftime('%A, %B %d, %Y'),
        'timezone': 'UTC'
    })

@app.route('/api/timezone/list')
def list_timezones():
    """List all available timezones"""
    cities = clock.list_available_timezones()
    return jsonify({'cities': cities, 'count': len(cities)})

@app.route('/api/timezone/add', methods=['POST'])
def add_timezone():
    """Add custom timezone"""
    data = request.json
    city = data.get('city')
    timezone = data.get('timezone')
    
    if not city or not timezone:
        return jsonify({'error': 'Missing parameters'}), 400
    
    if clock.add_timezone(city, timezone):
        return jsonify({'success': True, 'message': f'Added {city}'})
    else:
        return jsonify({'error': 'Invalid timezone'}), 400

@app.route('/api/timezone/difference')
def get_difference():
    """Get time difference between cities"""
    city1 = request.args.get('city1')
    city2 = request.args.get('city2')
    
    if not city1 or not city2:
        return jsonify({'error': 'Missing city parameters'}), 400
    
    diff = clock.time_difference(city1, city2)
    return jsonify(diff)

if __name__ == '__main__':
    print("🕐 JARVIS Web Clock starting...")
    print("📱 Open http://localhost:5001 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5001)
