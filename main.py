from flask import Flask,render_template,request,redirect,session,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:123456@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'random'

class Blog(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    owner_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __init__(self,title,body,owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog',backref='owner')

    def __init__(self,username,password):
        self.username = username
        self.password = password

@app.route('/signup',methods=["POST","GET"])
def signup():
    
    return render_template('signup.html')

@app.route('/login',methods=['POST',"GET"])
def login():

    return render_template('login.html')

@app.route('/newpost',methods=['POST','GET'])
def newpost():
    
    owner = User.query.filter_by(username=session['username']).first()

    title_error = ''
    body_error = ''

    if request.method == "POST":
        new_title = request.form["newpost_title"]
        new_post = request.form['newpost']
        
        if new_title == '':
            title_error = 'Please fill in the title'

        if new_post == '':
            body_error = 'Plase fill in the body'
            
        if not title_error and not body_error:
            new_entry = Blog(new_title,new_post,owner)
            db.session.add(new_entry)
            db.session.commit()
            return redirect('/blog?id=' + str(new_entry.id))
        else:
            return render_template("newpost.html",new_title=new_title, new_post= new_post, title_error=title_error,
                body_error=body_error)
    return render_template('newpost.html')  

@app.route('/blog',methods=['POST','GET'])
def blog():
    
    entry_id = request.args.get("id")
    if entry_id:
        post = Blog.query.filter_by(id=int(entry_id)).first()
        return render_template('entries.html',title=post.title, body=post.body)

    blogs = Blog.query.all()   
   
    return render_template('blog.html',blogs=blogs)   


@app.route("/")
def index():
    return redirect("/blog")

if __name__ == '__main__':
    app.run()