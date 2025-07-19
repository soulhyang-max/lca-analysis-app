import pandas as pd
import json

df = pd.read_excel('db_impact_values.xlsx')
records = df.to_dict('records')

with open('impact_db.txt', 'w', encoding='utf-8') as f:
    f.write('impact_db = ')
    json.dump(records, f, ensure_ascii=False, indent=2)