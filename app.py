from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask_wtf import Form, RecaptchaField
# from flask_wtf.file import FileField
# from wtforms import TextField, HiddenField, ValidationError, RadioField,\
#     BooleanField, SubmitField, IntegerField, FormField, validators, DateTimeField
# from wtforms.validators import Required
from wtforms.fields.html5 import DateField

class DateForm(Form):

	date1 = DateField('Enter a target date:', format='%Y-%m-%d')

def create_app(configfile=None):

    app = Flask(__name__)
    AppConfig(app, configfile)  # Flask-Appconfig is not necessary, but
                                # highly recommend =)
                                # https://github.com/mbr/flask-appconfig
    Bootstrap(app)

    # in a real app, these should be configured through Flask-Appconfig
    app.config['SECRET_KEY'] = 'devkey'
    app.config['RECAPTCHA_PUBLIC_KEY'] = \
        '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'

    @app.route('/', methods=('GET', 'POST'))
    def index():
        # form = ExampleForm()
        form = DateForm()
        form.validate_on_submit()  # to get error messages to the browser
        info = "Enter a date to get a prediction."
        flash(info, 'info')
        flash("Under Construction", 'critical')
        return render_template('index.html', form=form)

    return app

if __name__ == '__main__':
    create_app().run(debug=True)