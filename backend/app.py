from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import os
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import timedelta
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
import re

# Load environment variables
load_dotenv()

app = Flask(__name__)
bcrypt = Bcrypt(app)

# CORS allows the frontend
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)



app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY",
                                         "your_secret_key")  # add in your secret key in for the encryption
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)  # jwt token expires in 30 minutes
app.config["JWT_TOKEN_LOCATION"] = ["headers"]  # jwt token is in the header

jwt = JWTManager(app)


# connect to the PostgreSQL database
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('HOST'),
        port=os.getenv('PORT'),
        database=os.getenv('DATABASE'),
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD')
    )



# API to responsible for the signup of users
@app.route('/api/signup', methods=['POST'])
def signup():
    """Enhanced signup endpoint with proper validation"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        # Validate required fields
        required_fields = ['firstName', 'lastName', 'email', 'password']
        missing = [field for field in required_fields if field not in data]
        if missing:
            return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

        # Sanitize inputs
        first_name = data['firstName'].strip()
        last_name = data['lastName'].strip()
        email = data['email'].lower().strip()
        password = data['password'].strip()

        # Validate email format
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            return jsonify({"error": "Invalid email format"}), 400

        # Validate password complexity
        password_pattern = re.compile(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        )
        if not password_pattern.match(password):
            return jsonify({
                "error": "Password must contain: 8+ characters, 1 uppercase, 1 lowercase, 1 number, 1 symbol (@$!%*?&)"
            }), 400

        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                # Check existing email
                cur.execute("SELECT email FROM AccountUser WHERE email = %s", (email,))
                if cur.fetchone():
                    return jsonify({"error": "Email already registered"}), 409

                # Hash password
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

                # Create user
                cur.execute(
                    """INSERT INTO AccountUser (first_name, last_name, email, password)
                    VALUES (%s, %s, %s, %s) RETURNING user_id""",
                    (first_name, last_name, email, hashed_password)
                )
                user_id = cur.fetchone()[0]
                conn.commit()

                return jsonify({
                    "message": "User registered successfully",
                    "user_id": user_id,
                    "email": email
                }), 201

        except psycopg2.DatabaseError as e:
            conn.rollback()
            app.logger.error(f"Database error: {str(e)}")
            return jsonify({"error": "Database operation failed"}), 500
        finally:
            conn.close()

    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500




# API used to log in to an account
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # Check if email exists
        cur.execute("SELECT user_ID, password FROM AccountUser WHERE email = %s", (email,))
        user = cur.fetchone()

        if not user:
            return jsonify({"message": "Invalid credentials"}), 401

        print(f"User found: {user}")

        # Validate password
        if not bcrypt.check_password_hash(user["password"], password):
            print("Password does not match")
            return jsonify({"message": "Invalid credentials"}), 401

        # Generate JWT token
        token = create_access_token(identity=email)
        print("Login successful, token generated")

        return jsonify({"token": token}), 200

    except Exception as e:
        print("Error:", str(e))  # Print the actual error to Flask logs
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=["GET"])
def index():
    return jsonify({"status":"ok"}), 200

# API to get all the info for the users dashboard
@app.route("/api/dashboard", methods=["GET"])
@jwt_required()
def get_dashboard():
    # gets the identity of the user from jwt
    user_email = get_jwt_identity()

    # connect to database
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        # query to get info from the db
        cur.execute("SELECT user_id, first_name FROM AccountUser WHERE email = %s", (user_email,))
        user = cur.fetchone()

        if not user:
            cur.close()
            conn.close()
            return jsonify({"message": "User not found"}), 404

        first_name = user["first_name"]

        cur.close()
        conn.close()

        return jsonify({
            "first_name": first_name
        }), 200
    except Exception as e:
        print("Error in /api/dashboard:", str(e))
        return jsonify({"error": str(e)}), 500


# portfolio API requires JWT Auth
@app.route("/api/portfolio", methods=["GET"])
@jwt_required()
def get_portfolio():
    # Get the user's email from JWT
    # Get the user's email from JWT
    user_email = get_jwt_identity()

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if user exists
        cur.execute("SELECT user_ID FROM AccountUser WHERE email = %s", (user_email,))
        user = cur.fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Get finance entries for this user
        cur.execute("""
            SELECT fe.entry_ID, fe.Title, fe.Amount, fe.date, c.name AS category_name
            FROM FinanceEntry fe
            JOIN AccountUser au ON fe.user_ID = au.user_ID
            JOIN Category c ON fe.Category = c.Category_ID
            WHERE au.email = %s
            ORDER BY fe.entry_ID;
        """, (user_email,))

        # Correct column names matching the SELECT query
        columns = ["entry_ID", "Title", "Amount", "date", "category_name"]
        entries = [dict(zip(columns, row)) for row in cur.fetchall()]

        cur.close()
        conn.close()
        
        return jsonify({
            'entries': entries,
            'status': 'success'
        })

    except Exception as e:
        print(f"🔥 Error in /api/portfolio: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/categories", methods=["GET"])
def get_industries():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * from category;")
    categories = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify({
            'categories': categories,
            'status': 'success'
        })
@app.route('/api/addentry', methods=['POST'])
@jwt_required()
def add_entry():
    data = request.get_json()
    user_email = get_jwt_identity()
    
    # Extracting and validating fields
    title = data.get('title')
    category_name = data.get('category_name')
    date = data.get('date')

    try:
        amount = int(data['amount'])
    except (KeyError, ValueError, TypeError):
        return jsonify({"error": "Amount must be a valid integer"}), 400

    if not all([title, category_name, amount, date]):
        return jsonify({"error": "All fields (title, category_name, amount, date) are required"}), 400

    if amount <= 0:
        return jsonify({"error": "Amount must be greater than 0"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Get the user's ID
        cur.execute("SELECT user_ID FROM AccountUser WHERE email = %s", (user_email,))
        user = cur.fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 400
        user_id = user[0]

        # Get or create the Category
        cur.execute("SELECT Category_ID FROM Category WHERE name = %s", (category_name,))
        category = cur.fetchone()

        if category:
            category_id = category[0]
        else:
            # Insert new category and get its ID
            cur.execute(
                "INSERT INTO Category (name) VALUES (%s) RETURNING Category_ID",
                (category_name,)
            )
            category_id = cur.fetchone()[0]
            conn.commit()

        # Insert into FinanceEntry
        cur.execute(
            """
            INSERT INTO FinanceEntry (user_ID, Category, Title, Amount, date)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING entry_ID
            """,
            (user_id, category_id, title, amount, date)
        )

        entry_id = cur.fetchone()[0]
        conn.commit()

        return jsonify({
            "message": "Finance entry added successfully",
            "entry_id": entry_id,
            "category_id": category_id
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


@app.route("/api/portfolio/<int:entry_id>", methods=["DELETE"])
@jwt_required()
def delete_entry(entry_id):
    user_email = get_jwt_identity()

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if user exists
        cur.execute("SELECT user_ID FROM AccountUser WHERE email = %s", (user_email,))
        user = cur.fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404

        user_id = user[0]  # Extract the user_ID
        
        cur.execute("SELECT entry_ID FROM FinanceEntry WHERE entry_ID = %s AND user_ID = %s", (entry_id, user_id))
        stock_entry = cur.fetchone()

        if not stock_entry:
            return jsonify({"error": "Entry not found"}), 404

        cur.execute(
            "DELETE FROM FinanceEntry WHERE entry_ID = %s AND user_ID = %s",
            (entry_id, user_id)
        )

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "User deleted stock successfully", "entry_id": entry_id}), 200

    except Exception as e:
        print(f"🔥 Error deleting stock: {str(e)}")

        return jsonify({"error": str(e)}), 500

@app.route("/api/portfolio/edit/<int:entry_id>", methods=["PUT"])
@jwt_required()
def update_finance_entry(entry_id):
    data = request.get_json()
    user_email = get_jwt_identity()
    category_id = data['category']  # This is now the category *ID*
    title = data['Title']  # Entry title

    try:
        amount = float(data['Amount'])  # Ensure amount is numeric
    except ValueError:
        return jsonify({"error": "Amount must be a valid number"}), 400

    date = data['date']  # Entry date

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Get user ID
        cur.execute("SELECT user_ID FROM AccountUser WHERE email = %s", (user_email,))
        user = cur.fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404
        user_id = user[0]

        # Check if finance entry exists and belongs to user
        cur.execute("SELECT entry_ID FROM FinanceEntry WHERE entry_ID = %s AND user_ID = %s", (entry_id, user_id))
        if not cur.fetchone():
            return jsonify({"error": "Finance entry not found or unauthorized"}), 404

        # Optional: Check if the category ID is valid
        cur.execute("SELECT category_id FROM Category WHERE category_id = %s", (category_id,))
        if not cur.fetchone():
            return jsonify({"error": "Invalid category ID"}), 400

        # Update finance entry using category_id
        cur.execute("""
            UPDATE FinanceEntry 
            SET title = %s, category = %s, amount = %s, date = %s
            WHERE entry_ID = %s AND user_ID = %s
        """, (title, category_id, amount, date, entry_id, user_id))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Finance entry updated successfully", "entry_id": entry_id}), 200

    except Exception as e:
        print(f"🔥 Error updating finance entry: {str(e)}")
        return jsonify({"error": str(e)}), 500


        
@app.route("/api/categories", methods=["GET"])
def get_categories():
    conn = get_db_connection()
    cur = conn.cursor()

    # Execute SQL query to fetch category names
    cur.execute("SELECT name FROM Category;")  # Assuming your table is called 'Category' and has a 'name' column
    categories = cur.fetchall()
    
    # Close the connection
    cur.close()
    conn.close()

    # Return the categories in JSON format
    return jsonify({
        'categories': [category[0] for category in categories],  # Extract category names from the result
        'status': 'success'
    }), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
