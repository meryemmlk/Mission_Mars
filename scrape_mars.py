# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import time

def init_browser(): 
# Use splinter to start up a Chrome driver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_nasa_news():
    news = {}
    url =  'https://mars.nasa.gov/news'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    # result = soup.find('li', class_='slide')
    result = soup.find('div', class_='slide')
    # Extract the most recent news' title and content
    # news_title = result.find('li', class_="content_title").find('a').text
    news_title = result.find('div', class_="content_title").find('a').text.strip()
    # news_p = result.find('li', class_="article_teaser_body").text
    news_p = result.a.text.strip()
    news["news_title"] = news_title
    news["news_p"] = news_p
    return news

def scrape_featured_image():
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    base_url ="https://www.jpl.nasa.gov"
    
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    article = soup.find("article")

    featured_img_url = base_url + article.a['data-fancybox-href']
    return featured_img_url 

def scrape_latest_twitt():
    url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    
    mars_weather = soup.find_all("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")[0].text
    return mars_weather

def scrape_mars_facts():
    url = 'http://space-facts.com/mars/'
    # Use Panda's `read_html` to parse the url
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['description', 'value']
    df.set_index('description', inplace=True)
    return df.to_html()

def scrape_hemispheres():
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url)
    soup = bs(response.text, 'lxml')

    hemispheres = []
    results = soup.find_all("div", class_="description")

    for result in results:
        hemispheres.append(result.h3.text)

    # hemispheres = ['Cerberus', 'Schiaparelli', 'Syrtis Major', 'Valles Marineris']
    return hemispheres

def scrape_hemisphere_info():
    hemispheres = scrape_hemispheres()
    hemisphere_info = []
    
    browser = init_browser()
    
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
        
    for hemi in hemispheres:
        #  Hemisphere
        browser.click_link_by_partial_text(f'{hemi}')

        # create HTML object, Parse HTML with Beautiful Soup
        html = browser.html
        soup = bs(html, 'html.parser')
        # Initialize the dict
        hemi_dict = {}
        # Scrape the incomplete URL
        inc_url = soup.find('img', class_='wide-image')['src']
        # Construct the complete URL
        img_url = 'https://astrogeology.usgs.gov' + inc_url
        # Store the data in a dictionary then add that dictionary to the tracking list
        hemi_dict["title"] = f'{hemi}'
        hemi_dict["img_url"] = img_url
        hemisphere_info.append(hemi_dict)
        
        # Return to the original page
        browser.click_link_by_partial_text('Back')
        
    browser.quit()
    return hemisphere_info


def scrape():
    mars_facts = {}
    mars_facts["news_title"] = scrape_nasa_news()["news_title"]
    mars_facts["news_p"] = scrape_nasa_news()["news_p"]
    mars_facts["featured_image_url"] = scrape_featured_image()
    mars_facts["mars_weather"] = scrape_latest_twitt()
    mars_facts["mars_facts_table"] = scrape_mars_facts()
    mars_facts["hemisphere_info"] = scrape_hemisphere_info()
    # Return the dictionary
    return mars_facts