from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
from db import query
class Userd(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('Rollno',type=int,required=True,help="Rollno cannot be left blank")
        data=parser.parse_args()
        try:
            d=query(f"""select  * from shruthi.User where Rollno={data['Rollno']};""",return_json=False)
            #z= query(f"""select event_id,event_title from shruthi.Event where event_id=any(select event_id from shruthi.registrations where user_id=(select user_id from shruthi.User where Rollno={data['Rollno']}));""",return_json=False)
            #d.extend(z)
            return d,200
        except:
            return {"message":"There was an error connecting to databasse"},500

class UserE(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('Rollno',type=int,required=True,help="Rollno cannot be left blank")
        data=parser.parse_args()
        try:

            z= query(f"""select event_id,event_title from shruthi.Event where event_id=any(select event_id from shruthi.registrations where user_id=(select user_id from shruthi.User where Rollno={data['Rollno']}));""",return_json=False)

            return z,200
        except:
            return {"message":"There was an error connecting to databasse"},500
class User(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('name',type=str,required=True,help="name cannot be left empty")
        parser.add_argument('password',type=str,required=True,help="password cannot be left empty")
        parser.add_argument('college',type=str,required=True,help="college cannot be left empty")
        parser.add_argument('Rollno',type=int,required=True,help="Rollno cannot be left empty")
        parser.add_argument('branch',type=str,required=True,help="branch cannot be left empty")
        parser.add_argument('year',type=int,required=True,help="year cannot be left empty")
        parser.add_argument('mobile_no',type=int,required=True,help="mobile_no cannot be left empty")
        parser.add_argument('email_id',type=str,required=True,help="email_id cannot be left empty")
        data=parser.parse_args()
        try:
            x=query(f"""select * from shruthi.User where Rollno={data['Rollno']}""",return_json=False)
            if len(x)>0: return{"message":"user with that Rollno already exists."},400
        except:
            return{"message":"there was an error inserting into table."},500
        try:
             query(f"""insert into shruthi.User(name,password,Rollno,college,branch,year,mobile_no,email_id)
                                values('{data['name']}',
                                        '{data['password']}',
                                        {data['Rollno']},
                                        '{data['college']}',
                                        '{data['branch']}',
                                        {data['year']},
                                        {data['mobile_no']},
                                        '{data['email_id']}')""")
             return {"message":" User Successfully Registered."},201
        except:
            return {"message":"There was an error Inserting to User table"},500

class User_ob():
    def __init__(self,Rollno,name,password):
        self.Rollno=Rollno
        self.name=name
        self.password=password

    @classmethod
    def getUserByRollno(cls,Rollno):
        result=query(f"""select Rollno,name,password from shruthi.User where Rollno='{Rollno}'""",return_json=False)
        if len(result)>0: return User_ob(result[0]['Rollno'],result[0]['name'],result[0]['password'])
        return None

    @classmethod
    def getUserByname(cls,name):
        result=query(f"""select Rollno,name,password from shruthi.User where name='{name}'""",return_json=False)
        if len(result)>0: return User_ob(result[0]['Rollno'],result[0]['name'],result[0]['password'])
        return None


class UserLogin(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('Rollno',type=int,required=True,help="Rollno cannot be left empty")
        parser.add_argument('password',type=str,required=True,help="password cannot be left empty")
        data=parser.parse_args()
        user=User_ob.getUserByRollno(data['Rollno'])
        if user and safe_str_cmp(user.password,data['password']):
            access_token=create_access_token(identity=user.Rollno,expires_delta=False)
            d=query(f"""select name,Rollno,branch,year from shruthi.User where Rollno={data['Rollno']};""",return_json=False)
            return {'access_token':access_token},200
        return{"message":"Invalid Credentials"},401
class Events(Resource):
    def get(self):
        return query(f"""select event_id,event_title,event_head_id,event_desc from shruthi.Event;""",return_json=False)
class User_ER(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('user_id',type=int,required=True,help="user_id cannot be left empty")
        parser.add_argument('event_id',type=int,required=True,help="event_id cannot be left empty")
        data=parser.parse_args()
        try:
            x=query(f"""select * from shruthi.registrations where user_id={data['user_id']} and event_id={data['event_id']} """,return_json=False)
            if len(x)>0: return{"message":"user has already registered this event."},400
        except:
            return{"message":"there was an error inserting into table."},500
        try:
             query(f"""insert into shruthi.registrations(user_id,event_id)
                                values({data['user_id']},
                                        {data['event_id']})""")
             return {"message":" User Successfully Registered to event."},201
        except:
            return {"message":"There was an error while registration"},500
class User_Interest(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('user_id',type=int,required=True,help="user_id cannot be left empty")
        parser.add_argument('event_id',type=int,required=True,help="event_id cannot be left empty")
        data=parser.parse_args()
        try:
            x=query(f"""select * from shruthi.events_interested where user_id={data['user_id']} and event_id={data['event_id']} """,return_json=False)
            if len(x)>0: return{"message":"This event is already in fav list."},400
        except:
            return{"message":"there was an error inserting into table."},500
        try:
             query(f"""insert into shruthi.events_interested(user_id,event_id)
                                values({data['user_id']},
                                        {data['event_id']})""")
             return {"message":" Event successfully added to fav list."},201
        except:
            return {"message":"There was an error while adding to fav list"},500
class User_fav(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('Rollno',type=int,required=True,help="Rollno cannot be left blank")
        data=parser.parse_args()
        try:

            z= query(f"""select event_id,event_title from shruthi.Event where event_id=any(select event_id from shruthi.events_interested where user_id=(select user_id from shruthi.User where Rollno={data['Rollno']}));""",return_json=False)

            return z,200
        except:
            return {"message":"There was an error connecting to databasse"},500


class User_ob2():
    def __init__(self,Rollno,name,password):
        self.Rollno=Rollno
        self.name=name
        self.password=password

    @classmethod
    def getUserByRollno(cls,Rollno):
        result=query(f"""select Rollno,name,password from shruthi.User where Rollno='{Rollno}'""",return_json=False)
        if len(result)>0: return User_ob(result[0]['Rollno'],result[0]['name'],result[0]['password'])
        return None

    @classmethod
    def getUserByname(cls,name):
        result=query(f"""select Rollno,name,password from shruthi.User where name='{name}'""",return_json=False)
        if len(result)>0: return User_ob(result[0]['Rollno'],result[0]['name'],result[0]['password'])
        return None


class UserLogin2(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('Rollno',type=int,required=True,help="Rollno cannot be left empty")
        #parser.add_argument('name',type=str,required=True,help="name cannot be left empty")
        data=parser.parse_args()
        user=User_ob2.getUserByRollno(data['Rollno'])
        if user: #and safe_str_cmp(user.name,data['name']):
            access_token=create_access_token(identity=user.Rollno,expires_delta=False)
             #d=query(f"""select name,Rollno,branch,year from shruthi.User where Rollno={data['Rollno']};""",return_json=False)
            return {'access_token':access_token},200
        return{"message":"Invalid Credentials"},401
