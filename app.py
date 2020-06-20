from flask import Flask
from flask_restful import Api
from resources.user import User
from resources.event_head import Event_Head
import pymysql
app=Flask(__name__)
api=Api(app)
api.add_resource(User,'/user')
api.add_resource(Event_Head,'/event_head')
app.run()
