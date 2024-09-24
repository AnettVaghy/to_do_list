from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Boolean, default=False)  # New status field

# Create the database and table
with app.app_context():
    db.create_all()

# Route for homepage (GET and POST)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        task_content = request.form['task']  # Get task content
        task_status = 'status' in request.form  # Get task status (True if checkbox is checked)
        
        new_task = Task(content=task_content, status=task_status)  # Create new task
        
        try:
            db.session.add(new_task)  # Add task to session
            db.session.commit()  # Commit to database
            return redirect('/')  # Redirect to homepage
        except:
            return 'There was an issue adding your task'
    
    tasks = Task.query.all()  # Query all tasks
    return render_template('index.html', tasks=tasks)

# Route to delete a task
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Task.query.get_or_404(id)  # Get task by ID

    try:
        db.session.delete(task_to_delete)  # Delete task
        db.session.commit()  # Commit changes to database
        return redirect('/')
    except:
        return 'There was an issue deleting that task'

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=True)

