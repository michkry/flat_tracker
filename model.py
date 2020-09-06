#!/usr/bin/python3

class _Base:
    def __init__(self, id):
        self._id = id
    def get_id(self):
        return self._id
    def set_id(self, id):
        self._id = id

class EmailConfig (_Base):

    def __init__(self, id, sender_email, sender_email_pass, notif_email):
        _Base.__init__(self, id)
        self._sender_email = sender_email
        self._sender_email_pass = sender_email_pass
        self._notif_email = notif_email

    def get_sender_email(self):
        return self._sender_email

    def get_sender_email_pass(self):
        return self._sender_email_pass

    def get_notif_email(self):
        return self._notif_email

    def set_sender_email(self, sender_email):
        self._sender_email = sender_email

    def set_sender_email_pass(self, sender_email_pass):
        self._sender_email_pass = sender_email_pass

    def set_notif_email(self, notif_email):
        self._notif_email = notif_email

class ReqTimeCtl (_Base):

    def __init__(self, id, last_req_date):
        _Base.__init__(self, id)
        self._last_req_date = last_req_date

    def get_last_req_date(self):
        return self._last_req_date

    def set_last_req_date(self, last_req_date):
        self._last_req_date = last_req_date

class Url (_Base):

    def __init__(self, id, url_alias, url, first_req_done):
        _Base.__init__(self, id)
        self._url_alias = url_alias
        self._url = url
        self._first_req_done = first_req_done

    def get_url_alias(self):
        return self._url_alias

    def get_url(self):
        return self._url

    def get_first_req_done(self):
        return self._first_req_done

    def set_url_alias(self, url_alias):
        self._url_alias = url_alias

    def set_url(self, url):
        self._url = url

    def set_first_req_done(self, first_req_done):
        self._first_req_done = first_req_done

class Flat (_Base):

    def __init__(self, id, flat_id, url_id, href, announcement_date):
        _Base.__init__(self, id)
        self._flat_id = flat_id
        self._url_id = url_id
        self._href = href
        self._announcement_date = announcement_date

    def get_flat_id(self):
        return self._flat_id

    def get_url_id(self):
        return self._url_id

    def get_href(self):
        return self._href

    def get_announcement_date(self):
        return self._announcement_date

    def set_flat_id(self, flat_id):
        self._flat_id = flat_id

    def set_url_id(self, url_id):
        self._url_id = url_id

    def set_href(self, href):
        self._href = href

    def set_announcement_date(self, announcement_date):
        self._announcement_date = announcement_date

    def __eq__(self, other):
        if isinstance(other, Flat):
            return self.get_flat_id() == other.get_flat_id()
        else:
            return False












































