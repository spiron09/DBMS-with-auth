import streamlit as st
import pandas as pd
from database import add_data, get_tables, get_cols, get_data, exec_sql, delete_data, get_row, update_data, get_column
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import warnings


def update():
    table_list = get_tables()
    table = st.selectbox('Select a Table', table_list)
    cols = get_cols(table)
    id_col = get_column(table, cols[0])

    ID = st.selectbox('Select a id to update', id_col)
    df_temp = pd.DataFrame(get_data(table), columns=cols)
    selected_prev_vals = df_temp[df_temp[cols[0]] == ID].iloc[0]

    inp_keyval = {}
    for i in range(1, len(cols)):
        inp_keyval[cols[i]] = st.text_input(
            cols[i] + ": ", value=selected_prev_vals[cols[i]])

    if st.button("Update Data"):
        for key in inp_keyval:
            temp = inp_keyval[key]
            try:
                temp2 = int(temp)
                inp_keyval[key] = temp
            except Exception:
                inp_keyval[key] = "'" + temp+"'"

        update_data(table, inp_keyval, cols[0], ID)
        st.success("Successfully Updated the Data")


warnings.simplefilter(action='ignore', category=FutureWarning)


def delete():
    table_list = get_tables()
    table = st.selectbox('Select a Table', table_list, key="Table Delete")
    cols = get_cols(table)
    data = pd.DataFrame(get_data(table), columns=cols)
    gb = GridOptionsBuilder.from_dataframe(data)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()

    gb.configure_selection('multiple', use_checkbox=True,
                           groupSelectsChildren="Group checkbox select children")
    gridOptions = gb.build()

    grid_response = AgGrid(
        data,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT',
        update_mode='MODEL_CHANGED',
        fit_columns_on_grid_load=False,
        enable_enterprise_modules=True,
        height=350,
        width='100%',
        reload_data=False,
        theme='streamlit'
    )

    if st.button("Delete Data"):
        data = grid_response['data']
        selected = grid_response['selected_rows']
        df_temp = pd.DataFrame(selected)[cols[0]]
        delete_data(table, df_temp)
        st.success("Successfully deleted the data")


def sql():
    query = st.text_input("Enter SQL Query to execute:")

    if st.button("Execute"):
        res = exec_sql(query)
        st.success("Successfully executed the query!")
        if res:
            st.write("Query Result : ")
            st.dataframe(res)


def read():
    table_list = get_tables()

    select_view_table = st.selectbox("Table to View :", table_list)
    cols = get_cols(select_view_table)
    df = pd.DataFrame(get_data(select_view_table), columns=cols)
    st.table(df)


def insert():
    table_list = get_tables()

    with st.expander("View Database"):
        select_view_table = st.selectbox("Table to View : ", table_list)
        cols = get_cols(select_view_table)
        df = pd.DataFrame(get_data(select_view_table), columns=cols)
        st.table(df)

    table = st.selectbox('Select a Table to add Data to', table_list)

    col_list = get_cols(table)
    dictionary = {}
    for i in range(len(col_list)):
        dictionary[col_list[i]] = st.text_input(col_list[i])

    if st.button("Insert Data"):
        for key in dictionary:
            temp = dictionary[key]
            try:
                temp2 = int(temp)
                dictionary[key] = temp
            except Exception:
                dictionary[key] = "'" + temp+"'"

        add_data(table, dictionary)
        st.success("Successfully Inserted the Data")


def login_auth(email, password):
    st_data = exec_sql("SELECT * FROM Student WHERE Email = '"+email+"'")
    if len(st_data) == 1 and st_data[0][1] == password:
        return True, 'student', st_data[0][0]
    
    in_data = exec_sql("SELECT * FROM Instructors WHERE Email = '"+email+"'")
    if len(in_data) == 1 and in_data[0][1] == password:
        return True, 'instructor', in_data[0][0]
    
    ad_data = exec_sql("SELECT * FROM Admin WHERE Admin_mail = '"+email+"'")
    print(ad_data)
    if len(ad_data) == 1 and ad_data[0][2] == password:
        return True, 'admin'
    
    return False, ''