from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# Helper function to connect to MySQL
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # Change this to your MySQL username
        password="Sanjivni@2004",  # Change this to your MySQL password
        database="task_db"
    )

# ROUTE: Serve the Login Page UI
@app.route('/')
def login_page():
    return render_template('login.html')

# ROUTE: Serve the Main Dashboard UI
@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

# API: Authenticate User Login
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    query = "SELECT id, role FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (data['username'], data['password']))
    user = cursor.fetchone()
    
    cursor.close()
    db.close()
    
    if user:
        return jsonify({"success": True, "role": user['role']})
    return jsonify({"success": False, "message": "Invalid username or password"}), 401

# API: Get List of All Employees (To populate the form's dropdown)
@app.route('/api/employees', methods=['GET'])
def api_get_employees():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, full_name FROM employees")
    employees = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(employees)

# API: Assign a New Task (UI Form -> DB)
@app.route('/api/tasks', methods=['POST'])
def api_create_task():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    
    query = "INSERT INTO tasks (title, assigned_to, status) VALUES (%s, %s, %s)"
    cursor.execute(query, (data['title'], data['assigned_to'], data['status']))
    
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"success": True, "message": "Task added to MySQL successfully!"})

if __name__ == '__main__':
    app.run(debug=True)