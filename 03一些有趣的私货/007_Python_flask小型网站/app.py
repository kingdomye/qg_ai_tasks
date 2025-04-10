from flask import Flask, render_template, session, request, redirect,send_from_directory
from manage import Class, Subjects, Schedules, Homeworks, Files, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_,or_,not_
from flask_migrate import Migrate
from act import SimpleAct
import random
import pymysql
import os

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = (f'mysql+pymysql://yr-class:Zhaoboyu666@@localhost:3306/yr-class')
app.secret_key = 'yr_class_yyds_nb'
app.config['UPLOAD_FOLDER'] = 'upload'
simple = SimpleAct()
db.init_app(app)

def Logged():
    logged = session.get('logged')
    if logged:
        return True
    else:
        return False

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

@app.route('/')
def index():
    if Logged():
        return redirect('/home')
    return render_template('index.html')

@app.route('/mobile_check',methods=["GET","POST"])
def mobile():
    if request.method == 'POST':
        class_number = request.form.get('class_num')
        password = request.form.get('password')
        check_class_number = Class.query.filter_by(class_number=class_number).first()
        if not check_class_number:
            return render_template('login.html', error=True)
        if check_password_hash(password=password, pwhash=check_class_number.password):
            session['logged'] = class_number
            return "true"
        return "false"

@app.route('/pricing')
def pricing():
    if Logged():
        return redirect('/home')
    return render_template('pricing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if Logged():
        return redirect('/home')
    if request.method == 'POST':
        class_number = request.form.get('class_num')
        password = request.form.get('password')
        check_class_number = Class.query.filter_by(class_number=class_number).first()
        if not check_class_number:
            return render_template('login.html', error=True)
        if check_password_hash(password=password, pwhash=check_class_number.password):
            session['logged'] = class_number
            return redirect('/home')
        return render_template('login.html', error=True)
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if Logged():
        return redirect('/home')
    if request.method == 'POST':
        e_mail = request.form.get('email')
        password = request.form.get('password')
        password_check = request.form.get('password_check')
        if e_mail and password and password_check and simple.IF_Email(e_mail) and password == password_check and len(
                password) >= 8 and Class.query.filter_by(email=e_mail).first()==None:
            class_number = simple.Random_Class_Num()
            while Class.query.filter_by(class_number=class_number).first() != None:
                class_number = simple.Random_Class_Num()
            my_class = Class(class_number=class_number, email=e_mail, password=generate_password_hash(password))
            db.session.add(my_class)
            db.session.commit()
            session['logged'] = class_number
            _class = Class.query.filter_by(class_number=session.get('logged')).first()
            db.session.execute(Subjects.__table__.insert(),[{'subject_name':i,'class_id':_class.id} for i in simple.subjects])
            db.session.commit()
            session['logged'] = class_number
            db.session.execute(Schedules.__table__.insert(),
                               [{'index':i,'class_id': _class.id} for i in range(16)])
            db.session.commit()
            return redirect('/show_number')
        return render_template('register.html', error=True)
    return render_template('register.html')

@app.route('/show_number')
def show_number():
    class_number = session.get('logged')
    if class_number:
        return render_template('show_number.html', class_number=class_number)


@app.route('/find', methods=['GET', 'POST'])
def find():
    if Logged():
        return redirect('/home')
    if request.method == 'POST':
        try:
            e_mail = session['email']
            if e_mail == request.form.get('email'):
                return redirect('/check')
        except:
            pass
        e_mail = request.form.get('email')
        if simple.IF_Email(e_mail):
            session['email'] = e_mail
            session['begin'] = simple.Now_time()
            session['password'] = simple.Send_Email(e_mail)
            return redirect('/check')
        return render_template('find.html', error=True)
    return render_template('find.html', error=False)


@app.route('/check', methods=['GET', 'POST'])
def check():
    try:
        e_mail = session['email']
        begin = session['begin']
    except:
        return redirect('/find')
    if request.method == 'POST':
        user_password = request.form.get('password')
        if user_password == session['password']:
            del session['password']
            return redirect('/un_know_change')
        else:
            now = simple.Now_time()
            if now - begin <= 60:
                return render_template('check.html', id='countdownBtn', count=60 - (now - begin), error=True)
            return render_template('check.html', error=False)
    if e_mail:
        now = simple.Now_time()
        if now - begin <= 60:
            return render_template('check.html', id='countdownBtn', count=60 - (now - begin))
        session['begin'] = simple.Now_time()
        session['password'] = simple.Send_Email(e_mail)
        return render_template('check.html', id='countdownBtn', count=60)


@app.route('/un_know_change', methods=['GET', 'POST'])
def un_know_change():
    try:
        e_mail = session['email']
    except:
        return redirect('/find')
    search = Class.query.filter_by(email=e_mail).first()
    if search == None:
        return redirect('/error')
    if request.method == 'POST':
        change_password = request.form.get('password')
        search = Class.query.filter_by(email=e_mail).first()
        if search != None:
            if len(change_password) >= 8:
                Class.query.filter(Class.email == e_mail).update({'password': generate_password_hash(change_password)})
                db.session.commit()
                del session['email']
                return redirect('/login')
            return render_template('un_know_change.html', error=True, class_number=search.class_number)
    return render_template('un_know_change.html', error=False, class_number=search.class_number)


@app.route('/error')
def error():
    if Logged():
        return redirect('/home')
    return render_template('error.html')


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if not Logged():
        return redirect('/login')
    _class = Class.query.filter_by(class_number=session.get('logged')).first()
    data=Files.query.filter(and_(Files.active==True,Files.class_id==_class.id)).all()
    length=len(data)
    if request.method == 'POST':
        file = request.files['file']
        true_name = file.filename
        file_extension=simple.File_Extension(true_name)
        if file and file_extension:
            fake_name = simple.Random_File_Name(true_name)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], fake_name))
            file_size = simple.File_Size(os.path.join(app.config['UPLOAD_FOLDER'], fake_name))
            upload=Files(true_name=true_name,fake_name=fake_name,file_size=file_size,file_extension=file_extension,date= simple.Now_Date(),class_id=_class.id)
            db.session.add(upload)
            db.session.commit()
            return redirect('/upload_file')
        return render_template('file_management.html',length=length,data=data)
    return render_template('file_management.html',length=length,data=data)

