from rzd_kpp import db #,login_manager
from datetime import datetime
from rzd_kpp import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model):
    __tablename__ = 'User'

    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Login = db.Column(db.String(55), nullable=False, unique=True)
    Password = db.Column(db.String(55), nullable=False)
    details = db.relationship('UserDetails', backref='parent', uselist=False, cascade="all, delete-orphan")
    user_passes = db.relationship('UserPass', backref='user', cascade="all, delete-orphan")

    def __repr__(self):
        return f'User(UserID={self.UserID}, Login={self.Login})'


class UserDetails(db.Model):
    __tablename__ = 'UserDetails'

    UserDetailsID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID'), nullable=False)
    Firstname = db.Column(db.String(55))
    Lastname = db.Column(db.String(55))
    Familyname = db.Column(db.String(55))
    IsAdmin = db.Column(db.Boolean, default=False)
    DateOfBirth = db.Column(db.Date)
    Address = db.Column(db.String(55))
    Active = db.Column(db.Boolean, default=True)
    DateCreated = db.Column(db.Date, default=datetime.utcnow)
    DataUpdated = db.Column(db.Date, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'UserDetails(UserDetailsID={self.UserDetailsID}, Firstname={self.Firstname}, Lastname={self.Lastname})'


class Pass(db.Model):
    __tablename__ = 'Pass'

    PassID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    PassType = db.Column(db.String(55))
    StartDate = db.Column(db.Date)
    ExpireDate = db.Column(db.Date)
    IsActive = db.Column(db.Boolean, default=True)
    CreatedAt = db.Column(db.Date, default=datetime.utcnow)
    UpdatedAt = db.Column(db.Date, onupdate=datetime.utcnow)
    user_passes = db.relationship('UserPass', backref='pass', cascade="all, delete-orphan")

    def __repr__(self):
        return f'Pass(PassID={self.PassID}, PassType={self.PassType})'


class UserPass(db.Model):
    __tablename__ = 'UserPass'

    UserPassID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID'), nullable=False)
    PassID = db.Column(db.Integer, db.ForeignKey('Pass.PassID'), nullable=False)
    CreatedAt = db.Column(db.Date, default=datetime.utcnow)
    EntranceDate = db.Column(db.DateTime)
    ExitDate = db.Column(db.DateTime)

    def __repr__(self):
        return f'UserPass(UserPassID={self.UserPassID}, UserID={self.UserID}, PassID={self.PassID})'
