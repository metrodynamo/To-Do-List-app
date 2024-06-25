
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# new instance of the Flask class
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'  # Assigns the right to the left
db = SQLAlchemy(app)  # Create an instance of SQLAlchemy and call it app


# db.Model is inheritance (comes from SQLAlchemy). It doesn't need any self or def init properties as this is written into the db.Model code
# Column, an integer and the primary key
# Limits strings to 300 (although the actual model is currently broken apparently). Is likely to be unique. Column, 300 limit and things cannot be entered twice

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Creates an integer column, which is also the primary key
    task = db.Column(db.String(300), unique=True) # Creates a string column
    complete = db.Column(db.Boolean, default=False) # Creating a way to complete a task, initially set to false
    date_created = db.Column(db.DateTime, default=datetime.now) #Addng a datetime column. datetime is imported. This part I used ChatGPT
   

@app.route("/")
def home():
    todo_list = Todo.query.all()
    print(todo_list)
    return render_template("index.html", todo_list = todo_list) #if the page sees todo_list, it is referencing the todo_list we made here

@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")  # Create a variable called task and grab the name 'task' from the form in the HTML file
    new_todo = Todo(task=task)  # Grab the variable 'task' and assign it to property of task from the 'new_todo' instance of Todo. Has to be done this way as the class has no def or self
    db.session.add(new_todo)  # Add the instance (object) to the DB
    db.session.commit()  # Like git, this is a process to add to the DB
    return redirect(url_for("home")) # Redirect to the URL associated with "home"

@app.route("/update/<todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first() # Find the specific (first) entry that has been entered into the form. We need to add .first() or it can mess up (even if all entries are unique)
    todo.complete = not todo.complete # Whatever it is at, change it. So false will become true, or true will become false
    db.session.commit() 
    return redirect(url_for("home"))

@app.route("/delete/<todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first() 
    db.session.delete(todo) # Delete the instance (object) from the DB
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure the database and tables are created
    app.run(debug=True, port=8000)