@app.route('/del_file')
def del_file():
    if not Logged():
        return redirect('/login')
    id=request.args.get('id')
    if id:
        _class=Class.query.filter_by(class_number=session.get('logged')).first()
        if _class:
            file =Files.query.filter(and_(Files.id==id,Files.class_id==_class.id)).first()
            if file:
                Files.query.filter(and_(Files.id==id,Files.class_id==_class.id)).update({'active':False})
                db.session.commit()
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file.fake_name))
                return redirect('/upload_file')
    return render_template('404.html')


@app.route('/download')
def download():
    if not Logged():
        return redirect('/login')
    id=request.args.get('id')
    if id:
        _class = Class.query.filter_by(class_number=session.get('logged')).first()
        if _class:
            file = Files.query.filter(and_(Files.id == id, Files.class_id == _class.id)).first()
            if file:
                return send_from_directory(app.config['UPLOAD_FOLDER'],file.fake_name,as_attachment=True)
    return render_template('404.html')
@app.route('/home')
def home():
    if not Logged():
        return redirect('/login')
    now_date=simple.Now_Date()
    _class = Class.query.filter_by(class_number=session.get('logged')).first()
    data = Subjects.query.filter_by(class_id=_class.id).all()
    if data:
        subject_data = []
        for item in data:
            subject_data.extend(Homeworks.query.filter(and_(Homeworks.subject_id==item.id,str(now_date)==Homeworks.finish_date)).all())
        if subject_data:
            subject=[]
            for i in subject_data:
                subject.append(Subjects.query.get(i.subject_id))
            return render_template('today_homework.html',data=subject_data,length=len(subject_data),if_data=True,subject=subject)
    return render_template('today_homework.html',if_data=False)
