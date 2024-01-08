from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

# Підключення до PostgreSQL
conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="lol123",
    host="localhost",
    port="5433",
    sslmode="prefer",
    connect_timeout=10
)

@app.route('/')
def index():
    # Отримати дані з бази даних та передати їх на сторінку
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cars')
    cars_data = cursor.fetchall()
    conn.close()

    return render_template('index.html', cars=cars_data)

if __name__ == '__main__':
    app.run(debug=True)
