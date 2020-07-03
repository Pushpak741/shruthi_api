from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
from db import query

class Event_Head(Resource):
    '''def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('Event_head_id',type=int,required=True,help="Event_head_id cannot be left blank")
        data=parser.parse_args()
        try:
            return query(f"""select * from shruthi.Event_Head where Event_head_id={data['Event_head_id']};""")
        except:
            return {"message":"There was an error connecting to Event_Head table"}'''
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
            if len(x)>0: return{"message":"event_head with that Rollno already exists."},400
        except:
            return{"message":"there was an error inserting into table."},500
        try:
             query(f"""insert into shruthi.Event_Head(name,password,Rollno,branch,year,mobile_no,email_id,event_id)
                                values('{data['name']}',
                                        '{data['password']}',
                                        {data['Rollno']},
                                        '{data['branch']}',
                                        {data['year']},
                                        {data['mobile_no']},
                                        '{data['email_id']}',
                                        {data['event_id']})""")
             return {"message":" Event head Successfully Registered."},201
        except:
            return {"message":"There was an error Inserting to  databasse"},500

class Head_ob():
    def __init__(self,Rollno,name,password):
        self.Rollno=Rollno
        self.name=name
        self.password=password

    @classmethod
    def getHeadByRollno(cls,Rollno):
        result=query(f"""select Rollno,name,password from shruthi.Event_Head where Rollno='{Rollno}'""",return_json=False)
        if len(result)>0: return Head_ob(result[0]['Rollno'],result[0]['name'],result[0]['password'])
        return None

    @classmethod
    def getHeadByname(cls,name):
        result=query(f"""select Rollno,name,password from shruthi.Event_Head where name='{name}'""",return_json=False)
        if len(result)>0: return Head_ob(result[0]['Rollno'],result[0]['name'],result[0]['password'])
        return None


class HeadLogin(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('Rollno',type=int,required=True,help="Rollno cannot be left empty")
        parser.add_argument('password',type=str,required=True,help="password cannot be left empty")
        data=parser.parse_args()
        head=Head_ob.getHeadByRollno(data['Rollno'])
        if head and safe_str_cmp(head.password,data['password']):
            access_token=create_access_token(identity=head.Rollno,expires_delta=False)
            return {'access_token':access_token},200
        return{"message":"Invalid Credentials"},401
class Changepwd(Resource):
    @jwt_required
    def post(self):
            parser=reqparse.RequestParser()
            parser.add_argument('Rollno',type=int,required=True,help="Rollno cannot be left empty")
            parser.add_argument('password',type=str,required=True,help="password cannot be left empty")
            data=parser.parse_args()
            try:
                query(f"""update shruthi.Event_Head set password='{data['password']}' where Rollno={data['Rollno']}""",return_json=False)
                return{"message":"password updated successfully"},200
            except:
                return{"message":"unable to update password"},500
class HeadReq(Resource):
        def post(self):
            parser=reqparse.RequestParser()
            parser.add_argument('event_head_name',type=str,required=True,help="name cannot be left empty")
            parser.add_argument('event_head_year',type=int,required=True,help="year cannot be left empty")
            parser.add_argument('event_desc',type=str,required=True,help="description cannot be left empty")
            parser.add_argument('email_id',type=str,required=True,help="email_id cannot be left empty")
            parser.add_argument('event_title',type=str,required=True,help="event_title cannot be left empty")
            parser.add_argument('Rollno',type=int,required=True,help="Rollno cannot be left empty")
            data=parser.parse_args()
            try:
                x=query(f"""select * from shruthi.Requests where event_title='{data['event_title']}'""",return_json=False)
                if len(x)>0: return{"message":"event with that title already exists."},400
            except:
                return{"message":"there was an error inserting into table."},500
            try:
                 query(f"""insert into shruthi.Requests(event_head_name,event_head_year,event_desc,email_id,event_title,Rollno)
                                    values('{data['event_head_name']}',
                                            {data['event_head_year']},
                                            '{data['event_desc']}',
                                            '{data['email_id']}',
                                            '{data['event_title']}',
                                            {data['Rollno']})""")
                 return {"message":" Request send successfully"},201
            except:
                return {"message":"There was an error Inserting to  databasse"},500
