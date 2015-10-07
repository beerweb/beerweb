import datetime
import logging
import os
import webapp2

from beers import beers

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import ndb

###############################################################################
# We'll just use this convenience function to retrieve and render a template.
def render_template(handler, templatename, templatevalues={}):
  path = os.path.join(os.path.dirname(__file__), 'templates/' + templatename)
  html = template.render(path, templatevalues)
  handler.response.out.write(html)


###############################################################################
# We'll use this convenience function to retrieve the current user's email.
def get_user_email():
  result = None
  user = users.get_current_user()
  if user:
    result = user.email()
  return result


###############################################################################
class MainPageHandler(webapp2.RequestHandler):
  def get(self):
    render_template(self, 'index.html')
  
###############################################################################
class OrderPageHandler(webapp2.RequestHandler):
  def get(self):
    render_template(self, 'order.html') 
  
###############################################################################
class AccountPageHandler(webapp2.RequestHandler):
  def get(self):
    render_template(self, 'account.html')
  
###############################################################################
class BeerPageHandler(webapp2.RequestHandler):
  def get(self):
    template_params = {
      'beers' : beers
    }
    render_template(self, 'beer.html', templatevalues=template_params)

  
###############################################################################
class PostedImage(ndb.Model):
  pass


###############################################################################
class ImageComment(ndb.Model):
  pass


###############################################################################
class ImageVote(ndb.Model):
  pass
  

###############################################################################
mappings = [
  ('/', MainPageHandler), 
  ('/order', OrderPageHandler),
  ('/account', AccountPageHandler),
  ('/beer', BeerPageHandler)
]
app = webapp2.WSGIApplication(mappings, debug=True)