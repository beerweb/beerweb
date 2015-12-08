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
class AdminPanelPageHandler(webapp2.RequestHandler):
  def get(self):
    email = get_user_email()
    if email and is_user_admin():
      page_params = {
        'user_email': email,
      }
      render_template(self, 'adminpanel.html', page_params)
    else:
      self.redirect('/home')


class AdminManageGiftPageHandler(webapp2.RequestHandler):
  def get(self):
    email = get_user_email()
    if email and is_user_admin():
      page_params = {
        'user_email': email,
      }
      render_template(self, 'adminmanagegifts.html', page_params)
    else:
      self.redirect('/home')


class GetGiftsHandler(webapp2.RequestHandler):
  def get(self):
    if not is_user_admin():
      self.response.out.write("Not logged in as admin")
      return
    respStr = ""
    giftCerts = GiftCert.query().order(GiftCert.usedBy).fetch()
    for cert in giftCerts:
      respStr += '$' + str(cert.balance) + ' "' + cert.giftCode + '" '
      respStr += cert.usedBy + ' '
      respStr += '<input type="submit" value="Delete" onclick="handleDelete(\''+cert.giftCode+'\');">'
      respStr += '<br>'
    self.response.out.write(respStr)

  def post(self):
    return self.get()


class GenerateGiftHandler(webapp2.RequestHandler):
  def get(self):
    if not is_user_admin():
      self.response.out.write("Not logged in as admin")
      return
    code = self.request.get("code")
    amount = self.request.get("amount")
    if code and amount:
      if GiftCert.is_code_valid(code):
        existingCert = GiftCert.get_gift_cert(code)
        self.response.out.write("Code already exists: $" + str(existingCert.balance) + " \"" + existingCert.giftCode + "\" " + existingCert.usedBy)
        return
      newGift = GiftCert()
      newGift.giftCode = code
      newGift.balance = float(amount)
      newGift.usedBy = ""
      newGift.put()
      self.response.out.write("$"+ amount + " gift card with code \"" + code + "\" is generated.")
    else:
      self.response.out.write("Invalid parameters")

  def post(self):
    return self.get()


class DeleteGiftHandler(webapp2.RequestHandler):
  def get(self):
    if not is_user_admin():
      return
    code = self.request.get("code")
    if code:
      giftCert = GiftCert.get_gift_cert(code)
      if giftCert:
        giftCert.key.delete()

  def post(self):
    return self.get()

###############################################################################
class AdminManageOrdersPageHandler(webapp2.RequestHandler):
  def get(self):
    email = get_user_email()
    if email and is_user_admin():
      page_params = {
        'user_email': email,
      }
      render_template(self, 'adminmanageorders.html', page_params)
    else:
      self.redirect('/home')

class GetOrdersTableHandler(webapp2.RequestHandler):
  def get(self):
    email = get_user_email()
    if email and is_user_admin():
      orders = BeerOrder.get_all_orders()      
      page_params = {
        'user_email': email,
        'orders': orders
      }
      render_template(self, 'adminmanageorders_table.html', page_params)

  def post(self):
    return self.get()

class SetOrderStatusHandler(webapp2.RequestHandler):
  def post(self):
    email = get_user_email()
    if email and is_user_admin():
      # get params from post request
      data = json.loads(self.request.body)
      transId = int(data["id"])
      newStatus = data["status"]
      # get order by id
      order = ndb.Key("BeerOrder", transId).get()
      if order:
        # if status is being set to cancelled, refund the user
        if newStatus == "Cancelled":
          order.cancel_and_refund()
        else:
          order.status = newStatus;
          order.put()
    else:
      self.redirect('/home')

###############################################################################
class AdminViewOrdersPageHandler(webapp2.RequestHandler):
    def get(self):
      email = get_user_email()
      if email and is_user_admin():
        page_params = {
          'user_email': email,
          'orders': BeerOrder.get_completed_orders(),
          'cancelledOrders': BeerOrder.get_cancelled_orders()
        }
        render_template(self, 'adminvieworders.html', page_params)
      else:
        self.redirect('/home')

###############################################################################
# This allows admins to manually place an order for a user
class ManualPlaceOrderHandler(webapp2.RequestHandler):
  def post(self):
    email = get_user_email()
    if email and is_user_admin():
      # get params from post request
      data = json.loads(self.request.body)
      order = BeerOrder()
      order.items = data["items"]
      order.priceSum = float(data["priceSum"])
      order.address = data["address"]
      order.status = "Verifying"
      order.orderedBy = data["orderedBy"]
      order.put()
    else:
      self.redirect('/home')

###############################################################################
mappings = [
  ('/admin/managegifts', AdminManageGiftPageHandler),
  ('/admin/get_gifts', GetGiftsHandler),
  ('/admin/gen_gift', GenerateGiftHandler),
  ('/admin/del_gift', DeleteGiftHandler),
  ('/admin/manageorders', AdminManageOrdersPageHandler),
  ('/admin/get_orders_table', GetOrdersTableHandler),
  ('/admin/set_order_status', SetOrderStatusHandler),
  ('/admin/vieworders', AdminViewOrdersPageHandler),
  ('/admin/place_order', ManualPlaceOrderHandler),  
  ('/admin/adminpanel', AdminPanelPageHandler)
]
app = webapp2.WSGIApplication(mappings, debug=True)
