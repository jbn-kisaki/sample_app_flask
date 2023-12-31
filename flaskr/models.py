# models.py
from flaskr.__init__ import db, login_manager
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user

from datetime import datetime, timedelta
from uuid import uuid4

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# ユーザーテーブル
class User(UserMixin, db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(
        db.String(128),
        default=generate_password_hash('flaskapp')
    )
    picture_path = db.Column(db.Text)
    is_active: bool = db.Column(db.Boolean, unique=False, default=False)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)
    
    def __init__(self, username, email):
        self.username = username
        self.email = email
    
    @classmethod
    def select_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def select_user_by_id(cls, id):
        return cls.query.get(id)
    
    @classmethod
    def search_by_name(cls, username):
        return cls.query.filter_by(
            is_active = True
        ).filter(
            cls.username.like(f'%{username}%'),
            cls.id != int(current_user.get_id())
        ).with_entities(
            cls.id, cls.username, cls.picture_path
        ).all()
    
    def validate_password(self, password):
        return check_password_hash(self.password, password)
    
    def create_new_user(self):
        db.session.add(self)

    def sava_new_password(self, new_password):
        self.password = generate_password_hash(new_password)
        self.is_active = True

# パスワード設定用トークン作成テーブル
class PasswordResetToken(db.Model):
    
    __tablename__ = 'password_reset_tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(
        db.String(128),
        unique=True,
        index=True,
        default=str(uuid4)
    )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    expire_at = db.Column(db.DateTime, default=datetime.now)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now)
    
    def __init__(self, token, user_id, expire_at):
        self.token = token
        self.user_id = user_id
        self.expire_at = expire_at
    
    @classmethod
    def publish_token(cls, user):
        token = str(uuid4())
        new_token = cls(
            token,
            user.id,
            datetime.now() + timedelta(days=1)
        )
        db.session.add(new_token)
        return token
    
    @classmethod
    def get_user_id_by_token(cls, token):
        now = datetime.now()
        record = cls.query.filter_by(token=str(token)).filter(cls.expire_at > now).first()
        if record:
            return record.user_id
        else:
            return None
    
    @classmethod
    def delte_token(cls, token):
        cls.query.filter_by(token=str(token)).delete()