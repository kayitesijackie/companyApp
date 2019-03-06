from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), index = True)
    email = db.Column(db.String(255),unique = True, index = True)
    bio = db.Column(db.String(1000))
    profile_pic_path = db.Column(db.String)
    password_secure = db.Column(db.String(255))
    companies = db.relationship('Company',backref = 'user', lazy = 'dynamic')
    comments = db.relationship('Comment', backref = 'user', lazy = 'dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self,password):
        self.password_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_secure,password)

    def __repr__(self):
        return f'User{self.username},{self.email}'

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String)
    company_content = db.Column(db.String(5000))
    category = db.Column(db.String(), nullable = False)
    services =db.Column(db.String(1000))
    contacts= db.Column(db.String(1000))
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comments = db.relationship('Comment',backref =  'company_id',lazy = "dynamic")


    def save_company(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_companies(cls,category):
        companies = Company.query.filter_by(category = category).all()
        return companies

    @classmethod
    def get_company(cls,id):
        company = Company.query.filter_by(id = id).first()

        return company

    @classmethod
    def count_company(cls,uname):
        user = User.query.filter_by(username = uname).first()
        companies = Company.query.filter_by(user_id = user.id).all()

        company_count = 0
        for company in companies:
            company_count += 1

        return company_count

    def __repr__(self):
        return f'Company {self.name},{self.category}'


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String(1000))
    name = db.Column(db.String)
    company = db.Column(db.Integer,db.ForeignKey("companies.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,company):
        comments = Comment.query.filter_by(company_id = company).all()
        return comments

    @classmethod
    def delete_comment(cls,id):
        comment = Comment.query.filter_by(id=id).first()
        db.session.delete(comment)
        db.session.commit()

    def __repr__(self):
        return f'Comment{self.comment}'

class Subscriber(db.Model):
    __tablename__ = 'subscribers'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(), unique = True)


