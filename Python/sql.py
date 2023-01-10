import streamlit as st
from database import exec_sql

def write_sql():
    query = st.text_input("Enter SQL Query to execute:")

    if st.button("Execute"):
        res = exec_sql(query)
        st.success("Successfully executed the query!")
        if res:
            st.write("Query Result : ")
            st.dataframe(res)