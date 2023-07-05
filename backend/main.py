from flask import Flask, jsonify, request
from flask_jwt_extended import (JWTManager, create_access_token,
                                jwt_required, get_jwt_identity)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from hashlib import md5

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@db:5432/todo_app'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

CORS(app, resources={r"*": {"origins": "*"}})
db = SQLAlchemy(app)
jwt = JWTManager(app)

class BaseModel(db.Model):
    __abstract__ = True

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Users(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Tokens(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    expires_at = db.Column(db.DateTime)

class Task_lists(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tasks = db.relationship('Tasks', backref='task_lists', lazy=True, cascade='all, delete-orphan')

class Tasks(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('task_lists.id'), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, server_default='f')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Both username and password are required'}), 400
    existing_user = Users.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400
    hashed_password = md5(password.encode()).hexdigest()
    user = Users(username=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Both username and password are required'}), 400
    user = Users.query.filter_by(username=username).first()
    hashed_password = md5(password.encode()).hexdigest()
    if not user or not (hashed_password == user.password):
        return jsonify({'message': 'Invalid username or password'}), 401
    token = create_access_token(identity=user.id)
    return jsonify({'token': token})

@app.route('/lists', methods=['GET'])
@jwt_required()
def get_task_lists():
    user_id = get_jwt_identity()
    task_lists = Task_lists.query.filter_by(user_id=user_id).all()
    return jsonify({'task_lists': [task_list.to_dict() for task_list in task_lists]})


@app.route('/lists', methods=['POST'])
@jwt_required()
def create_task_list():
    user_id = get_jwt_identity()
    data = request.json
    name = data.get('title')
    if not name:
        return jsonify({'message': 'Name is required'}), 400
    task_list = Task_lists(name=name, user_id=user_id)
    db.session.add(task_list)
    db.session.commit()
    return jsonify({'message': 'Task list created successfully', 'task_list': task_list.to_dict()})



@app.route('/lists/<int:list_id>', methods=['DELETE'])
@jwt_required()
def delete_task_list(list_id):
    user_id = get_jwt_identity()
    task_list = Task_lists.query.filter_by(id=list_id, user_id=user_id).first()
    if not task_list:
        return jsonify({'message': 'Task list not found'}), 404
    db.session.delete(task_list)
    db.session.commit()
    return jsonify({'message': 'Task list deleted successfully'})


@app.route('/lists/<int:list_id>/tasks', methods=['GET'])
@jwt_required()
def get_tasks(list_id):
    user_id = get_jwt_identity()
    task_list = Task_lists.query.filter_by(id=list_id, user_id=user_id).first()
    if not task_list:
        return jsonify({'message': 'Task list not found'}), 404
    tasks = Tasks.query.filter_by(list_id=list_id).all()
    return jsonify({'tasks': [task.to_dict() for task in tasks]})


@app.route('/lists/<int:list_id>/tasks', methods=['POST'])
@jwt_required()
def create_task(list_id):
    user_id = get_jwt_identity()
    task_list = Task_lists.query.filter_by(id=list_id, user_id=user_id).first()
    if not task_list:
        return jsonify({'message': 'Task list not found'}), 404
    data = request.json
    title = data.get('title')
    if not title:
        return jsonify({'message': 'title is required'}), 400
    task = Tasks(title=title, list_id=list_id)
    db.session.add(task)
    db.session.commit()
    return jsonify({'message': 'Task created successfully', 'task': task.to_dict()})


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    task = Tasks.query.join(Task_lists).filter(
        Tasks.id == task_id, Task_lists.user_id == user_id).first()
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})


@app.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()
    task = Tasks.query.join(Task_lists).filter(
        Tasks.id == task_id, Task_lists.user_id == user_id).first()
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    data = request.json
    title = data.get('title', task.title)
    completed = data.get('completed', task.completed)
    task.title = title
    task.completed = completed
    db.session.commit()
    return jsonify({'message': 'Task updated successfully'})


@app.route('/tasks/<int:task_id>/complete', methods=['POST'])
@jwt_required()
def complete_task(task_id):
    user_id = get_jwt_identity()
    task = Tasks.query.join(Task_lists).filter(
        Tasks.id == task_id, Task_lists.user_id == user_id).first()
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    task.completed = True
    db.session.commit()
    return jsonify({'message': 'Task completed successfully'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
