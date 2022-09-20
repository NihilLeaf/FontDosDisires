from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///font.db'
db = SQLAlchemy(app)

class Font(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)

    coin = db.Column(db.Integer, default = 3)

    def __repr__(self):
        return '<Task %r>' % self.id

db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        task_content = request.form['content']
        new_task = Font(content = task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')

        except:
            return 'Falha!'

    else:
        tasks = Font.query.order_by(Font.coin).all()
        return render_template('index.html', tasks=tasks)

@app.route('/deletar/<int:id>')
def delete(id):
    task_to_delete = Font.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Falha'

@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    task = Font.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Fail reach'

    else:
        return render_template('edit.html', task = task)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')