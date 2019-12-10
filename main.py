import datetime
import sqlite3
import os
import tkinter as tk
import tkinter.messagebox
import re

from tkinter import ttk

DB_FILE_PATH = os.path.join(os.path.curdir,"src","device_manager.db")

class device_manager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Device Manager v1")

        self.devices_list = ("egg",    "bunny",    "chicken","egg",    "bunny",    "chicken","egg",    "bunny",    "chicken","egg",    "bunny",    "chicken","egg",    "bunny",    "chicken","egg",    "bunny",    "chicken","egg",    "bunny",    "chicken","egg",    "bunny",    "chicken","egg",    "bunny",    "chicken","egg",    "bunny",    "chicken")

        self.entry_properties = {
            "font": ("Courier", 15),    
            "width" : 30,
        }

        self.label_properties = {
            "font": ("Courier", 15),
            "pady" : 10,
            "padx" : 10,
        }

        self.grid_properties = {
            "padx" : 10,
            "pady" : 10,
            "sticky" : "w"
        }

        self.button_properties = {
            "font": ("Courier", 15),
            "padx" : 5,
            "pady" : 10,
            "width" : 30
        }

        self.frame_properties = {
            "highlightbackground" : "black",
            "highlightthickness" : 1,
            "width" : 450,
            "height" : 100
        }

        self.result_text_properties = {
            "font": ("Courier", 15),
            "height" : 9,
            "width" : 30
        }

        self.option_menu_properties = {
            "font": ("Courier", 15),
            "padx" : 5,
            "pady" : 10,
            "width" : 30
        }

        self.left_frame = tk.Frame(self, self.frame_properties)
        self.right_frame = tk.Frame(self, self.frame_properties)

        self.left_frame.grid(row=0,column=0,sticky="nw")
        self.right_frame.grid(row=0,column=1,sticky="ne")
        
        #left side
        #==========
        self.find_device_label  = tk.Label(self.left_frame,self.label_properties,text = "Device Search", bg="black", fg="white", width="30")
        self.find_device_label.grid(self.grid_properties, row = 0, column = 0)

        #search box text
        self.search_box_label = tk.Label(self.left_frame,self.label_properties,text="Enter Device name",justify="center")
        self.search_box_label.grid(self.grid_properties, row = 1, column = 0, sticky = "w")
        
        #search box input
        self.search_box_Entry = tk.Entry(self.left_frame,self.entry_properties)
        self.search_box_Entry.grid(self.grid_properties,row=2,column=0)

        #search buttton
        self.search_button = tk.Button(self.left_frame,self.button_properties,text="Find Device")
        self.search_button.grid(self.grid_properties,row=3,column=0)

        #search result
        self.result_text = tk.Text(self.left_frame,self.result_text_properties)
        self.result_text.grid(self.grid_properties,row=4,column=0)
        
        #right side
        #===========
        #device name
        self.add_device_label = tk.Label(self.right_frame, self.label_properties,text = "Add new Device",bg="black",fg="white", width="30")
        self.add_device_label.grid(self.grid_properties, row=0,column=0)

        self.device_name_label = tk.Label(self.right_frame,self.label_properties,text="Device Name")
        self.device_name_label.grid(self.grid_properties, row = 1, column = 0)

        self.device_name_Entry = tk.Entry(self.right_frame, self.entry_properties)
        self.device_name_Entry.grid(self.grid_properties, row=2,column=0)

        #device mac address
        self.device_mac_address_label = tk.Label(self.right_frame,self.label_properties,text="Mac Address or serial")
        self.device_mac_address_label.grid(self.grid_properties, row = 3, column = 0)

        self.device_mac_address_Entry = tk.Entry(self.right_frame, self.entry_properties)
        self.device_mac_address_Entry.grid(self.grid_properties, row=4,column=0)

        #device holder name
        self.device_holder_name_label = tk.Label(self.right_frame,self.label_properties,text="User")
        self.device_holder_name_label.grid(self.grid_properties, row = 5, column = 0)

        self.device_holder_name_Entry = tk.Entry(self.right_frame,self.entry_properties)
        self.device_holder_name_Entry.grid(self.grid_properties, row=6,column=0)

        #add user button
        self.add_device = tk.Button(self.right_frame,self.button_properties,text="Add Device",command=self.add_user_to_db).grid(self.grid_properties,row=7,column=0)
        

        #frame_3
        self.frame_3 = tk.Frame(self, self.frame_properties)
        self.frame_3.grid(row=0,column=2,sticky="nw")

        #info label
        self.update_user_label = tk.Label(self.frame_3, self.label_properties, text = "Update User", bg="black", fg="white")
        self.update_user_label.grid(self.grid_properties,row=0,column=0,sticky="ew")

        #Devices available
        self.devices_available_label = tk.Label(self.frame_3,self.label_properties,text="Available Devices")
        self.devices_available_label.grid(self.grid_properties,row=1, column=0)

        #Drop down menu
        self.device_list_menu =  ttk.Combobox(self.frame_3, values=self.devices_list)
        self.device_list_menu.grid(self.grid_properties, row=2,column=0,sticky="ew",pady=10)
        self.device_list_menu.current(0)

        #device holder label
        self.new_device_holder_name_label = tk.Label(self.frame_3,self.label_properties,text="New user name")
        self.new_device_holder_name_label.grid(self.grid_properties, row = 3, column = 0)

        #new device holder name
        self.new_device_holder_name_Entry = tk.Entry(self.frame_3,self.entry_properties)
        self.new_device_holder_name_Entry.grid(self.grid_properties, row=4,column=0)

        #update new user button
        self.update_device_Button = tk.Button(self.frame_3,self.button_properties,text="Update user").grid(self.grid_properties,row=5,column=0)
    

    def validate_mac(self,mac_address):
        mac_address_regex =  re.compile(r'(?:[0-9a-fA-F]:?){12}')
        if len(re.findall(mac_address_regex,mac_address))==0:
            return 0
        return 1

    def pop_up_error_message(self,error_msg_type):
        if error_msg_type == "empty_field_error":
            tkinter.messagebox.showerror("Empty Field", "All fields are mandatory")
        if error_msg_type == "length_error":
            tkinter.messagebox.showerror("Length Error", "Length of each field should be more than 5")
        if error_msg_type == "mac_error":
            tkinter.messagebox.showerror("Mac Error", "Invalid Mac address")

    def add_user_to_db(self):
        device = self.device_holder_name_Entry.get()
        mac_address = self.device_mac_address_Entry.get()
        user = self.device_holder_name_Entry.get()
        time = datetime.datetime.now().strftime("%d-%B-%y %H:%M:%S")

        if device == "" or mac_address == "" or user == "":
            self.pop_up_error_message("empty_field_error")
        elif len(device) < 5 or len(mac_address) < 5 or len(user) < 5:
            self.pop_up_error_message("length_error")
        elif self.validate_mac(mac_address) == 0:
            self.pop_up_error_message("mac_error")
        else:
            pass

    # @staticmethod
    # def first_time_db():
        


if __name__ == '__main__':
    mainApp = device_manager()
    mainApp.mainloop()
