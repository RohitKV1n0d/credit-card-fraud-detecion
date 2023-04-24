from app import app,db, User
with app.app_context():
    db.create_all()


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     f_name = db.Column(db.String(200), nullable=False)
#     l_name = db.Column(db.String(20), nullable=False)
#     email = db.Column(db.String(100), nullable=False, unique=True)
#     username = db.Column(db.String(200))
#     pwd = db.Column(db.String(100), nullable=False)
#     # phone = db.Column(db.Integer, nullable=False)
#     balance = db.Column(db.Integer, nullable=False)
#     transactions = db.relationship('Transaction_history', backref='trans')
#     creditcard = db.relationship('Card_details', backref='credit')
# create admin user
admin = User(username='anjana',f_name='Anjana',l_name='Paul',email='anjanapaul0614@gmail.com',pwd='1234',balance=100000)
db.session.add(admin)
db.session.commit()


print("database Created")