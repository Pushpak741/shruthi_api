from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,jwt_required
from db import query
class admin_ob():
    def __init__(self,admin_id,admin_name,password):
        self.admin_id=admin_id
        self.admin_name=admin_name
        self.password=password

    @classmethod
    def getAdminByid(cls,admin_id):
        result=query(f"""select admin_id,admin_name,password from shruthi.Admin where admin_id='{admin_id}'""",return_json=False)
        if len(result)>0: return admin_ob(result[0]['admin_id'],result[0]['admin_name'],result[0]['password'])
        return None

    @classmethod
    def getAdminByname(cls,admin_name):
        result=query(f"""select admin_id,admin_name,password from shruthi.Admin where admin_name='{admin_name}'""",return_json=False)
        if len(result)>0: return admin_ob(result[0]['admin_id'],result[0]['admin_name'],result[0]['password'])
        return None


class AdminLogin(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('admin_id',type=int,required=True,help="admin_id cannot be left empty")
        parser.add_argument('password',type=str,required=True,help="password cannot be left empty")
        data=parser.parse_args()
        admin=admin_ob.getAdminByid(data['admin_id'])
        if admin and safe_str_cmp(admin.password,data['password']):
            access_token=create_access_token(identity=admin.admin_id,expires_delta=False)
            return {'access_token':access_token},200
        return{"message":"Invalid Credentials"},401

class Requests(Resource):
   @jwt_required
   def get(self):
        return query(f"""select * from shruthi.Requests""",return_json=False)
class ViewU(Resource):
    @jwt_required
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument('Rollno',type=int,required=True,help="Rollno cannot be left blank")
        data=parser.parse_args()
        try:
            d=query(f"""select  name,Rollno,year,branch,email_id from shruthi.User where Rollno={data['Rollno']};""",return_json=False)
            z= query(f"""select event_id,event_title from shruthi.Event where event_id=any(select event_id from shruthi.registrations where user_id=(select user_id from shruthi.User where Rollno={data['Rollno']}));""",return_json=False)
            d.extend(z)
            return d,200
        except:
            return {"message":"There was an error connecting to databasse"},500
class Adminrem(Resource):
    @jwt_required
    def delete(self):
        parser=reqparse.RequestParser()
        parser.add_argument('Rollno',type=int,required=True,help="Rollno cannot be left blank")
        data=parser.parse_args()
        try:
                query(f"""delete from shruthi.User where Rollno={data['Rollno']};""",return_json=False)
        except:
                return {"message":"there is no user with that Rollno to remove"},500
        return {"message":"user removed from the database Successfully"},200
class AdminremH(Resource):
    @jwt_required
    def delete(self):
        parser=reqparse.RequestParser()
        parser.add_argument('Rollno',type=int,required=True,help="Rollno cannot be left blank")
        data=parser.parse_args()
        try:
                query(f"""delete from shruthi.Event_Head where Rollno={data['Rollno']};""",return_json=False)
        except:
                return {"message":"there is no event head with that Rollno to remove"},500
        return {"message":"event head removed from the database Successfully"},200
