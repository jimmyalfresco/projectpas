from flask import Flask, render_template, request, redirect, url_for, session, flash
import secrets
import mysql.connector
from werkzeug.security import check_password_hash
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

from werkzeug.security import generate_password_hash
print(generate_password_hash('1234'))

mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    database="projectpas",  
    password=os.getenv("DB_PASSWORD", "")
)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/aksi_login', methods=["POST", "GET"])
def aksi_login():
    cursor = mydb.cursor()
    query = "SELECT * FROM user WHERE username = %s"  # Changed table name to user
    data = (request.form['username'],)
    cursor.execute(query, data)
    user = cursor.fetchone()
    if user and check_password_hash(user[2], request.form['password']):  # Assuming password is in the 3rd column
        session["user"] = request.form['username']
        return redirect(url_for('admin'))
    else:
        flash("Invalid username or password!", "danger")
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))

@app.route('/admin')
def admin():
    if session.get("user"):
        return render_template("admin.html")
    else:
        flash("You need to log in first!", "warning")
        return redirect(url_for("home"))

@app.route('/simpan', methods=["POST", "GET"])
def simpan():
    if session.get("user"):
        cursor = mydb.cursor()
        nama = request.form["nama"]
        nama_toko = request.form["nama_toko"]  
        query = "INSERT INTO user (nama, nama_toko) VALUES (%s, %s)"  
        data = (nama, nama_toko)
        cursor.execute(query, data)
        mydb.commit()
        cursor.close()
        flash("Data saved successfully!", "success")
        return redirect("/tampil")
    else:
        flash("You need to log in first!", "warning")
        return redirect(url_for("home"))

@app.route('/tampil')
def tampil():
    if session.get("user"):
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM user")  
        data = cursor.fetchall()
        return render_template('tampil.html', data=data)
    else:
        flash("You need to log in first!", "warning")
        return redirect(url_for("home"))

@app.route('/hapus/<id>')
def hapus(id):
    if session.get("user"):
        cursor = mydb.cursor()
        query = "DELETE FROM user WHERE id = %s" 
        data = (id,)
        cursor.execute(query, data)
        mydb.commit()
        cursor.close()
        flash("Data deleted successfully!", "success")
        return redirect('/tampil')
    else:
        flash("You need to log in first!", "warning")
        return redirect(url_for("home"))

@app.route('/update/<id>')
def update(id):
    if session.get("user"):
        cursor = mydb.cursor()
        query = "SELECT * FROM user WHERE id = %s" 
        data = (id,)
        cursor.execute(query, data)
        value = cursor.fetchone()
        return render_template('update.html', value=value) 
    else:
        flash("You need to log in first!", "warning")
        return redirect(url_for("home"))

@app.route('/aksiupdate', methods=["POST", "GET"])
def aksiupdate():
    if session.get("user"):
        cursor = mydb.cursor()
        id = request.form["id"]
        nama = request.form["nama"]
        nama_toko = request.form["nama_toko"]  
        query = "UPDATE user SET nama = %s, nama_toko"


if __name__ == "__main__":
    app.run(debug=True)