import json
import os
from flask import Flask, render_template, request, abort
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Custom Jinja filter for date formatting
def format_date(value, format_string='%Y/%m/%d %H:%M'):
    if isinstance(value, int):
        timestamp = value / 1000
    else:
        timestamp = int(value) / 1000
    return datetime.utcfromtimestamp(timestamp).strftime(format_string)

app.jinja_env.filters['format_date'] = format_date

# Load events data from a JSON file
def load_events_data():
    merged_schedule_file_path = os.path.join('data', 'schedules', 'merged_data_with_ids.json')
    with open(merged_schedule_file_path, 'r') as file:
        return json.load(file)

@app.route('/', methods=['GET', 'POST'])
def home():
    events_data = load_events_data()
    city_name = ""
    start_date = datetime.today().strftime('%Y-%m-%d')

    if request.method == 'POST':
        city_name = request.form.get('city_name', '').strip().lower()
        form_start_date = request.form.get('start_date')
        if form_start_date:
            start_date = form_start_date

    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    filtered_events = [event for event in events_data if datetime.utcfromtimestamp(event['Date'] / 1000) >= start_date_obj and (not city_name or city_name.lower() in event.get('Location', '').lower())]

    city_name = city_name.capitalize() if city_name else "All Cities"
    return render_template('schedule.html', events_data=filtered_events, city_name=city_name, start_date=start_date)

@app.route('/event-details/<event_id>')
def event_details(event_id):
    events_data = load_events_data()
    event = next((event for event in events_data if str(event['EventID']) == event_id), None)
    if event is None:
        abort(404)
    return render_template('event_details.html', event=event)

if __name__ == '__main__':
    app.run(debug=True)
