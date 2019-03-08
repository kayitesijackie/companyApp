from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import User,Company,Comment, Subscriber
from .. import db,photos
from .forms import UpdateProfile,CompanyForm,CommentForm, SubscriberForm
from flask_login import login_required,current_user
import datetime
from ..email import mail_message

@main.route('/')
def index():
    accountancy= Company.get_companies('accountancy')
    construction = Company.get_companies('construction')
    designer = Company.get_companies('designer')
    food = Company.get_companies('food')
    telecommunication = Company.get_companies('telecommunication')
    others= Company.get_companies('others')
    subscriber_form=SubscriberForm
    
    return render_template('index.html', title = 'Company App - Home',accountancy=accountancy, construction = construction, designer = designer, food = food, telecommunication=telecommunication, subscriber_form=subscriber_form, others = others)

@main.route('/companies/accountancy')
def accountancy():
    companies = Company.get_companies('Accountancy')
    print(companies)

    return render_template('accountancy.html',companies = companies)


@main.route('/companies/construction')
def construction():
    companies = Company.get_companies('construction')

    return render_template('construction.html',companies = companies)


@main.route('/companies/designer')
def designer():
    companies = Company.get_companies('designer')

    return render_template('designer.html',companies = companies)


@main.route('/companies/food')
def food():
    companies = Company.get_companies('food')

    return render_template('food.html',companies = companies)

@main.route('/companies/telecommunication')
def telecommunication():
    companies = Company.get_companies('telecommunication')

    return render_template('telecommunication.html',companies = companies)

@main.route('/companies/others')
def others():
    companies = Company.get_companies('others')

    return render_template('others.html',companies = companies)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template('profile/profile.html',user = user)


@main.route('/user/<uname>/update', methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname = user.username))

    return render_template('profile/update.html', form = form)


@main.route('/user/<uname>/update/pic', methods = ['POST'])
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()

    return redirect(url_for('main.profile', uname = uname))


@main.route('/company/new', methods = ['GET','POST'])
@login_required
def new_company():
    legend = 'New Company'
    form = CompanyForm()
    if form.validate_on_submit():
        name = form.name.data
        company = form.text.data
        services = form.services.data
        contacts = form.contacts.data
        category = form.category.data

        new_company = Company(name = name,company_content = company, category = category,user = current_user, services = services, contacts = contacts)
        new_company.save_company()

        subscriber = Subscriber.query.all()
        # for email in subscriber:
            # mail_message("New Company Post from Company App! ","email/notification",email.email,subscriber=subscriber)
        return redirect(url_for('main.index'))

    title = 'New Company'
    return render_template('new_company.html', legend = legend, title = title, company_form = form)

@main.route('/company/delete/<int:id>', methods = ['GET', 'POST'])
@login_required
def delete_company(id):
    company = Company.get_company(id)
    db.session.delete(company)
    db.session.commit()

    return render_template('companies.html', id=id, company = company)

@main.route('/company/comment/delete/<int:id>', methods = ['GET', 'POST'])
@login_required
def delete_comment(id):
    comment = Comment.query.filter_by(id=id).first()
    company_id = comment.company
    Comment.delete_comment(id)

    return redirect(url_for('main.company',id=company_id))

@main.route('/company/<int:id>', methods = ["GET","POST"])
def company(id):
    company = Company.get_company(id)
    posted_date = company.posted.strftime('%b %d, %Y')

    form = CommentForm()
    if form.validate_on_submit():
        comment = form.text.data
        name = form.name.data

        new_comment = Comment(comment = comment, name = name, company_id = company)

        new_comment.save_comment()

    comments = Comment.get_comments(company)

    return render_template('company.html', company = company, comment_form = form,comments = comments, date = posted_date)

@main.route('/user/<uname>/companies', methods = ['GET','POST'])
def user_companies(uname):
    user = User.query.filter_by(username = uname).first()
    companies = Company.query.filter_by(user_id = user.id).all()

    return render_template('profile/companies.html', user = user, companies = companies)

@main.route('/companies/recent', methods = ['GET','POST'])
def companies():
    companies = Company.query.order_by(Company.id.desc()).limit(5)

    return render_template('companies.html',companies = companies)


@main.route('/subscribe', methods=['GET','POST'])
def subscriber():
    subscriber_form=SubscriberForm()
    companies = Company.query.order_by(Company.posted.desc()).all()

    if subscriber_form.validate_on_submit():
        subscriber= Subscriber(email=subscriber_form.email.data,name = subscriber_form.name.data)

        db.session.add(subscriber)
        db.session.commit()

        # mail_message("Welcome to Company app","email/welcome_subscriber",subscriber.email,subscriber=subscriber)

        title= "Company App"
        
        return render_template('index.html',title=title, companies = companies)

    subscriber = Company.query.all()

    companies = Company.query.all()


    return render_template('subscribe.html',subscriber=subscriber,subscriber_form=subscriber_form,company = company)


@main.route('/company/<int:id>/update', methods = ['GET','POST'])
@login_required
def update_company(id):
    legend = 'Update Company'
    company = Company.get_company(id)
    form = CompanyForm()
    if form.validate_on_submit():
        company.name = form.name.data
        company.company_content = form.text.data
        company.category = form.category.data
        company.services = form.services.data
        company.contacts = form.contacts.data
        db.session.commit()
        return redirect(url_for('main.company', id = id))
    elif request.method == 'GET':
        form.name.data = company.name
        form.text.data = company.company_content
        form.services.data = company.services
        form.contacts.data = company.contacts
        form.category.data = company.category
    return render_template('new_company.html', legend = legend, company_form = form, id=id)
