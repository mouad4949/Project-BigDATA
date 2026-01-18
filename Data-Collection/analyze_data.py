import json

with open('final_data.json', 'r') as f:
    data = json.load(f)

print(f'Total articles: {len(data)}')

sources = {}
years = {}
for item in data:
    source = item.get('source', 'Unknown')
    sources[source] = sources.get(source, 0) + 1
    
    year = item.get('date_pub', 'Unknown')
    years[year] = years.get(year, 0) + 1

print('\nBy source:')
for k, v in sorted(sources.items()):
    print(f'  {k}: {v}')

print('\nBy year:')
for k, v in sorted(years.items()):
    print(f'  {k}: {v}')
