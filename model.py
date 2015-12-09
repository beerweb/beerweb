import datetime
import logging
import os
import webapp2

import emailsender

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import images
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers


###############################################################################
class ShoppingCart(ndb.Model):
  price = ndb.StringProperty()
  contents = ndb.JsonProperty()

###############################################################################
class BeerUser(ndb.Model):
  address = ndb.StringProperty()
  balance = ndb.FloatProperty()

  cart = ndb.StructuredProperty(ShoppingCart)

  # get or create user profile
  @staticmethod
  def get_user_profile(email):
    beerUser = ndb.Key("BeerUser", email).get()
    if beerUser is None:
      beerUser = BeerUser()
      beerUser.key = ndb.Key("BeerUser", email)
      beerUser.balance = 0.0
      beerUser.address = ""
      #beerUser.cart = ShoppingCart()
      #beerUser.cart.price = "0.00"
      #beerUser.cart.contents={}
      beerUser.put()
    return beerUser

  # This function returns the balance remaining in user's account
  @staticmethod
  def get_user_balance(email):
    return get_user_profile(email).balance

  # This function returns the address stored in user's account
  @staticmethod
  def get_user_address(email):
    return get_user_profile(email).address

  @staticmethod
  def set_user_balance(email, balance):
    prof = get_user_profile(email)
    prof.balance = balance
    prof.put()

  @staticmethod
  def set_user_address(email, address):
    prof = get_user_profile(email)
    prof.address = address
    prof.put()


###############################################################################
class Beer(ndb.Model):
  beerid = ndb.IntegerProperty()
  brewery = ndb.StringProperty()
  product = ndb.StringProperty()
  style = ndb.StringProperty()
  abv = ndb.FloatProperty()
  price = ndb.StringProperty()

###############################################################################
class GiftCert(ndb.Model):
  balance = ndb.FloatProperty()
  usedBy = ndb.StringProperty()
  giftCode = ndb.StringProperty()

  @staticmethod
  def get_gift_cert(code):
    result = GiftCert.query(GiftCert.giftCode == code).order(GiftCert.usedBy).fetch(1)
    if result:
      return result[0]
    else:
      return None

  # Returns true if gift cert with the code exists - both used and unused
  @staticmethod
  def is_code_valid(code):
    if GiftCert.get_gift_cert(code):
      return True
    else:
      return False

  # Returns true if gift cert exists and unused
  @staticmethod
  def is_code_unused(code):
    giftCert = GiftCert.get_gift_cert(code)
    if giftCert:
      # gift cert is valid
      if giftCert.usedBy:
        # gift cert is used
        return False
      else:
        # gift cert is unused
        return True
    else:
      # gift cert is not valid
      return False

  # Redeems gift to user
  def redeem_gift(self, email):
    if not self.usedBy:
      beerUser = BeerUser.get_user_profile(email)
      beerUser.balance += self.balance
      self.usedBy = email
      beerUser.put()
      self.put()
    else:
      pass


###############################################################################
class BeerOrder(ndb.Model):
  items = ndb.StringProperty() # items in order
  priceSum = ndb.FloatProperty() #sum of order
  address = ndb.StringProperty() # address of user
  status = ndb.StringProperty() # Verifying, Delivering, Completed, Cancelled
  orderedBy = ndb.StringProperty() # email of user
  timePlaced = ndb.DateTimeProperty(auto_now_add=True)
  # can use myOrder.key.id as transaction id

  # Returns all the orders placed by the user (new orders first)
  @staticmethod
  def get_user_orders(email):
    results = BeerOrder.query(BeerOrder.orderedBy == email).order(-BeerOrder.timePlaced).fetch()
    return results

  # Returns all completed orders (new orders first)
  @staticmethod
  def get_completed_orders():
    results = BeerOrder.query(BeerOrder.status == "Completed").order(-BeerOrder.timePlaced).fetch()
    return results

  # Returns all completed orders (new orders first)
  @staticmethod
  def get_cancelled_orders():
    results = BeerOrder.query(BeerOrder.status == "Cancelled").order(-BeerOrder.timePlaced).fetch()
    return results

  # Returns all orders (old orders first)
  @staticmethod
  def get_all_orders():
    results = BeerOrder.query().order(BeerOrder.timePlaced).fetch()
    return results

  def cancel_and_refund(self):
    # cannot cancel already cancelled or completed orders
    if self.status == "Cancelled" or self.status == "Completed":
      return
    userProf = BeerUser.get_user_profile(self.orderedBy)
    if userProf:
      userProf.balance += self.priceSum
      userProf.put()
    d = self.get_deliverer()
    if d:
      d.unassign_job()
    self.status = "Cancelled"
    self.put()

  def deliver_order(self):
    # do not allow delivering cancelled or completed orders
    if self.status == "Cancelled" or self.status == "Completed":
      return
    self.status = "Delivering"
    self.put()

  def complete_order(self):
    # do not allow delivering cancelled or completed orders
    if self.status == "Cancelled" or self.status == "Completed":
      return
    d = self.get_deliverer()
    if d:
      d.unassign_job()
    self.status = "Completed"
    self.put()
    
  def get_deliverer(self):
    # search deliverers and find the one that took this job
    result = Deliverer.query(Deliverer.job == self.key).fetch(1)
    if result:
      return result[0]
    else:
      return None

###############################################################################
class Deliverer(ndb.Model):
  name = ndb.StringProperty()
  job = ndb.KeyProperty(kind=BeerOrder)
  email = ndb.StringProperty()
  salary = ndb.FloatProperty()
  dateHired = ndb.DateProperty(auto_now_add=True)

  @staticmethod
  def get_by_name(name):
    result = Deliverer.query(Deliverer.name == name).fetch(1)
    if result:
      return result[0]
    else:
      return None

  @staticmethod
  def get_by_email(email):
    result = Deliverer.query(Deliverer.email == email).fetch(1)
    if result:
      return result[0]
    else:
      return None

  @staticmethod
  def get_all_deliverers():
    results = Deliverer.query().order(Deliverer.dateHired).fetch()
    return results

  def assign_job(self, order):
    if order.status == "Delivering":
      emailsender.send_assign_email(self.email, order)
      self.job = order.key
      self.put()

  def unassign_job(self):
    if self.job:
      emailsender.send_unassign_email(self.email, self.job)
      self.job = None
      self.put()
    
