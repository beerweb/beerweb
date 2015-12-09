import datetime
import logging
import os
import webapp2
import json

from beers import beers
from model import BeerUser, Beer, ShoppingCart, GiftCert, BeerOrder


from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import urlfetch
from google.appengine.api import mail
from google.appengine.api import memcache

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

def is_user_admin():
  user = users.get_current_user()
  if user:
    return users.is_current_user_admin()
  else:
    return False

###############################################################################
class VerifyAgePageHandler(webapp2.RequestHandler):
  def get(self):
    cookie_value = self.request.cookies.get('age-verified')
    if cookie_value and cookie_value == "Yes":
      self.redirect("/home")
    else:
      render_template(self, 'verifyage.html', {})

  def post(self):
    val = int(self.request.get("ageInput_form"));
    if val == 1:
      # set cookie
      self.response.set_cookie('age-verified', 'Yes', max_age=30*24*60*60)
      self.redirect("/home")
    else:
      self.redirect("http://www.toysrus.com/");

###############################################################################
class MainPageHandler(webapp2.RequestHandler):
  def get(self):
    # ensure all the beers are part of the ndb database. If they aren't, add them
    if len(Beer.query().fetch()) == 0:
      for beer in beers:
        ndbBeer = Beer()
        ndbBeer.beerid = int(beer['id'])
        ndbBeer.brewery = beer['brewery']
        ndbBeer.product = beer['product']
        ndbBeer.style = beer['style']
        ndbBeer.abv = float(beer['abv'])
        ndbBeer.price = beer['price']
        ndbBeer.key = ndb.Key('Beer', beer['id'])
        ndbBeer.put()


    email = get_user_email()
    user_is_admin = is_user_admin()
    page_params = {
      'user_email': email,
      "user_is_admin": user_is_admin,
      'login_url': users.create_login_url('/home'),
      'logout_url': users.create_logout_url('/home')
    }
    render_template(self, 'home.html', page_params)

###############################################################################
class OrderPageHandler(webapp2.RequestHandler):
  def get(self):
    email = get_user_email()
    user_is_admin = is_user_admin()
    totalcost = 0.0
    if email:
      beerUser = BeerUser.get_user_profile(email)
      if not beerUser.cart:
        beerUser.cart = ShoppingCart()
        beerUser.cart.price = "0.00"
        beerUser.cart.contents = {}
        beerUser.put()
      cart = beerUser.cart.contents
      beers_in_cart = []
      if len(cart) != 0:
        for beer in cart:
          ndb_beer = Beer.query(Beer.beerid == int(beer)).fetch(1)[0]
          totalcost += int(cart[beer]) * float(ndb_beer.price)
          beers_in_cart.append({
            "beerid":beer,
            "brewery":ndb_beer.brewery,
            "product":ndb_beer.product,
            "price":ndb_beer.price,
            "quantity":cart[beer]
            })
          #beers_in_cart.append(Beer.query(Beer.beerid == int(beer)).fetch(1)[0])
          #quantities.append(cart[beer])
      template_params={
        'user_email': email,
        'login_url': users.create_login_url('/home'),
        'logout_url': users.create_logout_url('/home'),
        "user_is_admin": user_is_admin,
        "savedAddress":beerUser.address,
        "beers":beers_in_cart,
        "total":'${:.2f}'.format(totalcost)
      }
      render_template(self, 'order.html', template_params)
    else:
      self.redirect(users.create_login_url('/order'))
      
###############################################################################
class AccountPageHandler(webapp2.RequestHandler):
  def get(self):
    email = get_user_email()
    user_is_admin = is_user_admin()
    if email:
      # query ndb to get funds
      beerUser = BeerUser.get_user_profile(email)
      balance = beerUser.balance

      page_params = {
        'user_email': email,
        "user_is_admin": user_is_admin,
      	'login_url': users.create_login_url('/account'),
      	'logout_url': users.create_logout_url('/home'),
        'balance': '${:.2f}'.format(balance)
      }
      render_template(self, 'account.html', page_params)
    else:
      self.redirect(users.create_login_url('/account'))

###############################################################################
class ViewOrdersPageHandler(webapp2.RequestHandler):
  def get(self):
    email = get_user_email()
    user_is_admin = is_user_admin()
    if email:
      page_params = {
        'user_email': email,
        "user_is_admin": user_is_admin,
      	'login_url': users.create_login_url('/home'),
      	'logout_url': users.create_logout_url('/home')
        }
      render_template(self, 'vieworders.html', page_params)
    else:
      self.redirect(users.create_login_url('/account'))

class GetMyOrdersTableHandler(webapp2.RequestHandler):
  def get(self):
    email = get_user_email()
    user_is_admin = is_user_admin()
    if email:
      # query ndb to get orders
      orders = BeerOrder.get_user_orders(email)
      page_params = {
        'user_email': email,
        "user_is_admin": user_is_admin,
      	'login_url': users.create_login_url('/home'),
      	'logout_url': users.create_logout_url('/home'),
        'orders': orders
        }
      render_template(self, 'vieworders_table.html', page_params)
  def post(self):
    return self.get()

