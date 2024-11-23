import streamlit as st
import subprocess
import pymysql
import hashlib

# Database connection
def create_connection():
    return pymysql.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="Sudarshan@SQL",  # Replace with your MySQL password
        database="user_management",
        cursorclass=pymysql.cursors.DictCursor  # Return results as dictionaries
    )

# Utility function for password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Registration Function
def register_user(email, password, name, phone):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO users (email, password, name, phone) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (email, hash_password(password), name, phone))
        conn.commit()
        st.success("Registration successful!")
    except pymysql.err.IntegrityError:
        st.error("Email already registered. Please use a different email.")
    except pymysql.Error as err:
        st.error(f"Database Error: {err}")
    finally:
        conn.close()

# Login Function
def login_user(email, password):
    conn = create_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE email = %s AND password = %s"
    cursor.execute(query, (email, hash_password(password)))
    user = cursor.fetchone()
    subprocess.run(["streamlit", "run", "E:\\streamlit\\cnvrted.py"])

    conn.close()
    return user

# Reset Password Function
def reset_password(email, new_password):
    conn = create_connection()
    cursor = conn.cursor()
    query_check = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query_check, (email,))
    user = cursor.fetchone()

    if user:
        query_update = "UPDATE users SET password = %s WHERE email = %s"
        cursor.execute(query_update, (hash_password(new_password), email))
        conn.commit()
        st.success("Password updated successfully!")
    else:
        st.error("Email not found. Please register first.")
    conn.close()

# Update User Information
def update_user(email, name, phone):
    conn = create_connection()
    cursor = conn.cursor()
    query_check = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query_check, (email,))
    user = cursor.fetchone()

    if user:
        query_update = "UPDATE users SET name = %s, phone = %s WHERE email = %s"
        cursor.execute(query_update, (name, phone, email))
        conn.commit()
        st.success("Information updated successfully!")
    else:
        st.error("Email not found. Please register first.")
    conn.close()

# Streamlit App
st.title("User Management System")

menu = ["Register", "Login", "Forgot Password", "Update Info"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Register":
    st.subheader("Register")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    name = st.text_input("Name")
    phone = st.text_input("Phone")
    if st.button("Register"):
        if email and password:
            register_user(email, password, name, phone)
        else:
            st.error("Please provide all required fields.")

elif choice == "Login":
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.success(f"Welcome, {user['name']}!")
            st.write(f"Your email: {user['email']}")
            st.write(f"Your phone: {user['phone']}")
        else:
            st.error("Invalid email or password.")

elif choice == "Forgot Password":
    st.subheader("Forgot Password")
    email = st.text_input("Email")
    new_password = st.text_input("New Password", type="password")
    if st.button("Reset Password"):
        if email and new_password:
            reset_password(email, new_password)
        else:
            st.error("Please provide both email and new password.")

elif choice == "Update Info":
    st.subheader("Update Info")
    email = st.text_input("Email")
    name = st.text_input("New Name")
    phone = st.text_input("New Phone")
    if st.button("Update"):
        if email:
            update_user(email, name, phone)
        else:
            st.error("Please provide your email.")
