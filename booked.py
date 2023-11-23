import streamlit as st
import mysql.connector
from datetime import date
session_state = st.session_state
import subprocess
import pandas as pd

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="amulya1623",
    database="hms",
    auth_plugin='mysql_native_password'
)


    
def booked_appointments_on_current_date(doctor_id):
    st.title("Booked Appointments on Current Date")

    if st.button("Show Booked Appointments on Current Date"):
        cursor = db.cursor()
        current_date_string = date.today()#.strftime("%Y-%m-%d")
        cursor.execute("SELECT D_name FROM doctor WHERE D_id=%s",(doctor_id,))
        doctor_name = cursor.fetchone()
        # Call the stored procedure to get appointments on the current date
        cursor.execute("CALL GetAppointmentsOnCurrentDate(%s,%s)", (current_date_string,doctor_name[0],))
        result = cursor.fetchall()
        if result:
            modified_result = []
            for row in result:
                row_list = list(row)
                row_list[6] = str(row_list[6])  # Assuming the 'time' column is at index 6
                modified_result.append(tuple(row_list))
            df = pd.DataFrame(modified_result, columns=["Patient ID", "Patient Name", "Doctor Name", "Date", "Hospital name", "Fee", "Time"])
            st.table(df)
        else:
            st.warning("No booked appointments on the current date")

def booked_appointments(doctor_id):
        if not db.is_connected():
            db.reconnect()

        st.title("Your Booked Appointments")
        cursor = db.cursor()
        cursor.execute("SELECT D_name FROM doctor WHERE D_id=%s",(doctor_id,))
        doctor_data = cursor.fetchone()
        cursor.execute("SELECT * FROM appointment WHERE D_name=%s", (doctor_data[0],))
        result2 = cursor.fetchall()
        if result2:
            modified_result = []
            for row in result2:
                row_list = list(row)
                row_list[6] = str(row_list[6])  # Assuming the 'time' column is at index 6
                modified_result.append(tuple(row_list))
            df = pd.DataFrame(modified_result, columns=["Patient ID", "Patient Name", "Doctor Name", "Date", "Hospital name", "Fee", "Time"])
            st.table(df)
        else:
             st.warning("No booked appointments")
        booked_appointments_on_current_date(doctor_id)

def booked_appointments_patient(patient_id):
        cursor = db.cursor()
        query = "SELECT * FROM appointment WHERE P_ID = %s"
        cursor.execute(query, (patient_id,))
        result2 = cursor.fetchall()
        if result2:
            modified_result = []
            for row in result2:
                row_list = list(row)
                row_list[6] = str(row_list[6])  # Assuming the 'time' column is at index 6
                modified_result.append(tuple(row_list))
            df = pd.DataFrame(modified_result, columns=["P_ID", "P_Name", "D_Name", "date", "H_name", "Fee", "time"])
            st.table(df)
        else:
             st.error("No booked appointments")
# Modify the selected_page section in your script
