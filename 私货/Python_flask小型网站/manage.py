from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pymysql

app=Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['SQLALCHEMY_DATABASE_URI']=(f'mysql+pymysql://root:root@localhost:3306/yr-class')#这个也得改
ctx=app.app_context()
ctx.push()
db=SQLAlchemy(app)
migrate=Migrate(app,db)


class Class(db.Model):
    __tablename__='classes'


    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    class_number=db.Column(db.String(80),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    password=db.Column(db.String(255),unique=True,nullable=False)
    files = db.relationship('Files', foreign_keys='Files.class_id',backref='classes')
    schedule = db.relationship('Schedules', foreign_keys='Schedules.class_id',backref='classes')
    subject = db.relationship('Subjects', foreign_keys='Subjects.class_id',backref='classes')
    active=db.Column(db.Boolean,default=True)

    def __repr__(self):
        return '<Class %r>'%self.class_number




class Files(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    true_name=db.Column(db.String(80),nullable=False)
    fake_name=db.Column(db.String(255),unique=True,nullable=False)
    file_size=db.Column(db.String(80),nullable=False)
    file_extension=db.Column(db.String(80),nullable=False)
    date=db.Column(db.String(80),nullable=False)
    active=db.Column(db.Boolean,default=True)
    class_id=db.Column(db.Integer,db.ForeignKey('classes.id'))

    def __repr__(self):
        return '<File %r>'%self.true_name

class Subjects(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_name=db.Column(db.String(80),nullable=False)
    active=db.Column(db.Boolean,default=True)
    class_id=db.Column(db.Integer,db.ForeignKey('classes.id'))
    homework=db.relationship('Homeworks',foreign_keys='Homeworks.subject_id',backref='subjects')

    def __repr__(self):
        return '<Subject %r>'%self.subject_name

class Schedules(db.Model):
    __tablename__ = 'schedules'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    monday=db.Column(db.String(80),default='')
    tuesday=db.Column(db.String(80),default='')
    wednesday=db.Column(db.String(80),default='')
    thursday=db.Column(db.String(80),default='')
    friday=db.Column(db.String(80),default='')
    saturday=db.Column(db.String(80),default='')
    sunday=db.Column(db.String(80),default='')
    index=db.Column(db.Integer)
    active=db.Column(db.Boolean,default=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))

    def __repr__(self):
        return '<Schedule %r>'%self.index
class Homeworks(db.Model):
    __tablename__ = 'homeworks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content=db.Column(db.Text)
    begin_date=db.Column(db.String(80),nullable=False)
    finish_date=db.Column(db.String(80))
    hand_in=db.Column(db.Boolean)
    active = db.Column(db.Boolean,default=True)
    subject_id=db.Column(db.Integer, db.ForeignKey('subjects.id'))

    def __repr__(self):
        return '<Homework %r>'%self.id

if __name__ == '__main__':

    db.create_all()