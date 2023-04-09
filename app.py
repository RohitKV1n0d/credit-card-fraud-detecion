from flask import Flask,render_template,request,url_for,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from flask_login import  UserMixin, login_user, LoginManager,login_required, logout_user, current_user
import os
app = Flask(__name__)


ENV = 'prod'

if ENV == 'dev' :
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///creditcard.db'
    app.config['SECRET_KEY'] = 'asdasdasdasdasdasdasdaveqvq34c'

else:
    app.debug = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SECRET_KEY'] = SECRET_KEY
    
SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy(app) #db initializing

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(200), nullable=False)
    l_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(200))
    pwd = db.Column(db.String(100), nullable=False)
    # phone = db.Column(db.Integer, nullable=False)
    balance = db.Column(db.Integer, nullable=False)
    transactions = db.relationship('Transaction_history', backref='trans')
    creditcard = db.relationship('Card_details', backref='credit')


#db model
class Transaction_history(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    datetime = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
      
class Card_details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    pin = db.Column(db.Integer, nullable=False)
    card_no = db.Column(db.String(200), nullable=False)
    cvv_no = db.Column(db.Integer, nullable=False)
    exp_date = db.Column(db.String(200), nullable=False)
    phn_no = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    
@property
def exp_month(self):
    return str(self.exp_date)[0:2]
    
@property
def exp_year(self):
    return str(self.exp_date)[2:]    


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/',methods=['POST','GET'])
def index():
    return render_template("index.html") 


@app.route('/userprofile',methods=['POST','GET'])
@login_required
def userprofile():
    return render_template("userprofile.html")

@app.route('/admin',methods=['POST','GET'])
def admin():
    return render_template("admin.html")


@app.route('/transaction',methods=['POST','GET'])
def transaction():
    return render_template("transaction.html") 

@app.route('/atm',methods=['POST','GET'])
def atm():
    return render_template("atm.html") 

# @app.route('/online_tran',methods=['POST','GET'])
# def online_tran():
#     return render_template("online.html") 

@app.route('/success',methods=['POST','GET'])
def success():
    return render_template("success.html") 


@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        username=request.form.get('username')
        pwd=request.form.get('pwd')
        print(username,pwd)
        try:
            user=User.query.filter_by(username=username).first()

            if username and pwd==user.pwd:
                login_user(user)
                return redirect(url_for('userprofile'))
            else:
                return 'wrong credentials'

        except Exception as e:
            return str(e)
            # flash('Error' + str(e) )
            # return render_template('login.html')
    return render_template('login.html')

@app.route('/logout',methods=['POST','GET'])
@login_required
def logout():
    logout_user()
    flash("logged out")
    return redirect(url_for('login'))
    

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        f_name=request.form['f_name']
        l_name=request.form['l_name']
        email=request.form['email']
        username=request.form['username']
        pwd=request.form['pwd']
        # phone=request.form['phone']
        #print(f_name,l_name,email,username,pwd)
       
        try:
           
            new_user=User(f_name=f_name, l_name=l_name, username=username, email=email, pwd=pwd, balance=10000)
            db.session.add(new_user)    
            db.session.commit()   
            flash('Registration successful!')  
            return redirect(url_for('login'))
        
        except Exception as e :
            flash('Registration failed. Please try again.')
            return str(e)
                    
    #new_user = User.query.all()
    return render_template("register.html")
    # return render_template("register.html")


@app.route('/tables',methods=['POST','GET'])
@login_required
def history():
    if request.method=='POST': 
        trans=current_user.id
        amount=request.form.get('amount')
        type=request.form.get('type')
        location=request.form.get('location')
        balance=request.form.get('balance')
        status=request.form.get('status')
        trans_history=Transaction_history(amount=amount,type=type,location=location,balance=balance,status=status, user_id=current_user.id)

        try:

            db.session.add(trans_history)    
            db.session.commit()     
            return redirect(url_for('history'))
        
        except Exception as e :
            return e
                    
    trans_history = Transaction_history.query.filter_by(user_id=current_user.id).all()
    print(trans_history)
    return render_template("tables.html", trans_history=trans_history)

@app.route('/carddetails',methods=['POST','GET'])
@login_required
def carddetails():
    if request.method == 'POST':
        credit=current_user.id
        name=request.form.get('name')
        pin=request.form.get('pin')
        card_no=request.form.get('card_no')
        cvv_no=request.form.get('cvv_no')
        exp_date=request.form.get('exp_date')
        phn_no=request.form.get('phn_no')
        print(name,pin,card_no,cvv_no,exp_date,phn_no)
        new_card=Card_details(name=name,pin=pin,card_no=str(card_no),cvv_no=cvv_no,exp_date=exp_date,phn_no=phn_no,user_id=current_user.id)
        try:

            db.session.add(new_card)    
            db.session.commit()     
            return redirect(url_for('carddetails'))
        
        except Exception as e :
            return str(e)
    new_card = Card_details.query.filter_by(user_id=current_user.id).all()
    return render_template("carddetails.html", new_card=new_card)
       
@app.route('/online',methods=['POST','GET'])
def online():
    if request.args.get('time') and request.args.get('location'):
        time = int(request.args.get('time'))
        location = request.args.get('location')
    print(time,location)
    from testPredict import predict # predict('Purchase', 100, 12, 'Chennai')
    if request.method=='POST':
        card_no_1=request.form.get('card_no_1')
        card_no_2=request.form.get('card_no_2')
        card_no_3=request.form.get('card_no_3')
        card_no_4=request.form.get('card_no_4')
        card_no=card_no_1 + card_no_2 + card_no_3 + card_no_4
        name=request.form.get('name')
        exp_month=request.form.get('exp_month')
        exp_year=request.form.get('exp_year')
        cvv_no=request.form.get('cvv_no')
        
        exp_date = datetime.strptime(exp_month + '/' + exp_year, '%m/%Y')
        print(card_no,name,exp_date,cvv_no)
        try:
            # card=Card_details.query.filter_by(card_no=card_no).first()
            card = Card_details.query.filter_by(card_no=card_no).first() 
            
            print(str(card.card_no) +' '+ str(card.name) +' '+ str(card.exp_date) +' '+ str(card.cvv_no))


            if card and cvv_no==str(card.cvv_no):
                user = User.query.filter_by(id=card.user_id).first()
            # if card and cvv_no==card.cvv_no and exp_date==card.exp_date:
                # login_user(card)
                # print( str(trans_history.balance) + ' ' + str(trans_history.status))
                if int(user.balance) > int(request.form.get("amount")):
                #code for succses 
                    if predict('Purchase',request.form.get("amount"),time, location) == 1:
                        trans_history = Transaction_history(amount=request.form.get("amount"), balance=int(user.balance) - int(request.form.get("amount")), status="success", user_id=user.id, type="online", location="online", datetime=datetime.now())  
                        db.session.add(trans_history)
                        db.session.commit()
                        user.balance = int(user.balance) - int(request.form.get("amount"))
                        db.session.commit()
                        return redirect(url_for('success'))
                    else:
                        trans_history = Transaction_history(amount=request.form.get("amount"), balance=user.balance, status="Fraud", user_id=user.id, type="online", location="online", datetime=datetime.now())  
                        db.session.add(trans_history)
                        db.session.commit()
                        return render_template('failed.html')

                    
                else:
                    trans_history = Transaction_history(amount=request.form.get("amount"), balance=user.balance, status="Low Balance", user_id=user.id, type="online", location="online", datetime=datetime.now())  
                    db.session.add(trans_history)
                    db.session.commit()
                    return render_template('failed.html')
            else:
                return 'invalid credentials' 

        except Exception as e:
            print(e)
            return 'An error occurred'
            # return str(e)
            # flash('Error' + str(e) )
            # return render_template('login.html')
    return render_template('online.html')

  

	
		


            
                    


   
