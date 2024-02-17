import pandas as pd

df = pd.read_excel('NBA_SCHEDULE_2024.xlsx')
#print(df.head())

arenas = {
    'TD Garden': 'Boston, MA',
    'Madison Square Garden (IV)': 'New York, NY',
    'FedEx Forum': 'Memphis, TN',
    'Delta Center': 'Salt Lake City, UT', # Note: Now known as Vivint Arena
    'Little Caesars Arena': 'Detroit, MI',
    'Capital One Arena': 'Washington, DC',
    'State Farm Arena': 'Atlanta, GA',
    'Gainbridge Fieldhouse': 'Indianapolis, IN',
    'Toyota Center': 'Houston, TX',
    'Target Center': 'Minneapolis, MN',
    'Paycom Center': 'Oklahoma City, OK',
    'Frost Bank Center': 'Corpus Christi, TX', # Assuming context; might not be a major sports arena
    'Ball Arena': 'Denver, CO',
    'Wells Fargo Center': 'Philadelphia, PA',
    'United Center': 'Chicago, IL',
    'American Airlines Center': 'Dallas, TX',
    'Spectrum Center': 'Charlotte, NC',
    'Kaseya Center': 'Miami, FL', # Note: Assuming a recent name change; historically known as American Airlines Arena
    'Rocket Mortgage FieldHouse': 'Cleveland, OH',
    'Barclays Center': 'Brooklyn, NY',
    'Smoothie King Center': 'New Orleans, LA',
    'Footprint Center': 'Phoenix, AZ',
    'Crypto.com Arena': 'Los Angeles, CA', # Formerly Staples Center
    'Golden 1 Center': 'Sacramento, CA',
    'Amway Center': 'Orlando, FL',
    'Fiserv Forum': 'Milwaukee, WI',
    'Moda Center': 'Portland, OR',
    'Scotiabank Arena': 'Toronto, ON', # Note: This is in Canada, not the US
    'Chase Center': 'San Francisco, CA',
}

# Print the city and state for each arena
for arena, location in arenas.items():
    print(f"{arena}: {location}")


# Map the 'Arena' column to the new 'Location' column
df['Location'] = df['Arena'].map(arenas)
df['Date'] = pd.to_datetime(df['Date'], format='%a, %b %d, %Y')

# Display the updated DataFrame
print(df.head())

file_path = "/Users/brendan/Desktop - Brendan’s MacBook Air/sportsInfo/sportsInfo/data/schedules/NBA_schedule_2024.json"  
df.to_json(file_path, orient='records')
df.to_csv('NBA_teams.csv')
