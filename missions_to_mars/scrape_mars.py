from splinter import Browser
from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import requests
from sqlalchemy import create_engine

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    compiled_dict = {}

    # Mars News URL of page to be scraped
    url_1 = "https://mars.nasa.gov/news/"
    browser.visit(url_1)
    html = browser.html
    soup = bs(html, 'html.parser')
    # Retrieve the latest news title and paragraph
    news_title = soup.find_all("div", class_="content_title")[1].get_text()
    news_p = soup.find("div", class_="article_teaser_body").get_text()

    # Mars Image to be scraped
    url_2 = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url_2)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    html = browser.html
    soup = bs(html, "html.parser")
    relative_image_path = soup.find('img', class_="fancybox-image")["src"]
    url_image = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"
    featured_image_url = url_image + relative_image_path

    # Mars facts to be scraped, converted into html table
    url_3 = "https://space-facts.com/mars/"
    fact_data = pd.read_html(url_3)
    df = fact_data[0]
    df.columns = ["Facts", "Value"]
    html_table = df.to_html()
    html_table.replace('\n', '')
    
    # Mars hemisphere name and image to be scraped
    # url = "https://astrogeology.usgs.gov"
    # mars_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    # browser.visit(mars_url)
    # html = browser.html
    # soup = bs(html, "html.parser")
    # # Mars hemispheres products data
    # products = soup.find('div', class_='collapsible results')
    # items = products.find_all('div', class_='item')
    # images = []

    # for item in items:
    #     find = item.find('div', class_="description")
    #     title = find.h3.text
    #     link = find.a["href"]
    #     browser.visit(url + link)
    #     html = browser.html
    #     soup = bs(html, "html.parser")
    #     image_find = soup.find('div', class_='downloads')
    #     image = image_find.find('li').a['href']

    #     image_dict = {}
    #     image_dict['title'] = title
    #     image_dict['img_url'] = image

    #     images.append(image_dict)

    compiled_dict = {
    "news_title": news_title,
    "news_p": news_p,
    "featured_image_url": featured_image_url,
    "fact_table": str(html_table),
    # "hemisphere_images_urls": images
    }

    return compiled_dict

print(scrape_info())
