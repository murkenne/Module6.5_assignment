from flask_marshmallow import Marshmallow
from marshmallow import fields

# Initialize Marshmallow
ma = Marshmallow()

# Define Member Schema
class MemberSchema(ma.Schema):
    id = fields.Int(dump_only=True)  
    name = fields.Str(required=True)
    age = fields.Int(required=True)
    gender = fields.Str(required=True)
    membership_type = fields.Str(required=True)

# Define WorkoutSession Schema
class WorkoutSessionSchema(ma.Schema):
    session_id = fields.Int(dump_only=True)
    member_id = fields.Int(required=True)
    session_date = fields.Date(required=True)
    session_time = fields.Str(required=True)
    activity = fields.Str(required=True)
