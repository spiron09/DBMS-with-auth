import streamlit as st
from functions import insert, update, delete, read
from sql import write_sql


def main():
    st.set_page_config(
        page_title="Driving School Management System",
        layout="wide",
    )

    st.title("Driving School Management System")
    menu = ["View Tables", "Insert Entry",
            "Update Entry", "Delete Entry", "Custom SQL"]

    view_tab, insert_tab, update_tab, delete_tab, custom_tab = st.tabs(menu)

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


if __name__ == '__main__':
    main()
