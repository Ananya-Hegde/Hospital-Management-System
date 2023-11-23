# Hospital-Management-System
## Open MySQL and create database 
```ruby
   CREATE DATABASE hms;
   USE hms;
   ```
## Create tables using the below commands in MySQL
```ruby
   CREATE TABLE login (
    ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    patient_id VARCHAR(255),
    patient_doctor CHAR(100) NOT NULL
);
```
```ruby
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
```
```ruby
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

```

```ruby
CREATE TABLE medical_history (
    P_id char(100) NOT NULL,
    P_name varchar(100),
    Surgeries_health_issues varchar(100),
    Medications varchar(100),
    Date date,
    PRIMARY KEY (P_id)
);
```
```ruby
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
```
```ruby
CREATE TABLE hospital (
    H_name varchar(100) NOT NULL,
    H_id varchar(100) PRIMARY KEY,
    Email varchar(100),
    Address varchar(100),
    contact bigint NOT NULL
);
```
```ruby
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
 ```
 ### Create functions,triggers,procedure using the below commands
  ```ruby
  DELIMITER //
CREATE TRIGGER set_patient_id BEFORE INSERT ON login
FOR EACH ROW
BEGIN
    SET NEW.patient_id = CONCAT('P_', NEW.ID);
END;
//
DELIMITER ;
```
```ruby
DELIMITER //
CREATE TRIGGER set_login_id_patient BEFORE INSERT ON patient
FOR EACH ROW
BEGIN
    SET NEW.ID = (
        SELECT patient_id FROM login
        WHERE ID = NEW.ID
    );
END;
//
DELIMITER ;
```
```ruby
DELIMITER //

CREATE PROCEDURE GetAppointmentsOnCurrentDate(IN current_date_param DATE,IN dname VARCHAR(100))
BEGIN
    SELECT * FROM appointment WHERE date = current_date_param and D_name=dname;
END //

DELIMITER ;
```
```ruby
DELIMITER //

CREATE FUNCTION IsDoctorAvailableForAppointment(
    doctor_name VARCHAR(100),
    appointment_date DATE,
    appointment_time TIME
) RETURNS BOOLEAN
DETERMINISTIC
BEGIN
    DECLARE appointment_count INT DEFAULT 0;

    -- Count the number of appointments for the doctor at the specified date and time
    SELECT COUNT(*)
    INTO appointment_count
    FROM appointment
    WHERE D_name = doctor_name
        AND date = appointment_date
        AND time = appointment_time;

    -- If the count is 0, the doctor is available; otherwise, the doctor is not available
    RETURN appointment_count = 0;
END //

DELIMITER ;
```
### Open vs code terminal or any other terminal and run the following commands
### Install streamlit using the command:
```ruby
pip install streamlit
``` 
### run the files using the given command:
```ruby
streamlit run login.py
```
  