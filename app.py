from flask import Flask, render_template, request
from flask_cors import CORS
from openai import OpenAI
import json
import os

client = OpenAI(api_key='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')

app = Flask(__name__)
CORS(app)

def get_sports_teams_info(city_name):
    try:
        file_path = os.path.join('data', city_name, f'{city_name}.json')
        with open(file_path, 'r') as file:
            city_json = json.load(file)
            # Assuming 'response' contains a JSON string that needs parsing
            city_data = json.loads(city_json['response'])
        return city_data
    except Exception as e:
        print(f"An error occurred for city {city_name}: {e}")
        return None


def read_city_data(city_name):
    file_path = os.path.join('data', city_name, f'{city_name}.json')
    try:
        with open(file_path, 'r') as file:
            city_data = json.load(file)
        return city_data  # Directly return the parsed JSON data
    except FileNotFoundError:
        return None


@app.route('/', methods=['GET', 'POST'])
def home():
    city_data = None
    if request.method == 'POST':
        city_name = request.form.get('city_name')
        if city_name:
            # Replace spaces with underscores to match file naming convention
            city_name_normalized = city_name.replace(" ", "_").capitalize()
            city_data = read_city_data(city_name_normalized)
    return render_template('index.html', city_data=city_data)


if __name__ == '__main__':
    app.run(debug=True)
