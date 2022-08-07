from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .forms import urlForm
from django.contrib import messages
import os
from LinkPreviewer.settings import BASE_DIR
# Create your views here.


def preview(request):
    if request.method == 'POST':
        form = urlForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(chrome_options=options)
            try:
                driver.get(url)
            except Exception as e:
                print('Invalid url/ No url found')
                return render(request, 'baseApp/index.html', {'form':form ,'invalid_url':True})
            # time.sleep(2)
            page = driver.page_source
            driver.quit()

            soup = BeautifulSoup(page, 'html.parser')

            #    OG: META TAGS
            title = soup.find("meta", property="og:title")['content'] if  soup.find("meta", property="og:title") else None
            description = soup.find("meta", property="og:description")['content'] if  soup.find("meta", property="og:description") else None
            image = soup.find("meta", property="og:image")['content'] if  soup.find("meta", property="og:image") else None
            url = soup.find("meta", property="og:url")['content'] if  soup.find("meta", property="og:url") else None
            site = soup.find("meta", property="og:site_name")['content'] if  soup.find("meta", property="og:site_name") else None

            #    TWITTER: META TAGS
            twtr_card = soup.find("meta", attrs={"name":"twitter:card"})
            twtr_title = soup.find("meta",attrs={"name":"twitter:title"})
            twtr_description = soup.find("meta", attrs={"name":"twitter:description"})
            twtr_img = soup.find("meta", attrs={"name":"twitter:image"})
            twtr_url = soup.find("meta", attrs={"name":"twitter:url"})
            twtr_site = soup.find("meta", attrs={"name":"twitter:site"})
            twtr_embeded = None
            if twtr_embeded and twtr_card['content']=='player':
                twtr_embeded = soup.find("meta", attrs={"name":"twitter:player"})

            og_tags = ['ogtitle', 'ogdescription', 'ogimage', 'ogurl', 'ogsite']
            og_content = [title, description, image, url, site]
            
            # ADD OG:TAGS TO THE CONTEXT DICTIONARY TO FORWARD TO THE TEMPLATE
            context_dict = dict(zip(og_tags, og_content))
            for key, value in context_dict.items():
                tag = key[:2] + ':' + key[2:]
                if value!=None:
                    messages.success(request, f'Tag {tag} Found')
                else:
                    messages.error(request, f'Couldn\'t found {tag} tag')

            # ADD TWITTER:TAGS TO THE CONTEXT DICTIONARY TO FORWARD TO THE TEMPLATE
            # OVERWRITE THE TWITTER TAGS WITH OG TAGS IF SOME OF TAGS NOT FOUND
            if twtr_card != None:
                tag = twtr_card['name']
                tag_content = twtr_card['content']
                messages.success(request, f'Tag {tag} {tag_content} Found')
                context_dict['twtr_card'] = twtr_card['content']
                context_dict['twtr_title'] = twtr_title['content'] if twtr_title else title
                context_dict['twtr_description'] = twtr_description['content'] if twtr_description else description
                context_dict['twtr_img'] = twtr_img['content'] if twtr_img else image
                context_dict['twtr_url'] = twtr_url['content'] if twtr_url else url
                context_dict['twtr_site'] = twtr_site['content'] if twtr_site else site
            if twtr_embeded and twtr_card['content']=='player':
                context_dict['twtr_embeded'] = twtr_embeded['content']

            context_dict['form'] = form
            return render(request, 'baseApp/index.html', context_dict)
    else:
        form = urlForm()
        return render(request, 'baseApp/index.html', {'form':form})