############################ Description ##############################
# - Parse DOM HTML using lxml’s HTML parser
# - Scrapes all category urls
# - Loop through every page of every category and extract product
#   json data in the HTML using lxml’s HTML parser
# - Write json data to a file
#######################################################################

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
    print("Getting all category urls")
    soup = getSoup(allDepartmentsUrl)
    categoryTags = soup.find_all("a", href=True)
    categoryUrls = [
        categoryTag["href"]
        for categoryTag in categoryTags
        if "https://www.homedepot.ca/en/home/categories/" in categoryTag["href"]
        and str(categoryTag["href"]).count("/") == 8
    ]
    distinctCategoryUrls = unique(categoryUrls)
    return distinctCategoryUrls


def getItemsDetailsInCategory(categoryUrl):
    sleep(randint(50, 200) / 1000)

    categoryName = categoryUrl.split("/")[-1].split(".")[0]
    print(f"Getting item details in category {categoryName}")
    soup = getSoup(categoryUrl)
    totalPageNumber = 1

    totalPageNumberString = (
        soup.find("plp-srp-pagination", class_="ng-star-inserted")
        .find("p", class_="acl-body")
        .text.split(" ")[-3]
    )

    if totalPageNumberString:
        totalPageNumber = (
            int(totalPageNumberString) // 40
            if int(totalPageNumberString) // 40 >= 1
            else 1
        )
    else:
        print("No total page number found.")
        return

    print(f"Page total in category {categoryName}: {totalPageNumber}")

    for pageNumber in range(totalPageNumber):
        currentPageUrl = categoryUrl + f"?page={pageNumber + 1}"

        print(f"Scraping {currentPageUrl}")

        soup = getSoup(currentPageUrl)

        itemsDict = json.loads(soup.find("script", type="application/ld+json").text)[
            "mainEntity"
        ]["offers"]["itemOffered"]

        global allItemsDetails

        for item in itemsDict:
            allItemsDetails.append(item)

    return


# ----------------------------------------- Main -------------------------------------------------
#  TIMER START
start = time.time()

# --------------------------- get and write all category urls -------------------------------------
allCategoryUrls = getAllCategoryUrls()

# --------------------------- THREADS get and write all item urls ---------------------------------
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    executor.map(getItemsDetailsInCategory, allCategoryUrls)


f = open("output/allCategoryUrls.txt", "w")
f.write(str(allCategoryUrls))

f = open("output/allItemsDetails.json", "w")
f.write(json.dumps(allItemsDetails, indent=2))

f.close()

# TIMER END
end = time.time()
print(end - start)
