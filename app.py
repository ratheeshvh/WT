# from flask import Flask, render_template, request, redirect, url_for, session
# from flask_login import current_user
# import mysql.connector
# import secrets

# app = Flask(__name__)
# app.secret_key = secrets.token_hex(16)

# # MySQL Database configuration
# config = {
#     'user': 'root',
#     'password': '11-Apr-05',
#     'host': 'localhost',
#     'database': 'python',
#     'raise_on_warnings': True
# }

# # Connect to MySQL database
# def get_db_connection():
#     return mysql.connector.connect(**config)

# # Route to display login form
# @app.route('/')
# def login():
#     return render_template('thivi.html')

# @app.route('/login', methods=['POST'])
# def process_login():
#     user_type = request.form.get('user-type')

#     db = get_db_connection()
#     cursor = db.cursor()

#     try:
#         if user_type == 'patient':
#             email = request.form.get('patient-email')
#             password = request.form.get('patient-password')
#             cursor.execute("SELECT * FROM patient WHERE email = %s AND password = %s", (email, password))
#         elif user_type == 'hospital':
#             hospital_name = request.form.get('hospital-name')
#             registration_no = request.form.get('registration-no')
#             password = request.form.get('hospital-password')
#             cursor.execute("SELECT * FROM hospital WHERE hospital_name = %s AND registration_no = %s AND password = %s", (hospital_name, registration_no, password))
        
#         user = cursor.fetchone()

#         if user:
#             # User authenticated, store user type in session and redirect to dashboard route
#             session['user_type'] = user_type
#             if user_type == 'hospital':
#                 session['hospital_name'] = hospital_name
#             return redirect(url_for('dashboard'))
#         else:
#             # Invalid credentials, display error message
#             return render_template('thivi.html')
#     except mysql.connector.Error as err:
#         return f"Error: {err}"
#     finally:
#         cursor.close()
#         db.close()

# @app.route('/dashboard')
# def dashboard():
#     user_type = session.get('user_type')

#     if user_type == 'patient':
#         return render_template('varun.html')
#     elif user_type == 'hospital':
#         # return render_template('hos_dashboard.html')
#         return redirect(url_for('submit_hospital'))
#     else:
#         # If user type is not found in session, redirect to login page
#         return redirect(url_for('login'))

# # Route to display patient information form
# @app.route('/patients', methods=['GET'])
# def show_patients_form():
#     return render_template('patients.html')

# # Route to handle form submission
# @app.route('/patients', methods=['POST'])
# def patients():
#     username = request.form['username']
#     age = request.form['age']
#     dob = request.form['dob']
#     blood = request.form['blood']
#     gender = request.form['gender']
#     address = request.form['address']
#     allergy = request.form['allergy']
#     disability = request.form['disability']
#     mentalissues = request.form['mentalissues']
#     operations = request.form['operations']
#     whom = request.form['whom']

#     db = get_db_connection()
#     cursor = db.cursor()
#     sql = "INSERT INTO patients (username, Age, DOB, Blood, Gender, Address, Allergy, Disability, Mentalissues, Operations, Whom) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
#     val = (username, age, dob, blood, gender, address, allergy, disability, mentalissues, operations, whom)
#     cursor.execute(sql, val)
#     db.commit()
#     cursor.close()

#     return "Patient data submitted successfully!"

# @app.route('/doctors', methods=['GET'])
# def show_doctors_form():
#     return render_template('Add_doctors.html')

# @app.route('/doctors', methods=['POST'])
# def save_doctor():
#     name = request.form['name']
#     specialty = request.form['specialty']
#     experience = request.form['experience']
#     languages = request.form['languages']
#     contact = request.form['contact']
#     operating_hours = request.form['operating_hours']
#     affiliated_hospitals = request.form['affiliated_hospitals']
#     branch = request.form['branch']
    
#     db = get_db_connection()
#     cursor = db.cursor()
    
#     query = """
#     INSERT INTO doctors (name, specialty, experience, languages_spoken, contact_information, operating_hours, affiliated_hospitals, branch)
#     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#     """
#     values = (name, specialty, experience, languages, contact, operating_hours, affiliated_hospitals, branch)
    
#     cursor.execute(query, values)
#     db.commit()
#     cursor.close()

