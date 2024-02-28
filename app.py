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
        city_name = request.form.get('city_name', '').strip()
        form_start_date = request.form.get('start_date')
        if form_start_date:
            start_date = form_start_date

    city_name = city_name.lower()
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    # Adjusted list comprehension to handle None values in 'Location'
    filtered_events = [
        event for event in events_data 
        if datetime.utcfromtimestamp(event['Date'] / 1000) >= start_date_obj 
        and (not city_name or city_name in (event.get('Location') or '').lower())
    ]

    city_name = city_name.capitalize() if city_name else "All Cities"
    return render_template('index.html', events_data=filtered_events, city_name=city_name, start_date=start_date)


@app.route('/event-details/<city>/<team>/<event_id>')
def event_details(city, team, event_id):
    # Ensure city parameter is correctly formatted with underscores
    formatted_city = city.replace(" ", "_")
    team_data_file_path = os.path.join('data', formatted_city, f'{team}.json')
    
    # Attempt to load the team data JSON file
    try:
        with open(team_data_file_path, 'r') as file:
            team_data = json.load(file)
    except FileNotFoundError:
        abort(404)  # File not found
    except json.JSONDecodeError:
        abort(500)  # JSON syntax error in the file

    # Load event data
    events_data = load_events_data()
    event = next((event for event in events_data if str(event['EventID']) == event_id), None)
    if event is None:
        abort(404)  # Event not found

    
    # Prepare seating options and savings tips for rendering
    seating_options_tips = team_data.get('venue', {}).get('best_seats_pricing', {})

    return render_template('event_details.html', event=event, team_data=team_data, city=city.replace("_", " "), seating_options_tips=seating_options_tips)



if __name__ == '__main__':
    app.run(debug=True)
