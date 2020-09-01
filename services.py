from daos import *
from model import *
from dtos import FormDto
import requests
from bs4 import BeautifulSoup
### TESTING ###
from requests_file import FileAdapter
### TESTING ###

class FlatCheckerService:

    def __init__(self):
        self._email_config_dao = EmailConfigDao()
        self._url_dao = UrlDao()

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
        self._url_dao.delete_by_url_alias(url_alias)

    def retrieve_table_rows(self, header_name_list):
        rows_list = []
        url_list = self._url_dao.get_all()
        for url in url_list:
            rows_list.append({header_name_list[0]: url.get_url_alias(), header_name_list[1]: url.get_url()})
        return rows_list

    def check_alias_not_duplicated(self, url_alias):
        # TODO add check if alias exists in DDBB
        return True
