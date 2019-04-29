from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'



class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
        if request.method == 'POST':
            title = request.form['title']
            body = request.form['body']
            if title=="" or body=="":
                flash("title or body can't be empty!" , 'error')
            else:
                new_blog = Blog(title, body)
                db.session.add(new_blog)
                db.session.commit()
                blog = Blog.query.get(new_blog.body)
                return render_template('post.html', new_blog=new_blog)


        return render_template('newpost.html')

@app.route('/delete-blog', methods=['POST'])
def delete_blog():

    blog_id = int(request.form['blog-id'])
    blog = Blog.query.get(blog_id)
    db.session.delete(blog)
    db.session.commit()

    return redirect('/')


@app.route('/print_blog', methods=['GET','POST'])
def print_blog():

    blog_id = request.args.get('id')
    new_blog = Blog.query.get(blog_id)
    return render_template('post.html',  new_blog=new_blog)

@app.route('/', methods=['POST', 'GET'])
def index():


    blogs = Blog.query.all()
    return render_template('blog.html',title="Add A Blog!", 
        blogs=blogs)


if __name__ == '__main__':
    app.run()
