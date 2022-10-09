# ecommerce-webscraper-bs4

# Description
The web scraper is built with beautifulsoup4, it scrapes json data for every item of every category from homedepot. The data collected is saved to a json file. Rotating user agents, reusable request and mutiple threads were inplemented to increase the speed, to fully utilize threads and minimize scraping speed, extra proxy service will be required.

# Sample output
```
[
  {
    "name": "High Tech Pet Products WA-1, Medium Wall Tunnel for Door and Wall Installations",
    "price": "32.99",
    "description": "Make the installation of your power pet door quick and easy with the High Tech Pet Products WA-1 Medium Wall Adapter for the PX-1 Power Pet Door. Designed to give you professional results in under two hours, this adapter eliminates the need for difficult framing of the hole that you cut into your wall. One end fits snugly into the back of the pet door, while the other end telescopes into the outside frame that comes with the pet door. All you have to do is cut the hole in your wall, mount the power pet door, and then slide in the adapter. Then mount it from the outside, and the installation is complete!",
    "image": "https://images.homedepot.ca/productimages/p_1001535758.jpg?product-images=l",
    "sku": "1001535758"
  },
  {
    "name": "Petsafe Microchip Cat Door by Petsafe",
    "price": "204",
    "description": "Give your cat a key to your home! The PetSafe Microchip Cat Door reads your cats unique 15-digit microchip ID and allows access to the programmed pet while restricting the entry of unwanted animals (like those clever raccoons). This cat door programs up to 40 pets, so its great for multi-pet households! Simply program your pets microchip to the door with the press of a button. The manual 4-way lock allows you to control your cats access, allowing you to lock it at night to keep your kitty safe inside; set to Locked, Unlocked, Enter Only or Exit Only. This door is powered by 4 AA Alkaline batteries and will signal when its time to change batteries. PetSafe brand is here to help you and your pet live happy together.",
    "image": "https://images.homedepot.ca/productimages/p_1001624995.jpg?product-images=l",
    "sku": "1001624995"
  },
  {
    "name": "Petsafe Cat Door , 4-Way Locking - Big Cat - White",
    "price": "54.67",
    "description": "Give your favorite felines the ability to come and go as they please. This cat door is generously sized for large cats or even small dogs up to 25 pounds. The 4-Way lock allows you to choose from four access options to control your pets access in and out of your home: open, locked, in-only or out-only. The open option allows entry or exit, the locked option does not allow entry or exit, the in-only option allows entry but no exit and the out-only option allows exit but no entry.",
    "image": "https://images.homedepot.ca/productimages/p_1001624993_alt_PPA00-11326_PT06.jpg?product-images=l",
    "sku": "1001624993"
  }
]
 
```

# Stack
- [Python3](https://www.python.org/downloads)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4)
- [requests](https://pypi.org/project/requests)
- [selenium4](https://pypi.org/project/selenium/)

# Getting started

```
python3 [filename.py]
```
