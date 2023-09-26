from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
import json

# MY db connection
local_server= True
app = Flask(__name__)
app.secret_key='kusumachandashwini'


# this is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/databas_table_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/deathratedbms'
db=SQLAlchemy(app)

# here we will create db models that is tables
class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))

class Diseases(db.Model):
    did=db.Column(db.Integer,primary_key=True)
    dname=db.Column(db.String(100))
    type=db.Column(db.String(100))
    classify=db.Column(db.String(100))
    cause=db.Column(db.String(100))
    cagent=db.Column(db.String(100))



class Mrate(db.Model):
    mid=db.Column(db.Integer,primary_key=True)
    dname=db.Column(db.String(100))
    mortalrate=db.Column(db.Integer())

    infections=db.Column(db.Integer())
    totaldeaths=db.Column(db.Integer())

class Trig(db.Model):
    tid=db.Column(db.Integer,primary_key=True)
    ssn=db.Column(db.String(100))
    action=db.Column(db.String(100))
    timestamp=db.Column(db.String(100))


class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))





class Deaths(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    ssn=db.Column(db.String(50))
    name=db.Column(db.String(50))
    age=db.Column(db.Integer)
    gender=db.Column(db.String(50))
    dname=db.Column(db.String(50))
    email=db.Column(db.String(50))
    number=db.Column(db.String(12))
    address=db.Column(db.String(100))
    time=db.Column(db.String(100))
    date=db.Column(db.String(100))
    

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/queries')
def queries(): 
    return render_template('queries.html')


@app.route('/query1')
def query1():
    query=db.engine.execute(f"call `query1`")
    return render_template('query1.html',query=query)

@app.route('/query2')
def query2():
    query=db.engine.execute(f"call `query2`")
    return render_template('query2.html',query=query)
@app.route('/query3')
def query3():
    query=db.engine.execute(f"call `query3`")
    return render_template('query3.html',query=query)

@app.route('/query4')
def query4():
    query=db.engine.execute(f"call `query4`")
    return render_template('query4.html',query=query)

@app.route('/query5')
def query5():
    query=db.engine.execute(f"call `query5`")
    return render_template('query5.html',query=query)

@app.route('/query6')
def query6():
    query=db.engine.execute(f"call `query6`")
    return render_template('query6.html',query=query)
    
    
    

@app.route('/alldeaths')
def alldeaths():
    query=db.engine.execute(f"SELECT * FROM `deaths`") 
    return render_template('alldeaths.html',query=query)
    
@app.route('/disease')
def disease():
    query=db.engine.execute(f"SELECT * FROM `mrate`,`diseases` WHERE `mrate`.`dname`=`diseases`.`dname`") 
    return render_template('disease.html',query=query)

@app.route('/alldiseases')
def alldiseases():
    query=db.engine.execute(f"SELECT * FROM `diseases`") 
    return render_template('alldiseases.html',query=query)

@app.route('/triggers')
def triggers():
    query=db.engine.execute(f"SELECT * FROM `trig`") 
    return render_template('triggers.html',query=query)

@app.route('/diseases',methods=['POST','GET'])
def diseases():
    if request.method=="POST":
        dname=request.form.get('dname')
        classify=request.form.get('classify')
        cause=request.form.get('cause')
        cagent=request.form.get('cagent')
        infections=request.form.get('infections')
        totaldeaths=request.form.get('totaldeaths')
        mortal=(int(totaldeaths)/int(infections))*100
        query=Diseases.query.filter_by(dname=dname).first()
        if query:
            flash("Disease Already Exist","warning")
            return redirect('/diseases')
        dep=Diseases(dname=dname,type=type,classify=classify,cause=cause,cagent=cagent)
        atte=Mrate(dname=dname,mortalrate=mortal,infections=infections,totaldeaths=totaldeaths)
         
        db.session.add(atte)
        db.session.add(dep)
        #query2=db.engine.execute(f"UPDATE `mrate` SET `infections`=`{infections}` WHERE `dname`=`{dname}`")

        db.session.commit()


        flash("New Disease Added","success")
    return render_template('diseases.html')

@app.route('/addmortalrate',methods=['POST','GET'])
def addmortalrate():
    query=db.engine.execute(f"SELECT * FROM `diseases`") 
    if request.method=="POST":
        dname=request.form.get('dname')
        morrate=request.form.get('morrate')
        
        totaldeaths=request.form.get('totaldeaths')
        query1=Mrate.query.filter_by(dname=dname).first()
        if query1:
            flash("Data Already Exist, Cant add or manipulate","warning")
            return redirect('/addmortalrate')
        print(morrate,dname)

        atte=Mrate(dname=dname,mortalrate=morrate,totaldeaths=totaldeaths)
        db.session.add(atte)
        db.session.commit()
        flash("New Mortality Rate added ","warning")

        
    return render_template('mortalrate.html',query=query)

@app.route('/search',methods=['POST','GET'])
def search():
    
    if request.method=="POST":
        ssn=request.form.get('roll')
        dname=request.form.get('dname')
        bio=Deaths.query.filter_by(ssn=ssn).first()
        morrate=Mrate.query.filter_by(dname=dname).first()
        return render_template('search.html',bio=bio,morrate=morrate)
        
    return render_template('search.html')

@app.route("/delete/<string:id>",methods=['POST','GET'])
@login_required
def delete(id):
    db.engine.execute(f"DELETE FROM `deaths` WHERE `deaths`.`id`={id}")
    flash("Data Deleted Successfully","danger")
    return redirect('/alldeaths')


@app.route("/deletedisease/<string:mid>",methods=['POST','GET'])
@login_required
def deletedisease(mid):
    db.engine.execute(f"DELETE FROM `mrate` WHERE `mrate`.`mid`={mid}")
    
    flash("Data Deleted Successfully","danger")
    return redirect('/disease')

@app.route("/deletediseases/<string:did>",methods=['POST','GET'])
@login_required
def deletediseases(did):
    db.engine.execute(f"DELETE FROM `diseases` WHERE `diseases`.`did`={did}")
    
    flash("Data Deleted Successfully","danger")
    return redirect('/alldiseases')


@app.route("/edit/<string:id>",methods=['POST','GET'])
@login_required
def edit(id):
    dname=db.engine.execute("SELECT * FROM `diseases`")
    posts=Deaths.query.filter_by(id=id).first()
    if request.method=="POST":
        ssn=request.form.get('ssn')
        name=request.form.get('name')
        age=request.form.get('age')
        gender=request.form.get('gender')
        dname=request.form.get('dname')
        email=request.form.get('email')
        num=request.form.get('num')
        address=request.form.get('address')
        date=request.form.get('date')
        time=request.form.get('time')
        query=db.engine.execute(f"UPDATE `deaths` SET `ssn`='{ssn}',`name`='{name}',`age`='{age}',`gender`='{gender}',`dname`='{dname}',`email`='{email}',`number`='{num}',`address`='{address}', `date`='{date}', `time`='{time}' WHERE `id` = {id}")
        flash("Data is Updated","success")
        return redirect('/alldeaths')
    
    return render_template('edit.html',posts=posts,dname=dname)

@app.route("/editdisease/<string:did>",methods=['POST','GET'])
@login_required
def editdisease(did):

    posts=Diseases.query.filter_by(did=did).first()
    if request.method=="POST":
        dname=request.form.get('dname')
        classify=request.form.get('classify')
        cause=request.form.get('cause')
        cagent=request.form.get('cagent')
        query=db.engine.execute(f"UPDATE `diseases` SET `dname`='{dname}',`classify`='{classify}',`cause`='{cause}',`cagent`='{cagent}' WHERE `did` = {did}")
        
        
        flash("Data is Updated","success")
        return redirect('/alldiseases')
    
    return render_template('editdisease.html',posts=posts)
    
@app.route("/editmrate/<string:mid>",methods=['POST','GET'])
@login_required
def editmrate(mid):
    dname=db.engine.execute(f"SELECT * FROM `diseases`")
    posts=Mrate.query.filter_by(mid=mid).first()
    if request.method=="POST":
        dname=request.form.get('dname')
        infections=request.form.get('infections')
        totaldeaths=request.form.get('totaldeaths')
        mortal=(int(totaldeaths)/int(infections))*100
        db.engine.execute(f"UPDATE `mrate` SET `dname`='{dname}',`mortalrate`='{mortal}',`infections`='{infections}',`totaldeaths`='{totaldeaths}' WHERE `mid` = {mid}")
        
        
        flash("Data is Updated","success")
        return redirect('/disease')
    
    return render_template('editmrate.html',posts=posts,dname=dname)

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template('/signup.html')
        encpassword=generate_password_hash(password)

        new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")


        flash("Signup Succes Please Login","success")
        return render_template('login.html')

          

    return render_template('signup.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for('index'))
        else:
            flash("invalid credentials","danger")
            return render_template('login.html')    

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))



