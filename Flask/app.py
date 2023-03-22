from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
#config file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#initialize database
db = SQLAlchemy(app)
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
        
@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == "POST":
        task_content = request.form['content']
        new_Task = Todo(content=task_content)

        try:
            db.session.add(new_Task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("dashboard.html", tasks=tasks)
        
@app.route('/delete/<int:id>' )
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "there was a problem deleting that task"

@app.route('/update/<int:id>', methods = ['POST', 'GET'] )
def update(id):
    task_to_update = Todo.query.get_or_404(id)
    if request.method == "POST":
        task_content = request.form["content"]
        task_to_update.content = task_content
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "there was a problem updating that task"
    else:
        return render_template('update.html', task_to_update=task_to_update)

@app.route('/checkbox/<int:id>', methods = ['POST', 'GET'])
def checkbox(id):
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        if request.form.get("Check") == "on":
            task.completed = 1
        else:

            task.completed = 0
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "there was a problem updating that task"
    

if __name__ ==  "__main__":
    app.run(debug = True) 