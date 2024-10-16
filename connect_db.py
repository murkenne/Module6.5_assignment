import mysql.connector
from mysql.connector import Error

# Function to connect to the database
def connect_database():
    db_name = "fitness_center_database"
    user = "root"
    password = "Tekking58!"
    host = "localhost"

    try:
        conn = mysql.connector.connect(
            database=db_name,
            user=user,
            password=password,
            host=host
        )
        return conn
    except Error as e:
        print(f"Database connection error: {e}")
        return None

# Function to add a new member to the database
def add_member_to_db(name, age, gender, membership_type):
    conn = connect_database()
    cursor = conn.cursor()

    query = "INSERT INTO Members (name, age, gender, membership_type) VALUES (%s, %s, %s, %s)"
    values = (name, age, gender, membership_type)

    cursor.execute(query, values)
    conn.commit()
    
    member_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return member_id

# Function to retrieve a member by ID
def get_member_from_db(member_id):
    conn = connect_database()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM Members WHERE id = %s"
    cursor.execute(query, (member_id,))
    member = cursor.fetchone()

    cursor.close()
    conn.close()

    return member

# Function to update a member by ID
def update_member_in_db(member_id, name, age, gender, membership_type):
    conn = connect_database()
    cursor = conn.cursor()

    query = """
    UPDATE Members 
    SET name = %s, age = %s, gender = %s, membership_type = %s 
    WHERE id = %s
    """
    values = (name, age, gender, membership_type, member_id)

    cursor.execute(query, values)
    conn.commit()

    rowcount = cursor.rowcount
    cursor.close()
    conn.close()

    return rowcount > 0  # Return True if a row was updated

# Function to delete a member by ID
def delete_member_from_db(member_id):
    conn = connect_database()
    cursor = conn.cursor()

    query = "DELETE FROM Members WHERE id = %s"
    cursor.execute(query, (member_id,))
    conn.commit()

    rowcount = cursor.rowcount
    cursor.close()
    conn.close()

    return rowcount > 0  # Return True if a row was deleted
