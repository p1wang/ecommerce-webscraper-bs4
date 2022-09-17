# ecommerce-webscraper-bs4

# Description
The web scraper is built with beautifulsoup4, it scrapes json data for every item of every category from homedepot. The data collected is saved to a json file. Rotating user agents, reusable request and mutiple threads were inplemented to increase the speed, to fully utilize threads and minimize scraping speed, extra proxy service will be required.

# Sample output
```
{
    "@context": "https://schema.org/",
    "@type": "Product",
    "name": "3/8-inch Drive Combination Deep Impact Socket Set with Ratchet (23-Piece)",
    "url": "https://www.homedepot.ca/product/dewalt-3-8-inch-drive-combination-deep-impact-socket-set-with-ratchet-23-piece-/1001104068",
    "image": "https://images.homedepot.ca/productimages/p_1001104068.jpg",
    "description": "DEWALT 3/8-inch Drive Combination Deep Impact Socket Set with Ratchet (23-Piece)",
    "sku": "1001104068",
    "aggregateRating": {
      "@type": "AggregateRating",
      "ratingValue": 4.7131,
      "reviewCount": 237,
      "bestRating": 5,
      "worstRating": 1
    },
    "brand": {
      "@type": "Thing",
      "name": "DEWALT"
    },
    "offers": {
      "@type": "Offer",
      "price": 118,
      "priceCurrency": "CAD"
    }
  }
```

# Stack
- [Python3](https://www.python.org/downloads)
-  [beautifulsoup4](https://pypi.org/project/beautifulsoup4)
- [requests](https://pypi.org/project/requests)

# Getting started

```
python3 [filename.py]
```
