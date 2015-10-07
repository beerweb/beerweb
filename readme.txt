# Pitt Beer Delivery Service

This is the repository for the Pitt Beer Delivery Service. CS1520

## Synopsis

The project will focus around being a product purchasing service (beer). A user will come to the site, enter their delivery address, and get a list of available products for the Pitt University campus area. The user will then choose what and how many products they want (up to a set limit) and perform a checkout operation that is completed with a payment. Order details will be generated, and the user will receive the product in a calculated amount of time.

## MVP (Minimal Viable Product)

1. Users will come to the site and enter their delivery address (within the Pitt campus area).
2. A list of available beer will come up to choose from.
3. The user will build a shopping cart of the beer products they want.
4. Checkout will be completed using a credit card and calling our delivery number.
5. Order details will be emailed to the User.
6. A delivery order will be generated and emailed to our driver to pick up the beer from each location that beer was ordered from.

## Additional / Extra Features (using numbered points from above)

* The website should be VERY simple and render on mobile devices. [HTML & CSS]

(1.) A disclaimer needs to be shown, “You must be 21 or older to enter”. Two buttons can be clicked, “Yes, I am over 21” and “No, I am not over 21”. [JAVASCRIPT]

(1.) Create a Google login that will allow the user to keep their address on file. [PYTHON]

(1.) Use Google Maps API to make sure their delivery address is within 5 miles of campus. [JAVASCRIPT]

(2.) The login account could also be used to keep address and order history. [PYTHON]

(2.) A database will hold the available beers with pictures, prices, and address of where it is located. [GOOGLE DB?]

(3.) The shopping cart could have built-in features like tax per bottle, tax per location, free delivery if the maximum amount of beer is ordered (192 ounces, or 2 six packs). [JAVASCRIPT]

(4.) Checkout could use Google Wallet or PayPal (or some other simple, easy to implement API). [PYTHON / JAVASCRIPT?]

(5.) Order details could be associated with the login account when emailed to user. [PYTHON]

(5.) Order details could include an ETA using Google Maps. We will use the Maps API to input all of the locations plus the delivery location and grab the ETA. [PYTHON? / JAVASCRIPT?]

## Milestone #1
- Create a basic page with inputs (no CSS just basic inputs and layout).
- Show popup when user enters the site alerting them they must be 21 years of age or over.
- Implement the Google login platform for user accounts.
- Research the Google Apps database plugin for inventory. But for this milestone, implement inventory as a static list on the page. This will give a skeleton HTML layout that can be used when switching over to querying items from the database.

## Milestone #2
- Make the popup set a cookie which gets checked every time the page loads. If the cookie exists, then don’t show the popup (because they already answered ‘Yes, I am over 21’).
- Get address information from the inputs.
- Static address info will be in the database and queried.
- Build a static database (no updates, deletes, etc) that can be queried. Swap this out for the static inventory list.
- Format the web page inputs to look decent. Add some CSS to give it a unique style.
- Implement Google Maps API. 

## Milestone #3
- Address information will be associated with the user’s login and stored in our database.
- Google Maps API call to make sure user address is within 5 miles of the Pitt campus.
- Shopping Cart component added (might not function).
- Online payment system component added (might not function).
- Email system implemented to email the user, and email order details to the driver.
- The user will receive an order receipt.
- The driver will receive a destination itinerary and list of products to get.
- Google Maps API call to determine the ETA for the driver to travel to all of the necessary locations and arrive at the deliver address. Attach this to the user’s order receipt.

## Caveats and Legalities
* The sale is limited to 192 ounces of beer, or two six-packs of 16-ounce bottles.
* Only “Restaurant,” “Eating Place Malt Beverage” or “Hotel” licensees can sell beer for delivery.
* The beer must be purchased BEFORE delivery (by calling or using an online payment system).
* No purchases can be made after 2:00AM.
* Valid ID is needed upon delivery of the beer, along with a signature.
* The person signing cannot be visibly (overly) intoxicated.
* A “Transport for Hire Class A or B” license is needed for the drivers.
* Persons transporting the beer must be 21 years of age or older.
* No wine or liquor can be ordered (yet).
* Sources:
  * [Official PALCB Release](http://bit.ly/1BzAJiD)
  * [Summary of Rules](http://bit.ly/1FBQ5IM)
