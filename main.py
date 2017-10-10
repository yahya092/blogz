from flask import Flask,render_template,request,redirect,session,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:yahya092@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))


    def __init__(self,title,body):
        self.title = title
        self.body = body

@app.route('/newpost',methods=['POST','GET'])
def newpost():

    if request.method == "POST":
        new_title = request.form["newpost_title"]
        new_post = request.form['newpost']
        new_entry = Blog(new_title,new_post)
        db.session.add(new_entry)
        db.session.commit()

        return redirect('/blog')

    return render_template('newpost.html')  

@app.route('/blog',methods=['POST','GET'])
def blog():
    blog_title = str(Blog.query.filter_by(title=title).all())
    entry = str(Blog.query.filter_by(body=body).all())
    
    return render_template('blog.html',blog_title=title,entry=entry)


@app.route("/")
def index():
    return render_template('base.html')

if __name__ == '__main__':
    app.run()