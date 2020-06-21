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
        parser.add_argument('Rollno',type=int,required=True,help="Rollno cannot be left empty")
        parser.add_argument('branch',type=str,required=True,help="branch cannot be left empty")
        parser.add_argument('year',type=int,required=True,help="year cannot be left empty")
        parser.add_argument('mobile_no',type=int,required=True,help="mobile_no cannot be left empty")
        parser.add_argument('email_id',type=str,required=True,help="email_id cannot be left empty")
        parser.add_argument('event_id',type=int,required=True,help="event_id cannot be left empty")
        data=parser.parse_args()
        try:
            x=query(f"""select * from shruthi.Event_Head where Rollno={data['Rollno']}""",return_json=False)
            if len(x)>0: return{"message":"user with that Rollno already exists."},400
        except:
            return{"message":"there was an error inserting into table."},500
        try:
             query(f"""insert into shruthi.Event_head_id(name,password,Rollno,branch,year,mobile_no,email_id,event_id)
                                values('{data['name']}',
                                        '{data['password']}',
                                        {data['Rollno']},
                                        '{data['branch']}',
                                        {data['year']},
                                        {data['mobile_no']},
                                        '{data['email_id']}',
                                        {data['event_id']})""")
             return {"message":"Successfully Inserted."},201
        except:
            return {"message":"There was an error Inserting to User table"},500
