from sqlalchemy import create_engine

import geopandas as gpd
import matsim
import logging
import shapely.geometry as shp

crs = {'init': "EPSG:26914"}

plans = matsim.plan_reader('scenarios/sioux_falls_uam/output/output_plans.xml.gz', selectedPlansOnly=True)

persons_list = []
trips_list = []

logging.info('Getting leg info from plans.xml')

for person, plan in plans:

    # Summarise legs into trips, assumption there is a home activity at the start and end of the day

    legs = filter(lambda e: e.tag == 'leg', plan)
    for leg in legs:
        # id of the person travelling
        leg_dict = {'person_id': person.attrib['id']}

    # get home locations
    # get x and y coordinates from first home activity
    for event in plan:
        if event.tag == 'activity' and event.attrib['type'] == 'home':
            home_x = float(event.attrib['x'])
            home_y = float(event.attrib['y'])
            break

    home_geom = shp.Point(home_x, home_y)
    person_dict.update({'home_x': home_x, 'home_y': home_y, 'home_geom': home_geom})

    # get work locations
    # not all plans have a work activity, so make them None instead, writing shapes if there is a work activity
    work_x = None
    for event in plan:
        if event.tag == 'activity' and event.attrib['type'] == 'work':
            work_x = float(event.attrib['x'])
            work_y = float(event.attrib['y'])
            break
    if work_x is not None:
        work_geom = shp.Point(work_x, work_y)
        person_dict.update({'work_x': work_x, 'work_y': work_y, 'work_geom': work_geom})

    # get secondary locations
    secondary_x = None
    for event in plan:
        if event.tag == 'activity' and event.attrib['type'] == 'secondary':
            secondary_x = float(event.attrib['x'])
            secondary_y = float(event.attrib['y'])
            break
    if secondary_x is not None:
        secondary_geom = shp.Point(secondary_x, secondary_y)
        person_dict.update({'secondary_x': secondary_x, 'secondary_y': secondary_y, 'secondary_geom': secondary_geom})

    persons_list.append(person_dict)

logging.info('Done.')
logging.info('Writing to PostGIS...')

# Convert lists of dicts to GeoDataFrames, filtering those rows that contain the respective geometry
home_out = gpd.GeoDataFrame(persons_list, crs=crs, geometry='home_geom')
work_out = gpd.GeoDataFrame(filter(lambda d: 'work_geom' in d.keys(), persons_list), crs=crs, geometry='work_geom')
secondary_out = gpd.GeoDataFrame(filter(lambda d: 'secondary_geom' in d.keys(), persons_list), crs=crs,
                                 geometry='secondary_geom')

engine = create_engine("postgresql+psycopg2://postgres:hainich@localhost:5433/matsim", echo=True, future=True)

with engine.connect() as conn:
    try:
        home_out.to_postgis('home_locations', conn, schema="sioux_falls", if_exists='fail', index=False)
    except ValueError as ve:
        logging.info(str(ve) + ", skipping.")

    try:
        work_out.to_postgis('work_locations', conn, schema="sioux_falls", if_exists='fail', index=False)
    except ValueError as ve:
        logging.info(str(ve) + ", skipping.")

    try:
        secondary_out.to_postgis('secondary_locations', conn, schema="sioux_falls", if_exists='fail', index=False)
    except ValueError as ve:
        logging.info(str(ve) + ", skipping.")

    conn.commit()
