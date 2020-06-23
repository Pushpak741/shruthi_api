from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
from db import query
import jsonify
class User(Resource):
    '''@jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('user_id',type=int,required=True,help="user_id cannot be left blank")
        data=parser.parse_args()
        try:
            return query(f"""select * from shruthi.User where user_id={data['user_id']};""")
        except:
            return {"message":"There was an error connecting to User table"}'''

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
            c=d[0]
            c['access_token']=access_token
            return d
        return{"message":"Invalid Credentials"},401
