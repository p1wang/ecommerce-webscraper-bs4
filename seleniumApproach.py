from bs4 import BeautifulSoup
import requests
import random
from random import randint
from time import sleep
import time
import json

from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.webdriver import Chrome, ChromeOptions
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType


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

# ---------------------------------------- Functions ---------------------------------------
def getDriver():
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument(f"user-agent={user_agent}")
    # options.add_argument("proxy-server=24.109.252.48:3128")
    driver = Chrome(service=Service("/usr/local/bin/chromedriver"), options=options)

    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    return driver


def getSoup(url):
    try:
        driver = getDriver()
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "lxml")
        driver.quit()
        return soup
    except Exception as err:
        print(f"Something went wrong getting soup {url}, ERROR is {err}.")


def getItemDetails(itemUrl):
    sleep(randint(50, 200) / 1000)
    print(f"Getting itemDetails for: {itemUrl}")
    soup = getSoup(itemUrl)

    try:
        name = (
            soup.find(
                "span", class_="hdca-product__description-title-manufacturer"
            ).text
            + soup.find(
                "span", class_="hdca-product__description-title-product-name"
            ).text
        )
        price = (
            soup.find("span", {"itemprop": "price"}).text
            if soup.find("span", {"itemprop": "price"})
            else "n/a"
        )
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
        return details
    except:
        print(f"Error getting details for: {itemUrl}.")


def getAllCategoryUrls():
    print("Getting allCategoryUrls")
    soup = getSoup(allDepartmentsUrl)

    try:
        categoryTags = soup.find_all("a", href=True)
        categoryUrls = [
            categoryTag["href"]
            for categoryTag in categoryTags
            if "https://www.homedepot.ca/en/home/categories/" in categoryTag["href"]
            and str(categoryTag["href"]).count("/") == 8
        ]
        uniqueCategoryUrls = list(set(categoryUrls))
        return uniqueCategoryUrls
    except:
        print("Error getting all category urls.")


def getItemsUrlsInCategory(categoryUrl):
    sleep(randint(50, 200) / 1000)
    print("Getting itemUrlsOnPage")
    print(categoryUrl)
    soup = getSoup(categoryUrl)
    totalPageNumber = 1

    try:
        totalItemsOnPage = int(
            soup.find("plp-srp-pagination", class_="ng-star-inserted")
            .find("p", class_="acl-body")
            .text.split(" ")[-3]
        )
        print(totalItemsOnPage)

        totalPageNumber = totalItemsOnPage // 40 + 1
        print(totalPageNumber)

        itemsUrlsInCategory = []

        for pageNumber in range(totalPageNumber):
            currentPageUrl = categoryUrl + f"?page={pageNumber + 1}"
            print(currentPageUrl)
            soup = getSoup(currentPageUrl)

            try:
                urls = [
                    baseUrl + itemLinkElement["href"]
                    for itemLinkElement in soup.find_all(
                        "a", class_="acl-product-card__title-link ng-star-inserted"
                    )
                ]

                uniqueUrls = list(set(urls))

                print(f"Current page item count: {len(uniqueUrls)}")

                for url in uniqueUrls:
                    itemsUrlsInCategory.append(url)

            except Exception as err:
                print(f"Error getting urls on current category page. {err}")

        return itemsUrlsInCategory
    except:
        print("Error finding total page number.")


def main():
    # ----------------------------------------- Main -------------------------------------------------
    #  TIMER START
    start = time.time()

    allItemsDetails = []
    allItemUrls = []

    # --------------------------- get and write all category urls -------------------------------------
    allCategoryUrls = getAllCategoryUrls()

    f = open("output/allCategoryUrls.txt", "w")
    f.write(str(allCategoryUrls))

    # --------------------------- THREADS get and write all item details with submit ------------------
    with ThreadPoolExecutor(max_workers=6) as executor:
        fs = (
            executor.submit(getItemsUrlsInCategory, url) for url in allCategoryUrls[0:5]
        )
        for f in as_completed(fs):
            if f.result():
                allItemUrls += f.result()

    f = open("output/allItemUrls.txt", "w")
    f.write(str(allItemUrls))

    # -----------------------------------------------------------------------------------------------------
    with ThreadPoolExecutor(max_workers=6) as executor:
        fs = (executor.submit(getItemDetails, url) for url in allItemUrls)
        for f in as_completed(fs):
            if f.result():
                allItemsDetails.append(f.result())

    f = open("output/allItemsDetails.json", "w")
    f.write(json.dumps(list(filter(None, allItemsDetails)), indent=2))

    # -----------------------------------------------------------------------------------------------------

    f.close()

    # TIMER END
    end = time.time()
    print(end - start)


if __name__ == "__main__":
    main()
