import sqlite3
from flask import Blueprint, render_template

resource = Blueprint('resource', __name__)

select_sample_data = """
    SELECT * FROM TEMPERATURE;
"""


@resource.route("/resource_check")
def resource_check():
    conn = sqlite3.connect('database/database_sql.db')
    cur = conn.cursor()
    cur.execute(select_sample_data)
    rows = cur.fetchall()

    return render_template("resource_check.html", resources=rows)