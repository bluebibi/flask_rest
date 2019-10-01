import sqlite3

insertion_resource = """
    INSERT INTO TEMPERATURE VALUES (null, ?, ?, ?, ?);
"""

selection_resource_by_sensor_id = """
    SELECT * FROM TEMPERATURE WHERE sensor_id=?
"""

update_resource_by_sensor_id = """
    UPDATE TEMPERATURE SET temperature=?, datetime=?, location=? WHERE sensor_id=?
"""

delete_resource_by_sensor_id = """
    DELETE FROM TEMPERATURE WHERE sensor_id = ?
"""

class Temperature:
    def __init__(self):
        self.id = None
        self.sensor_id = None
        self.temperature = None
        self.datetime = None
        self.location = None



class Resource:
    def __init__(self):
        self.conn = sqlite3.connect('database/database_sql.db')

    def insert(self, temperature):
        curr = self.conn.cursor()
