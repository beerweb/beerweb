import datetime
import logging
import os
import webapp2

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
      beerUser.cart = ShoppingCart()
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