@app.route('/layout',methods=['GET', 'POST'])
def layout():
    if not Logged():
        return redirect('/login')
    if request.method=='POST':
        subject=request.form.get('subject')
        content=request.form.get('content')
        begin_date=request.form.get('begin_date')
        finish_date=request.form.get('finish_date')
        hand_in=request.form.get('hand_in')
        if subject and content and begin_date:
            if finish_date:
                if simple.Date_Stamp(begin_date)-simple.Date_Stamp(finish_date)>0:
                    return render_template('homework_layout.html',error=True,subjects=simple.subjects)
            _class = Class.query.filter_by(class_number=session.get('logged')).first()
            data=Subjects.query.filter(and_(Subjects.subject_name==subject, Subjects.class_id==_class.id)).first()
            if hand_in and finish_date:
                hand_in=True
            else:
                hand_in=False
            upload=Homeworks(content=content,begin_date=begin_date,finish_date=finish_date,hand_in=hand_in,subject_id=data.id)
            db.session.add(upload)
            db.session.commit()
            return redirect('/home')
        return render_template('homework_layout.html',error=True,subjects=simple.subjects)
    return render_template('homework_layout.html',error=False,subjects=simple.subjects)
@app.route('/schedule_change',methods=['GET', 'POST'])
def schedule_change():
    if not Logged():
        return redirect('/login')
    _class = Class.query.filter_by(class_number=session.get('logged')).first()
    schedule = Schedules.query.filter(Schedules.class_id == _class.id,Schedules.active == True).all()
    if request.method=='POST':
        for i in range(16):
            data = []
            for k in range(1,8):
                num=request.form.get(f'{i*7+k}')
                data.append(num)
            line=Schedules(index=i,monday=data[0],tuesday=data[1],wednesday=data[2],thursday=data[3],friday=data[4],saturday=data[5],sunday=data[6],class_id=_class.id)
            db.session.add(line)
            db.session.commit()
        for j in schedule:
            db.session.delete(j)
            db.session.commit()
        return redirect('/schedule')
    return render_template('schedule_change.html', schedule=schedule, length=len(simple.arrange), arrange=simple.arrange, subjects=simple.subjects)
@app.route('/schedule')
def schedule():
    if not Logged():
        return redirect('/login')
    _class = Class.query.filter_by(class_number=session.get('logged')).first()
    schedule=Schedules.query.filter(Schedules.class_id==_class.id,Schedules.active==True).all()
    return render_template('schedule_check.html',schedule=schedule,length=len(simple.arrange),arrange=simple.arrange)
@app.route('/homeworks',methods=['GET', 'POST'])
def homeworks():
    if not Logged():
        return redirect('/login')
    _class = Class.query.filter_by(class_number=session.get('logged')).first()
    data = Subjects.query.filter_by(class_id=_class.id).all()
    if data:
        subject_data = []
        for item in data:
            subject_data.extend(Homeworks.query.filter(Homeworks.subject_id == item.id).all())
        if subject_data:
            subject = []
            for i in subject_data:
                subject.append(Subjects.query.get(i.subject_id))
            return render_template('homework_list.html', data=subject_data, length=len(subject_data), if_data=True,
                                   subject=subject)
    return render_template('homework_list.html', if_data=False)

@app.route('/homework_detail')
def homework_detail():
    if not Logged():
        return redirect('/login')
    id=request.args.get('id')
    if id:
        _class = Class.query.filter_by(class_number=session.get('logged')).first()
        data = Homeworks.query.filter_by(id=id).first()
        if data:
            subject = Subjects.query.filter_by(class_id=_class.id, id=data.subject_id).first()
            if subject:
                return render_template('detail.html',data=data,subject=subject,id=id)
        return render_template('404.html')

@app.route('/del_homework')
def del_homework():
    if not Logged():
        return redirect('/login')
    id=request.args.get('id')
    if id:
        _class = Class.query.filter_by(class_number=session.get('logged')).first()
        data = Homeworks.query.filter_by(id=id).first()
        if data:
            subject = Subjects.query.filter_by(class_id=_class.id, id=data.subject_id).first()
            if subject:
                db.session.delete(data)
                db.session.commit()
                return redirect('/home')
    return render_template('404.html')



@app.route('/know_change', methods=['GET', 'POST'])
def know_change():
    if not Logged():
        return redirect('/login')
    if request.method == 'POST':
        password=request.form.get('password')
        password_check=request.form.get('password_check')
        if password==password_check and len(password)>=8:
            _class = Class.query.filter_by(class_number=session.get('logged')).first()
            Class.query.filter(Class.id==_class.id).update({'password': generate_password_hash(password)})
            db.session.commit()
            return redirect('/home')
        return render_template('know_change.html',error=True)
    return render_template('know_change.html',error=False)



@app.route('/logout')
def logout():
    if Logged():
        del session['logged']
    return redirect('/login')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8001)