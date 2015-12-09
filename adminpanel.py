import datetime
import logging
import os
import webapp2
import json
import emailsender

from beers import beers
from model import BeerUser, Beer, ShoppingCart, GiftCert, BeerOrder, Deliverer


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

class GetOrderDetailsHandler(webapp2.RequestHandler):
  def get(self):
    email = get_user_email()
    if email and is_user_admin():
      orderId = self.request.get("id")
      if not orderId:
        self.response.out.write("Order ID not specified")
        return
      order = ndb.Key("BeerOrder", int(orderId)).get()
      if not order:
        self.response.out.write("Order not found")
        return
      deliverer = ""
      d = order.get_deliverer()
      if d:
        deliverer = d.name
      page_params = {
        'user_email': email,
        'order': order,
        'deliverer': deliverer
      }
      render_template(self, 'admingetorderdetails.html', page_params)

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
        elif newStatus == "Completed":
          order.complete_order()
        elif newStatus == "Delivering":
          order.deliver_order()
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
class AdminManageDeliverers(webapp2.RequestHandler):
  def get(self):
    email = get_user_email()
    if email and is_user_admin():
      orderId = self.request.get("orderId")
      order = ""
      deliverer = ""
      if orderId:
        order = ndb.Key("BeerOrder", int(orderId)).get()
        if order:
          deliverer = order.get_deliverer()
          if deliverer:
            deliverer = deliverer.name
      page_params = {
        'user_email': email,
        'order': order,
        'deliverer': deliverer
      }
      render_template(self, 'adminmanagedeliverers.html', page_params)
    else:
      self.redirect('/home')

class GetDeliverersTableHandler(webapp2.RequestHandler):
  def get(self):
    email = get_user_email()
    if email and is_user_admin():
      page_params = {
        'user_email': email,
        'deliverers': Deliverer.get_all_deliverers()
      }
      render_template(self, 'adminmanagedeliverers_table.html', page_params)

  def post(self):
    return self.get()

class HireDelivererHandler(webapp2.RequestHandler):
  def post(self):
    email = get_user_email()
    if email and is_user_admin():
      # get params from post request
      data = json.loads(self.request.body)
      name = data["name"]
      email = data["email"]
      salary = float(data["salary"])
      # do not hire a person with same name
      if Deliverer.get_by_name(name):
        return
      else:
        boy = Deliverer()
        boy.name = name
        boy.email = email
        boy.salary = salary
        boy.put()
        # email the deliverer
        emailsender.send_hire_email(boy.email, boy)
    else:
      self.redirect('/home')

class FireDelivererHandler(webapp2.RequestHandler):
  def post(self):
    email = get_user_email()
    if email and is_user_admin():
      # get params from post request
      data = json.loads(self.request.body)
      name = data["name"]
      personToFire = Deliverer.get_by_name(name)
      if personToFire:
        personToFire.key.delete()
        # email the deliverer
        emailsender.send_fire_email(personToFire.email, personToFire)
    else:
      self.redirect('/home')

class AssignDelivererHandler(webapp2.RequestHandler):
  def post(self):
    email = get_user_email()
    if email and is_user_admin():
      # get params from post request
      data = json.loads(self.request.body)
      name = data["name"]
      orderId = int(data["orderId"])
      deliverer = Deliverer.get_by_name(name)
      if deliverer:
        order = ndb.Key("BeerOrder", orderId).get()
        if order:
          # check if order already has a deliverer
          oldD = order.get_deliverer()
          if oldD:
            oldD.unassign_job()
          deliverer.assign_job(order)
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
  ('/admin/get_order_details', GetOrderDetailsHandler),
  ('/admin/set_order_status', SetOrderStatusHandler),
  ('/admin/vieworders', AdminViewOrdersPageHandler),
  ('/admin/place_order', ManualPlaceOrderHandler),
  ('/admin/managedeliverers', AdminManageDeliverers),
  ('/admin/get_deliverers_table', GetDeliverersTableHandler),
  ('/admin/hire_deliverer', HireDelivererHandler),
  ('/admin/fire_deliverer', FireDelivererHandler),
  ('/admin/assign_deliverer', AssignDelivererHandler),
  ('/admin/adminpanel', AdminPanelPageHandler)
]
app = webapp2.WSGIApplication(mappings, debug=True)
