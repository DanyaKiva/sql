from faker import Faker
import random
from datetime import datetime, timedelta
import mysql.connector

fake = Faker()

# Connect to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='lol123',
    database='car_dealership'
)
cursor = conn.cursor()

def generate_brands():
    for _ in range(100):
        brand_name = fake.company()

        # Перевірка існування перед вставкою
        cursor.execute('SELECT id FROM brands WHERE name = %s', (brand_name,))
        existing_brand = cursor.fetchone()

        if not existing_brand:
            cursor.execute('INSERT INTO brands (name, created_at, updated_at) VALUES (%s, %s, %s)',
                           (brand_name, datetime.now(), datetime.now()))
            conn.commit()

# Generate 100 models
for i in range(100):
    model_name = f'CarModel{i}'
    brand_id = random.randint(1, 100)
    cursor.execute('INSERT INTO models (name, brand_id, created_at, updated_at) VALUES (%s, %s, %s, %s)',
                   (model_name, brand_id, datetime.now(), datetime.now()))
    conn.commit()

# Generate 100 cars
for _ in range(100):
    vin = fake.unique.uuid4()[:17]
    # Замість генерації випадкового model_id, виберіть існуючий випадковим чином
    cursor.execute('SELECT id FROM models ORDER BY RAND() LIMIT 1')
    model_id = cursor.fetchone()[0]

    mileage = random.randint(0, 200000)
    price = round(random.uniform(1000, 50000), 2)
    cursor.execute('INSERT INTO cars (vin, model_id, mileage, price, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)',
                   (vin, model_id, mileage, price, datetime.now(), datetime.now()))
    conn.commit()

# Generate 100 customers
for _ in range(100):
    customer_name = fake.name()
    phone = fake.phone_number()
    cursor.execute('INSERT INTO customers (name, phone, created_at, updated_at) VALUES (%s, %s, %s, %s)',
                   (customer_name, phone, datetime.now(), datetime.now()))
    conn.commit()

# Generate 100 sales
for _ in range(100):
    car_id = random.randint(1, 100)
    customer_id = random.randint(1, 100)
    sale_date = fake.date_between(start_date='-1y', end_date='today')
    price = round(random.uniform(1000, 50000), 2)
    cursor.execute('INSERT INTO sales (car_id, customer_id, sale_date, price, created_at) VALUES (%s, %s, %s, %s, %s)',
                   (car_id, customer_id, sale_date, price, datetime.now()))
    conn.commit()

# Generate 100 services
for _ in range(100):
    service_name = fake.word()
    service_price = round(random.uniform(50, 500), 2)
    cursor.execute('INSERT INTO services (name, price, created_at, updated_at) VALUES (%s, %s, %s, %s)',
                   (service_name, service_price, datetime.now(), datetime.now()))
    conn.commit()

# Generate 100 service_sales
for _ in range(100):
    service_id = random.randint(1, 100)
    car_id = random.randint(1, 100)
    sale_date = fake.date_between(start_date='-1y', end_date='today')
    price = round(random.uniform(50, 500), 2)
    cursor.execute('INSERT INTO service_sales (service_id, car_id, sale_date, price, created_at) VALUES (%s, %s, %s, %s, %s)',
                   (service_id, car_id, sale_date, price, datetime.now()))
    conn.commit()

# Generate 100 employees
for _ in range(100):
    employee_name = fake.name()
    position = fake.word()
    cursor.execute('INSERT INTO employees (name, position, created_at, updated_at) VALUES (%s, %s, %s, %s)',
                   (employee_name, position, datetime.now(), datetime.now()))
    conn.commit()

# Generate 100 employee_sales
for _ in range(100):
    employee_id = random.randint(1, 100)
    sale_id = random.randint(1, 100)
    cursor.execute('INSERT INTO employee_sales (employee_id, sale_id, created_at) VALUES (%s, %s, %s)',
                   (employee_id, sale_id, datetime.now()))
    conn.commit()

# Generate 100 car_photos
for _ in range(100):
    car_id = random.randint(1, 100)
    photo_url = fake.image_url()
    cursor.execute('INSERT INTO car_photos (car_id, photo_url) VALUES (%s, %s)',
                   (car_id, photo_url))
    conn.commit()

# Close the connection
cursor.close()
conn.close()
