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

        self.devices_list = []

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
            "font": ("Courier"),
            "height" : 9,
            "width" : 40
        }

        self.option_menu_properties = {
            "font": ("Courier", 15),
            "padx" : 5,
            "pady" : 10,
            "width" : 30
        }

        self.left_frame = tk.Frame(self, self.frame_properties)
        self.middle_frame = tk.Frame(self, self.frame_properties)

        self.left_frame.grid(row=0,column=0,sticky="nw")
        self.middle_frame.grid(row=0,column=1,sticky="ne")
        
        #left frame
        #==========
        self.find_device_label  = tk.Label(self.left_frame,self.label_properties,text = "Device Search", bg="black", fg="white")
        self.find_device_label.grid(self.grid_properties, row = 0, column = 0, sticky="ew")

        #search box text
        self.search_box_label = tk.Label(self.left_frame,self.label_properties,text="Enter Device name",justify="center")
        self.search_box_label.grid(self.grid_properties, row = 1, column = 0, sticky = "w")
        
        #search box input
        self.search_box_combobox = ttk.Combobox(self.left_frame)
        self.search_box_combobox.grid(self.grid_properties,row=2,column=0,sticky="ew")

        #search buttton
        self.search_button = tk.Button(self.left_frame,self.button_properties,text="Find Device", command=self.search_user)
        self.search_button.grid(self.grid_properties,row=3,column=0,sticky="ew")

        #search result
        self.result_text = tk.Text(self.left_frame,self.result_text_properties)
        self.result_text.grid(self.grid_properties,row=4,column=0)
        
        #middle frame
        #===========
        #device name
        self.add_device_label = tk.Label(self.middle_frame, self.label_properties,text = "Add new Device",bg="black",fg="white", width="30")
        self.add_device_label.grid(self.grid_properties, row=0,column=0)

        self.device_name_label = tk.Label(self.middle_frame,self.label_properties,text="Device Name")
        self.device_name_label.grid(self.grid_properties, row = 1, column = 0)

        self.device_name_Entry = tk.Entry(self.middle_frame, self.entry_properties)
        self.device_name_Entry.grid(self.grid_properties, row=2,column=0)

        #device mac address
        self.device_mac_address_label = tk.Label(self.middle_frame,self.label_properties,text="Mac Address or serial")
        self.device_mac_address_label.grid(self.grid_properties, row = 3, column = 0)

        self.device_mac_address_Entry = tk.Entry(self.middle_frame, self.entry_properties)
        self.device_mac_address_Entry.grid(self.grid_properties, row=4,column=0)

        #device holder name
        self.device_holder_name_label = tk.Label(self.middle_frame,self.label_properties,text="User")
        self.device_holder_name_label.grid(self.grid_properties, row = 5, column = 0)

        self.device_holder_name_Entry = tk.Entry(self.middle_frame,self.entry_properties)
        self.device_holder_name_Entry.grid(self.grid_properties, row=6,column=0)

        #add user button
        self.add_device = tk.Button(self.middle_frame,self.button_properties,text="Add Device",command=self.add_user_to_db)
        self.add_device.grid(self.grid_properties,row=7,column=0)
        

        #right frame
        self.right_frame = tk.Frame(self, self.frame_properties)
        self.right_frame.grid(row=0,column=2,sticky="nw")

        #info label
        self.update_user_label = tk.Label(self.right_frame, self.label_properties, text = "Update User", bg="black", fg="white")
        self.update_user_label.grid(self.grid_properties,row=0,column=0,sticky="ew")

        #Devices available
        self.devices_available_label = tk.Label(self.right_frame,self.label_properties,text="Available Devices")
        self.devices_available_label.grid(self.grid_properties,row=1, column=0)

        #Drop down menu
        self.device_list_menu =  ttk.Combobox(self.right_frame, state="readonly")
        self.device_list_menu.grid(self.grid_properties, row=2,column=0,sticky="ew",pady=10)
        # self.device_list_menu.current(0)

        #device holder label
        self.new_device_holder_name_label = tk.Label(self.right_frame,self.label_properties,text="New user name")
        self.new_device_holder_name_label.grid(self.grid_properties, row = 3, column = 0)

        #new device holder name
        self.new_device_holder_name_Entry = tk.Entry(self.right_frame,self.entry_properties)
        self.new_device_holder_name_Entry.grid(self.grid_properties, row=4,column=0)

        #update new user button
        self.update_device_Button = tk.Button(self.right_frame,self.button_properties,text="Update user", command=self.update_holder)
        self.update_device_Button.grid(self.grid_properties,row=5,column=0)

        #delete device button
        self.delete_device_Button = tk.Button(self.right_frame, self.button_properties, text="Delete Device",command=self.delete_device)
        self.delete_device_Button.grid(self.grid_properties,row=6,column=0,sticky="ew")

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
        device = self.device_name_Entry.get().strip()
        mac_address = self.device_mac_address_Entry.get().strip()
        user = self.device_holder_name_Entry.get().strip()
        time = datetime.datetime.now().strftime("%d-%B-%y %H:%M:%S")
        if device == "" or mac_address == "" or user == "":
            self.pop_up_error_message("empty_field_error")
        elif len(device) < 5 or len(mac_address) < 5 or len(user) < 5:
            self.pop_up_error_message("length_error")
        elif self.validate_mac(mac_address) == 0:
            self.pop_up_error_message("mac_error")
        else:
            insert_query = "INSERT INTO devices (device_name,mac_address,device_holder,timestamp) VALUES (?,?,?,?)"
            insert_values = (device, mac_address, user, time)
            device_manager.run_query(insert_query, insert_values)
            self.device_holder_name_Entry.delete(0,tk.END)
            self.device_mac_address_Entry.delete(0,tk.END)
            self.device_name_Entry.delete(0,tk.END)
            self.populate_available_devices_list()
            tkinter.messagebox.showinfo("Success", "Device Added Successfully")

    def populate_available_devices_list(self):
        sql = "SELECT device_name FROM devices"
        query_result = device_manager.run_query(sql,input_value=False, return_value=True)
        for device in query_result:
        	if device[0] not in self.devices_list:
        		self.devices_list.append(device[0])
        self.devices_list.sort()
        self.device_list_menu['values'] = self.devices_list 
        self.search_box_combobox['values'] = self.devices_list
        self.device_list_menu.set("Select a device")
        self.search_box_combobox.set("Select a device")

    def search_user(self):
        query = "SELECT * FROM devices where device_name=?"
        device_name = (str(self.search_box_combobox.get()),)
        query_result = device_manager.run_query(query,device_name,return_value=True)
        self.result_text.delete(1.0,tk.END)
        for row in query_result:
            result = f'''
Device name   : {row[0]}
Mac Address   : {row[1]}
Device Holder : {row[2]}
Date Issued   : {row[3]} 
            '''
            self.result_text.insert(tk.END,result)
            
    def update_holder(self):
        new_device_holder = self.new_device_holder_name_Entry.get().strip()
        if new_device_holder == "":
            self.pop_up_error_message("empty_field_error")
        elif len(new_device_holder) < 5:
            print(len(new_device_holder))
            self.pop_up_error_message("length_error")
        else:    
            device_name = self.device_list_menu.get()
            input_value = (new_device_holder,device_name)
            query = "UPDATE devices SET device_holder = ? where device_name = ?"
            device_manager.run_query(query,input_value)
            self.new_device_holder_name_Entry.delete(0,tk.END)
            self.device_list_menu.set("Select a device")
            tkinter.messagebox.showinfo("Success", "User updated Successfully")
            
    def delete_device(self):
        device_name = (self.device_list_menu.get(),)
        query = "DELETE FROM devices WHERE device_name = ?"
        device_manager.run_query(query,device_name)
        tkinter.messagebox.showinfo("Success", "Device deleted Successfully")
        self.devices_list.remove(device_name[0])
        self.populate_available_devices_list()

    @staticmethod
    def run_query(sql, input_value=False, return_value=False):
        connection = sqlite3.connect(DB_FILE_PATH)
        cursor = connection.cursor()
        if input_value:
            cursor.execute(sql,input_value)
        else:
            cursor.execute(sql)
        if return_value:
            return cursor.fetchall()
        connection.commit()
        cursor.close()

    @staticmethod
    def first_time_db():
        create_table_query = "CREATE TABLE devices ( device_name VARCHAR(20), mac_address VARCHAR(20) UNIQUE, device_holder VARCHAR(30),\
         timestamp VARCHAR(20) )"
        device_manager.run_query(create_table_query)

        
if __name__ == '__main__':
    if not os.path.isfile(DB_FILE_PATH):    
        device_manager.first_time_db()
    mainApp = device_manager()
    mainApp.resizable(width=False, height=False)
    mainApp.populate_available_devices_list()
    mainApp.mainloop()