#     # return redirect(url_for('login'))
#     return render_template('hos_dashboard.html')

# @app.route('/doctors-info', methods=['GET', 'POST'])
# def get_doctors():
#     db = get_db_connection()
#     cursor = db.cursor(dictionary=True)
    
#     try:
#         selected_specialty = request.form.get('specialty') if request.method == 'POST' else None
#         selected_branch = request.form.get('branch') if request.method == 'POST' else None

#         query = "SELECT * FROM doctors WHERE 1=1"
#         params = []

#         if selected_specialty:
#             query += " AND specialty = %s"
#             params.append(selected_specialty)

#         if selected_branch:
#             query += " AND branch = %s"
#             params.append(selected_branch)

#         cursor.execute(query, params)
#         doctors = cursor.fetchall()

#         cursor.execute("SELECT DISTINCT specialty FROM doctors")
#         specialties = cursor.fetchall()
#         specialties = [specialty['specialty'] for specialty in specialties]

#         cursor.execute("SELECT DISTINCT branch FROM doctors")
#         branches = cursor.fetchall()
#         branches = [branch['branch'] for branch in branches]

#         return render_template('Alldoctors.html', doctors=doctors, specialties=specialties, branches=branches, selected_specialty=selected_specialty, selected_branch=selected_branch)
#     except mysql.connector.Error as err:
#         return f"Error: {err}"
#     finally:
#         cursor.close()
#         db.close()

        
# @app.route('/submit_hospital', methods=['GET'])
# def show_hospitals_form():
#             db = get_db_connection()
#             cursor = db.cursor(dictionary=True)
            
#             try:
#                 # Fetch hospital details based on user's session
#                 hospital_name = session.get('hospital_name')
#                 if hospital_name:
#                     # Fetch hospital details
#                     cursor.execute("SELECT * FROM hospitals WHERE hospital_name = %s", (hospital_name,))
#                     hospital = cursor.fetchone()
#                     if hospital:
#                         # Fetch branch details
#                         cursor.execute("SELECT * FROM branches WHERE hospital_id = %s", (hospital['hospital_id'],))
#                         branches = cursor.fetchall()
#                         branch_count = len(branches)  # Calculate the branch count
#                     else:
#                         hospital = None
#                         branches = None
#                         branch_count = 0
#                 else:
#                     # If hospital_name is not in session, display the empty form
#                     hospital = None
#                     branches = None
#                     branch_count = 0
#             except mysql.connector.Error as err:
#                 return f"Error: {err}"
#             finally:
#                 cursor.close()
#                 db.close()
            
#             return render_template('hos_dashboard.html', hospital=hospital, branches=branches, branch_count=branch_count)
        
# @app.route('/submit_hospital', methods=['POST'])
# def submit_hospital():
#     hospital_name = request.form['hospitalName']
#     hospital_address = request.form['hospitalAddress']
#     hospital_contact = request.form['hospitalContact']
#     ambulance_count = request.form['ambulanceCount']
#     doctor_count = request.form['doctorCount']

#     connection = get_db_connection()
#     cursor = connection.cursor(dictionary=True)

#     # Insert or update hospital data using an alias for the inserted values
#     cursor.execute('''
#         INSERT INTO hospitals (hospital_name, hospital_address, hospital_contact, ambulance_count, doctor_count)
#         VALUES (%s, %s, %s, %s, %s) AS new
#         ON DUPLICATE KEY UPDATE
#         hospital_address = new.hospital_address,
#         hospital_contact = new.hospital_contact,
#         ambulance_count = new.ambulance_count,
#         doctor_count = new.doctor_count
#     ''', (hospital_name, hospital_address, hospital_contact, ambulance_count, doctor_count))

#     # Get hospital_id for branches insertion or update
#     cursor.execute("SELECT hospital_id FROM hospitals WHERE hospital_name = %s", (hospital_name,))
#     hospital_id = cursor.fetchone()['hospital_id']

#     # Extract and insert/update branch data
#     for key, value in request.form.items():
#         if key.startswith('branches[') and key.endswith('][name]'):
#             branch_index = key.split('[')[1].split(']')[0]
#             branch_id = request.form.get(f'branches[{branch_index}][id]', '')  # Added branch_id
#             branch_name = request.form.get(f'branches[{branch_index}][name]', '')
#             branch_address = request.form.get(f'branches[{branch_index}][address]', '')
#             branch_contact = request.form.get(f'branches[{branch_index}][contact]', '')

