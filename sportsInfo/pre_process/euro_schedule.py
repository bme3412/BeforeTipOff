import pandas as pd
import json

df = pd.read_excel('euro_schedule_2024.xlsx')
#print(df.head())



# Optional: Convert the 'Date' column to datetime format if needed
# Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%a, %b %d, %Y')


print(df.head())
#print(df['Location'].value_counts())

file_path = "/Users/brendan/Desktop - Brendan’s MacBook Air/sportsInfo/sportsInfo/data/schedules/euroleague_schedule_2024.json"  
df.to_json(file_path, orient='records')
df.to_csv('euro_teams.csv')