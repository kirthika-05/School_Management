from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from werkzeug.exceptions import BadRequest
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = ''        
app.config['MYSQL_PASSWORD'] = ''   
app.config['MYSQL_DB'] = 'school_management'

mysql = MySQL(app)


def execute_query(query, data):
    cur = mysql.connection.cursor()
    cur.execute(query, data)
    mysql.connection.commit()
    cur.close()

# ------------------ STUDENT ADMISSION ------------------
@app.route('/api/students', methods=['POST'])
def add_student():
    try:
        data = request.json
        required_fields = ['student_name', 'dob', 'grade', 'parent_info', 'previous_school']
        for field in required_fields:
            if field not in data or not str(data[field]).strip():
                return jsonify({"error": f"'{field}' is required and cannot be empty"}), 400

        query = """
            INSERT INTO students (student_name, dob, grade, parent_info, previous_school) 
            VALUES (%s, %s, %s, %s, %s)
        """
        execute_query(query, (
            data['student_name'], data['dob'], data['grade'],
            data['parent_info'], data['previous_school']
        ))
        return jsonify({"message": "Student added successfully"}), 200

    except BadRequest:
        return jsonify({"error": "Invalid JSON or malformed request"}), 400
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# ------------------ TEACHER REGISTRATION ------------------
@app.route('/api/teachers', methods=['POST'])
def add_teacher():
    try:
        data = request.json
        required_fields = ['name', 'subject_special', 'email', 'phone', 'qualification']
        for field in required_fields:
            if field not in data or not str(data[field]).strip():
                return jsonify({"error": f"'{field}' is required and cannot be empty"}), 400

        query = """
            INSERT INTO teachers (name, subject_special, email, phone, qualification) 
            VALUES (%s, %s, %s, %s, %s)
        """
        execute_query(query, (
            data['name'], data['subject_special'], data['email'],
            data['phone'], data['qualification']
        ))
        return jsonify({"message": "Teacher added successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# ------------------ CLASS SCHEDULE ------------------
@app.route('/api/class_schedule', methods=['POST'])
def add_class_schedule():
    try:
        data = request.json
        required_fields = ['class_name', 'subject', 'teacher_id', 'days', 'time_slot']
        for field in required_fields:
            if field not in data or not str(data[field]).strip():
                return jsonify({"error": f"'{field}' is required and cannot be empty"}), 400

        query = """
            INSERT INTO class_schedule (class_name, subject, teacher_id, days, time_slot) 
            VALUES (%s, %s, %s, %s, %s)
        """
        execute_query(query, (
            data['class_name'], data['subject'], data['teacher_id'],
            data['days'], data['time_slot']
        ))
        return jsonify({"message": "Class schedule added successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# ------------------ EXAM RESULT ------------------
@app.route('/api/exam_results', methods=['POST'])
def add_exam_result():
    try:
        data = request.json
        required_fields = ['student_id', 'subject', 'exam_date', 'marks_obtained']
        for field in required_fields:
            if field not in data or not str(data[field]).strip():
                return jsonify({"error": f"'{field}' is required and cannot be empty"}), 400

        query = """
            INSERT INTO exam_results (student_id, subject, exam_date, marks_obtained) 
            VALUES (%s, %s, %s, %s)
        """
        execute_query(query, (
            data['student_id'], data['subject'], data['exam_date'], data['marks_obtained']
        ))
        return jsonify({"message": "Exam result added successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# ------------------ START FLASK APP ------------------
if __name__ == '__main__':
    app.run(debug=True)
