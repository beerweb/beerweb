# This is a simple, hard coded list of beer objects that we will pull from
beers = [
	{
		"brewery": "Angry Orchard (Boston Brewing)",
		"product": "Crisp Apple",
		"style": "Cider",
		"abv": "5.00",
		"price": "4.00"
	},
	{
		"brewery": "Guinness Ltd",
		"product": "Smithwick's Irish Ale",
		"style": "Irish Red Ale",
		"abv": "4.50",
		"price": "4.50"
	},
	{
		"brewery": "Hoppin' Frog Brewery",
		"product": "Silk Porter",
		"style": "American Porter",
		"abv": "6.20",
		"price": "5.50"
	},
	{
		"brewery": "Magic Hat",
		"product": "Magic Hat #9",
		"style": "Fruit Beer",
		"abv": "5.10",
		"price": "4.00"
	},
	{
		"brewery": "Penn Brewery",
		"product": "Oktoberfest",
		"style": "Oktoberfest",
		"abv": "5.60",
		"price": "4.50"
	},
	{
		"brewery": "Rivertowne",
		"product": "Maxwell's Scottish Ale",
		"style": "Scottish Ale",
		"abv": "5.10",
		"price": "4.50"
	},
	{
		"brewery": "Victory",
		"product": "Braumeister Pils",
		"style": "Pilsner",
		"abv": "5.50",
		"price": "3.50"
	},
	{
		"brewery": "Weihenstephaner",
		"product": "Vitus",
		"style": "Weizenbock",
		"abv": "7.70",
		"price": "7.00"
	},
	{
		"brewery": "Anchor Brewing",
		"product": "Anchor Humming Ale",
		"style": "American Pale Ale",
		"abv": "5.90",
		"price": "4.50"
	},
	{
		"brewery": "Ayinger",
		"product": "Brau-Weisse",
		"style": "Hefeweizen",
		"abv": "5.10",
		"price": "7.50"
	},
	{
		"brewery": "Ayinger",
		"product": "Oktober Fest-Marzen",
		"style": "Marzen / Oktoberfest",
		"abv": "5.80",
		"price": "5.00"
	},
	{
		"brewery": "Goose Island Beer Company",
		"product": "Bourbon Country Brand Stout",
		"style": "Imperial Stout",
		"abv": "14.20",
		"price": "7.50"
	},
	{
		"brewery": "Great Lakes",
		"product": "Burning River Pale Ale",
		"style": "Pale Ale",
		"abv": "6.00",
		"price": "6.50"
	},
	{
		"brewery": "Maui Brewing",
		"product": "CoCoNut Porter",
		"style": "American Porter",
		"abv": "6.00",
		"price": "7.50"
	},
	{
		"brewery": "Mike's",
		"product": "Boddingtons Brew",
		"style": "Bitter",
		"abv": "4.70",
		"price": "8.00"
	},
	{
		"brewery": "North Country Brewing",
		"product": "Station 33 Firehouse Red",
		"style": "Irish Red Ale",
		"abv": "5.50",
		"price": "7.00"
	},
	{
		"brewery": "Unibroue",
		"product": "La Fin Du Monde",
		"style": "Tripel",
		"abv": "9.00",
		"price": "5.00"
	},
	{
		"brewery": "Ayinger",
		"product": "Celebrator",
		"style": "Doppelbock",
		"abv": "6.70",
		"price": "5.50"
	},
	{
		"brewery": "Brooklyn Brewery",
		"product": "Winter Ale",
		"style": "Scottish Ale",
		"abv": "6.10",
		"price": "5.00"
	},
	{
		"brewery": "Brooklyn Brewery",
		"product": "Lager",
		"style": "American Amber",
		"abv": "5.20",
		"price": "5.00"
	},
	{
		"brewery": "Cigar City",
		"product": "Maduro Oatmeal Brown Ale",
		"style": "English Brown Ale",
		"abv": "5.50",
		"price": "6.00"
	},
	{
		"brewery": "Firestone Walker",
		"product": "Parabola",
		"style": "Russian Imperial Stout",
		"abv": "13.00",
		"price": "5.00"
	},
	{
		"brewery": "Great Lakes",
		"product": "Conways Irish Ale",
		"style": "Irish Red Ale",
		"abv": "6.50",
		"price": "4.00"
	},
	{
		"brewery": "Harpoon",
		"product": "UFO Hefeweizen",
		"style": "American Pale Wheat",
		"abv": "4.80",
		"price": "3.50"
	},
	{
		"brewery": "Warsteiner Brauerei",
		"product": "Warsteiner Premium Verum",
		"style": "German Pilsener",
		"abv": "4.80",
		"price": "4.00"
	},
	{
		"brewery": "Bell's",
		"product": "Oberon",
		"style": "American Pale Wheat Ale",
		"abv": "5.80",
		"price": "4.50"
	},
	{
		"brewery": "Carlsberg-Tetley Brewing",
		"product": "Tetley's English Ale",
		"style": "English Pale Ale",
		"abv": "3.60",
		"price": "8.00"
	},
	{
		"brewery": "Flying Dog",
		"product": "Double Dog Double Pale Ale (Nitro)",
		"style": "American Strong Ale",
		"abv": "11.50",
		"price": "8.00"
	},
	{
		"brewery": "Flying Dog",
		"product": "Dogtoberfest",
		"style": "Oktoberfest",
		"abv": "5.80",
		"price": "9.50"
	},
	{
		"brewery": "Great Lakes",
		"product": "Dortmunder Gold",
		"style": "Dortmunder Lager",
		"abv": "5.80",
		"price": "3.50"
	},
	{
		"brewery": "Leffe",
		"product": "Brune",
		"style": "Belgian Dark Ale",
		"abv": "6.50",
		"price": "8.00"
	},
	{
		"brewery": "New Belgium Brewing",
		"product": "Fat Tire Amber",
		"style": "Amber Ale",
		"abv": "5.20",
		"price": "6.50"
	},
	{
		"brewery": "Rust Belt",
		"product": "McPoyle's Milk Stout",
		"style": "Sweet Stout",
		"abv": "7.50",
		"price": "6.00"
	},
	{
		"brewery": "Straub Brewery",
		"product": "American Amber (Special Dark)",
		"style": "American Amber",
		"abv": "4.10",
		"price": "3.50"
	},
	{
		"brewery": "Voodoo Brewery",
		"product": "Cowbell Imperial Oatmeal Milk Stout",
		"style": "Milk / Sweet Stout",
		"abv": "8.50",
		"price": "4.00"
	},
	{
		"brewery": "Anheuser-Busch",
		"product": "Shock Top",
		"style": "Belgian White",
		"abv": "5.20",
		"price": "3.00"
	},
	{
		"brewery": "DuClaw",
		"product": "Sweet Baby Jesus Chocolate Peanut Butter Porter",
		"style": "American Porter",
		"abv": "6.50",
		"price": "4.00"
	},
	{
		"brewery": "East End Brewery",
		"product": "Monkey Boy",
		"style": "Hefeweizen",
		"abv": "4.80",
		"price": "9.00"
	},
	{
		"brewery": "Rivertowne",
		"product": "Hala Kahiki Pineapple",
		"style": "Fruit Beer",
		"abv": "4.80",
		"price": "8.50"
	},
	{
		"brewery": "Spaten-Franziskaner-Brau",
		"product": "Spaten Munchner Hell (Premium Lager)",
		"style": "Munich Helles Lager",
		"abv": "5.20",
		"price": "8.00"
	},
	{
		"brewery": "Spring House",
		"product": "Big Gruesome Peanut Butter Chocolate Stout",
		"style": "American Imperial Stout",
		"abv": "8.00",
		"price": "7.00"
	},
	{
		"brewery": "Straub Brewery",
		"product": "American Light Lager",
		"style": "Pale Lager",
		"abv": "3.16",
		"price": "3.00"
	},
	{
		"brewery": "Boulder",
		"product": "Shake Chocolate Porter",
		"style": "American Porter",
		"abv": "5.90",
		"price": "6.00"
	},
	{
		"brewery": "Brooklyn Brewery",
		"product": "Brown Ale",
		"style": "American Brown Ale",
		"abv": "5.60",
		"price": "4.00"
	},
	{
		"brewery": "Budejovicky Budvar",
		"product": "Czechvar / Budvar",
		"style": "Czech Pilsener",
		"abv": "5.00",
		"price": "8.00"
	},
	{
		"brewery": "Clown Shoes",
		"product": "Brown Angel",
		"style": "American Double Brown Ale",
		"abv": "7.00",
		"price": "6.00"
	},
	{
		"brewery": "Duvel Moortgat",
		"product": "Maredsous 8 (Brune)",
		"style": "Dubbel",
		"abv": "8.00",
		"price": "5.00"
	},
	{
		"brewery": "Goose Island Beer Company",
		"product": "312 Urban Wheat",
		"style": "American Pale Wheat Ale",
		"abv": "4.20",
		"price": "6.00"
	},
	{
		"brewery": "Guinness Ltd",
		"product": "Guinness Draught",
		"style": "Irish Dry Stout",
		"abv": "4.20",
		"price": "4.50"
	},
	{
		"brewery": "Diageo",
		"product": "Smithwick's Ale",
		"style": "Irish Ale",
		"abv": "5.00",
		"price": "7.00"
	},
	{
		"brewery": "East End Brewery",
		"product": "Fat Gary Nut Brown Ale",
		"style": "English Brown Ale",
		"abv": "3.60",
		"price": "4.00"
	},
	{
		"brewery": "Hoegaarden",
		"product": "Hoegaarden",
		"style": "Belgian White",
		"abv": "4.90",
		"price": "4.00"
	},
	{
		"brewery": "Kronenbourg",
		"product": "Kronenbourg 1664",
		"style": "Pale Lager",
		"abv": "5.50",
		"price": "8.50"
	},
	{
		"brewery": "Miller Coors",
		"product": "Miller Lite",
		"style": "Pale Lager",
		"abv": "4.20",
		"price": "3.00"
	},
	{
		"brewery": "Rogue",
		"product": "Hazelnut Brown Nectar Ale",
		"style": "American Brown Ale",
		"abv": "6.20",
		"price": "6.00"
	},
	{
		"brewery": "Rolling Rock",
		"product": "Rock Green Light",
		"style": "Pale Lager",
		"abv": "3.70",
		"price": "4.50"
	},
	{
		"brewery": "Rolling Rock",
		"product": "Extra Pale",
		"style": "American Lager",
		"abv": "4.60",
		"price": "8.50"
	},
	{
		"brewery": "Samuel Adams",
		"product": "Noble Pils",
		"style": "Czech Pilsner",
		"abv": "4.90",
		"price": "9.50"
	},
	{
		"brewery": "Stella Artois",
		"product": "Stella Artois",
		"style": "Euro Pale Lager",
		"abv": "5.00",
		"price": "6.00"
	},
	{
		"brewery": "SweetWater Brewing Company",
		"product": "Georgia Brown",
		"style": "English Brown Ale",
		"abv": "5.10",
		"price": "7.50"
	},
	{
		"brewery": "Bass",
		"product": "Bass Ale",
		"style": "English Pale Ale",
		"abv": "5.20",
		"price": "5.50"
	},
	{
		"brewery": "Bear Republic",
		"product": "Racer 5",
		"style": "American IPA",
		"abv": "7.00",
		"price": "8.00"
	},
	{
		"brewery": "East End Brewery",
		"product": "Oatmeal Stout",
		"style": "Oatmeal Stout",
		"abv": "8.20",
		"price": "8.00"
	},
	{
		"brewery": "Founders",
		"product": "Oatmeal Stout (Nitro)",
		"style": "Oatmeal Stout",
		"abv": "4.50",
		"price": "8.50"
	},
	{
		"brewery": "Guinness Ltd",
		"product": "Harp Lager",
		"style": "Euro Pale Lager",
		"abv": "5.00",
		"price": "5.00"
	},
	{
		"brewery": "North Coast Brewing",
		"product": "Old Stock Ale",
		"style": "Old Ale",
		"abv": "11.90",
		"price": "8.50"
	},
	{
		"brewery": "Samuel Adams",
		"product": "Oktoberfest",
		"style": "Oktoberfest",
		"abv": "5.30",
		"price": "4.50"
	},
	{
		"brewery": "Sierra Nevada",
		"product": "Pale Ale",
		"style": "American Pale Ale",
		"abv": "5.00",
		"price": "5.50"
	},
	{
		"brewery": "Sly Fox",
		"product": "Helles Golden Lager",
		"style": "American Lager",
		"abv": "4.90",
		"price": "6.50"
	},
	{
		"brewery": "Southern Tier",
		"product": "2X Stout (Nitro)",
		"style": "Sweet Stout",
		"abv": "7.50",
		"price": "7.50"
	},
	{
		"brewery": "Alltech",
		"product": "Kentucky Bourbon Ale",
		"style": "English Strong Ale",
		"abv": "8.20",
		"price": "6.50"
	},
	{
		"brewery": "Erdinger Weissbrau",
		"product": "Erdinger Weissbier Dunkel",
		"style": "Dunkelweizen",
		"abv": "5.30",
		"price": "8.00"
	},
	{
		"brewery": "Fat Head's",
		"product": "Bumble Berry Honey Blueberry Ale",
		"style": "Fruit",
		"abv": "5.30",
		"price": "7.50"
	},
	{
		"brewery": "Fuller Smith & Turner PLC",
		"product": "Fuller's London Porter",
		"style": "English Porter",
		"abv": "5.40",
		"price": "6.00"
	},
	{
		"brewery": "Penn Brewery",
		"product": "St. Nikolaus Bock Reserve",
		"style": "Doppelbock",
		"abv": "8.50",
		"price": "7.50"
	},
	{
		"brewery": "Rust Belt",
		"product": "Rusted River Irish Red",
		"style": "Irish Red Ale",
		"abv": "5.50",
		"price": "8.50"
	},
	{
		"brewery": "Church Brew Works",
		"product": "Arand The Red / Absolution Ale",
		"style": "Irish Ale",
		"abv": "4.50",
		"price": "3.50"
	},
	{
		"brewery": "Coors",
		"product": "Coors Light",
		"style": "Pale Lager",
		"abv": "4.20",
		"price": "9.00"
	},
	{
		"brewery": "Helltown",
		"product": "Mischievous Brown Ale",
		"style": "English Brown Ale",
		"abv": "5.50",
		"price": "5.50"
	},
	{
		"brewery": "North Coast Brewing",
		"product": "Scrimshaw",
		"style": "German Pilsner",
		"abv": "4.40",
		"price": "5.50"
	},
	{
		"brewery": "Penn Brewery",
		"product": "Penn Pilsner",
		"style": "Pilsner / Vienna Lager",
		"abv": "4.00",
		"price": "6.50"
	},
	{
		"brewery": "Pivovary Staropramen",
		"product": "Staropramen Lager",
		"style": "Czech Pilsener",
		"abv": "5.00",
		"price": "4.50"
	},
	{
		"brewery": "Wells & Young",
		"product": "Double Chocolate Stout (Nitro)",
		"style": "Stout",
		"abv": "5.20",
		"price": "4.50"
	},
	{
		"brewery": "Labatt",
		"product": "Blue Light",
		"style": "Lager",
		"abv": "4.00",
		"price": "3.00"
	},
	{
		"brewery": "Leffe",
		"product": "Blonde",
		"style": "Belgian Pale Ale",
		"abv": "6.60",
		"price": "4.00"
	},
	{
		"brewery": "Rust Belt",
		"product": "Blast Furnace Blonde",
		"style": "Blonde Ale",
		"abv": "5.50",
		"price": "7.00"
	},
	{
		"brewery": "Stone Brewing Co",
		"product": "Stone IPA",
		"style": "American IPA",
		"abv": "6.90",
		"price": "6.00"
	},
	{
		"brewery": "Yuengling",
		"product": "Traditional Lager",
		"style": "American Amber",
		"abv": "4.40",
		"price": "7.00"
	},
	{
		"brewery": "Allagash Brewing Company",
		"product": "White",
		"style": "Belgian Style Wheat",
		"abv": "5.00",
		"price": "5.50"
	},
	{
		"brewery": "Fat Head's",
		"product": "Head Hunter",
		"style": "American IPA",
		"abv": "7.50",
		"price": "5.00"
	},
	{
		"brewery": "Lindeman's",
		"product": "Pomme",
		"style": "Apple Lambic",
		"abv": "3.50",
		"price": "6.50"
	},
	{
		"brewery": "McKenzie's Hard Cider",
		"product": "Lemon Cider",
		"style": "Cider",
		"abv": "5.00",
		"price": "9.50"
	},
	{
		"brewery": "McKenzie's Hard Cider",
		"product": "Black Cherry",
		"style": "Cider",
		"abv": "5.00",
		"price": "3.50"
	},
	{
		"brewery": "Penn Brewery",
		"product": "Dark",
		"style": "Dunkel",
		"abv": "5.00",
		"price": "7.00"
	},
	{
		"brewery": "Weltenburger",
		"product": "Asam Bock",
		"style": "Doppelbock",
		"abv": "6.90",
		"price": "6.00"
	}
]