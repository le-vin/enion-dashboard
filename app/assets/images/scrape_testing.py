
import requests
import pandas as pd
import bs4
import boto3
from io import StringIO
import json

f = open("./credentials.json")
credentials = json.load(f)
access_key  = credentials["aws_access_key_id"]
secret_access_key = credentials["aws_secret_access_key"]

class EUStartups:
    def __init__(self):
        self.spanish_startups = 'https://www.eu-startups.com/directory/wpbdp_category/spanish-startups/'
        self.portuguese_startups = 'https://www.eu-startups.com/directory/wpbdp_category/portuguese-startups/'


    def get_dictionary(self):

        links = self.get_startup_links(self.spanish_startups)
        links += self.get_next_links(self.portuguese_startups)

        data = self.get_startup_data(links)

        name = data[0]
        city = data[1]
        description = data[2]
        keywords = data[3]
        funding = data[4]
        founded = data[5]
        website = data[6]

        startup_dict = {"comp_name": name,
                        "description": description,
                        "business_model": [None]*len(name),
                        "customer": [None]*len(name),
                        "keywords": keywords,
                        "stage": [None]*len(name),
                        "total_funding": funding,
                        "num_investors": [None]*len(name),
                        "date_founded": founded,
                        "location": city,
                        "employees": [None]*len(name),
                        "website": website
                    }
        
        return(startup_dict)


    def get_csv(self):
        startup_dict = self.get_dictionary()
        df = pd.DataFrame(startup_dict)
        
        return df

    
    def get_next_links(self, url):
        html = requests.get(url)
        data = bs4.BeautifulSoup(html.text, "html.parser")

        links_2 = []
        divs = data.find_all("div", {"class": "listing-title"})

        for div in divs:
            links_2.append(div.find('a').get("href"))
        
        try:
            next_button = data.find("span", {"class": "next"})
            next_link = next_button.find('a').get("href")
        
        except:
            next_link = None

        return(links_2)
    

    def get_startup_links(self, url):  
        links = []
        
        while (True):

            try:
                result = self.get_next_links(url)
                links_gathered = result[0]
                links = links + links_gathered
                url = result[1]

            except:
                break

        return links
    

    def get_startup_data(self, links):
        name_list = []
        city_list = []
        description_list = []
        keywords_list = []
        funding_list = []
        founded_list = []
        website_list = []
        
        for link in links:
        
            html = requests.get(link)
            data = bs4.BeautifulSoup(html.text, "html.parser")

            try:
                name = data.find("div", {"class": "wpbdp-field-display wpbdp-field wpbdp-field-value field-display field-value wpbdp-field-business_name wpbdp-field-title wpbdp-field-type-textfield wpbdp-field-association-title"}).find("div", {"class": "value"}).find(text=True)
                name_list.append(name)
            except:
                name_list.append("None") 

            try:
                description = data.find("div", {"class": "wpbdp-field-display wpbdp-field wpbdp-field-value field-display field-value wpbdp-field-business_description wpbdp-field-meta wpbdp-field-type-textarea wpbdp-field-association-meta"}).find("div", {"class": "value"}).find(text=True)
                description_list.append(description)
            except:
                description_list.append(None)
                

            try:
                city = data.find("div", {"class": "wpbdp-field-display wpbdp-field wpbdp-field-value field-display field-value wpbdp-field-based_in wpbdp-field-meta wpbdp-field-type-textfield wpbdp-field-association-meta"}).find("div", {"class": "value"}).find(text=True)
                city_list.append(city)
            except:
                city_list.append(None)
                

            try:
                keywords = data.find("div", {"class": "wpbdp-field-display wpbdp-field wpbdp-field-value field-display field-value wpbdp-field-tags wpbdp-field-meta wpbdp-field-type-textfield wpbdp-field-association-meta"}).find("div", {"class": "value"}).find(text=True).split(", ")
                keywords_list.append(keywords)
            except:
                keywords_list.append(None)
                

            try:
                funding = data.find("div", {"class": "wpbdp-field-display wpbdp-field wpbdp-field-value field-display field-value wpbdp-field-total_funding wpbdp-field-meta wpbdp-field-type-select wpbdp-field-association-meta"}).find("div", {"class": "value"}).find(text=True)
                funding_list.append(int(funding))
            except:
                funding_list.append(None)

            try:
                founded = data.find("div", {"class": "wpbdp-field-display wpbdp-field wpbdp-field-value field-display field-value wpbdp-field-founded wpbdp-field-meta wpbdp-field-type-select wpbdp-field-association-meta"}).find("div", {"class": "value"}).find(text=True)
                founded_list.append(founded)
            except:
                founded_list.append(None)
                

            try:
                website = data.find("div", {"class": "wpbdp-field-display wpbdp-field wpbdp-field-value field-display field-value wpbdp-field-website wpbdp-field-meta wpbdp-field-type-textfield wpbdp-field-association-meta"}).find("div", {"class": "value"}).find(text=True)
                website_list.append(website)
            except:
                website_list.append(None)
        
        return (name_list, city_list, description_list, keywords_list, funding_list, founded_list, website_list)


csv = EUStartups().get_csv()

#Creating Session With Boto3.
session = boto3.Session(
aws_access_key_id= access_key, 
aws_secret_access_key= secret_access_key
)

s3_res = session.resource('s3')
csv_buffer = StringIO()
csv.to_csv(csv_buffer)
bucket_name = 'capstoneenion'
s3_object_name = 'test.csv'
s3_res.Object(bucket_name, s3_object_name).put(Body=csv_buffer.getvalue())

print("Scrape worked!")


