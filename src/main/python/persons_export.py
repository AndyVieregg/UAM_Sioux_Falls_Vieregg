from sqlalchemy import create_engine

import geopandas as gpd
import matsim
import logging
import shapely.geometry as shp

crs = {'init': "EPSG:26914"}

plans = matsim.plan_reader('scenarios/sioux_falls_uam/output/output_plans.xml.gz', selectedPlansOnly=True)

persons_list = []

for person, plan in plans:
    person_id = person.attrib['id']
    person_dict = {'person_id': person_id}

    # get x and y coordinates from first home activity
    for event in plan:
        if event.tag == 'activity' and event.attrib['type'] == 'home':
            home_x = float(event.attrib['x'])
            home_y = float(event.attrib['y'])
            break

    home_geom = shp.Point(home_x, home_y)

    person_dict.update({'home_x': home_x, 'home_y': home_y, 'home_geom': home_geom})

    persons_list.append(person_dict)

print(persons_list[0:100])

persons_out = gpd.GeoDataFrame(persons_list, crs=crs, geometry='home_geom')

engine = create_engine("postgresql+psycopg2://postgres:hainich@localhost:5433/matsim", echo=True, future=True)

with engine.connect() as conn:
    try:
        persons_out.to_postgis('popp_test', conn, schema="sioux_falls", if_exists='replace', index=False)
    except ValueError as ve:
        logging.info(str(ve) + ", skipping.")

    conn.commit()


