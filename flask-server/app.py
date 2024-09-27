from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

# Initialize app
app = Flask(__name__)
CORS(app)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db
db = SQLAlchemy(app)

# Initialize ma
ma = Marshmallow(app)

# Student Class/Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    course = db.Column(db.String(100))

    def __init__(self, name, email, course):
        self.name = name
        self.email = email
        self.course = course

# Student Schema
class StudentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'course')

# Initialize schema
student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

# Create a Student
@app.route('/students', methods=['POST'])
def add_student():
    data = request.json
    print(f"Received data: {data}")
    
    name = data.get('name')
    email = data.get('email')
    course = data.get('course')

    if not all([name, email, course]):
        return jsonify({"error": "Missing required fields"}), 400

    new_student = Student(name, email, course)

    try:
        db.session.add(new_student)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Could not add student", "details": str(e)}), 500

    return student_schema.jsonify(new_student), 201

# Get All Students
@app.route('/students', methods=['GET'])
def get_students():
    try:
        students = Student.query.all()
        result = students_schema.dump(students)  # Use dump instead of jsonify
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": "Could not fetch students", "details": str(e)}), 500

# Delete a Student
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    
    if not student:
        return jsonify({"error": "Student not found"}), 404
    
    try:
        db.session.delete(student)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Could not delete student", "details": str(e)}), 500
    
    return jsonify({"message": f"Student with id {id} has been deleted successfully"}), 200

# Run Server
if __name__ == '__main__':
    app.run(debug=True)
