from beerlist import beers

# This is a python script that returns a very simply html table of beers from the beerlist.py file

page_contents = "<table>"

# Create the first table row, with headers
page_contents += "<tr>"		# Add a row to the table
page_contents += "<th>"		# Add a cell to the row
page_contents += "Name"
page_contents += "</th>"	# Close cell

page_contents += "<th>"		# Add a cell to the row
page_contents += "Brewery"
page_contents += "</th>"	# Close cell

page_contents += "<th>"		# Add a cell to the row
page_contents += "Style"
page_contents += "</th>"	# Close cell

page_contents += "<th>"		# Add a cell to the row
page_contents += "ABV"
page_contents += "</th>"	# Close cell


page_contents += "</tr>"	# Close the table row

for beer in beers:
	page_contents += "<tr>"		# Add a row to the table
	page_contents += "<td>"		# Add a cell to the row
	page_contents += beer["product"]
	page_contents += "</td>"	# Close cell

	page_contents += "<td>"		# Add a cell to the row
	page_contents += beer["brewery"]
	page_contents += "</td>"	# Close cell

	page_contents += "<td>"		# Add a cell to the row
	page_contents += beer["style"]
	page_contents += "</td>"	# Close cell

	page_contents += "<td>"		# Add a cell to the row
	page_contents += beer["abv"]
	page_contents += "</td>"	# Close cell


	page_contents += "</tr>"	# Close the table row

page_contents += "</table>"

return page_contents