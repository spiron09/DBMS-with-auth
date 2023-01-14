import pandas as pd
import streamlit as st
from functions import insert, update, delete, read, login_auth
from database import exec_sql, get_lesson_data_student, create_user, get_lesson_data_inst
from sql import write_sql
import mysql.connector
# database = mysql.connector.connect(
#     host="localhost", user="root", password="root", database="Drivingschool"
# )
# curs = database.cursor(buffered=True)
def logged_in_clicked(user_name, password):
    auth_res = login_auth(user_name, password)
    print(auth_res)
    if auth_res[0]:
        st.session_state['userType'] = auth_res[1]
        st.session_state['loggedIn'] = True
        if st.session_state['userType'] == 'student':
            st.session_state['studentID'] = auth_res[2]
        elif st.session_state['userType'] == 'instructor':
            st.session_state['instructorID'] = auth_res[2]
        
    else:
        st.session_state['loggedIn'] = False
        st.error("Invalid user name or password")

def register_clicked(sid, password, fname, lname, phone_number,user_name):
    st.session_state['loggedIn'] = False
    if exec_sql("SELECT * FROM Student WHERE Student_ID = '"+sid+"'"):
        st.error("Student ID already exists")
    elif exec_sql("SELECT * FROM Student WHERE Email = '"+user_name+"'"):
        st.error("Email already exists")
    else:
        create_user("INSERT INTO Student VALUES ("+sid+",'"+password+"', '"+fname+"', '"+lname+"', '"+phone_number+"','"+user_name+"')")
        # curs.execute(q)  
        st.success("Successfully registered the user")

def login(login_page):
    with login_page:
        m = ["Login", "Register"]
        login_tab, register_tab = st.tabs(
            m)
        with login_tab:
            st.subheader("Login")
            if st.session_state['loggedIn'] == False:
                user_name = st.text_input("Enter your email")
                password = st.text_input("Enter password", type="password")
                st.button("Login", on_click=logged_in_clicked,
                        args=(user_name, password))
        with register_tab:
            st.subheader("Register")
            sid = st.text_input("Enter Student ID")
            fname = st.text_input("Enter First Name")
            lname = st.text_input("Enter Last Name")
            user_name = st.text_input("Enter Mail")
            phone_number = st.text_input("Enter Phone Number", type="default")
            password = st.text_input("Enter Password", type="password")
            st.button("Register", on_click=register_clicked,
                    args=(sid, password, fname, lname, phone_number, user_name))


def logged_out_clicked():
    st.session_state['loggedIn'] = False


def logout(logout_page, login_page):
    login_page.empty()
    with logout_page:
        st.button("Log Out", key="logout", on_click=logged_out_clicked)


def student(student_page):
    with student_page:
        m = ["My Lessons", "Book Lesson"]
        lesson_tab, book_lesson_tab = st.tabs(
            m)
        with lesson_tab:
            cols = ["Date", "Time", "Duration", "Instructor_Name", "Vehicle_Name"]
            df = pd.DataFrame(get_lesson_data_student(str(st.session_state['studentID'])), columns=cols)
            res = exec_sql("SELECT Date, Time, Duration, First_Name as Instructor_Name, Brand as Vehicle_Name from Instructors NATURAL JOIN Lessons NATURAL JOIN Vehicles WHERE Student_ID = '"+str(st.session_state['studentID'])+"'")
            # res = exec_sql("SELECT * from Instructors NATURAL JOIN Lessons NATURAL JOIN Vehicles WHERE Student_ID = '"+str(st.session_state['studentID'])+"'")
            # print(res)
            stu_name = exec_sql("SELECT First_Name from Student WHERE Student_ID = '"+str(st.session_state['studentID'])+"'")
            # print(name)
            st.subheader(stu_name[0][0]+"'s" + " Lessons")
            # st.success("Successfully executed the query!")
            if res:
                st.table(df)
            else:
                st.error("No lessons found")
        with book_lesson_tab:
            st.subheader("Book Lesson")
            date = st.date_input("Enter Date")

def instructor(instrucutor_page):
    with instrucutor_page:
        m = ["My Schedule", "Book Lesson"]
        my_schedule, book_lesson_tab = st.tabs(
            m)
        with my_schedule:
            cols = ["Date", "Time", "Duration", "Student_Name", "Vehicle_Name"]
            df = pd.DataFrame(get_lesson_data_inst(str(st.session_state['instructorID'])), columns=cols)
            res = exec_sql("SELECT Date, Time, Duration, First_Name as Student_Name, Brand as Vehicle_Name from Student NATURAL JOIN Lessons NATURAL JOIN Vehicles WHERE Student_ID = '"+str(st.session_state['instructorID'])+"'")
            # res = exec_sql("SELECT * from Instructors NATURAL JOIN Lessons NATURAL JOIN Vehicles WHERE Student_ID = '"+str(st.session_state['studentID'])+"'")
            # print(res)
            in_name = exec_sql("SELECT First_Name from Instructors WHERE Instructor_ID = '"+str(st.session_state['instructorID'])+"'")
            # print(name)
            st.subheader(in_name[0][0]+"'s" + " Schedule")
            # st.success("Successfully executed the query!")
            if res:
                st.table(df)
            else:
                st.error("No lessons found")
        with book_lesson_tab:
            st.subheader("Book Lesson")
            date = st.date_input("Enter Date")



def admin(admin_page):
    with admin_page:
        # in_name = exec_sql("SELECT First_Name from admins WHERE admin_ID = '"+str(st.session_state['admin_ID'])+"'")
        st.subheader("Welcome admin!")
        menu = ["View Tables", "Insert Entry",
                "Update Entry", "Delete Entry", "Custom SQL"]

        view_tab, insert_tab, update_tab, delete_tab, custom_tab = st.tabs(
            menu)

        with view_tab:
            st.subheader("View Issues Database")
            st.write("Choose to view one Table from the Database")
            read()
        with insert_tab:
            st.subheader("Insert Row into Table")
            st.write("Choose a Table to Insert a Row of Data")
            insert()
        with update_tab:
            st.subheader("Update Existing Row in Table")
            st.write("Choose a Table to Update a Row of Data")
            update()
        with delete_tab:
            st.subheader("Delete Existing Row in Table")
            st.write("Choose a Table to Delete a Row of Data")
            delete()
        with custom_tab:
            st.subheader("Write Custom SQL Query")
            write_sql()


def main():
    st.set_page_config(
        page_title="Driving School Management System",
        layout="wide",
    )

    page = st.container()
    login_page = st.container()
    logout_page = st.container()
    student_page = st.container()
    admin_page = st.container()
    instructor_page = st.container()

    with page:
        st.title("Driving School Management System")

        if 'loggedIn' not in st.session_state:
            st.session_state['loggedIn'] = False
            login(login_page)
        else:
            if st.session_state['loggedIn'] and st.session_state['userType'] == 'student':
                logout(logout_page, login_page)
                student(student_page)
            elif st.session_state['loggedIn'] and st.session_state['userType'] == 'admin':
                logout(logout_page, login_page)
                admin(admin_page)
            elif st.session_state['loggedIn'] and st.session_state['userType'] == 'instructor':
                
                logout(logout_page, login_page)
                instructor(instructor_page)
            else:
                login(login_page)


if __name__ == '__main__':
    main()
