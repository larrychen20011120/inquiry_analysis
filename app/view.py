from flask import Flask, request, render_template, redirect, url_for, session
from flask_login import login_user, current_user, login_required, logout_user
from app.form import LoginForm, RegisterForm, UploadForm
from app import app, db
from app.model import User, File, AnalysisResult, Blog, Task
import os
import time
import json
import base64

@app.route('/', methods=['GET'])
def index():
    # index will redirect to login
    return redirect(url_for('login'))

@app.route('/register', methods=['POST'])
def register():
    loginForm = LoginForm()
    registerForm = RegisterForm()
    errors = []
    login = False
    if registerForm.validate_on_submit():
        account = User.query.filter_by(account=registerForm.account.data).first()
        if account is None:
            user = User(
                name=registerForm.name.data,
                account=registerForm.account.data,
                quota=3
            )
            user.password=registerForm.password.data
            db.session.add(user)
            db.session.commit()
            print("register Success!")
            return redirect(url_for('login'))
        else:
            errors.append({'field': 'register', 'messages': ["該電子信箱已被註冊"]})

    # error collection
    if registerForm.errors:
        for key in registerForm.errors.keys():
            errors.append({'field': key, 'messages': registerForm.errors[key]} )

    return render_template('login.html', loginForm=loginForm, registerForm=registerForm, errors=errors, login=login)

@app.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm()
    registerForm = RegisterForm()
    errors = []
    login = True
    if loginForm.validate_on_submit():
        user = User.query.filter_by(account=loginForm.account.data).first()
        if user is not None and user.verify_password(loginForm.password.data):
            print("Login Success!!")
            # not to remember in cookie
            login_user(user, False)
            return redirect(url_for('home'))
        else:
            errors.append({'field': 'login', 'messages': ["查無此帳號或是密碼錯誤"]})

    # error collection
    if loginForm.errors:
        for key in loginForm.errors.keys():
            errors.append({'field': key, 'messages': loginForm.errors[key]} )

    return render_template('login.html', loginForm=loginForm, registerForm=registerForm, errors=errors, login=login)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    uploadForm = UploadForm()
    errors = []
    if uploadForm.validate_on_submit():
        userId = current_user.id;
        file = request.files['uploadFile']
        if file and allowed_file(file.filename):
            filename = filename_encode(file.filename, current_user.id);
            url = os.path.join( os.path.join(app.config['ENTRY'], 'uploads'), filename )
            file.save(url)
            newFile = File(
                name=uploadForm.title.data,
                patient=uploadForm.patient_name.data if uploadForm.patient_name.data else None,
                date = uploadForm.date.data,
                completed=False,
                userId=userId,
                url=url
            )
            db.session.add(newFile)
            db.session.commit()

            # test result("https://i.imgur.com/UKFoMHf.png")
            """
            ar = AnalysisResult (
                fileId = newFile.id,
                result_url = app.config['ENTRY'] + "results/test.txt",
                wordcloud_url = "https://i.imgur.com/UKFoMHf.png"
            )
            """
            # create new text to do
            task = Task(
                fileId=newFile.id
            )
            db.session.add(task)
            db.session.commit()
            errors.append({'field': 'success', 'messages': ["上傳成功"]})
            return render_template('upload.html', uploadForm=UploadForm(), errors=errors)
        else:
            errors.append({'field': 'uploadFile', 'messages': ["檔案格式不是語音檔"]})
            return render_template('upload.html', uploadForm=uploadForm, errors=errors) # return to upload page
    return render_template('upload.html', uploadForm=uploadForm, errors=errors)

@app.route('/home', methods=['GET'])
@login_required
def home():
    return render_template('home.html')

@app.route('/api/public_record', methods=['POST'])
@login_required
def public_record():
    data = dict( json.loads(request.get_data().decode()))
    ret = {
        'items': []
    }
    user = User.query.filter_by(name=current_user.name).first()
    # validate
    if 'name' in data and user:
        # show only others in blog
        blogs = Blog.query.filter(Blog.owner != user.id).all()
        for blog in blogs:
            result = File.query.filter_by(id = blog.fileId).first()
            item = {
                'name': result.name,
                'date': str(result.date),
                'patient': result.patient,
                'id': result.id
            }
            ret['items'].append(item)
        ret['valid'] = 'success'
    else:
        ret['valid'] = 'error'
    return json.dumps(ret, ensure_ascii=False)

@app.route('/api/chat_record', methods=['POST'])
@login_required
def chatRecord():
    data = dict( json.loads(request.get_data().decode()))
    ret = {
        'items': []
    }
    file = File.query.filter_by(id=data['id']).first()
    result = AnalysisResult.query.filter_by(fileId=data['id']).first()
    # validate (no error detection)
    result_path =result.result_url
    wav_path = file.url
    img_url = result.wordcloud_url
    enc = str( base64.b64encode( open(wav_path, 'rb').read() ))
    with open(result_path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.rstrip().split(':', 1)
            identity, content = line[0], line[1]
            if content:
                item = {
                    'identity': identity,
                    'content': content
                }
                ret['items'].append(item)

    ret['valid'] = 'success'
    ret['code'] = enc
    ret['img_url'] = img_url
    return json.dumps(ret, ensure_ascii=False)

@app.route('/analysis/<id>', methods=['GET'])
@login_required
def analysis(id):
    return render_template('analysis.html', id=id);

@app.route('/blog', methods=['GET'])
@login_required
def blog():
    return render_template('blog.html');

@app.route('/api/myrecord', methods=['POST'])
@login_required
def myrecord():
    data = dict( json.loads(request.get_data().decode()))
    ret = {
        'items': []
    }
    user = User.query.filter_by(name=current_user.name).first()
    # validate
    if 'name' in data and user:
        results = File.query.filter_by(userId = current_user.id).all()
        for result in results:
            item = {
                'name': result.name,
                'date': str(result.date),
                'patient': result.patient,
                'id': result.id
            }
            ret['items'].append(item)
        ret['valid'] = 'success'
    else:
        ret['valid'] = 'error'
    return json.dumps(ret, ensure_ascii=False)

@app.route('/api/share', methods=['POST'])
@login_required
def share():
    data = dict( json.loads(request.get_data().decode()))
    file = File.query.filter_by(id=int(data['id'])).first()
    blog = Blog(
        fileId=file.id,
        owner=file.userId
    )
    db.session.add(blog)
    db.session.commit()
    return json.dumps({'valid': 'success'}, ensure_ascii=False)

# personal defined function
def allowed_file(filename):
    # check the file is audio file type
    return '.' in filename and filename.split('.')[-1] in app.config["ALLOWED_EXTENSIONS"]
def filename_encode(filename, id):
    # encode the file name
    filename, ext = filename.split('.')[0], filename.split('.')[1]
    return (''.join(sorted(filename))) + '_'+ str(id) + '_' + str(int(time.time())) + "." + ext