@app.route('/deaths',methods=['POST','GET'])
@login_required
def deaths():
    dname=db.engine.execute("SELECT * FROM `diseases`")
    
    if request.method=="POST":

        ssn=request.form.get('ssn')
        name=request.form.get('name')
        age=request.form.get('age')
        gender=request.form.get('gender')
        dname=request.form.get('dname')
        email=request.form.get('email')
        num=request.form.get('num')
        address=request.form.get('address')
        date=request.form.get('date')
        time=request.form.get('time')
        query1=Deaths.query.filter_by(ssn=ssn).first()
        

        
        if query1:
            flash("Data Already Exist, Cant add or manipulate","warning")
            
        
            return redirect('/deaths')
        
 
        query=db.engine.execute(f"INSERT INTO `deaths` (`ssn`,`name`,`age`,`gender`,`dname`,`email`,`number`,`address`,`date`,`time`) VALUES ('{ssn}','{name}','{age}','{gender}','{dname}','{email}','{num}','{address}','{date}','{time}' )")
        
        flash("New Data Added","info")
        return redirect('alldeaths')
       

    return render_template('/deaths.html',dname=dname)
@app.route('/test')
def test():
    try:
        Test.query.all()
        return 'My database is Connected'
    except:
        return 'My db is not Connected'


app.run(debug=True)    