# forms.py
from flaskr.models import User
from wtforms.form import Form
from wtforms.fields import (
    StringField, FileField, PasswordField, SubmitField, HiddenField
)
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_login import current_user
from flask import flash

# ログイン用フォーム
class LoginForm(Form):
    email = StringField(
        'メール: ', validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'パスワード: ', validators=[DataRequired(), EqualTo('confirm_password', message='パスワードが一致しません')]
    )
    confirm_password = PasswordField(
        'パスワード再入力: ', validators=[DataRequired()]
    )
    submit = SubmitField('ログイン')

# 登録用フォーム
class RegisterForm(Form):
    email = StringField(
        'メール: ', validators=[DataRequired(), Email('メールアドレスが誤っています')]
    )
    username = StringField(
        '名前: ', validators=[DataRequired()]
    )
    submit = SubmitField('登録')
    
    def validate_email(self, field):
        if User.select_user_by_email(field.data):
            raise ValidationError('メールアドレスは既に登録されています')

# パスワード設定用フォーム
class ResetPasswordForm(Form):
    password = PasswordField(
        'パスワード: ', validators=[DataRequired(), EqualTo('confirm_password', message='パスワードが一致しません')]
    )
    confirm_password = PasswordField(
        'パスワード再入力: ', validators=[DataRequired()]
    )
    submit = SubmitField('パスワードを更新する')
    
    def validate_password(self, field):
        if len(field.data) < 8:
            raise ValidationError('パスワードは8文字以上です')

# パスワード再設定用フォーム
class ForgotPasswordForm(Form):
    email = StringField(
        'メール: ', validators=[DataRequired(), Email()]
    )
    submit = SubmitField('パスワードを再設定する')
    
    def validate_email(self, field):
        if not User.select_user_by_email(field.data):
            raise ValidationError('そのメールアドレスは登録されていません')

# ユーザー情報更新用フォーム
class UserForm(Form):
    email = StringField(
        'メール: ', validators=[DataRequired(), Email('メールアドレスが誤っています')]
    )
    username = StringField(
        '名前: ', validators=[DataRequired()]
    )
    picture_path = FileField('ファイルアップロード')
    submit = SubmitField('登録情報更新')
    
    def validate(self):
        if not super(Form, self).validate():
            return False
        user = User.select_user_by_email(self.email.data)
        # 入力されたメールアドレスがDBに既に存在する場合
        if user:
            # 存在したメールアドレスが別のユーザーだった場合
            if user.id != int(current_user.get_id()):
                flash('そのメールアドレスは既に登録されています')
                return False
        return True

class ChangePasswordForm(Form):
    password = PasswordField(
        'パスワード: ', validators=[DataRequired(), EqualTo('confirm_password', message='パスワードが一致しません')]
    )
    confirm_password = PasswordField(
        'パスワード再入力: ', validators=[DataRequired()]
    )
    submit = SubmitField('パスワードを更新する')
    
    def validate_password(self, field):
        if len(field.data) < 8:
            raise ValidationError('パスワードは8文字以上です')