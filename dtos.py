from tkinter import StringVar

class FormDto:

    def __init__(self):
        self.sender_email = StringVar()
        self.sender_email_pass = StringVar()
        self.notification_email = StringVar()
        self.url_to_check = StringVar()
        self.url_alias = StringVar()
        self.urls_list = []
