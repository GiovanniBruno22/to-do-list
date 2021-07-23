from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todolist.db"
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)

db = SQLAlchemy(app)


# -------------------- To Do List Configuration -------------------- #

class ToDoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(250), unique=True, nullable=False)
    done = db.Column(db.Boolean, nullable=False)


# db.create_all()


# -------------------- Form Configuration -------------------- #

class Task(FlaskForm):
    task = StringField(default="Type here your new task..", validators=[DataRequired()])

# -------------------- Flask Routes -------------------- #


@app.route("/", methods=["GET", "POST"])
def home():
    form = Task()
    current_list = ToDoList.query.all()
    if form.validate_on_submit():
        new_task = ToDoList(
            task=request.form.get("task"),
            done=False
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("index.html", form=form, current_list=current_list)


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    task_to_delete = ToDoList.query.get(task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
