from flask import Flask, render_template, request, redirect, url_for
from models import db, Task
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Initialize the database
with app.app_context():
    db.create_all()

# Home route - Display all tasks
@app.route('/')
def index():
    tasks = Task.query.order_by(Task.id).all()
    return render_template('index.html', tasks=tasks)

# Add a new task
@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form.get('description', '')
    priority = request.form['priority']
    due_date = request.form['due_date']
    assigned_to = request.form['assigned_to']
    status = request.form['status']
    
    new_task = Task(
        title=title,
        description=description,
        priority=priority,
        due_date=datetime.strptime(due_date, '%Y-%m-%d'),
        assigned_to=assigned_to,
        status=status
    )
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

# Update task status and assignee
@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update_task(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.status = request.form['status']
        task.assigned_to = request.form['assigned_to']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', task=task)

# Delete task
@app.route('/delete/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
