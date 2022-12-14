############################ Description ##################################
# - Parse DOM HTML using lxml’s HTML parser
# - Scrapes all category urls
# - Scrapers all item urls of each page of each category
# - Loop through every item page and scrapes product details using itemprop
# - Write json data to a file
###########################################################################


from bs4 import BeautifulSoup
import concurrent.futures
import requests
import random
from random import randint
from time import sleep
import json
import time
import math

# ------------------------------------ list of user agents ---------------------------------
user_agent_list = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
]

# ------------------------------------ list of canada proxies ------------------------------
proxies = {}

# -------------------------------- randomize current user agent ----------------------------
for _ in user_agent_list:
    user_agent = random.choice(user_agent_list)
    headers = {"User-Agent": user_agent}

# --------------------------------- persist session ----------------------------------------
s = requests.Session()

# ---------------------------------------- Variables ---------------------------------------
baseUrl = "https://www.homedepot.ca"
allDepartmentsUrl = "https://www.homedepot.ca/en/home/all-departments.html"
allItemsDetails = []
allItemUrls = []
totalItems = int


# ---------------------------------------- Functions ---------------------------------------
def getSoup(url):
    data = s.get(url, headers=headers).content
    soup = BeautifulSoup(data, "lxml")
    return soup


def unique(inputList):
    listSet = set(inputList)
    uniqueList = list(listSet)
    return uniqueList


def getAllCategoryUrls():
    print("getting allCategoryUrls")
    soup = getSoup(allDepartmentsUrl)
    categoryTags = soup.find_all("a", href=True)
    categoryUrls = [
        categoryTag["href"]
        for categoryTag in categoryTags
        if "https://www.homedepot.ca/en/home/categories/" in categoryTag["href"]
        and str(categoryTag["href"]).count("/") == 8
    ]
    # distinctCategoryUrls = list(dict.fromkeys(categoryUrls))
    distinctCategoryUrls = unique(categoryUrls)
    return distinctCategoryUrls


def getItemsUrlsOnPage(categoryUrl):
    sleep(randint(50, 200) / 1000)
    print("getting itemUrlsOnPage")
    soup = getSoup(categoryUrl)
    totalPageNumber = 1

    totalPageNumberString = (
        soup.find("plp-srp-pagination", class_="ng-star-inserted")
        .find("p", class_="acl-body")
        .text.split(" ")[-3]
    )

    print(totalPageNumberString)

    if totalPageNumberString:
        totalPageNumber = int(totalPageNumberString) // 40
    else:
        print("No total page number found.")
        return

    if totalPageNumber < 0:
        totalPageNumber = 1

    print(totalPageNumber)

    for pageNumber in range(totalPageNumber):
        currentPageUrl = categoryUrl + f"?page={pageNumber + 1}"
        print(currentPageUrl)
        soup = getSoup(currentPageUrl)
        items = soup.find_all("a", href=True)

        urls = [baseUrl + item["href"] for item in items if "/product/" in item["href"]]
        print(f"All urls: {len(urls)}")
        # distinctUrls = list(dict.fromkeys(urls))
        distinctUrls = unique(urls)
        print(f"Distinct urls: {len(distinctUrls)}")
        for distinctUrl in distinctUrls:
            global allItemUrls
            allItemUrls.append(distinctUrl)
    return


def getItemDetails(itemUrl):
    sleep(randint(50, 200) / 1000)
    print("getting itemDetails")

    global allItemUrls

    soup = getSoup(itemUrl)

    try:
        name = (
            soup.find("div", {"itemprop": "Product"})
            .find("span", {"itemprop": "name"})
            .text
        )
        price = soup.find("span", {"itemprop": "price"}).text
        description = soup.find("span", {"itemprop": "description"}).text
        image = soup.find("img", {"itemprop": "image"})["src"]
        sku = soup.find("span", {"itemprop": "sku"}).text
        details = {
            "name": name,
            "price": price,
            "description": description,
            "image": image,
            "sku": sku,
        }
        global allItemsDetails
        allItemsDetails.append(details)
        return
    except:
        print("Something went wrong at getItemDetails")

def main():
    # ----------------------------------------- Main -------------------------------------------------
    #  TIMER START
    start = time.time()

    # --------------------------- get and write all category urls -------------------------------------
    allCategoryUrls = getAllCategoryUrls()

    # --------------------------- THREADS get and write all item urls ---------------------------------
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(getItemsUrlsOnPage, allCategoryUrls)
        # executor.map(getItemsUrlsOnPage, allCategoryUrls[2:3])

    # ---------------------------------- Update total items -------------------------------------------
    totalItems = len(allItemUrls)
    print(totalItems)

    # -------------------------- THREADS get all item details ----------------------------
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(getItemDetails, allItemUrls)
        # executor.map(getItemDetails, allItemUrls[:100])

    f = open("output/allCategoryUrls.txt", "w")
    f.write(str(allCategoryUrls))

    f = open("output/allItemUrls.txt", "w")
    f.write(str(allItemUrls))

    f = open("output/allItemsDetails.json", "w")
    f.write(json.dumps(allItemsDetails, indent=2))

    f.close()

    # TIMER END
    end = time.time()
    print(end - start)

if __name__ == "__main__":
    main()
