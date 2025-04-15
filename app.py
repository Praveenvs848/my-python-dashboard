from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)
conn = mysql.connector.connect(
    host="mysql",
    user="root",
    password="praveen@2000",
    database="user_dashboard",
    port=3306
)

cursor = conn.cursor()

@app.route('/', methods=['GET', 'POST'])
def index():
    keyword = request.form.get('keyword')
    if keyword:
        query = "SELECT * FROM employees WHERE id LIKE %s name LIKE %s OR email LIKE %s OR contact LIKE %s OR address LIKE %s"
        like_keyword = f"%{keyword}%"
        cursor.execute(query, (like_keyword, like_keyword, like_keyword, like_keyword))
    else:
        cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    return render_template('index.html', employees=employees)

@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        address = request.form['address']
        contact = request.form['contact']
        
        # Insert statement without the id field
        cursor.execute("""
            INSERT INTO employees (id, name, email, password, gender, address, contact)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (id, name, email, password, gender, address, contact))
        conn.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    cursor.execute("SELECT * FROM employees WHERE id = %s", (id,))
    employee = cursor.fetchone()

    if request.method == 'POST':
        new_id = request.form['id']  # Get new ID from form
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        address = request.form['address']
        contact = request.form['contact']

        cursor.execute("""
            UPDATE employees 
            SET id=%s, name=%s, email=%s, password=%s, gender=%s, address=%s, contact=%s 
            WHERE id=%s
        """, (new_id, name, email, password, gender, address, contact, id))  # Now updates ID too
        
        conn.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', employee=employee)


@app.route('/delete/<int:id>')
def delete_employee(id):
    cursor.execute("DELETE FROM employees WHERE id = %s", (id,))
    conn.commit()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    cursor.execute("SELECT * FROM employees ORDER BY id")
    employees = cursor.fetchall()
    return render_template('dashboard.html', employees=employees)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
