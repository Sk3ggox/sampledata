from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

class ConfigClass(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://mainflaskapp:AllGreekToMe@172.18.0.2:3306/eindhovencustoms'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

def create_app():
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass')
    db=SQLAlchemy(app)

    # Def item model
    class Items(db.Model):
        __tablename__ = 'item_table'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100, collation='utf8_bin'), nullable=False)
        oem = db.Column(db.String(100, collation='utf8_bin'), nullable=False)
        amount = db.Column(db.Integer, nullable=False)
        minamount = db.Column(db.Integer, nullable=False)

    ##Def user-data model
    class User(db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer(), unique=True, primary_key=True)
        active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
        #User auth info
        username = db.Column(db.String(100, collation='utf8_bin'), nullable=False, server_default='1')
        password = db.Column(db.String(255), nullable=False, server_default='')
        #Define relationship to Role via UserRoles
        roles = db.relationship('Role', secondary='user_roles')

    # Define the Role Data-model
    class Role(db.Model):
        __tablename__ = 'roles'
        id = db.Column(db.Integer(), unique=True, primary_key=True)
        name = db.Column(db.String(50), unique=True)

    #Define UserRoles association table
    class UserRoles(db.Model):
        __tablename__ = 'user_roles'
        id = db.Column(db.Integer(), primary_key=True)
        user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
        role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

    # Define logging table
    class LogTable(db.Model):
        __tablename__='logs'
        id = db.Column(db.Integer(), primary_key=True)
        user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
        item = db.Column(db.String(100), nullable=False)
        #action = db.Column(db.String(100), nullable=False)
        amount = db.Column(db.Integer(), nullable=False)
        timestamp = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    db.create_all()

    manager_role = Role(name = 'Manager')
    mechanic_role = Role(name= 'Mechanic')
    admin_role = Role(name= 'Admin')

    # Create sample data, 2 users with different roles, item and log
    if not Items.query.filter(Items.name == 'testitem').first():
        item = Items(
            name = 'testitem',
            oem = '609 319 093',
            amount = 24,
            minamount = 30
        )
        db.session.add(item)
        db.session.commit()

    def createLogs():
        if not LogTable.query.filter(LogTable.id == 1).first():
            item = LogTable(
                user_id = 1,
                item = '609 319 093',
                amount = -44,
                timestamp = '2022-06-10 09:06:15'
            )
            db.session.add(item)
            db.session.commit()

        if not LogTable.query.filter(LogTable.id == 2).first():
            item = LogTable(
                user_id = 1,
                item = '609 319 093',
                amount = 45,
                timestamp = '2022-06-11 09:06:15'
            )
            db.session.add(item)
            db.session.commit()

        if not LogTable.query.filter(LogTable.id == 3).first():
            item = LogTable(
                user_id = 1,
                item = '609 319 093',
                amount = 160,
                timestamp = '2022-06-12 09:06:15'
            )
            db.session.add(item)
            db.session.commit()

        if not LogTable.query.filter(LogTable.id == 4).first():
            item = LogTable(
                user_id = 1,
                item = '609 319 093',
                amount = -50,
                timestamp = '2022-06-13 09:06:15'
            )
            db.session.add(item)
            db.session.commit()
    createLogs()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0',port=8080, debug=True)