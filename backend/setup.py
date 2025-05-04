import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv


def create_tables():
    connection = psycopg2.connect(
        host=os.getenv('HOST'),
        port=os.getenv('PORT'),
        database=os.getenv('DATABASE'),
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD')
    )
    cursor = connection.cursor()

    queries = [
        """
        CREATE TABLE IF NOT EXISTS AccountUser (
            user_ID SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Category (
            Category_ID SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS FinanceEntry (
            entry_ID SERIAL PRIMARY KEY,
            user_ID INT NOT NULL REFERENCES AccountUser(user_ID),
            Category INT NOT NULL REFERENCES Category(Category_ID),
            Title VARCHAR(255) NOT NULL,
            Amount INT NOT NULL,
            date DATE NOT NULL
        );
        """
    ]

    for query in queries:
        cursor.execute(query)
        print("Executed table creation query.")

    sample_inserts = [
        """
        INSERT INTO AccountUser (first_name, last_name, email, password) VALUES
        ('John', 'Doe', 'john.doe@test.com', '$2b$12$exampleHashedPassword1'),
        ('Jane', 'Smith', 'jane.smith@test.com', '$2b$12$exampleHashedPassword2');
        """,
        """
        INSERT INTO Category (name) VALUES
        ('Income'),
        ('Rent'),
        ('Groceries'),
        ('Entertainment'),
        ('Utilities'),
        ('Transportation'),
        ('Healthcare');
        """,
        """
        INSERT INTO FinanceEntry (user_ID, Category, Title, Amount, date) VALUES
        (1, 1, 'Salary Payment', 3000, '2024-03-01'),
        (1, 2, 'Monthly Rent', -1200, '2024-03-03'),
        (2, 3, 'Weekly Groceries', -150, '2024-03-05'),
        (2, 4, 'Movie Night', -40, '2024-03-07'),
        (1, 5, 'Electric Bill', -100, '2024-03-08'),
        (2, 6, 'Bus Pass', -60, '2024-03-10'),
        (1, 7, 'Doctor Visit', -200, '2024-03-11');
        """
    ]

    for insert in sample_inserts:
        cursor.execute(insert)
        print("Executed sample data insert.")

    connection.commit()
    cursor.close()
    connection.close()
    print("Database setup complete.")


if __name__ == "__main__":
    load_dotenv()
    create_tables()
