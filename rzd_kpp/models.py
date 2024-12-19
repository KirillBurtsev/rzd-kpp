from rzd_kpp import db, login_manager
from datetime import datetime
from rzd_kpp import db
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'User'

    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Login = db.Column(db.String(55), nullable=False, unique=True)
    Password = db.Column(db.String(60), nullable=False)
    details = db.relationship('UserDetails', backref='parent', uselist=False, cascade="all, delete-orphan")
    user_passes = db.relationship('UserPass', backref='user', cascade="all, delete-orphan")

    def __repr__(self):
        return f'User(UserID={self.UserID}, Login={self.Login})'
    def get_id(self):
        return str(self.UserID)


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

class PassType(db.Model):
    __tablename__ = 'PassType'

    PassTypeID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    Name = db.Column(db.String(55), nullable=False, unique=True)
    passes = db.relationship('Pass', backref='pass_type', cascade="all, delete-orphan")

    def __repr__(self):
        return f'PassType(PassTypeID={self.PassTypeID}, Name={self.Name})'


class Pass(db.Model):
    __tablename__ = 'Pass'

    PassID = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    PassTypeID = db.Column(db.Integer, db.ForeignKey('PassType.PassTypeID'), nullable=False)  # Foreign key for PassType
    StartDate = db.Column(db.Date)
    ExpireDate = db.Column(db.Date)
    IsActive = db.Column(db.Boolean, default=True)
    CreatedAt = db.Column(db.Date, default=datetime.utcnow)
    UpdatedAt = db.Column(db.Date, onupdate=datetime.utcnow)
    user_passes = db.relationship('UserPass', backref='pass', cascade="all, delete-orphan")

    def __repr__(self):
        return f'Pass(PassID={self.PassID}, PassType={self.pass_type.Name}, StartDate={self.StartDate})'
    



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
