from flask_restful import Resource,reqparse
from db import query
class Event_Head(Resource):
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('Event_head_id',type=int,required=True,help="Event_head_id cannot be left blank")
        data=parser.parse_args()
        try:
            return query(f"""select * from shruthi.Event_Head where Event_head_id={data['Event_head_id']};""")
        except:
            return {"message":"There was an error connecting to Event_Head table"}
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('name',type=str,required=True,help="name cannot be left empty")
        parser.add_argument('password',type=str,required=True,help="password cannot be left empty")
        parser.add_argument('Rollno',type=int)
        parser.add_argument('branch',type=str)
        parser.add_argument('year',type=int)
        parser.add_argument('mobile_no',type=int,required=True,help="mobile_no cannot be left empty")
        parser.add_argument('email_id',type=str)
        parser.add_argument('event_id',type=int)

        data=parser.parse_args()
