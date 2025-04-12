from flask import Flask, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",  # change if needed
            database="issue"
        )
        return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

@app.route('/')
def index():
    connection = get_db_connection()
    deliveries = []
    defects = []
    late_deliveries = []
    technichal_issues = []
    other = []  # New variable

    if connection:
        try:
            cursor = connection.cursor(dictionary=True)

            cursor.execute("SELECT * FROM wrong_order_delivery")
            deliveries = cursor.fetchall()

            cursor.execute("SELECT * FROM product_defect")
            defects = cursor.fetchall()

            cursor.execute("SELECT * FROM late_delivery")
            late_deliveries = cursor.fetchall()

            cursor.execute("SELECT * FROM technichal_issues")  # Keep "technichal_issues" as it was
            technichal_issues = cursor.fetchall()

            cursor.execute("SELECT * FROM other")  # New query
            other = cursor.fetchall()

        except Error as e:
            print("Error executing query:", e)
        finally:
            cursor.close()
            connection.close()

    return render_template(
        'index.html',
        deliveries=deliveries,
        defects=defects,
        late_deliveries=late_deliveries,
        technichal_issues=technichal_issues,
        other=other  # Pass to template
    )

if __name__ == '__main__':
    app.run(debug=True)
