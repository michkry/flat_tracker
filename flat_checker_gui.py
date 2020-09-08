#!/usr/bin/python3

from tkinter import Tk, Frame, Label, W, E, N, S, Entry, Button, Toplevel, StringVar, SUNKEN, RAISED
from PIL import ImageTk, Image
import utils as u
import dtos
import services as s
from paphra_tktable import table as t
import multithreading as m

def root_on_close_event(root):
    print("Application closed!")
    root.destroy()

def configure_root(root):
    root.geometry("800x600")
    root.resizable(0, 0)
    root.title(literals["app_title"])
    root.grid_columnconfigure(0, weight=1)
    root.protocol("WM_DELETE_WINDOW", lambda rt = root : root_on_close_event(rt))

def load_header(root):
    header_frame = Frame(root, bg="yellow", width=800, height=100)
    header_frame.grid_propagate(0)
    header_frame.grid_columnconfigure(0, weight=1)
    header_label = Label(header_frame, text=literals["header"], bg="green", font=("TkDefaultFont", 44))
    header_frame.grid(row=0, column=0, pady=15)
    header_label.grid(row=0, column=0, sticky=W+E)

def load_sender_email(frame):
    sender_email_label = Label(frame, text=literals["sender_email_label"],bg="red")
    sender_email_label.grid(row=0, column=0, sticky=W)
    sender_email_entry = Entry(frame, textvariable=dto.sender_email)
    sender_email_entry.grid(row=0, column=1, sticky=W)

def load_sender_email_pass(frame):
    sender_email_pass_label = Label(frame, text=literals["sender_email_pass_label"],bg="red")
    sender_email_pass_label.grid(row=1, column=0, sticky=W)
    sender_email_pass_entry = Entry(frame, textvariable=dto.sender_email_pass)
    sender_email_pass_entry.grid(row=1, column=1, sticky=W)

def load_notification_email(frame):
    notification_email_label = Label(frame, text=literals["notification_email_label"],bg="red")
    notification_email_label.grid(row=2, column=0, sticky=W)
    notification_email_entry = Entry(frame, textvariable=dto.notification_email)
    notification_email_entry.grid(row=2, column=1, sticky=W)

def load_form_frame(root):
    form_frame = Frame(root, bg="blue", width=800, height=400)
    load_sender_email(form_frame)
    load_sender_email_pass(form_frame)
    load_notification_email(form_frame)
    form_frame.grid(row=1, column=0, sticky=W, padx=15)

def acc_btn_click_event(event, prompt, table):
    uae = prompt.children["entry_form"].children["url_alias_entry"]
    utce = prompt.children["entry_form"].children["url_to_check_entry"]
    uae.config(bg="white")
    utce.config(bg="white")
    if fc_service.check_alias_not_duplicated(dto.url_alias.get()):
        if dto.url_alias.get() and dto.url_to_check.get():
            dto.urls_list.append({literals["urls_table_header_0"]: dto.url_alias.get(), literals["urls_table_header_1"]: dto.url_to_check.get()})
            table.add_rows(dto.urls_list)
            fc_service.insert_url(dto.url_alias.get(), dto.url_to_check.get())
            dto.url_alias = StringVar()
            dto.url_to_check = StringVar()
            prompt.destroy()
            return "break"
        if not dto.url_alias.get():
            uae.config(bg="red")
        if not dto.url_to_check.get():
            utce.config(bg="red")
    else:
        uae.config(bg="red")

def cl_btn_click_event(event, prompt):
    prompt.destroy()
    return "break"

def load_prompt_frame(prompt, table):
    frame = Frame(prompt, name="entry_form")
    frame.grid(row=0, column=0, padx=10, pady=10, sticky=W)
    url_alias_label = Label(frame, text=literals["url_alias_label"])
    url_alias_label.grid(row=0, column=0, sticky=W)
    url_alias_entry = Entry(frame, textvariable=dto.url_alias, name="url_alias_entry")
    url_alias_entry.grid(row=0, column=1, sticky=W)
    url_to_check_label = Label(frame, text=literals["url_to_check_label"])
    url_to_check_label.grid(row=1, column=0)
    url_to_check_entry = Entry(frame, textvariable=dto.url_to_check, name="url_to_check_entry")
    url_to_check_entry.grid(row=1, column=1)
    button_frame = Frame(prompt)
    button_frame.grid(row=1)
    acc_btn = Button(button_frame, text=literals["acc_btn"])
    acc_btn.grid(row=0, column=0)
    acc_btn.bind("<Button-1>", lambda event, prmt=prompt, tbl=table : acc_btn_click_event(event, prmt, tbl))
    cl_btn = Button(button_frame, text=literals["cl_btn"])
    cl_btn.grid(row=0, column=1)
    cl_btn.bind("<Button-1>", lambda event, prmt=prompt : cl_btn_click_event(event, prmt))