class CancelMyOrderHandler(webapp2.RequestHandler):
  def post(self):
    email = get_user_email()
    if email:
      data = json.loads(self.request.body)
      orderId = int(data["id"])
      order = ndb.Key("BeerOrder", orderId).get()
      # only allow user to cancel verifying orders
      if order and order.status == "Verifying" and order.orderedBy == email:
        order.cancel_and_refund()

###############################################################################
class LoadFundsPageHandler(webapp2.RequestHandler):
  def get(self):
    email = get_user_email()
    user_is_admin = is_user_admin()
    if email:
      beerUser = BeerUser.get_user_profile(email)
      balance = beerUser.balance

      process_url = blobstore.create_upload_url('/loadfunds_process')
      page_params = {
        'user_email': email,
        "user_is_admin": user_is_admin,
      	'login_url': users.create_login_url('/home'),
      	'logout_url': users.create_logout_url('/home'),
        'balance': '${:.2f}'.format(balance),
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
      if amount <= 0 or amount > 100:
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
Your new balance is """ + '${:.2f}'.format(beerUser.balance) +
"""

Pitt Beer Delivery Service
""")

    self.redirect('/account')

###############################################################################
class RedeemGiftPageHandler(webapp2.RequestHandler):
  def get(self):
    email = get_user_email()
    user_is_admin = is_user_admin()
    if email:
      beerUser = BeerUser.get_user_profile(email)
      balance = beerUser.balance

      page_params = {
        'user_email': email,
        "user_is_admin": user_is_admin,
      	'login_url': users.create_login_url('/home'),
      	'logout_url': users.create_logout_url('/home'),
        'balance': '${:.2f}'.format(balance),
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
          self.response.out.write('${:.2f}'.format(totalcost)+" is added to your account")
        else:
          # code is valid but used
          self.response.out.write("Code already used")

    else:
      self.response.out.write("Please enter a gift code")

  def post(self):
    return self.get()

###############################################################################
class BeerPageHandler(webapp2.RequestHandler):
  def get(self):
    email = get_user_email()
    user_is_admin = is_user_admin()
    beers_ndb = memcache.get('beerslist')
    if beers_ndb is None:
      beers_ndb = Beer.query().fetch()
      memcache.add('beerslist', beers_ndb)
    else:
      logging.info('beers are in memcache lets goooooo')
    template_params = {
      'user_email': email,
      "user_is_admin": user_is_admin,
      'login_url': users.create_login_url('/beer'),
      'logout_url': users.create_logout_url('/home'),
      'beers' : beers_ndb
    }
    render_template(self, 'beer.html', templatevalues=template_params)

###############################################################################
class BeerBreweryPageHandler(webapp2.RequestHandler):
  def get(self):
    email = get_user_email()
    user_is_admin = is_user_admin()
    beers_ndb = Beer.query().fetch()
    template_params = {
      'user_email': email,
      "user_is_admin": user_is_admin,
      'login_url': users.create_login_url('/beer'),
      'logout_url': users.create_logout_url('/home'),
      'beers' : sorted(beers_ndb, key = lambda beer: beer["brewery"])
    }
    render_template(self, 'beer.html', templatevalues=template_params)

###############################################################################
class BeerNamePageHandler(webapp2.RequestHandler):
  def get(self):
    email = get_user_email()
    user_is_admin = is_user_admin()
    beers_ndb = Beer.query().fetch()
    template_params = {
    'user_email': email,
    "user_is_admin": user_is_admin,
    'login_url': users.create_login_url('/beer'),
    'logout_url': users.create_logout_url('/home'),
      'beers' : sorted(beers_ndb, key = lambda beer: beer["product"])
    }
    render_template(self, 'beer.html', templatevalues=template_params)

###############################################################################
class BeerStylePageHandler(webapp2.RequestHandler):
  def get(self):
    email = get_user_email()
    user_is_admin = is_user_admin()
    beers_ndb = Beer.query().fetch()
    template_params = {
    'user_email': email,
    "user_is_admin": user_is_admin,
    'login_url': users.create_login_url('/beer'),
    'logout_url': users.create_logout_url('/home'),
      'beers' : sorted(beers_ndb, key = lambda beer: beer["style"])
    }
    render_template(self, 'beer.html', templatevalues=template_params)

###############################################################################
class BeerAbvPageHandler(webapp2.RequestHandler):
  def get(self):
    email = get_user_email()
    user_is_admin = is_user_admin()
    beers_ndb = Beer.query().fetch()
    template_params = {
    'user_email': email,
    "user_is_admin": user_is_admin,
    'login_url': users.create_login_url('/beer'),
    'logout_url': users.create_logout_url('/home'),
      'beers' : sorted(beers_ndb, key = lambda beer: float(beer["abv"]))
    }
    render_template(self, 'beer.html', templatevalues=template_params)

###############################################################################
class BeerPricePageHandler(webapp2.RequestHandler):
  def get(self):
    email = get_user_email()
    user_is_admin = is_user_admin()
    beers_ndb = Beer.query().fetch()
    template_params = {
    'user_email': email,
    "user_is_admin": user_is_admin,
    'login_url': users.create_login_url('/beer'),
    'logout_url': users.create_logout_url('/home'),
      'beers' : sorted(beers_ndb, key = lambda beer: beer["price"])
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

class AddToCartHandler(webapp2.RequestHandler):
  def post(self):
    email = get_user_email()
    if not email:
      self.redirect(users.create_login_url('/account'))

    # query ndb to get the current user
    beerUser = BeerUser.get_user_profile(email)
    if not beerUser.cart:
      beerUser.cart = ShoppingCart()
      beerUser.cart.price = "0.00"
      beerUser.cart.contents = {}

    data = json.loads(self.request.body)
    beer_id = int(data["beerID"])
    quantity = int(data["quant"])
    price = float(Beer.query(Beer.beerid == beer_id).fetch(1)[0].price) * quantity

    # check negative quantity
    if quantity < 0:
      return
    
    beerUser.cart.contents[beer_id] = quantity
    beerUser.cart.price = str(float(beerUser.cart.price) + price)

    beerUser.put()

class RemoveFromCartHandler(webapp2.RequestHandler):
  def post(self):
    email = get_user_email()
    if not email:
      self.redirect(users.create_login_url('/account'))
    # query ndb to get the current user
    beerUser = BeerUser.get_user_profile(email)
    if not beerUser.cart:
      beerUser.cart = ShoppingCart()
      beerUser.cart.price = "0.00"
      beerUser.cart.contents = {}

    data = json.loads(self.request.body)
    beer_id = int(data["beerID"])
    quantity = beerUser.cart.contents[data["beerID"]]
    price = float(Beer.query(Beer.beerid == beer_id).fetch(1)[0].price) * quantity

    beerUser.cart.price = str(float(beerUser.cart.price) - price)
    del beerUser.cart.contents[data["beerID"]]
    #beerUser.cart.contents[beer_id] = quantity
    #beerUser.cart.price = str(float(beerUser.cart.price) + price)

    beerUser.put()  

class PlaceOrderHandler(webapp2.RequestHandler):
  def post(self):
    email = get_user_email()
    if not email:
      self.redirect(users.create_login_url('/account'))
    # query ndb to get the current user
    beerUser = BeerUser.get_user_profile(email)
    cart = beerUser.cart.contents
    address = self.request.get("addressTxt")
    beers_in_cart = []

    if not address:
      render_template(self, "ordercomplete.html", {"msg":"Invalid delivery address!"})
      return

    if len(cart) != 0:
      order_string = ""
      totalcost=0
      # Build the order object and save it to the ndb
      new_order = BeerOrder()
      for beer in cart:
        ndb_beer = Beer.query(Beer.beerid == int(beer)).fetch(1)[0]
        totalcost += int(cart[beer]) * float(ndb_beer.price)

        quantity = cart[str(ndb_beer.beerid)]
        if quantity > 0:
          order_string += "{!s}x {!s}\n".format(quantity,ndb_beer.product)

      if totalcost > beerUser.balance:
        render_template(self, "ordercomplete.html", {"msg":"Insufficient funds."})
        return
      
      new_order.items = order_string
      new_order.priceSum = totalcost
      new_order.address = address
      new_order.status = "Verifying"
      new_order.orderedBy = email

      new_order.put()

      # save the address for the user
      beerUser.address = address
      beerUser.balance = beerUser.balance - new_order.priceSum
      #clear their shopping cart
      beerUser.cart = ShoppingCart()
      beerUser.cart.price = "0.00"
      beerUser.cart.contents = {}
      beerUser.put()

      mail.send_mail('Beer@Pittbeerdelivery.appspotmail.com', email, 'Order Verifying', 'You have successfully placed a beer order! Your order will be verified shortly and completed! Thanks!')

      render_template(self, "ordercomplete.html", {"msg":"Your order has been placed."})
    else:
      render_template(self, "ordercomplete.html",{"msg":"Shopping cart is empty."})

###############################################################################
mappings = [
  ('/', VerifyAgePageHandler),
  ('/home', MainPageHandler),
  ('/order', OrderPageHandler),
  ('/account', AccountPageHandler),
  ('/vieworders', ViewOrdersPageHandler),
  ('/get_my_orders_table', GetMyOrdersTableHandler),
  ('/cancel_my_order', CancelMyOrderHandler),
  ('/loadfunds', LoadFundsPageHandler),
  ('/loadfunds_process', LoadFundsProcessHandler),
  ('/redeemgift', RedeemGiftPageHandler),
  ('/redeemgift_process', RedeemGiftProcessHandler),
  ('/beer', BeerPageHandler),
  ('/beerbrewery', BeerBreweryPageHandler),
  ('/beername', BeerNamePageHandler),
  ('/beerstyle', BeerStylePageHandler),
  ('/beerabv', BeerAbvPageHandler),
  ('/beerprice', BeerPricePageHandler),
  ('/getdistance', GetDistanceHandler),
  ('/addToCart', AddToCartHandler),
  ('/removeFromCart', RemoveFromCartHandler),
  ("/placeOrder", PlaceOrderHandler),
]
app = webapp2.WSGIApplication(mappings, debug=True)
