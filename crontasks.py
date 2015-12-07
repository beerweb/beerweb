import datetime
import logging
import os
import webapp2
import json

from model import BeerUser, BeerOrder

from google.appengine.ext import ndb

###############################################################################
class DeleteOldOrdersHandler(webapp2.RequestHandler):
  def get(self):
    # delete orders older than 90 days
    earliest = datetime.datetime.now() - datetime.timedelta(days=90)
    oldOrderKeys = BeerOrder.query(BeerOrder.timePlaced <= earliest).fetch(keys_only=True)
    for k in oldOrderKeys:
      k.delete()

###############################################################################
mappings = [
  ('/tasks/delete_old_orders', DeleteOldOrdersHandler)
]
app = webapp2.WSGIApplication(mappings, debug=True)
