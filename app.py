from flask import Flask, render_template, request, jsonify
import json
import os
from collections import defaultdict

app = Flask(__name__)

SCHEDULE_FILE = 'schedule.json'

def load_schedule():
    if os.path.exists(SCHEDULE_FILE) and os.path.getsize(SCHEDULE_FILE) > 0:
        with open(SCHEDULE_FILE, 'r') as file:
            try:
                return json.load(file)  # Should be a dictionary
            except json.JSONDecodeError:
                return defaultdict(list)  # Return empty schedule if file is invalid
    return defaultdict(list)

def save_schedule(items):
    with open(SCHEDULE_FILE, 'w') as file:
        json.dump(items, file)

@app.route('/')
def index():
    schedule_items = load_schedule()
    events = []
    for date, items in schedule_items.items():
        for item in items:
            events.append({
                'title': item,
                'start': date,
            })
    return render_template('index.html', items=events)

@app.route('/get_events')
def get_events():
    schedule_items = load_schedule()
    events = []
    for date, items in schedule_items.items():
        for item in items:
            events.append({
                'title': item,
                'start': date,
            })
    return jsonify(events)

@app.route('/add_event', methods=['POST'])
def add_event():
    data = request.get_json()  # Get data from the client
    item = data['title']
    date = data['date']
    
    items = load_schedule()
    if date not in items:
        items[date] = []
    items[date].append(item)
    save_schedule(items)
    
    return '', 204  # Return no content

if __name__ == '__main__':
    app.run(debug=True)