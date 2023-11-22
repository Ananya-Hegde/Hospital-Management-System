import streamlit as st
import mysql.connector
from datetime import date
session_state = st.session_state
import subprocess


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="amulya1623",
    database="hms",
    auth_plugin='mysql_native_password'
)



def view_mh(patient_id):
    st.title("Your Medical History")
    cursor = db.cursor()
    query = "SELECT * FROM medical_history WHERE P_ID = %s"
    cursor.execute(query, (patient_id,))
    result2 = cursor.fetchall()
    if result2:
        for mh in result2:
            st.write("###### Patient ID:",mh[0])
            st.write("###### Patient Name:",mh[1])
            st.write("###### Surgeries/Health issues:",mh[2])
            st.write("###### Medications:",mh[3])
            st.write("###### Date:",mh[4])
            st.write("=======================================================")
    else:
            st.info("No medical history")


st.write("Outside the form")


    
def add_mh(patient_id):
        st.title("Add Medical History")
        s_hi = st.text_input("Surgeries or Health issues:")
        m = st.text_input("Medications (before and current):")
        d = st.date_input("Date of surgery/diagnosis")
        if st.button("ADD"):
            cursor=db.cursor()
            query = "SELECT name FROM patient WHERE ID = %s"
            cursor.execute(query, (patient_id,))
            name = cursor.fetchone()
            cursor.execute("INSERT INTO medical_history(p_id,p_Name,Surgeries_health_issues,Medications,date) VALUES(%s,%s,%s,%s,%s)",(patient_id,name[0],s_hi,m,d))
            db.commit()
            st.write("Added successfully!")
        
                
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
