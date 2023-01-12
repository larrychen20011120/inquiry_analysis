from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, RadioField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired, Email, EqualTo, Length
import email_validator
from app.model import User
from flask_uploads import UploadSet

class LoginForm(FlaskForm):
    account = StringField(validators=[DataRequired(), Email('並非電子信箱格式')])
    password = PasswordField(validators=[DataRequired(), Length(8, 20, '密碼需要有8-20個字元')])
    submit = SubmitField('登入帳號')

class RegisterForm(FlaskForm):
    name = StringField(validators=[DataRequired(), Length(8, 20, '帳號需要有8-20個字元')])
    account = StringField(validators=[DataRequired(), Email('並非電子信箱格式')])
    password = PasswordField(validators=[
        DataRequired(), Length(8, 20, '密碼需要有8-20個字元'), EqualTo('confirmPasswd', message='密碼必須相符')]
    )
    confirmPasswd = PasswordField()
    submit = SubmitField('註冊帳號')

class UploadForm(FlaskForm):
    uploadFile = FileField(
        validators = [
            FileRequired()
        ]
    )
    title = StringField(validators=[DataRequired(), Length(1, 20, '標題長度必須在1~20')])
    patient_name = StringField(validators=[Length(0, 10, '病患名稱過長')])
    date = DateField()
    radio = RadioField('對話語言： ', choices=[('chinese','國語'),('taiwanese','台語')])
    submit = SubmitField('傳送檔案')