#             # Check if branch already exists
#             cursor.execute("SELECT id FROM branches WHERE branch_id = %s AND hospital_id = %s", (branch_id, hospital_id))
#             existing_branch = cursor.fetchone()

#             if existing_branch:
#                 # Update existing branch
#                 cursor.execute('''
#                     UPDATE branches
#                     SET branch_name = %s,
#                         branch_address = %s,
#                         branch_contact = %s
#                     WHERE branch_id = %s AND hospital_id = %s
#                 ''', (branch_name, branch_address, branch_contact, branch_id, hospital_id))
#             else:
#                 # Insert new branch
#                 cursor.execute('''
#                     INSERT INTO branches (branch_id, branch_name, branch_address, branch_contact, hospital_id)
#                     VALUES (%s, %s, %s, %s, %s)
#                 ''', (branch_id, branch_name, branch_address, branch_contact, hospital_id))

#     connection.commit()
#     cursor.close()

#     # Store hospital name in session for future use
#     session['hospital_name'] = hospital_name

#     return 'Data submitted successfully'



# def fetch_data():
#     connection = get_db_connection()
#     cursor = connection.cursor(dictionary=True)
#     cursor.execute('SELECT * FROM `pharmacy`')
#     data = cursor.fetchall()
#     connection.close()
#     return data

# @app.route('/pharmacy')
# def index():
#     data = fetch_data()
#     return render_template('pharmacy.html', data=data)

# @app.route('/hospitals-info', methods=['GET', 'POST'])
# def get_hospitals():
#     db = get_db_connection()
#     cursor = db.cursor(dictionary=True)
    
#     try:
#         if request.method == 'POST':
#             selected_location = request.form.get('location')
#             query = "SELECT * FROM hospitals WHERE %s = '' OR hospital_address = %s"
#             params = (selected_location, selected_location)
#             cursor.execute(query, params)
#         else:
#             cursor.execute("SELECT * FROM hospitals")
        
#         hospitals = cursor.fetchall()

#         cursor.execute("SELECT DISTINCT hospital_address FROM hospitals")
#         locations = cursor.fetchall()
#         locations = [location['hospital_address'] for location in locations]

#         return render_template('Allhospitals.html', hospitals=hospitals, locations=locations, selected_location=request.form.get('location') if request.method == 'POST' else '')
    
#     except mysql.connector.Error as err:
#         return f"Error: {err}"
    
#     finally:
#         cursor.close()
#         db.close()

# @app.route('/hospital-branch', methods=['GET'])

# def hospital_branch():
#     db = get_db_connection()
#     cursor = db.cursor(dictionary=True)
    
#     try:
#         # Fetch the hospital name of the logged-in hospital
#         hospital_name = session.get('hospital_name')

#         # Fetch branches associated with the logged-in hospital name
#         cursor.execute("""
#             SELECT b.id, b.branch_name, b.branch_address, b.branch_contact
#             FROM branches b 
#             INNER JOIN hospitals h ON h.hospital_id = b.hospital_id
#             WHERE h.hospital_name = %s
#         """, (hospital_name,))
        
#         branches = cursor.fetchall()

#         return render_template('AllhospitalBranch.html', branches=branches)
    
#     except mysql.connector.Error as err:
#         return f"Error: {err}"
    
#     finally:
#         cursor.close()
#         db.close()

# @app.route('/firstAid', methods=['GET'])
# def show_firstAid_form():
#     return render_template('FirstAid.html')

# @app.route('/delete-branch/<int:id>', methods=['POST'])
# def delete_branch(id):
#     print("Branch ID:",id) 
#     db = get_db_connection()
#     cursor = db.cursor()

#     try:
#         # Delete the branch with the specified branch_id from the branches table
#         cursor.execute("DELETE FROM branches WHERE id = %s", (id,))
#         db.commit()
#         return redirect(url_for('hospital_branch'))  # Redirect to the hospital_branch route after deletion
#     except mysql.connector.Error as err:
#         return f"Error: {err}"
#     finally:
#         cursor.close()
#         db.close()

# if __name__ == '__main__':
#     app.run(debug=True)