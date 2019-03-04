from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import User,Blog,Comment, Subscriber
from .. import db,photos
from .forms import UpdateProfile,blogForm,CommentForm
from flask_login import login_required,current_user
import datetime
from ..request import get_quote
# Views
@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    quote=get_quote()
    blogs = Blog.query.order_by(Blog.posted.desc()).limit(3).all()

    title = 'Home - Welcome to The Blogger'

    return render_template('index.html', title=title, blogs=blogs ,quote=quote)


@main.route('/blog/new', methods=['GET', 'POST'])
@login_required
def new_blog():
    blog_form = blogForm()
    if blog_form.validate_on_submit():
        title = blog_form.title.data
        text = blog_form.text.data

        users = User.query.all()

        # Update blog instance
        new_blog = Blog(blog_title=title, blog_content=text, user=current_user)

        # Save blog method
        new_blog.save_blog()

        # for user in users:
        #     if user.subscription:
        #         mail_message("New blog", "email/new_blog",
        #                         user.email, user=user)

        return redirect(url_for('.index'))

    # else:
    #     return redirect(url_for('.index'))

    title = 'New blog'
    return render_template('new_blog.html', title=title, blog_form=blog_form)


@main.route('/blogs')
def all_blogs():
    blogs = Blog.query.order_by(Blog.posted.desc()).all()

    title = 'Blogger blogs'

    return render_template('blogs.html', title=title, blogs=blogs)


@main.route('/blog/<int:id>', methods=['GET', 'POST'])
def blog(id):
    form = CommentForm()
    blog = Blog.get_blog(id)

    if form.validate_on_submit():
        comment = form.text.data

        new_comment = Comment(comment=comment, user=current_user, blog_id=blog.id)

        new_comment.save_comment()

    comments = Comment.get_comments(id=id)

    title = f'{blog.blog_title}'
    return render_template('blog.html', title=title, blog=blog, form=form, comments=comments)


@main.route('/delete_comment/<id>/<blog_id>', methods=['GET', 'POST'])
def delete_comment(id, blog_id):
    comment = Comment.query.filter_by(id=id).first()

    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for('main.index'))


@main.route('/delete_blog/<id>', methods=['GET', 'POST'])
def delete_blog(id):
    blog = Blog.query.filter_by(id=id).first()

    db.session.delete(blog)
    db.session.commit()

    return redirect(url_for('main.all_blogs'))


@main.route('/subscribe/<id>')
def subscribe(id):
    user = User.query.filter_by(id=id).first()

    user.subscription = True

    db.session.commit()

    return redirect(url_for('main.index'))


@main.route('/blog/update/<id>', methods=['GET', 'POST'])
def update_blog(id):
    form = blogForm()

    blog = Blog.query.filter_by(id=id).first()

    form.title.data = blog.title
    form.text.data = blog.text

    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data

        blog.title = title
        blog.text = text

        db.session.commit()

        return redirect(url_for('main.blog', id=blog.id))

    return render_template('update.html', form=form)
