import streamlit as st
import mysql.connector
import sys,base64
from datetime import date,datetime
session_state = st.session_state
import subprocess
from mh import view_mh,add_mh
import pandas as pd
from booked import booked_appointments_patient

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="amulya1623",
    database="hms",
    auth_plugin='mysql_native_password'
)

def patient_page():
    st.title("Patient Page")
    st.header("Welcome to the Patient Page!")
    # Add content specific to the patient page

def is_doctor_available(doctor_name, appointment_date, appointment_time):
    cursor = db.cursor()
    cursor.execute("SELECT IsDoctorAvailableForAppointment(%s, %s, %s)",
                   (doctor_name, appointment_date, appointment_time))
    result = cursor.fetchone()
    return bool(result[0])
   
def schedule_appointment():
    hospital_name = ["Ashok Rera Hospital", "Ashok Adlux Hospital", "Ashok CBCC Hospital"]  # Add your appointment options here
    selected_hospital = st.selectbox("Select a hospital", hospital_name)
    cursor = db.cursor()

    # Retrieve doctor data from the database
    cursor.execute("SELECT D_name, Speciality FROM doctor")
    doctor_data = cursor.fetchall()

    # Create a list of tuples with doctor name and speciality
    doctor_options = [(f"{doctor[0]} - {doctor[1]}", doctor[0]) for doctor in doctor_data]
    selected_doctor = st.selectbox("Select a Doctor", doctor_options)
    selected_date = st.date_input("Select a date", date.today())
    selected_time = st.time_input("Select a time")
    availability_status = is_doctor_available(selected_doctor[1], selected_date, selected_time)
    if st.button("Schedule"):
        if availability_status:
            st.success("Doctor is available for the appointment!")
            cursor = db.cursor()
            query = "SELECT * FROM patient WHERE ID = %s"
            cursor.execute(query, (patient_id,))
            result = cursor.fetchone()
            query = "SELECT D_name,Fee FROM doctor WHERE D_name = %s"
            cursor.execute(query, (selected_doctor[1],))
            result1 = cursor.fetchone()
            cursor.execute("INSERT INTO APPOINTMENT(p_id,p_Name,d_name,date,H_name,Fee,time) VALUES(%s,%s,%s,%s,%s,%s,%s)",(patient_id,result[1],result1[0],selected_date,selected_hospital,result1[1],selected_time))
            db.commit()
            st.success("Appointment scheduled successfully")
        else:
            st.warning("Doctor is not available at the specified date and time.")
            

def cancel_apppointment():
        st.title("Cancel Your Appointments")
        selected_date1 = st.date_input("Select a date", date.today())
        selected_time = st.time_input("Select a time")
        if st.button("Cancel"):
            cursor = db.cursor()
            query = "DELETE FROM Appointment WHERE date = %s AND time=%s"
            cursor.execute(query, (selected_date1,selected_time,))
            db.commit()
            st.warning("Cancelled")

def display_appointments():
    st.title("Appointments")
    appointment_options = ["Schedule an appointment", "Booked appointments", "Cancel appointment"]  # Add your appointment options here
    selected_appointment = st.selectbox("Select an option", appointment_options)
    st.write(" ")
    if selected_appointment=="Schedule an appointment":
        schedule_appointment()
    elif selected_appointment=="Booked appointments":
        booked_appointments_patient(patient_id)
    else:
        cancel_apppointment()
def payment():
        st.title("Your Payments")
        cursor=db.cursor()
        cursor.execute("SELECT Name FROM patient WHERE ID=%s",(patient_id,))
        result = cursor.fetchone()
        query = "SELECT * FROM payment WHERE P_name = %s"
        cursor.execute(query, (result))
        result2 = cursor.fetchall()
        if result2:
            modified_result = []
            for row in result2:
                row_list = list(row)
                row_list[6] = str(row_list[6])  # Assuming the 'time' column is at index 6
                modified_result.append(tuple(row_list))
            df = pd.DataFrame(modified_result, columns=["payment_id", "P_Name", "treatment_amount", "medicine_amount", "total_amount", "date", "time","Paid"])
            st.table(df)
        else:
             st.error("No Payments")
def hospitals():
        st.title("Our Hospitals")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM hospital")
        result2 = cursor.fetchall()
        df = pd.DataFrame(result2, columns=["Hospital Name", "Hospital id", "Email", "Address", "Contact"])
        st.table(df)


def parse_args():
    args = sys.argv
    arg_dict = {}
    i = 1
    while i < len(args):
        if args[i].startswith("--"):
            arg_name = args[i][2:]
            if i + 1 < len(args) and not args[i + 1].startswith("--"):
                arg_value = args[i + 1]
                arg_dict[arg_name] = arg_value
                i += 2
            else:
                arg_dict[arg_name] = None
                i += 1
        else:
            i += 1
    return arg_dict

# Function to retrieve patient_id from command-line arguments
def get_patient_id(args):
    return args.get("patient_id", None)


def display_profile():
    st.title("Profile")
    if patient_id is not None:
        cursor = db.cursor()
        query = "SELECT * FROM patient WHERE ID = %s"
        cursor.execute(query, (patient_id,))
        result = cursor.fetchone()
        if result:
            st.write("#### ID:", result[0])
            st.write("#### Name:", result[1])
            st.write("#### Gender:", result[2])
            st.write("#### DOB:", result[3])
            st.write("#### Contact:", result[4])
            st.write("#### Address:", result[5])
            st.write("#### Email:", result[6])
        else:
            st.markdown("Patient not found")
    else:
        st.write("Patient ID not set")
        
def medical_history():
    st.title("Medical History")
    if st.button("View your medical history"):
        view_mh(patient_id)
    if st.button("Add your medical history"):
        add_mh()
               
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/avif;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
    
set_background('./p.avif')
 
st.sidebar.title("Navigation")
args = parse_args()
patient_id = get_patient_id(args) 
# Create radio buttons in the sidebar
selected_page = st.sidebar.radio("Go to", ("Appointments", "View Medical History","Add Medical History", "Payment","Our Hospitals","Profile"))

if selected_page == "Appointments":
    display_appointments()
elif selected_page == "View Medical History":
    view_mh(patient_id)
elif selected_page == "Add Medical History":
    add_mh(patient_id)
elif selected_page == "Payment":
    payment()
elif selected_page =="Our Hospitals":
    hospitals()
elif selected_page =="Profile":
    display_profile()


# By default, display the patient page
if selected_page is None:
    patient_page()

