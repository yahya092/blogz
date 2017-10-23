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

@app.before_request
def require_login():
    allowed_routes = ['login','signup','blog','index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/signup',methods=["POST","GET"])
def signup():

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        verify_pass = request.form['verify-password']

        username_error = ''
        password_error = ''
        verify_error = ''

        if len(username) < 3 or len(username) > 20:
            username_error = 'Not a valid username'
    
        if len(password) < 3 or len(password) > 20:
            password_error = "That's not a valid password"

        if verify_pass != password:
            verify_error = "Passwords don't match"
    
        existing_user = User.query.filter_by(username=username).first()

        if not password_error and not username_error and not verify_error:
            if not existing_user:
                new_user = User(username,password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/newpost')
            else:
                flash('User already exist','error')

        else:
            return render_template('signup.html',
                username=username,
                username_error=username_error,
                password_error=password_error,
                verify_error=verify_error) 

    return render_template('signup.html')

@app.route('/login',methods=['POST',"GET"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['username'] = username
            return redirect('/newpost')
        else:
            flash('User password incorrect or user does not exist','error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

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

    username = request.args.get('user')
    if username:
        userobj = User.query.filter_by(username=username).first()
        userid = userobj.id
        blogs = Blog.query.filter_by(owner_id=userid)
        return render_template("user_entries.html",blogs=blogs)
    else:
        blogs = Blog.query.all()    
    return render_template('blog.html',blogs=blogs)   


@app.route("/")
def index():
    
    users = User.query.all()
   
    return render_template('index.html',users=users)

if __name__ == '__main__':
    app.run()