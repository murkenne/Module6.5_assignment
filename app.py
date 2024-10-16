from flask import Flask, jsonify, request
from connect_db import add_member_to_db, get_member_from_db, update_member_in_db, delete_member_from_db
from workout_sessions import schedule_workout_session, update_workout_session, get_workout_sessions_by_member, get_all_workout_sessions
from schemas import ma, MemberSchema, WorkoutSessionSchema  # Import the schemas

app = Flask(__name__)
ma.init_app(app)  # Initialize Marshmallow with the Flask app

# Route to add a new member
@app.route("/members", methods=['POST'])
def add_member():
    data = request.get_json()

    # Validate input data using Marshmallow
    member_schema = MemberSchema()
    errors = member_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Destructure data for database insertion
    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')
    membership_type = data.get('membership_type')

    try:
        member_id = add_member_to_db(name, age, gender, membership_type)
        member_data = {
            "id": member_id,
            "name": name,
            "age": age,
            "gender": gender,
            "membership_type": membership_type
        }
        result = member_schema.dump(member_data)
        return jsonify({"message": "Member added successfully", "member": result}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to get a member by ID
@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    try:
        member = get_member_from_db(id)
        if member:
            member_schema = MemberSchema()
            result = member_schema.dump(member)
            return jsonify(result), 200
        else:
            return jsonify({"message": "Member not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to update a member by ID
@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    data = request.get_json()

    # Validate input data using Marshmallow
    member_schema = MemberSchema()
    errors = member_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')
    membership_type = data.get('membership_type')

    try:
        result = update_member_in_db(id, name, age, gender, membership_type)
        if result:
            return jsonify({"message": "Member updated successfully"}), 200
        else:
            return jsonify({"message": "Member not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to delete a member by ID
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    try:
        result = delete_member_from_db(id)
        if result:
            return jsonify({"message": "Member deleted successfully"}), 200
        else:
            return jsonify({"message": "Member not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to schedule a new workout session
@app.route('/workoutsessions', methods=['POST'])
def schedule_workout():
    data = request.get_json()

    # Validate input data using Marshmallow
    workout_schema = WorkoutSessionSchema()
    errors = workout_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    member_id = data.get('member_id')
    session_date = data.get('session_date')
    session_time = data.get('session_time')
    activity = data.get('activity')

    try:
        session_id = schedule_workout_session(member_id, session_date, session_time, activity)
        session_data = {
            "session_id": session_id,
            "member_id": member_id,
            "session_date": session_date,
            "session_time": session_time,
            "activity": activity
        }
        result = workout_schema.dump(session_data)
        return jsonify({"message": "Workout session scheduled", "workout_session": result}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to update a workout session
@app.route('/workoutsessions/<int:session_id>', methods=['PUT'])
def update_workout(session_id):
    data = request.get_json()

    # Validate input data using Marshmallow
    workout_schema = WorkoutSessionSchema()
    errors = workout_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    session_date = data.get('session_date')
    session_time = data.get('session_time')
    activity = data.get('activity')

    try:
        result = update_workout_session(session_id, session_date, session_time, activity)
        if result:
            return jsonify({"message": "Workout session updated successfully"}), 200
        else:
            return jsonify({"message": "Workout session not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to get all workout sessions
@app.route('/workoutsessions', methods=['GET'])
def get_all_workoutsessions():
    try:
        sessions = get_all_workout_sessions()
        workout_schema = WorkoutSessionSchema(many=True)
        result = workout_schema.dump(sessions)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to get all workout sessions for a specific member
@app.route('/members/<int:member_id>/workoutsessions', methods=['GET'])
def get_workout_sessions(member_id):
    try:
        sessions = get_workout_sessions_by_member(member_id)
        if sessions:
            workout_schema = WorkoutSessionSchema(many=True)
            result = workout_schema.dump(sessions)
            return jsonify(result), 200
        else:
            return jsonify({"message": "No workout sessions found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
