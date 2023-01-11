import mysql.connector

database = mysql.connector.connect(
    host="localhost", user="root", password="root", database="Drivingschool"
)
curs = database.cursor(buffered=True)


def get_tables():
    curs.execute('SHOW TABLES')
    raw_tables = curs.fetchall()
    table_list = [x[0] for x in raw_tables]
    return table_list


def get_cols(name):
    curs.execute('SHOW COLUMNS FROM {}'.format(name))
    raw_cols = curs.fetchall()
    col_list = [x[0] for x in raw_cols]
    return col_list


def add_data(name, data):
    col_names = ",".join(data.keys())
    vals = ",".join(data.values())
    curs.execute(f"INSERT INTO {name} ({col_names}) VALUES ({vals})")
    database.commit()


def get_data(name):
    curs.execute(f"SELECT * FROM {name}")
    data = curs.fetchall()
    return data

def get_lesson_data(id):
    curs.execute(f"SELECT Date, Time, Duration, First_Name as Instructor_Name, Brand as Vehicle_Name from Instructors NATURAL JOIN Lessons NATURAL JOIN Vehicles WHERE Student_ID = '{id}'")
    data = curs.fetchall()
    return data


def delete_data(name, df):
    for each_id in df:
        curs.execute(f"DELETE FROM {name} WHERE {df.name}='{each_id}'") 
    # database.commit


def get_row(name, df):
    curs.execute(f"SELECT * FROM {name} WHERE {df.name}='{df[0]}'")
    data = curs.fetchall()
    return data


def get_column(name, col_name):
    curs.execute(f"SELECT {col_name} FROM {name}")
    data = curs.fetchall()
    return ([i[0] for i in data])


def update_data(name, inp_keyval, id_col_name, id_col_val):
    col_val = ""
    for k in inp_keyval:
        col_val += k + " = " + inp_keyval[k] + ","
    col_val = col_val[:-1]

    curs.execute(
        f"UPDATE {name} SET {col_val} WHERE {id_col_name}='{id_col_val}'")
    database.commit()


def exec_sql(query):
    curs.execute(query)
    data = curs.fetchall()
    return data

def create_user(query):
    print(query)
    curs.execute(query)
    database.commit()
   