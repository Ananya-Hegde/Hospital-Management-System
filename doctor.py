import streamlit as st
import mysql.connector
import sys,base64
from datetime import date,datetime,timedelta
session_state = st.session_state
import subprocess
from mh import view_mh,add_mh
import pandas as pd
from booked import booked_appointments_on_current_date,booked_appointments

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="amulya1623",
    database="hms",
    auth_plugin='mysql_native_password'
)

def get_doctor_stats(doctor_name):
    cursor = db.cursor()
    start_date = date.today() - timedelta(days=date.today().weekday())
    end_date = start_date + timedelta(days=6)
    query = """
    SELECT
        (SELECT COUNT(*)
        FROM appointment
        WHERE D_name = %s
            AND date BETWEEN %s AND %s) AS appointment_count,
        (SELECT SUM(Fee)
        FROM appointment
        WHERE D_name = %s
            AND date BETWEEN %s AND %s) AS total_earnings
    """
    cursor.execute(query, (doctor_name, start_date,end_date, doctor_name,start_date,end_date,))
    result = cursor.fetchall()
    appointment_count=result[0][0]
    total_earnings=result[0][1]
    return appointment_count, total_earnings

def doctor_page():
    cursor=db.cursor()
    cursor.execute("SELECT D_name FROM doctor WHERE D_id=%s",(doctor_id,))
    doctor_name = cursor.fetchone()
    st.title("Earnings this week")
    appointment_count, total_earnings = get_doctor_stats(doctor_name[0])
    st.write(f"#### Appointment Count: {appointment_count}")
    st.write(f"#### Total Earnings: {total_earnings}")
    # Add content specific to the patient page

def update_medical_history():
    st.title("Update Medical History")
    pid=st.text_input("Patient id:")
    cursor = db.cursor()
    # Retrieve doctor data from the database
    cursor.execute("SELECT Surgeries_health_issues FROM medical_history WHERE P_id=%s",(pid,))
    mh_data = cursor.fetchall()

    # Create a list of tuples with doctor name and speciality
    mh_options = [(mh[0]) for mh in mh_data]
    selected_mh = st.selectbox("Select the option", mh_options)
    m = st.text_input("Medications (ex:,crocin,aspirin,):")
    if st.button("Update"):
        cursor = db.cursor()
        cursor.execute("UPDATE medical_history SET Medications = CONCAT( Medications, %s) WHERE Surgeries_health_issues=%s",(m,selected_mh))
        db.commit()
        st.success("Updated successfully!")

def view_medical_history():
    st.title("Medical History")
    st.write("This is the Medical History page content.")
    pid=st.text_input("Patient ID:")
    if st.button("View"):
        cursor = db.cursor()
        query = f"SELECT * FROM patient WHERE id = '{pid}'"
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            query = "SELECT * FROM medical_history WHERE P_ID = %s"
            cursor.execute(query, (pid,))
            result2 = cursor.fetchall()
            if result2:
                df = pd.DataFrame(result2, columns=["Patient_id", "Patient Name", "Surgeries/Health Issues", "Medications", "Date"])
                st.table(df)
            else:
                st.warning("No medical history")
        else:
            st.error("Patient Not Available")
def update_medical_history():
    st.title("Update Medical History")
    pid=st.text_input("Patient id:")
    s_hi = st.text_input("Surgeries or Health issues:")
    m = st.text_input("Medications (before and current):")
    d = st.date_input("Date of surgery/diagnosis")
    if st.button("Add"):
        cursor = db.cursor()
        cursor = db.cursor()
        query = "SELECT name FROM patient WHERE ID = %s"
        cursor.execute(query, (pid,))
        result = cursor.fetchone()
        cursor.execute("INSERT INTO medical_history(p_id,p_Name,Surgeries_health_issues,Medications,date) VALUES(%s,%s,%s,%s,%s)",(pid,result[1],s_hi,m,d))
        db.commit()
        st.success("Added successfully!")
        
def cancel_apppointment():
        st.title("Cancel Your Appointments")
        selected_date1 = st.date_input("Select a date", date.today())
        st.write(selected_date1)
        selected_time = st.time_input("Select a time")
        st.write("Selected time:", selected_time)
        if st.button("Cancel"):
            cursor = db.cursor()
            query = "DELETE FROM Appointment WHERE date = %s AND time=%s"
            cursor.execute(query, (selected_date1,selected_time,))
            db.commit()
            st.warning("Cancelled")


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
def get_doctor_id(args):
    return args.get("doctor_id", None)


def display_profile():
    st.title("Profile")
    if doctor_id is not None:
        cursor = db.cursor()
        query = "SELECT * FROM doctor WHERE D_id = %s"
        cursor.execute(query, (doctor_id,))
        result = cursor.fetchone()
        if result:
            st.write("#### Id:", result[0])
            st.write("#### Name:", result[1])
            st.write("#### Speciality:", result[2])
            st.write("#### Hospital Address:", result[6])
            st.write("#### Hospital ID:", result[3])
            st.write("#### Fee:", result[4])
            st.write("#### Contact:", result[5])
    else:
        st.write("Doctor ID not set")

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/jpg;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
    
set_background('./doctor_bg.jpg')
                
st.sidebar.title("Choose")
args = parse_args()
doctor_id = get_doctor_id(args) 
# Create radio buttons in the sidebar
selected_page = st.sidebar.radio("Go to", ("Booked Appointments","Cancel Appointment","View Medical History","Update Medical History","Earnings","Profile"))

if selected_page == "Earnings":
    doctor_page()
elif selected_page == "Booked Appointments":
    booked_appointments(doctor_id)
elif selected_page == "Cancel Appointment":
    cancel_apppointment()
elif selected_page == "View Medical History":
    view_medical_history()
elif selected_page == "Update Medical History":
    update_medical_history()
elif selected_page=="Profile":
    display_profile()


# By default, display the patient page


