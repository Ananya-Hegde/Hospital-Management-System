import mysql.connector
import streamlit as st
import subprocess,base64,time
session_state = st.session_state
from streamlit import components

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="amulya1623",
    database="hms",
    auth_plugin='mysql_native_password'
)

# Define the main page
def main():
    st.title("ASHOK HOSPITALS")
    st.header("Choose an option:")
    
    if st.button("Login"):
        st.session_state.page = "login_page"
    
    if st.button("Sign Up"):
        st.session_state.page = "signup_page"


patient_id=None
doctor_id=None
# Define the login page
def refresh_page():
    # Add a button to refresh the page
    if st.button("Refresh Page"):
        # Display a message indicating that the page is refreshing

            # Manually trigger a rerun of the Streamlit app
            st.rerun()

# Example usage

def login_page():
    st.title("Login Page")
    with st.form("login_form"):
        st.subheader("Please enter your login credentials:")
        user=st.text_input("Patient(P)/Doctor(D)")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Submit")
        if submit_button:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM login WHERE patient_doctor=%s AND username = %s AND password = %s", (user,username, password))
            result = cursor.fetchone()
            if result:
                if user == "P":
                    st.success("Login successful as Patient")
                    # Execute the patient.py script when the login is successful
                    global patient_id
                    patient_id = result[3] 
                    subprocess.run(["streamlit", "run", "patient.py","--","--patient_id", str(patient_id)])
                else:
                    st.success("Login successful as Doctor")
                    global doctor_id
                    doctor_id = result[3] 
                    subprocess.run(["streamlit", "run", "doctor.py","--","--doctor_id", str(doctor_id)])
            else:
                st.error("Wrong password/username")
    
    refresh_page()
        
# Define the sign-up page
def signup_page():
    st.title("Sign Up Page")
    st.header("Please sign up for a new account:")
    with st.form("login_form"):
        new_name=st.text_input("Full Name")
        new_gender=st.text_input("Gender(F/M)")
        new_dob=st.text_input("Date Of Birth(YYYY-MM-DD)")
        new_contact=st.text_input("Contact(10 digits)")
        new_address=st.text_input("Address")
        new_email=st.text_input("Email")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        submit_button = st.form_submit_button("Register")
        if submit_button:
            # Store the new user in the database (you can add your logic here)
            try:
                cursor = db.cursor()
                cursor.execute("INSERT INTO login (patient_doctor,username, password) VALUES (%s,%s, %s)", ('P',new_username, new_password))
                cursor.execute("SELECT LAST_INSERT_ID()")
                last_inserted_id = cursor.fetchone()[0]
                cursor.execute("INSERT INTO Patient(id,Name,Gender,DOB,Contact,Address,Email) VALUES(%s,%s,%s,%s,%s,%s,%s)",(last_inserted_id,new_name,new_gender,new_dob,new_contact,new_address,new_email))
                db.commit()
                st.success("User registered successfully")
            except Exception as e:
                st.error(f"Fill all the right details")

#st.image("image(2).png")
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/jpeg;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
    
set_background('./l.jpeg')
# Create a page router
def page_router():
    if st.session_state.page == "login_page":
        login_page()
    elif st.session_state.page == "signup_page":
        signup_page()
    else:
        main()  # Default to the main page

if "page" not in st.session_state:
    st.session_state.page = "main_page"

page_router()