from flask import Flask, redirect, url_for,render_template,request,session,flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(seconds=50)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self,name,email):
        self.name = name
        self.email = email

# @app.route("/<name>")
# def home(name):
#     return render_template('index.html', content=['Mustafa','Hala','Mena','Yousif'])

@app.route("/admin")
def admin():
    return redirect(url_for("home", name="admin!"))

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        
        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(user,"")
            db.session.add(usr)          # like staging area it's some change not bees saved to the db yet.
            db.session.commit()          # it's like commit in git this to save changes to the db.
        
        flash("Login Successful!")
        # return redirect(url_for("user", usr=user))
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user",methods=["GET","POST"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved!")
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user.html",user=user,email=email)
 
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session['user']
        flash(f"You have been logged out, {user} !", "info")
    session.pop("user",None)
    return redirect(url_for("login"))

@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())

if __name__ == "__main__":
    with app.app_context(): 
        db.create_all()
    app.run(debug=True)