from flask import Flask,jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import User,UserLogin,Events,Userd,User_ER,UserE
from resources.event_head import Event_Head,HeadLogin
from resources.admin import AdminLogin,Requests,ViewU,Adminrem,AdminremH
import pymysql
app=Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS']=True
app.config['JWT_SECRET_KEY']='shruthiapi'
api=Api(app)
jwt=JWTManager(app)

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
            'error':'authorized_required',
            "description":"Request does not contain an access token."
    }),401
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'error':'invalid_token',
        'message':'Signature verification failed.'
    }),401

api.add_resource(User,'/user_register')
api.add_resource(Userd,'/user_details')
api.add_resource(UserLogin,'/user_login')
api.add_resource(Event_Head,'/eventhead_reg')
api.add_resource(HeadLogin,'/eventhead_login')
api.add_resource(Events,'/events')
api.add_resource(User_ER,'/user_evtreg')
api.add_resource(AdminLogin,'/admin_login')
api.add_resource(Requests,'/requests')
api.add_resource(ViewU,'/view_user')
api.add_resource(UserE,'/user_event')
api.add_resource(Adminrem,'/user_remove')
api.add_resource(AdminremH,'/head_remove')
if __name__=='__main__':
    app.run()
