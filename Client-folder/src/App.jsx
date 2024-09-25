import React, { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [students, setStudents] = useState([]);
  const [student, setStudent] = useState({ id: null, name: "", email: "", course: "" });
  const [isEditing, setIsEditing] = useState(false);
  const [error, setError] = useState(null);

  // Fetch all students when the component loads
  useEffect(() => {
    fetchStudents();
  }, []);

  // Function to fetch all students
  const fetchStudents = async () => {
    try {
      const response = await axios.get("http://localhost:5000/students");
      setStudents(response.data);
    } catch (error) {
      console.error("Error fetching students:", error);
    }
  };

  // Handle form input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setStudent({ ...student, [name]: value });
  };

  // Create or Update student based on the editing mode
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (isEditing) {
      try {
        await axios.put(`http://localhost:5000/students/${student.id}`, student);
        setIsEditing(false);
        setStudent({ id: null, name: "", email: "", course: "" });
        fetchStudents(); // Refresh the student list after editing
      } catch (error) {
        setError(error.response?.data?.error || "Error updating student.");
        console.error("Error updating student:", error);
      }
    } else {
      try {
        await axios.post("http://localhost:5000/students", student);
        setStudent({ id: null, name: "", email: "", course: "" });
        fetchStudents(); // Refresh the student list after adding
      } catch (error) {
        setError(error.response?.data?.error || "Error adding student.");
        console.error("Error adding student:", error);
      }
    }
  };

  // Edit a student
  const handleEdit = (student) => {
    setIsEditing(true);
    setStudent(student); // Populate form with the selected student's data
  };

  // Delete a student
  const handleDelete = async (id) => {
    try {
      await axios.delete(`http://localhost:5000/students/${id}`);
      fetchStudents(); // Refresh the student list after deletion
    } catch (error) {
      console.error("Error deleting student:", error);
    }
  };

  return (
    <div className="container mx-auto p-5">
      <h1 className="text-4xl font-bold text-center mb-10 text-blue-600">Student Registration</h1>

      {/* Display error messages */}
      {error && <div className="text-red-500 mb-4">{error}</div>}

      {/* Form to Create / Update Students */}
      <form className="space-y-6 bg-white shadow-lg p-8 rounded-lg" onSubmit={handleSubmit}>
        <input
          type="text"
          name="name"
          value={student.name}
          onChange={handleChange}
          placeholder="Name"
          className="border border-gray-300 p-3 w-full rounded-lg focus:ring-2 focus:ring-blue-500"
          required
        />
        <input
          type="email"
          name="email"
          value={student.email}
          onChange={handleChange}
          placeholder="Email"
          className="border border-gray-300 p-3 w-full rounded-lg focus:ring-2 focus:ring-blue-500"
          required
        />
        <input
          type="text"
          name="course"
          value={student.course}
          onChange={handleChange}
          placeholder="Course"
          className="border border-gray-300 p-3 w-full rounded-lg focus:ring-2 focus:ring-blue-500"
          required
        />
        <button
          type="submit"
          className={`w-full py-3 rounded-lg text-white font-bold transition-transform transform hover:scale-105 bg-gradient-to-r ${
            isEditing ? "from-yellow-400 to-yellow-500" : "from-blue-500 to-blue-600"
          }`}
        >
          {isEditing ? "Update Student" : "Add Student"}
        </button>
      </form>

      {/* List of Students */}
      <div className="mt-12">
        <h2 className="text-3xl font-bold mb-6 text-gray-700">Student List</h2>
        <ul className="space-y-6">
          {students.map((student) => (
            <li
              key={student.id}
              className="flex justify-between items-center bg-white shadow-md p-6 rounded-lg hover:shadow-xl transition-shadow"
            >
              <div>
                <h3 className="text-xl font-semibold text-gray-800">{student.name}</h3>
                <p className="text-gray-600">{student.email}</p>
                <p className="text-gray-600">{student.course}</p>
              </div>
              <div className="space-x-4">
                <button
                  onClick={() => handleEdit(student)}
                  className="py-2 px-4 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 transition-colors"
                >
                  Edit
                </button>
                <button
                  onClick={() => handleDelete(student.id)}
                  className="py-2 px-4 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
                >
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
