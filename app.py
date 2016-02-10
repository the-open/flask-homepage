from flask import Flask, render_template
import os, psycopg2, gunicorn
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config.from_object('settings_default')
app.config.from_envvar('SITE_SETTINGS', silent=True)


db = SQLAlchemy(app)

class Staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    name = db.Column(db.String(80), unique=True)
    title = db.Column(db.String(80), nullable=True)
    active = db.Column(db.Boolean, default=True)
    location = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(80), nullable=True)
    description = db.Column(db.Text, nullable=True)
    order = db.Column(db.Integer, nullable=True)

class Organisation(db.Model):
    __tablename__ = 'organisation'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    slug = db.Column(db.String(80), unique=True)
    title = db.Column(db.String(120), nullable=True)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(80), nullable=True)
    code = db.Column(db.String(3), nullable=True)
    code2 = db.Column(db.String(2), nullable=True)
    founded = db.Column(db.DateTime, nullable=True)
    url = db.Column(db.String(80), nullable=True)
    logo = db.Column(db.String(120), nullable=True)
    coordinates = db.Column(db.String(80), nullable=True)

class ContentBlock(db.Model):
    __tablename__ = 'content_block'
    id = db.Column(db.Text, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    name = db.Column(db.String(80), unique=True)
    contents = db.Column(db.Text, default="")

#class Country(db.Model):
#   id = db.Column(db.Text, primary_key=True)
#   created_at = db.Column(db.DateTime, default="current_timestamp")
#   updated_at = db.Column(db.DateTime, onupdate="current_timestamp")


site = {
        'domainroot': 'https://sheltered-mountain-64816.herokuapp.com',
        'title': 'The Online Progressive Engagement Network',
        'description': 'Our member organisations use a common model of member-led, large-scale campaigning to help a combined 15+ million supporters act together for the common good. OPEN exists to help this unique global family of national movements collaborate, share and grow. Join Us!',
        'fb_description': 'OPEN is a sisterhood of grassroots campaigning organisations from around the world. Our member organisations use a common model of member-led, large-scale campaigning to help a combined 15+ million supporters act together for the common good. OPEN exists to help this unique global family of national movements collaborate, share and grow.',
        'keywords': 'online progressive engagement network political non-party independent activism citizen empowermend social climate economic racial justice human rights feminism equality gender sexuality expression non-conforming people-powered grassroots digital petition protest vote volunteer donate',
        'fb_site_name': 'The OPEN',
        'fb_title': 'The Online Progressive Engagement Network',
    }

@app.route("/")
def home():
    return render_template("home.html", site=site, name="home", )

@app.route("/organisations")
def organisations():
    orgs = {}
    return render_template("organisations.html", site=site, name="organisations",
            add_facebook=True,
            title="OPEN Member Organisations",
            orgs=orgs,
        )

@app.route("/about")
def about():
    staff = Staff.query.filter(Staff.active==True).all()
        #.order_by(Staff.order.desc())
    return render_template("about.html", site=site, name="about",
            title="About OPEN",
            staff=staff,
        )

@app.route("/contact")
def contact():
    return render_template("contact.html", site=site, name="contact", )

admin = Admin(app, name="the-open.net", template_mode="bootstrap3")

class StaffView(ModelView):
    form_widget_args = dict(description={'class': 'form-control ckeditor'})
    create_template = 'admin/ck-create.html'
    edit_template = 'admin/ck-edit.html'
    form_excluded_columns = ['created_at', 'updated_at']

class OrganisationView(ModelView):
    form_widget_args = dict(description={'class': 'form-control ckeditor'})
    create_template = 'admin/ck-create.html'
    edit_template = 'admin/ck-edit.html'
    form_excluded_columns = ['created_at', 'updated_at']

class ContentBlockView(ModelView):
    form_widget_args = dict(description={'class': 'form-control ckeditor'})
    create_template = 'admin/ck-create.html'
    edit_template = 'admin/ck-edit.html'
    form_excluded_columns = ['created_at', 'updated_at']


admin.add_view(StaffView(Staff, db.session))
admin.add_view(OrganisationView(Organisation, db.session))
admin.add_view(ContentBlockView(ContentBlock, db.session))

if __name__ == "__main__":
    app.run(debug=True)
