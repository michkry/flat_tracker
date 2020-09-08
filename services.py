#!/usr/bin/python3

import datetime
import subprocess
from logging_factory import logger
from daos import *
from model import *
from dtos import FormDto
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

class FlatCheckerService:

    def __init__(self):
        self._email_config_dao = EmailConfigDao()
        self._url_dao = UrlDao()
        self._flat_dao = FlatDao()
        self._DOMAIN_NAME = "https://www.idealista.com"

    def init_form_dto(self):
        email_config = self._email_config_dao.get_config()
        dto = FormDto()
        dto.sender_email.set(email_config.get_sender_email())
        dto.sender_email_pass.set(email_config.get_sender_email_pass())
        dto.notification_email.set(email_config.get_notif_email())
        return dto

    def update_email_config(self, form_dto):
        persisted_config = self._email_config_dao.get_config()
        persisted_config.set_sender_email(form_dto.sender_email.get())
        persisted_config.set_sender_email_pass(form_dto.sender_email_pass.get())
        persisted_config.set_notif_email(form_dto.notification_email.get())
        self._email_config_dao.update(persisted_config)

    def insert_url(self, url_alias, url):
        u = Url(None, url_alias, url, 0)
        self._url_dao.insert(u)

    def del_url_by_url_alias(self, url_alias):
        self._flat_dao.delete_by_url_alias(url_alias)
        self._url_dao.delete_by_url_alias(url_alias)

    def retrieve_table_rows(self, header_name_list):
        rows_list = []
        url_list = self._url_dao.get_all()
        for url in url_list:
            rows_list.append({header_name_list[0]: url.get_url_alias(), header_name_list[1]: url.get_url()})
        return rows_list

    def check_alias_not_duplicated(self, url_alias):
        return True

    def get_flats_from_url(self, url):
        flats_list = []
        page_url = url
        while page_url:
            logger.info("Processing the url: {}".format(str(page_url)))
            flats_list.extend(self._get_flats_from_page(page_url))
            page_url = self._get_next_page_url(page_url)
        return flats_list

    def _get_flats_from_page(self, url):
        flats_from_page_list = []
        page_bs = self._url_to_bs4page(url.get_url())
        if page_bs != None:
            article_list = page_bs.find_all(lambda tag : tag.name == "article" and "data-adid" in tag.attrs)
            for article in article_list:
                flat_id = article["data-adid"]
                href = self._DOMAIN_NAME + article.find(lambda tag : tag.name == "a" 
                                                        and "href" in tag.attrs 
                                                        and tag.attrs.get("class") != None 
                                                        and "item-link" in tag.attrs["class"])["href"]
                logger.info("Article: flat_id = {} and href = {}".format(flat_id, href))
                flat = Flat(None, flat_id, url.get_id(), href, datetime.datetime.now())
                flats_from_page_list.append(flat)
        return flats_from_page_list

    def _get_next_page_url(self, current_url):
        next_url = None
        page_bs = self._url_to_bs4page(current_url.get_url())
        if page_bs:
            pagination_div = page_bs.find("div", class_="pagination")
            if pagination_div:
                tag_li_next = pagination_div.find("li", class_="next")
                if tag_li_next:
                    next_url = Url(current_url.get_id(), current_url.get_url_alias(), self._DOMAIN_NAME + tag_li_next.find("a")["href"], current_url.get_first_req_done())
        return next_url

    def _url_to_bs4page(self, url):
        bs4_page = None
        try:
            options = FirefoxOptions()
            options.add_argument("--headless")
            # Make firefox directory a parameter
            binary = FirefoxBinary('/usr/bin/firefox-esr')
            driver = webdriver.Firefox(options=options, firefox_binary=binary)
            driver.get(url)
            bs4_page = BeautifulSoup(driver.page_source, "html.parser")
            self._kill_idle_browser_processes()
        except:
            print("There was an error while trying to connect to the website")
        return bs4_page

    def _kill_idle_browser_processes(self):
        bash_cmd = "kill -9 $(ps -ef | grep '/usr/bin/firefox-esr --marionette --headless' | awk '{print $2}')"
        p1 = subprocess.Popen(["ps", "-ef"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["grep", "/usr/bin/firefox-esr --marionette --headless"], stdin=p1.stdout, stdout=subprocess.PIPE)
        p3 = subprocess.Popen(["awk", "{print $2}"], stdin=p2.stdout, stdout=subprocess.PIPE)
        p4 = subprocess.Popen(["xargs", "kill", "-9"], stdin=p3.stdout)

    def start_tracking(self):
        persisted_url_list = self._url_dao.get_all()
        for url in persisted_url_list:
            new_flat_list = []
            flats_from_url = self.get_flats_from_url(url)
            if url.get_first_req_done():
                logger.info("The url has been already processed in the past")
                persisted_flat_list = self._flat_dao.get_by_url(url)
                for flat in flats_from_url:
                    if flat not in persisted_flat_list:
                        new_flat_list.append(flat)
                if len(new_flat_list) > 0:
                    #self._send_notif(new_flat_list)
                    pass
            else:
                logger.info("The url is being processed for the first time")
                new_flat_list = flats_from_url
                url.set_first_req_done(1)
                self._url_dao.update(url)
            if len(new_flat_list) > 0:
                self._flat_dao.insert_list(new_flat_list)

###
#fc = FlatCheckerService()
#test_url = Url(123, "alias lala", "https://www.idealista.com/alquiler-viviendas/valencia-valencia/con-precio-hasta_600,metros-cuadrados-mas-de_40/?ordenado-por=precios-asc", 0)
#fc.start_tracking()
###

