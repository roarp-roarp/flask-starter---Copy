from flask import Flask, render_template, request, redirect
app = Flask(__name__)

variable = []
import sqlite3

conn = sqlite3.connect("groceries.sqlite", check_same_thread=False)
c = conn.cursor()
@app.route('/')
def index():
  stuff = get_all()
  return render_template("home.html", list = stuff)
# CRUD - Create Read Update Delete

def create_table():
  query = '''CREATE TABLE IF NOT EXISTS groceries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    date TEXT
  )'''
  c.execute(query)

def get_columns():
  query = "PRAGMA table_info(groceries)"
  print((c.execute(query)).fetchall())
def get_all():
  query = "SELECT * FROM groceries"
  return (c.execute(query)).fetchall()
def add_item(n, d):
  query = "INSERT INTO groceries (name, date) VALUES (?, ?)"
  c.execute(query, (n, d))
  conn.commit()


def search_item(n):
  query = "SELECT name FROM groceries WHERE name = (?)"
  found = c.execute(query, (n,)).fetchone()
  if type(found) == tuple:
    return found
  else:
    return -1

def main():
  create_table()  

@app.route('/submit', methods=["GET"])
def displayform():
  # view the form
  return render_template("form.html")

@app.route('/domessage', methods=["POST"])
def doform():
  info2 = request.form.get("username")
  if len(info2) < 1:
    return redirect('submit')
  else:
    # receive and process the form
    info = request.form.get("message")# the name attribute of the html form field
    variable.append(info)# save the data to a variable
    return redirect('/')

@app.route('/add', methods=["POST"])
def add():
  name2 = request.form.get("name")
  date2 = request.form.get("date")
  add_item(name2, date2)
  return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):
  query = 'DELETE FROM groceries WHERE id=?'
  c.execute(query, (id, ))
  conn.commit()
  return redirect('/')


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
  if request.method == 'GET':
    query = 'SELECT * FROM groceries WHERE id=?'
    q = (c.execute(query, (id, ))).fetchone()
    return render_template("edit.html", task = q)
  else:
    query = 'UPDATE groceries SET name=?, date=? WHERE id=?'
    name = request.form.get("name")
    date = request.form.get("date")
    c.execute(query, (name, date, id))
    conn.commit()
    return redirect('/')
  
if __name__ == '__main__':
  main()
  app.run()



