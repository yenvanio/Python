import json

with open('coordinates.json') as json_file:
    data = json.load(json_file)
    sql = ''
    for building in data['buildings']:
        statement = 'INSERT INTO building (name, location, building_id) VALUES ('
        statement += "'" + building['name'] + "'," + "'" + building['location'] + "', '" + building['building_id']
        statement += "');"
        sql += statement + "\n"
    print(sql)
