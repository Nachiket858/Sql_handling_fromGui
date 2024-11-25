from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'demo'
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch the most recently updated or added record
    cursor.execute('SELECT * FROM Person ORDER BY PersonID DESC LIMIT 1')
    recent_person = cursor.fetchone()

    cursor.close()
    conn.close()
    return render_template('index.html', recent_person=recent_person)

@app.route('/all_data')
def all_data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Person')
    people = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('all_data.html', people=people)

@app.route('/add', methods=['POST'])
def add():
    last_name = request.form['LastName']
    first_name = request.form['FirstName']
    address = request.form['Address']
    city = request.form['City']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Person (LastName, FirstName, Address, City) VALUES (%s, %s, %s, %s)',
                   (last_name, first_name, address, city))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        last_name = request.form['LastName']
        first_name = request.form['FirstName']
        address = request.form['Address']
        city = request.form['City']
        cursor.execute('UPDATE Person SET LastName = %s, FirstName = %s, Address = %s, City = %s WHERE PersonID = %s',
                       (last_name, first_name, address, city, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('all_data'))
    
    cursor.execute('SELECT * FROM Person WHERE PersonID = %s', (id,))
    person = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit.html', person=person)

@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Person WHERE PersonID = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('all_data'))

if __name__ == '__main__':
    app.run(debug=True)
