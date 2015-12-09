import datetime
import logging
import os
import webapp2
import json

from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
from google.appengine.api import mail

###############################################################################
# Renders email template
def render_template(templatename, templatevalues={}):
  path = os.path.join(os.path.dirname(__file__), 'templates/' + templatename)
  text = template.render(path, templatevalues)
  return text

###############################################################################
def send_assign_email(toEmail, order):
  mail.send_mail(
    sender="deliverymanager@pittbeerdelivery.appspotmail.com",
    to=toEmail,
    subject="Delivery job assigned",
    body=render_template("email_deliverer.txt", {"order":order})
  )

###############################################################################
def send_unassign_email(toEmail, order):
  mail.send_mail(
    sender="deliverymanager@pittbeerdelivery.appspotmail.com",
    to=toEmail,
    subject="Delivery job unassigned",
    body=render_template("email_deliverer.txt", {"order":order})
  )

###############################################################################
def send_hire_email(toEmail, deliverer):
  mail.send_mail(
    sender="deliverymanager@pittbeerdelivery.appspotmail.com",
    to=toEmail,
    subject="You have been hired!",
    body=render_template("email_hire.txt", {"deliverer":deliverer})
  )

###############################################################################
def send_fire_email(toEmail, deliverer):
  mail.send_mail(
    sender="deliverymanager@pittbeerdelivery.appspotmail.com",
    to=toEmail,
    subject="You have been FIRED!",
    body=render_template("email_fire.txt", {"deliverer":deliverer})
  )
