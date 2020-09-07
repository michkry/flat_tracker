#!/usr/bin/python3

import sqlite3
from os.path import isfile
from model import *

def _ddbb_init():
    ddbb_name = "ift.db"
    ddbb_exists = isfile(ddbb_name)
    global _conn
    _conn = sqlite3.connect("ift.db")
    if not ddbb_exists and _conn:
        c = _conn.cursor()
        with open("init_ddbb.sql") as sql_file:
            sql_script = sql_file.read()
            c.executescript(sql_script)
            _conn.commit()
_ddbb_init()

class EmailConfigDao:

    _INSERT_TEMPLATE = "INSERT INTO email_config (sender_email, sender_email_pass, notif_email) VALUES(?, ?, ?)"

    _GET_CONFIG_TEMPLATE = "SELECT id, sender_email, sender_email_pass, notif_email FROM email_config"
    _UPDATE_TEMPLATE = "UPDATE email_config SET sender_email=?, sender_email_pass=?, notif_email=?"

    def insert(self, email_config):
        c = _conn.cursor()
        c.execute(self._INSERT_TEMPLATE, (email_config.get_sender_email(), email_config.get_sender_email_pass(), email_config.get_notif_email()))
        _conn.commit()

    def update(self, email_config):
        c = _conn.cursor()
        c.execute(self._UPDATE_TEMPLATE, (email_config.get_sender_email(), email_config.get_sender_email_pass(), email_config.get_notif_email(),))
        _conn.commit()

    def get_config(self):
        c = _conn.cursor()
        c.execute(self._GET_CONFIG_TEMPLATE)
        query_result = c.fetchone()
        result = None
        if query_result:
            result = EmailConfig(query_result[0], query_result[1], query_result[2], query_result[3])
        return result

class UrlDao:

    _INSERT_TEMPLATE = "INSERT INTO url (url_alias, url, first_req_done) VALUES(?, ?, ?)"
    _GET_ALL_TEMPLATE = "SELECT id, url_alias, url, first_req_done FROM url"
    _DEL_BY_URL_A_TEMPLATE = "DELETE FROM url WHERE url_alias=?"
    _UPDATE_TEMPLATE = "UPDATE url SET url_alias=?, url=?, first_req_done=? WHERE id=?"

    def insert(self, url):
        c = _conn.cursor()
        c.execute(self._INSERT_TEMPLATE, (url.get_url_alias(), url.get_url(), url.get_first_req_done()))
        _conn.commit()

    def update(self, url):
        c = _conn.cursor()
        c.execute(self._UPDATE_TEMPLATE, (url.get_url_alias(), url.get_url(), url.get_first_req_done(), url.get_id(),))
        _conn.commit()

    def delete_by_url_alias(self, url_alias):
        c = _conn.cursor()
        c.execute(self._DEL_BY_URL_A_TEMPLATE, (url_alias,))
        _conn.commit()

    def get_all(self):
        c = _conn.cursor()
        c.execute(self._GET_ALL_TEMPLATE)
        query_result = c.fetchall()
        result = []
        for row in query_result:
            url = Url(row[0], row[1], row[2], row[3])
            result.append(url)
        return result

class FlatDao:

    _INSERT_LIST_TEMPLATE = "INSERT INTO flat (flat_id, url_id, announcement_date) VALUES(?, ?, ?)"
    _GET_BY_URL_TEMPLATE = "SELECT id, flat_id, url_id, announcement_date FROM flat WHERE url_id=?"

    def insert_list(self, flat_list):
        c = _conn.cursor()
        for flat in flat_list:
            print(str(flat))
            c.execute(self._INSERT_LIST_TEMPLATE, (flat.get_flat_id(), flat.get_url_id(), flat.get_announcement_date(),))
        _conn.commit()

    def get_by_url(self, url):
        result = []
        c = _conn.cursor()
        c.execute(self._GET_BY_URL_TEMPLATE, (url.get_id(),))
        query_result = c.fetchall()
        for row in query_result:
            flat = Flat(row[0], row[1], row[2], None, row[3])
            result.append(flat)
        return result




