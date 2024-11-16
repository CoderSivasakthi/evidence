from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)
CORS(app)

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Function to create a new database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root254",
            database="case_db",
            port=3306
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


case_data = {
    "case_id": 3244,
    "evidence_id": "34GJ545514Y45D5",
    "crime_type": "Theft",
    "crime_description": "A theft occurred at the OthakkalMandapam Bus Stand on the evening of October 4th. The incident took place in the electronics department, specifically within the mobile phone section. A customer was observed removing a high-end smartphone from a display case. The customer then concealed the phone in their jacket pocket and proceeded to exit the store without paying.",
    "evidence_details": "CCTV Camera Recordings in the Electronics Store",
    "crime_area": "OthakkalMandapam Bus Stand, OthakkalMandapam, Coimbatore",
    "eye_witnesses": "Ram Kumar",
    "evidence_file_url": "/path/to/evidence/file",
}

# Route to render HTML form
@app.route('/')
def index():
    return render_template('Dashboard.html')

@app.route('/cases')
def cases():
    return render_template('Cases.html')

@app.route('/audit&logs')
def Auditlogs():
    return render_template('Auditlogs.html')
@app.route('/case-details')
def case_details():
    return render_template('Case_Details.html')

# API Endpoint to handle form submissions
@app.route('/submit-evidence', methods=['POST'])
def submit_evidence():
    try:
        # Retrieve form data
        data = request.form
        file = request.files.get('uploadEvidence')

        # Extract data
        case_id = data.get('hash')
        evidence_id = data.get('evidenceId')
        crime_type = data.get('crimeType')
        crime_description = data.get('crimeDescription')
        evidence_details = data.get('evidenceDetails')
        crime_area = data.get('crimeArea')
        witnesses = data.get('witnesses', None)

        # Save uploaded file
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
        else:
            return jsonify({"error": "File upload is required"}), 400

        # Insert data into MySQL
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            sql = """
                INSERT INTO cases (caseId, evidenceId, crimeType, crimeDescription, 
                collectiveEvidenceDetails, crimeArea, eyeWitnesses)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (case_id, evidence_id, crime_type, crime_description, evidence_details, crime_area, witnesses)
            cursor.execute(sql, values)
            connection.commit()
            cursor.close()
            connection.close()

            return jsonify({"message": "Data successfully inserted!"}), 200
        else:
            return jsonify({"error": "Failed to connect to the database"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/fetch-case-details/<case_id>', methods=['GET'])
def fetch_case_details(case_id):
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM cases WHERE caseId = %s", (case_id,))
            result = cursor.fetchone()

            if not result:
                return jsonify({"error": "Case not found"}), 404

            # Map result to a dictionary using column names
            columns = [desc[0] for desc in cursor.description]
            case_details = dict(zip(columns, result))

            cursor.close()
            connection.close()

            return jsonify(case_details), 200
        else:
            return jsonify({"error": "Failed to connect to the database"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/case-details', methods=['GET'])
def case_details_page():
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM cases")
            cases = cursor.fetchall()

            # Map results to a list of dictionaries
            columns = [desc[0] for desc in cursor.description]
            case_list = [dict(zip(columns, case)) for case in cases]

            cursor.close()
            connection.close()

            return render_template('Case_Details.html', cases=case_list)
        else:
            return jsonify({"error": "Failed to connect to the database"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
