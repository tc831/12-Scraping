# Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager


# Define function to choose the executable path
def init_browser():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless = False, user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36")

# Set variable for multiple use string
parser = "html.parser"

# Full Scrape function
def scrape():

    # Connect to Mars News Site
    browser = init_browser()
    

    """ NASA Mars News """
    # Visit to Mars News Site
    mars_news_url = "http://redplanetscience.com"
    browser.visit(mars_news_url)

    # HTML Object
    html = browser.html

    # Parse HTML with Beautiful Soup
    news_soup = bs(html, parser)    

    # Retrieve the latest article's title
    news_title = news_soup.find("div", class_ = "content_title")
    news_title = news_title.text.strip()
    print(news_title)

    # Retrieve the latest article's paragraph
    news_paragraph = news_soup.find("div", class_ = "article_teaser_body")
    news_paragraph = news_paragraph.text.strip()
    print(news_paragraph)


    """ JPL Mars Space Images - Featured Image """
    # Connection to JPL Mars Space Images - Featured Image
    mars_featured_image_url = "http://spaceimages-mars.com/"
    browser.visit(mars_featured_image_url)

    # HTML Object
    html = browser.html

    # Parse HTML with Beautiful Soup
    image_soup = bs(html, parser)

    # Assign the full url string to a variable called "featured_image_url"
    featured_image = image_soup.find("img", class_ = "headerimage fade-in")
    featured_image_url = mars_featured_image_url + featured_image["src"]
    print(featured_image_url)


    """ Mars Facts """
    # URL for Mars Facts
    mars_facts_url = "http://space-facts.com/mars/"

    # Use Pandas to convert the data to a HTML table string
    mars_facts = pd.read_html(mars_facts_url)

    # Save as DataFrame
    mars_facts_df = pd.DataFrame(mars_facts[1])

    #  Save DataFrame to html
    mars_facts = mars_facts_df.to_html(header = True, index = True)


    """ Mars Hemispheres """
    # Visit the url for Mars Hemisphere
    mars_hemispheres_url = "http://marshemispheres.com/"
    browser.visit(mars_hemispheres_url)

    # HTML Object
    html = browser.html

    # Parse HTML with Beautiful Soup
    hemispheres_soup = bs(html, parser)

    # Each link is located in "div" tag, class "description"
    # Find all elements and store in variable
    hems_url = hemispheres_soup.find_all("div", class_ = "description")

    # Create empty list for each Hemisphere URL
    hemis_url = []

    # Append all URL
    for hem in hems_url:
        hem_url = hem.find("a")["href"]
        hemis_url.append(hem_url)

    # Create list of dictionaries called hemisphere_image_urls
    hemisphere_image_urls = []

    # Iterate through all URLs saved in hemis_url
    for hemi in hemis_url:
        mars_hem_url = mars_hemispheres_url + hemi
        print(mars_hem_url)
        
        # Visit to Hemisphere
        browser.visit(mars_hem_url)
        
        # HTML Object
        html = browser.html

        # Parse HTML with Beautiful Soup
        hemi_soup = bs(html, parser)

        # Locate each title and save to raw_title, to be cleaned
        raw_title = hemi_soup.find("h2", class_ = "title").text
        
        # Remove " Enhanced" tag text from each "title" via split on " Enhanced"
        title = raw_title.split(" Enhanced")[0]
        
        # Find all full-resolution image for all Hemisphere URLs
        img_url = hemi_soup.find("img", class_ = "wide-image")["src"]
        
        # Append title and img_url to "hemisphere_image_url"
        hemisphere_image_urls.append({"title": title, "img_url": mars_hemispheres_url + img_url})

    # Exit Browser
    browser.quit()

    print(hemisphere_image_urls)

    
    """ Mars Data Dictionary - MongoDB """
    # Create dictionary for all Mars Data
    mars_data = {}

    # Append news_title and news_paragraph to mars_data
    mars_data["news_title"] = news_title
    mars_data["news_paragraph"] = news_paragraph

    # Append featured_image_url to mars_data
    mars_data["featured_image_url"] = featured_image_url

    # Append mars_facts to mars_data
    mars_data["mars_facts"] = mars_facts

    # Append hemisphere_image_urls to mars_data
    mars_data["hemisphere_image_urls"] = hemisphere_image_urls

    return mars_data