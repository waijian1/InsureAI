import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('../../insurance.db')
cursor = conn.cursor()

# Create the products table with NOT NULL constraints
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        types TEXT NOT NULL CHECK(types IN ('Death', 'TPD', 'Critical Illness', 'Accidental', 'Hospitalisation')),
        features TEXT NOT NULL,
        company TEXT NOT NULL
    )
''')
conn.commit()

# Define the types and corresponding descriptions for each product
types = ['Death', 'TPD', 'Critical Illness', 'Accidental', 'Hospitalisation']
product_details = {
    'A': '{"coverage": "term", "premium": 100, "SA":10000}',
    'B': '{"coverage": "endowment", "premium": 200, "SA":20000}',
    'C': '{"coverage": "full", "premium": 300, "SA":30000}'
}
company = 'InsureAI'

# Check if products exist
cursor.execute("SELECT COUNT(*) FROM products WHERE company = ?", (company,))
product_count = cursor.fetchone()[0]

# Insert 3 products for each type only if there are no existing records
if product_count == 0:
    for t in types:
        for label, feature in product_details.items():
            name = f'{t} {label}'
            cursor.execute('''
                INSERT INTO products (name, types, features, company)
                VALUES (?, ?, ?, ?)
            ''', (name, t, feature, company))
    conn.commit()
    print("Products inserted successfully.")
else:
    print("Products already exist. No new records inserted.")

# Fetch data
cursor.execute('SELECT * FROM products')
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close connection
conn.close()