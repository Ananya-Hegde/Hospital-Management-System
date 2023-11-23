# Hospital-Management-System
## Open MySQL and create database 
'''ruby
   CREATE DATABASE hms;
   '''
## change the database to hms using "use hms;" and create tables using the below commands in MySQL
'''ruby
   CREATE TABLE login (
    ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    patient_id VARCHAR(255),
    patient_doctor CHAR(100) NOT NULL
);
'''
'''
CREATE TABLE patient (
    ID varchar(50) NOT NULL,
    Name char(100) NOT NULL,
    Gender char(1) NOT NULL,
    DOB date NOT NULL,
    Contact bigint,
    Address varchar(200),
    Email varchar(30),
    PRIMARY KEY (ID)
);
'''
'''
CREATE TABLE doctor (
    D_id varchar(100) NOT NULL,
    D_name varchar(200),
    Speciality varchar(100) NOT NULL,
    Hospital_id varchar(10) NOT NULL,
    Fee int,
    Contact bigint,
    Address varchar(200),
    PRIMARY KEY (D_id),
    FOREIGN KEY (Hospital_id) REFERENCES hospital(H_id) ON DELETE CASCADE
);

'''

'''
CREATE TABLE medical_history (
    P_id char(100) NOT NULL,
    P_name varchar(100),
    Surgeries_health_issues varchar(100),
    Medications varchar(100),
    Date date,
    PRIMARY KEY (P_id)
);
'''
'''
CREATE TABLE appointment (
    P_ID varchar(100) NOT NULL,
    P_NAME char(100),
    D_name char(100),
    date date,
    H_name varchar(100),
    Fee int,
    time time,
    PRIMARY KEY (P_ID),
    FOREIGN KEY (D_name) REFERENCES doctor(D_name) ON DELETE CASCADE,
    FOREIGN KEY (H_name) REFERENCES hospital(H_name) ON DELETE CASCADE
);
'''
'''
CREATE TABLE hospital (
    H_name varchar(100) NOT NULL,
    H_id varchar(100) PRIMARY KEY,
    Email varchar(100),
    Address varchar(100),
    contact bigint NOT NULL
);
'''
'''
CREATE TABLE payment (
    payment_id varchar(1000) NOT NULL,
    P_name varchar(100),
    treatment_amount int,
    medicines_amount int,
    total_amount int,
    date date,
    time time,
    Paid char(3)
);
 ''' 