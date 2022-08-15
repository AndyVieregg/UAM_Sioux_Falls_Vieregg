from lxml import etree as ET
from sqlalchemy import create_engine
import pandas as pd 
import sys
import traceback


# read input files
cpacs_tree = ET.parse('scenarios/sioux_falls_uam/schedule.xml')
root_node = cpacs_tree.getroot()

stops_node = root_node.find('.//transitStops')

stops_list = []
i=1
for child in stops_node:
    stops_list.append({'name': child.attrib['name'],'x': child.attrib['x'], 'y': child.attrib['y']})
    i+=1

print(stops_list)
df = pd.DataFrame(stops_list)

print(df)

engine = create_engine("postgresql+psycopg2://postgres:hainich@localhost:5433/matsim", echo=True, future=True)

with engine.connect() as conn:
    df.to_sql('pt_stops', conn, schema="sioux_falls", if_exists='fail', index=False)

    conn.commit()
