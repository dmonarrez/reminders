from email.mime.text import MIMEText
from flask import Flask, flash, redirect, render_template
from flask.ext.wtf import Form
from threading import Timer
from wtforms import SelectField, StringField
from wtforms.validators import DataRequired, Email
import smtplib
import time

app = Flask(__name__)

app.config.update(
  WTF_CSRF_ENABLED = True,
  SECRET_KEY = '<REDACTED>'
)

class ReminderForm(Form):
  delay = SelectField('delay',
                         choices=[('1', '1 minute'),
                                  ('5', '5 minutes'),
                                  ('10', '10 minutes'),
                                  ('20', '20 minutes'),
                                  ('60', '1 hour')])
  email = StringField('email', validators=[DataRequired(), Email()])

def send_reminder(email):
  msg = MIMEText('Reminder!')
  msg['Subject'] = 'Reminder Application Demo!'
  msg['From'] = 'brandlivereminders@gmail.com'
  msg['To'] = str(email)
  
  s = smtplib.SMTP('smtp.gmail.com', 587)
  s.starttls()
  s.login('brandlivereminders@gmail.com', '<REDACTED>')
  s.sendmail('brandlivereminders@gmail.com', [str(email)], msg.as_string())
  s.quit()

def schedule_message(email, delay):
  countdown = int(delay) * 60
  Timer(countdown, send_reminder, [str(email)]).start()

@app.route("/", methods=['GET', 'POST'])
def hello():
  form = ReminderForm()
  
  if form.validate_on_submit():
    schedule_message(form.email.data, form.delay.data)
    flash('Reminder set for %s minute(s)!' % form.delay.data)
    return redirect('/')

  return render_template('index.html', form=form)

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
