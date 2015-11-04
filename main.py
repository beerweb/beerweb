import datetime
import logging
import os
import webapp2

from beers import beers
from model import BeerUser
from model import GiftCert

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import urlfetch
from google.appengine.api import mail

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
class VerifyAgePageHandler(webapp2.RequestHandler):
  def get(self):
    render_template(self, 'verifyage.html', {})
    
  def post(self):
    val = int(self.request.get("ageInput_form"));
    if val == 1:
      self.redirect("/home")
    else:
      self.redirect("http://www.toysrus.com/");
	
###############################################################################
class MainPageHandler(webapp2.RequestHandler):
  def get(self):
    email = get_user_email()
    page_params = {
      'user_email': email,
      'login_url': users.create_login_url('/home'),
      'logout_url': users.create_logout_url('/home')
    }
    render_template(self, 'home.html', page_params)
  
###############################################################################
class OrderPageHandler(webapp2.RequestHandler):
  def get(self):
    render_template(self, 'order.html') 
  
###############################################################################
class AccountPageHandler(webapp2.RequestHandler):
  def get(self):
    email = get_user_email()
    if email:
      # query ndb to get funds
      beerUser = BeerUser.get_user_profile(email)
      balance = beerUser.balance
      
      page_params = {
        'user_email': email,
        'balance': balance
      }
      render_template(self, 'account.html', page_params)
    else:
      self.redirect(users.create_login_url('/account'))


###############################################################################
class LoadFundsPageHandler(webapp2.RequestHandler):
  def get(self):
    email = get_user_email()	  
    if email:
      beerUser = BeerUser.get_user_profile(email)
      balance = beerUser.balance
      
      process_url = blobstore.create_upload_url('/loadfunds_process')
      page_params = {
        'user_email': email,
        'balance': balance,
        'loadfunds_process_url': process_url
      }
      render_template(self, 'loadfunds.html', page_params)
    else:
      self.redirect('/home')
      
###############################################################################
class LoadFundsProcessHandler(webapp2.RequestHandler):
  def post(self):
    email = get_user_email()
    if email:
      try:
        amount = float(self.request.get('amount'))
      except ValueError:
        self.redirect("loadfunds")
        return
      if amount <= 0:
        self.redirect("loadfunds")
        return
      
      beerUser = BeerUser.get_user_profile(email)
      beerUser.balance += amount
      beerUser.put()

      mail.send_mail(sender="noreply@pittbeerdelivery.appspotmail.com", 
      to=email,
      subject="Your balance is updated",
      body="""
Dear User:

You have added $""" + str(amount) +
""" to your account.
Your new balance is $""" + str(beerUser.balance) +
"""

Pitt Beer Delivery Service
""")
      
    self.redirect('/account')

###############################################################################
class RedeemGiftPageHandler(webapp2.RequestHandler):
  def get(self):
    email = get_user_email()	  
    if email:
      beerUser = BeerUser.get_user_profile(email)
      balance = beerUser.balance
      
      page_params = {
        'user_email': email,
        'balance': balance,
      }
      render_template(self, 'redeemgift.html', page_params)
    else:
      self.redirect('/home')
      
###############################################################################
class RedeemGiftProcessHandler(webapp2.RequestHandler):
  def get(self):
    email = get_user_email()
    if not email:
      self.redirect('/home')
      return
    
    code = self.request.get("code")
    if code:
      giftCert = GiftCert.get_gift_cert(code)
      if giftCert is None:
        # code is not valid
        self.response.out.write("Invalid code")
        #return
      else:
        # code is valid - check if it's used
        if not giftCert.usedBy:
          # code is valid and unused
          giftCert.redeem_gift(email)
          self.response.out.write("$"+str(giftCert.balance)+" is added to your account")
        else:
          # code is valid but used
          self.response.out.write("Code already redeemed")
          
    else:
      self.response.out.write("Please enter a gift code")

  def post(self):
    return self.get()

###############################################################################
class GenerateGiftHandler(webapp2.RequestHandler):
  def get(self):
    code = self.request.get("code")
    if code:
      newGift = GiftCert()
      newGift.giftCode = code
      newGift.balance = 0.0
      newGift.usedBy = ""
      newGift.put()
      self.response.out.write("$0 gift card created")
    else:
      self.response.out.write("Please enter a gift code")

  def post(self):
    return self.get()

###############################################################################
class BeerPageHandler(webapp2.RequestHandler):
  def get(self):
    template_params = {
      'beers' : beers
    }
    render_template(self, 'beer.html', templatevalues=template_params)

###############################################################################
class BeerBreweryPageHandler(webapp2.RequestHandler):
  def get(self):
    template_params = {
      'beers' : sorted(beers, key = lambda beer: beer["brewery"])
    }
    render_template(self, 'beer.html', templatevalues=template_params)

###############################################################################
class BeerNamePageHandler(webapp2.RequestHandler):
  def get(self):
    template_params = {
      'beers' : sorted(beers, key = lambda beer: beer["product"])
    }
    render_template(self, 'beer.html', templatevalues=template_params)

###############################################################################
class BeerStylePageHandler(webapp2.RequestHandler):
  def get(self):
    template_params = {
      'beers' : sorted(beers, key = lambda beer: beer["style"])
    }
    render_template(self, 'beer.html', templatevalues=template_params)

###############################################################################
class BeerAbvPageHandler(webapp2.RequestHandler):
  def get(self):
    template_params = {
      'beers' : sorted(beers, key = lambda beer: float(beer["abv"]))
    }
    render_template(self, 'beer.html', templatevalues=template_params)

###############################################################################
class BeerPricePageHandler(webapp2.RequestHandler):
  def get(self):
    template_params = {
      'beers' : sorted(beers, key = lambda beer: beer["price"])
    }
    render_template(self, 'beer.html', templatevalues=template_params)
  
class GetDistanceHandler(webapp2.RequestHandler):
  def get(self):
    address = self.request.get("address")
    if address:
      # send http request to google maps
      #logging.info(address)
      url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=cathedral%20of%20learning&destinations=" + address + "&mode=driving&language=en-US&units=imperial&key=AIzaSyCXyR3f0rdJZsxwTNaFp2HRFnLUqlOnbvE"
      result = urlfetch.fetch(url)
      #self.response.out.write(address)
      self.response.out.write(result.content)
    else:
      self.response.out.write("")

  def post(self):
    return self.get()

###############################################################################
mappings = [
  ('/', VerifyAgePageHandler),
  ('/home', MainPageHandler), 
  ('/order', OrderPageHandler),
  ('/account', AccountPageHandler),
  ('/loadfunds', LoadFundsPageHandler),
  ('/loadfunds_process', LoadFundsProcessHandler),
  ('/redeemgift', RedeemGiftPageHandler),
  ('/redeemgift_process', RedeemGiftProcessHandler),
  ('/_gen_gift', GenerateGiftHandler),
  ('/beer', BeerPageHandler),
  ('/beerbrewery', BeerBreweryPageHandler),
  ('/beername', BeerNamePageHandler),
  ('/beerstyle', BeerStylePageHandler),
  ('/beerabv', BeerAbvPageHandler),
  ('/beerprice', BeerPricePageHandler),
  ('/getdistance', GetDistanceHandler)
]
app = webapp2.WSGIApplication(mappings, debug=True)