def add_btn_click_event(event, root, table):
    prompt = Toplevel()
    prompt.grid_columnconfigure(0, weight=1)
    prompt.resizable(0, 0)
    prompt.title(literals["add_url_prompt_title"])
    prompt_width = 400
    prompt_height = 100
    middle_x_pos = int(root.winfo_x() - prompt_width / 2 + root.winfo_width() / 2)
    middle_y_pos = int(root.winfo_y() - prompt_height / 2 + root.winfo_height() / 2)
    prompt.geometry("%sx%s+%s+%s" %(prompt_width, prompt_height, middle_x_pos, middle_y_pos))
    load_prompt_frame(prompt, table)

def rm_btn_click_event(event, tbl):
    url_alias = tbl.get_selected()[tbl.titles[0]["text"]]
    if tbl.delete_row():
        fc_service.del_url_by_url_alias(url_alias)
    return "break"

def load_table_button_frame(root, table):
    button_frame = Frame(root, bg="green")
    button_frame.grid(row=4, column=0, sticky=W, padx=15)
    add_btn = Button(button_frame, text=literals["add_url_btn"])
    add_btn.bind("<Button-1>", lambda event, rt=root, tbl=table : add_btn_click_event(event, rt, tbl))
    add_btn.pack(side="left")
    rm_btn = Button(button_frame, text=literals["rm_btn"])
    rm_btn.bind("<Button-1>", lambda event, tbl=table : rm_btn_click_event(event, tbl))
    rm_btn.pack(side="left")

def load_table_frame(root):
    table_frame = Frame(root)
    table_frame.grid(row=2, column=0, sticky=W, padx=15, pady=15)
    keys_list = [literals["urls_table_header_0"], literals["urls_table_header_1"]]
    header_list = []
    header_list.append({"text": keys_list[0], "width": 25, "type": "l"})
    header_list.append({"text": keys_list[1], "width": 45, "type": "l"})
    table = t.Table(table_frame, keys_list, header_list, height=100)
    dto.urls_list = fc_service.retrieve_table_rows(keys_list)
    table.add_rows(dto.urls_list)
    load_table_button_frame(root, table)

def start_btn_click_event(event, btn):
    global start_btn_pressed
    start_btn_pressed = not start_btn_pressed
    if start_btn_pressed:
        fc_service.update_email_config(dto)
        ##
        fc_service.start_tracking()
        ##
        btn.config(relief=SUNKEN, text=literals["stop_btn"])
        global th
        th = m.TrackingThread(5)
        th.daemon = True
        th.start()
    else:
        btn.config(relief=RAISED, text=literals["start_btn"])
        th.stop()
    return "break"

def load_start_btn_frame(root):
    frame = Frame(root)
    frame.grid(row=5, column=0, padx=15, pady=30)
    start_btn = Button(frame, text=literals["start_btn"], width=20)
    start_btn.grid(row=0, column=0)
    start_btn.bind("<Button-1>", lambda event, btn=start_btn : start_btn_click_event(event, btn))

def load_frames(root):
    load_header(root)
    load_form_frame(root)
    load_table_frame(root)
    load_start_btn_frame(root)

def create_global_vars():
    global dto
    global literals
    global fc_service
    global start_btn_pressed
    literals = u.get_literals_dict("literals.txt", "=")
    fc_service = s.FlatCheckerService()
    dto = fc_service.init_form_dto()
    start_btn_pressed = False

def start_app():
    root = Tk()
    create_global_vars()
    configure_root(root)
    load_frames(root)
    root.mainloop()

if __name__ == "__main__":
    start_app()
