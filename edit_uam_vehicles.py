from lxml import etree as ET
from sqlalchemy import create_engine
import pandas as pd 
import sys
import traceback


# read input files
cpacs_tree = ET.parse('scenarios/sioux_falls_uam/uam_vehicles_ideal.xml')
root_node = cpacs_tree.getroot()

vehicles_node = root_node.find('.//vehicles')


default_no_vehicles = 5000
vehicle_nos = {
1: 500,
2: 5000,
3: 1000,
4: 100,
5: 2000,
6: 1000,
7: 2000,
8: 2000,
9: 100,
10: 1000,
}

for stop_no in range(1,11):
    vehicle_maxno = default_no_vehicles
    if vehicle_nos.get(stop_no) is not None:
        vehicle_maxno = vehicle_nos.get(stop_no)
    for vehicle_no in range(1,vehicle_maxno+1):
        vehicle_node = ET.SubElement(vehicles_node, 'vehicle')
        vehicle_node.attrib.update({'id': f'{stop_no}-new-{vehicle_no}', 'type':'Default', 'initialstation':f'{stop_no}',
        'starttime':'0:00:00', 'endtime':'24:00:00'})

# write output CPACS
    ET.indent(root_node)
    cpacs_tree.write('scenarios/sioux_falls_uam/uam_vehicles_idealout.xml', pretty_print=True)