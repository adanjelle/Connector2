from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    course = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Student {self.name}>'

# Student schema
class StudentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Student

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

# Create the database
with app.app_context():
    db.create_all()

# Helper function to retrieve student
def get_student_or_404(id):
    student = Student.query.get(id)
    if not student:
        return None
    return student

# Routes

# Get all students
@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return students_schema.jsonify(students), 200

# Add a new student
@app.route('/students', methods=['POST'])
def add_student():
    try:
        # Get JSON data
        data = request.json
        print("Received data:", data)  # Debug line

        # Validate required fields
        name = data.get('name')
        email = data.get('email')
        course = data.get('course')

        if not name or not email or not course:
            return jsonify({"error": "All fields are required"}), 400

        new_student = Student(name=name, email=email, course=course)
        db.session.add(new_student)
        db.session.commit()

        return student_schema.jsonify(new_student), 201
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except IntegrityError:
        db.session.rollback()  # Rollback session if error occurs
        return jsonify({"error": "Email already exists"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update a student
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = get_student_or_404(id)
    if not student:
        return jsonify({'message': 'Student not found'}), 404

    try:
        # Get JSON data
        data = request.json
        print("Update data:", data)  # Debug line

        # Update student fields if provided
        student.name = data.get('name', student.name)
        student.email = data.get('email', student.email)
        student.course = data.get('course', student.course)
        db.session.commit()

        return student_schema.jsonify(student), 200
    except IntegrityError:
        db.session.rollback()  # Rollback session if error occurs
        return jsonify({"error": "Email already exists"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a student
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = get_student_or_404(id)
    if not student:
        return jsonify({'message': 'Student not found'}), 404

    db.session.delete(student)
    db.session.commit()

    return jsonify({'message': 'Student deleted'}), 204

if __name__ == "__main__":
    app.run(debug=True)
