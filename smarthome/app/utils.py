import requests


def get_sensors_info() -> list:
    url = 'http://172.16.230.225:8123/api/states'
    headers = {'x-ha-access': 'tokyocommit', 'content-type': 'application/json'}
    r = requests.get(url, headers=headers)
    data = r.json()[3:]
    sensors = list()
    for row in data:
        try:
            name = row['attributes']['friendly_name']
            entity_id = row['entity_id']
            state = row['state']
            sensor_info = dict(
                name=name,
                entity_id=entity_id,
                state=state
            )
            if name != "all switches":
                sensors.append(sensor_info)
        except KeyError:
            pass
    return sensors

