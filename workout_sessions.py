import mysql.connector
from mysql.connector import Error
from connect_db import connect_database  

# Function to schedule a new workout session
def schedule_workout_session(member_id, session_date, session_time, activity):
    conn = connect_database()
    cursor = conn.cursor()

    query = """
    INSERT INTO WorkoutSessions (member_id, session_date, session_time, activity)
    VALUES (%s, %s, %s, %s)
    """
    values = (member_id, session_date, session_time, activity)

    cursor.execute(query, values)
    conn.commit()
    
    session_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return session_id

def get_all_workout_sessions():
    conn = connect_database()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM WorkoutSessions"
    cursor.execute(query)
    sessions = cursor.fetchall()

    cursor.close()
    conn.close()

    return sessions


# Function to update a workout session
def update_workout_session(session_id, session_date, session_time, activity):
    conn = connect_database()
    cursor = conn.cursor()

    query = """
    UPDATE WorkoutSessions 
    SET session_date = %s, session_time = %s, activity = %s 
    WHERE session_id = %s
    """
    values = (session_date, session_time, activity, session_id)

    cursor.execute(query, values)
    conn.commit()

    rowcount = cursor.rowcount
    cursor.close()
    conn.close()

    return rowcount > 0  # Return True if a row was updated


def get_workout_sessions_by_member(member_id):
    conn = connect_database()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM WorkoutSessions WHERE member_id = %s"
    cursor.execute(query, (member_id,))
    sessions = cursor.fetchall()

    cursor.close()
    conn.close()

    return sessions
