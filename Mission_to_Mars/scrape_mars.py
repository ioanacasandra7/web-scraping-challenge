
from splinter import Browser
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()
    # Create Mission to Mars dictionary 

    mars_data = {}
    # Visit visitcostarica.herokuapp.com
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    time.sleep(5)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the latest article
    article = soup.find('div', class_="list_text")

    # Get the news title
    news_title = article.find('div', class_="content_title").text  
    # Get the news paragraph
    news_p = article.find('div', class_="article_teaser_body").text 

    #Visit the url for JPL Featured Space Image
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)
    time.sleep(5)

    #Use splinter to navigate the site and find the image url 
    #for the current Featured Mars Image and assign the url string to a variable called featured_image_url
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    print(html)

    # Find the src for the sloth image
    image =soup.find('img', class_="thumb")["src"]
    #Get the complete url to the jpg
    featured_image_url="https://jpl.nasa.gov"+ image
    print(featured_image_url)

    #Go to the website to scrape information about mars
    url3 = "https://space-facts.com/mars/"
    browser.visit(url3)
    time.sleep(5)
    #Grab the data from the website and save it as a dataframe
    grab=pd.read_html(url3)
    mars_data=pd.DataFrame(grab[0])
    mars_data.columns=['Mars','Data']
    mars_table_df=mars_data.set_index("Mars")
    mars_table_html = mars_table_df.to_html(classes="mars_table_df")
    mars_table_html = mars_table_html.replace('\n',' ')

    #Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres.
    url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url5)
    time.sleep(5)
    # HTML Object
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []

    
    #Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres.
    url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url5)
    time.sleep(5)

    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []

    #   Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'
    # Loop through the items previously stored
    for i in items: 
        title = i.find('h3').text
        partial_img_url = i.find('a', class_='itemLink product-item')['href'] 
        browser.visit(hemispheres_main_url + partial_img_url)
        partial_img_html = browser.html
        soup = BeautifulSoup( partial_img_html, 'html.parser')
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    
    # Store data in a dictionary
    mars_data = {
    "News_Title": news_title,
    "News_Paragraph": news_p,
    "Featured_Image": featured_image_url,
    "Mars_Table": mars_table_html,
    "Hemisphere_Data": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
    
