# coding=utf-8
# -*- coding: UTF-8 -*-
from flask import Flask, request, url_for, render_template, session
from flask.ext.sqlalchemy import SQLAlchemy
import re, time, os
from werkzeug import secure_filename
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://wangdi2:asqwzx456@119.29.169.60/askui'
db = SQLAlchemy(app)
app.secret_key = 'A0Zr98=j/3yXNR5~XHH!jmN]LWX/,?CRT'
app.config['USERNAME'] = 'icebe'
app.config['PASSWORD'] = 'asqwzx456'
CORS(app)

UPLOAD_FOLDER = '/usr/share/nginx/html/image/'
UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    title = db.Column(db.Text)
    time = db.Column(db.String(30))

    def __init__(self, id, content, title, time):
        self.id = id
        self.content = content
        self.title = title
        self.time = time


@app.route('/')
def index():
     articleSet = Article.query.filter().all()
     for article in articleSet:
        dr = re.compile(r'<[^>]+>', re.S)
        article.content = dr.sub('', article.content)
        article.content = article.content[:100]
        #article.id = './article/' + str(article.id)
     return render_template('index.html', articleSet=articleSet)


@app.route('/article/<int:articleId>')
def articleShower(articleId):
    article = Article.query.filter(Article.id == articleId).first()
    return render_template('article.html', article=article)


@app.route('/admin', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == app.config['USERNAME'] and request.form['password'] == app.config['PASSWORD']:
            session['logged_in'] = True
            return render_template('admin.html')
        else:
            return render_template('login.html')
    else:
        if session.get('logged_in'):
            return render_template('admin.html')
        else:
            return render_template('login.html')


@app.route('/admin/addArticle', methods=['POST'])
def addArticle():
    if session.get('logged_in'):
        qset = Article.query.filter().all()
        i = 0
        for q in qset:
            i = i + 1
        i = i + 1
        tmpTime = time.strftime('%Y-%m-%d %H-%M', time.localtime(time.time()))
        tmpArticle = Article(i, request.form['content'], request.form['title'], tmpTime)
        db.session.add(tmpArticle)
        db.session.commit()
        return render_template('admin.html')
    else:
        return render_template('login.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            ttmp = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            filename = ttmp + secure_filename(file.filename)
            turl = 'http://www.bangnicool.com/image/' + filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = '上传成功---'
            success = success.decode('utf8')
            return '<textarea>success</textarea>'
        return '<textarea>fail</textarea>'
    else:
        return render_template('index.html')

@app.route('/testupload', methods=['GET', 'POST'])
def testupload():
    return render_template('testupload.html')


if __name__ == '__main__':
    app.run()
