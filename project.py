from cgitb import text
from distutils import command
from distutils.command.upload import upload
from doctest import master
from itertools import chain
from operator import length_hint
import string
from tabnanny import check
import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter import END, RAISED, RIDGE, SOLID, mainloop, ttk,CENTER,Text,messagebox,filedialog,Toplevel
import json
import datetime
from turtle import update, width
from os.path import exists
import time
import pandas
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import pandas as pd
import openpyxl





        





      
    
    

    

                   


# Gregorian & Jalali ( Hijri_Shamsi , Solar ) Date Converter  Functions
# Author: JDF.SCR.IR =>> Download Full Version :  http://jdf.scr.ir/jdf
# License: GNU/LGPL _ Open Source & Free :: Version: 2.80 : [2020=1399]
# ---------------------------------------------------------------------
# 355746=361590-5844 & 361590=(30*33*365)+(30*8) & 5844=(16*365)+(16/4)
# 355666=355746-79-1 & 355668=355746-79+1 &  1595=605+990 &  605=621-16
# 990=30*33 & 12053=(365*33)+(32/4) & 36524=(365*100)+(100/4)-(100/100)
# 1461=(365*4)+(4/4)   &   146097=(365*400)+(400/4)-(400/100)+(400/400)

filename = 'database.json'     
file_exists = exists(filename)     
if file_exists == False :
    with open(filename, 'w') as file_object:   
        json.dump({}, file_object) 

def gregorian_to_jalali(gy, gm, gd):
 g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
 if (gm > 2):
  gy2 = gy + 1
 else:
  gy2 = gy
 days = 355666 + (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99) // 100) + ((gy2 + 399) // 400) + gd + g_d_m[gm - 1]
 jy = -1595 + (33 * (days // 12053))
 days %= 12053
 jy += 4 * (days // 1461)
 days %= 1461
 if (days > 365):
  jy += (days - 1) // 365
  days = (days - 1) % 365
 if (days < 186):
  jm = 1 + (days // 31)
  jd = 1 + (days % 31)
 else:
  jm = 7 + ((days - 186) // 30)
  jd = 1 + ((days - 186) % 30)
 return [jy, jm, jd]


def jalali_to_gregorian(jy, jm, jd):
 jy += 1595
 days = -355668 + (365 * jy) + ((jy // 33) * 8) + (((jy % 33) + 3) // 4) + jd
 if (jm < 7):
  days += (jm - 1) * 31
 else:
  days += ((jm - 7) * 30) + 186
 gy = 400 * (days // 146097)
 days %= 146097
 if (days > 36524):
  days -= 1
  gy += 100 * (days // 36524)
  days %= 36524
  if (days >= 365):
   days += 1
 gy += 4 * (days // 1461)
 days %= 1461
 if (days > 365):
  gy += ((days - 1) // 365)
  days = (days - 1) % 365
 gd = days + 1
 if ((gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0)):
  kab = 29
 else:
  kab = 28
 sal_a = [0, 31, kab, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
 gm = 0
 while (gm < 13 and gd > sal_a[gm]):
  gd -= sal_a[gm]
  gm += 1
 return [gy, gm, gd]

 

def update_read_data():
    read_data(arg ="all" , value="1")
    selectoptions()

root= tk.Tk()
root.title("حساب کتاب")

# tk.geometry("500x500")
root.resizable(False,False)

w = 624 # width for the Tk tk
h = 400 # height for the Tk tk

# # get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen
# # calculate x and y coordinates for the Tk tk window
x = (ws/2) - (w/2)


# # set the dimensions of the screen 
# # and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, 50))

# style = ttk.Style()
# style.theme_use('vista')

tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)



tabControl.add(tab1, text ='ثبت جدید')
tabControl.add(tab2, text ='لیست هزینه‌ها')
tabControl.add(tab3, text ='آمار')
tabControl.pack(expand = 1, fill ="both")

types = []
selectoption = ttk.Combobox(tab2, width = 15 , justify=CENTER   )
selectoption.insert(0,"انتخاب نوع" )
selectoption.place(x=160,y=336,height=23)
def selectoptions():
    with open(filename, "r") as file_object:  
        data = json.load(file_object) 
                
        
        
        for key in data:
            if data[key]["type"] not in types :
                types.append(data[key]["type"])

        selectoption['values'] = types

        

selectoptions()
selectoption.bind("<<ComboboxSelected>>",lambda e: tab2.focus())

def handleReturn(event):
    print("return: event.widget is",event.widget)
    print("focus is:", tab2.focus_get())

tab2.bind("<Return>", handleReturn)


def save():
    files = [("Excel files", ".xlsx .xls")]
    file = filedialog.asksaveasfile(filetypes = files, defaultextension = files , initialfile="database.xlsx",mode='a')
    filename = "database.json"   
    database={"money":[],"date":[],"type":[],"comment":[]}
    def get_data():
        with open(filename, "r") as file_object:
            data = json.load(file_object) 
            for key in data:
                database["money"].append(str(data[key]["money"]))
                database["date"].append(data[key]["date"])
                database["type"].append(data[key]["type"])
                database["comment"].append(data[key]["comment"])
    get_data()
    json_f = json.dumps(database)
    df_json = pd.read_json(json_f)
    df_json.to_excel(file.name,index=False)
    if file.name != None :
        messagebox.showinfo("صحت عملیات","فایل با موفقیت ذخیره شد")
 

  
btn = ttk.Button(tab2, text = 'خروجی اکسل', command =save)
btn.place(x=466,y=335)

def all_children (window) :
    _list = window.winfo_children()

    for item in _list :
        if item.winfo_children() :
            _list.extend(item.winfo_children())

    return _list

filename="database.json"
def openNewWindow(item):

    top = Toplevel(root)
    top.geometry('%dx%d+%d+%d' % (w, h, 200, 200))
    top.title("ویرایش/حذف")
    money_edit = ttk.Entry(top,width= 70 ,justify=CENTER)
    money_edit.insert(0,item["values"][1] )
    money_edit.place(x=40,y=50)
    ttk.Label(top,text =": مبــــــــــــــــــــــــلغ*").place(x=500,y=50)

    comment_edit = ttk.Entry(top,width= 70 ,justify=CENTER)
    comment_edit.insert(0,item["values"][4] )
    comment_edit.place(x=40,y=100)
    ttk.Label(top,text =": توضــــــــــــــیحات").place(x=500,y=100)

    type_edit = ttk.Entry(top,width= 70 ,justify=CENTER)
    type_edit.insert(0,item["values"][3] )
    type_edit.place(x=40,y=150)
    ttk.Label(top,text =": نـــــــــــــــــــــــــــوع*").place(x=500,y=150)

    date_edit = ttk.Entry(top,width= 70 ,justify=CENTER)
    date_edit.insert(0,item["values"][2] )
    date_edit.place(x=40,y=200)
    ttk.Label(top,text =": تاریـــــــــــــــــــــــــخ").place(x=500,y=200)

    def check_values_update(index):

     check = [money_edit.get(),comment_edit.get(),type_edit.get(),date_edit.get()]
     one_money = True
     two_comment = True
     three_type = True
     four_date = True
     if len(check[0]) == 0 or check[0] == "مبلغ مورد نظر را وارد کنید" :
         one_money = False
         messagebox.showerror("خطا", "مبلغ را وارد کنید")
     elif check[0].isnumeric() == False :
         one_money = False
         messagebox.showerror("خطا", "مبلغ باید مقداری عددی باشد")

     if len(check[2]) == 0 or check[2] == "نوع کار را وارد کنید" :
         three_type = False
         messagebox.showerror("خطا", "نوع کار را مشخص کنید")

     
     if len(check[3]) > 0 and check[3] != "(1400/5/23)تاریخ را وارد کنید" :
        
        date_string = check[3]
        format = r"%Y/%m/%d"
        try:
          datetime.strptime(date_string, format)
        except ValueError:
          
          four_date = False
          messagebox.showerror("خطا", "(1400/5/23)تاریخ را با فرمت رو به رو وارد کنید ")

     if check[1] == "توضیحی قرار دهید" or check[1] == "":
         check[1] = "--------------"

     if check[3] == "" or check[3] == "(1400/5/23)تاریخ را وارد کنید" :
       sh_date = gregorian_to_jalali(time.localtime()[0], time.localtime()[1], time.localtime()[2])
       check[3] = str(sh_date[0])+"/"+str(sh_date[1])+"/"+str(sh_date[2])
     if one_money == True and two_comment==True and three_type==True and four_date==True :      
            with open(filename, "r") as file_object:  
                data = json.load(file_object) 
                data[str(index)]["money"] = check[0]
                data[str(index)]["comment"] = check[1]
                data[str(index)]["type"] = check[2]
                data[str(index)]["date"] = check[3]
                
          
            file = open(filename,"w")
            file.close()           
            with open(filename, "w") as file_object:  
               json.dump(data, file_object) 
            messagebox.showinfo("صحت عملیات","اطلاعات با موفقیت ویرایش شد")
            update_read_data()
            widget_list = all_children(tab3)
            for item in widget_list:
                item.pack_forget()
                chart_data()
            top.destroy()

    submit = ttk.Button(top, width=70 ,text = "ویرایش" , command= lambda : check_values_update(item["values"][0]))
    submit.place(x=40,y=250)

    def delete(index) :
     id = str(index)      
     with open(filename, "r") as file_object:  
      data = dict(json.load(file_object)) 
      if id in data:
        try :
            answer = messagebox.askquestion(title='اخطار',
                        message='آیا از حذف مطمئن هستید؟')
            if answer == "yes":
                data.pop(id)
                messagebox.showinfo("صحت عملیات","داده با موفقیت حذف شد")
                
        except  :
            messagebox.showerror("خطا","داده ای با این کد وجود ندارد")
      else:
           messagebox.showerror("خطا","داده ای با این کد وجود ندارد") 
              
     file = open(filename,"w")
     file.close()           
     with open(filename, "w") as file_object:  
        json.dump(data, file_object) 
        
     update_read_data()
     widget_list = all_children(tab3)
     for item in widget_list:
            item.pack_forget()
     chart_data()
     top.destroy()


    submit = ttk.Button(top, width=70 ,text = "حذف" , command= lambda : delete(item["values"][0]))
    submit.place(x=40,y=350)



def chart_data():
#   tabControl.forget(tab3)
  
    chart = {'day':[],'costs':[]}
    last = 30
    with open(filename, "r") as file_object:
        data = json.load(file_object) 
        def costs(day):
            sum = 0
            for key in data:
                    jalali_database =str(data[key]["date"])
                    sep_data = jalali_database.split("/")
                    gregorian_list = jalali_to_gregorian(int(sep_data[0]),int(sep_data[1]),int(sep_data[2]))
                    gregorian = str(gregorian_list[0])+"/"+str(gregorian_list[1])+"/"+str(gregorian_list[2])
                    time = datetime.strptime(gregorian, r"%Y/%m/%d").timestamp()
                    if day == time :
                        sum+=int(data[key]["money"])
            return sum 

        gregorian_today = str(time.localtime()[0])+"/"+str(time.localtime()[1])+"/"+str(time.localtime()[2])
        today = datetime.strptime(gregorian_today, r"%Y/%m/%d").timestamp()
        start_time = today-(last*86400)
        while start_time <= today :
            dt_object = datetime.fromtimestamp(start_time).strftime(r"%Y/%m/%d")
            sep_data = dt_object.split("/")
            sh_date = gregorian_to_jalali(int(sep_data[0]), int(sep_data[1]), int(sep_data[2]))
            jalali = str(sh_date[1])+"/"+str(sh_date[2])
            chart["day"].append(jalali)
            chart["costs"].append(costs(start_time))
            start_time+=86400



    

        # list of squares
    x = chart["day"]
    y = chart["costs"]


    fig = Figure(figsize=(20,20))
    a = fig.add_subplot(111)
    a.plot(x,y,color='blue')
    a.grid(True)
    # a.axes()
    a.set_xticks(x)
    a.set_xticklabels(x, rotation=60 ,fontsize=8 )
    a.set_title (f"""({sum(chart["costs"])} = ﻪﻨﯾﺰﻫ ﻉﻮﻤﺠﻣ) ﻪﺘﺷﺬﮔ ﺯﻭﺭ ۳۰ ﯼﺎﻫ ﻪﻨﯾﺰﻫ ﺭﺍﺩﻮﻤﻧ""", fontsize=12)
    canvas = FigureCanvasTkAgg(fig, master=tab3)
    canvas.get_tk_widget().pack()
    canvas.draw()
  

    
   


def del1(self):
  if money.get() == "مبلغ مورد نظر را وارد کنید" :
   money.delete(0,END)
   money.configure(foreground="black")
def del2(self):
  if comment.get() == "توضیحی قرار دهید" :  
   comment.delete(0,END)
   comment.configure(foreground="black")
def del3(self):
  if type.get() == "نوع کار را وارد کنید" :  
   type.delete(0,END)
   type.configure(foreground="black")
def del4(self):
 if date.get() == "(1400/5/23)تاریخ را وارد کنید" :   
   date.delete(0,END)
   date.configure(foreground="black")
def del6(self):
 if search_data_entry.get() == "عبارت خود را برای جستجو وارد کنید" :   
   search_data_entry.delete(0,END)
   search_data_entry.configure(foreground="black")




money = ttk.Entry(tab1 , width= 70 ,foreground="gray",justify=CENTER)
money.insert(0,"مبلغ مورد نظر را وارد کنید" )
money.place(x=40,y=50)
money.bind("<FocusIn>" , del1)
ttk.Label(tab1,text =": مبــــــــــــــــــــــــلغ*").place(x=500,y=50)

comment = ttk.Entry(tab1 , width= 70 ,foreground="gray",justify=CENTER)
comment.bind("<FocusIn>" , del2)
comment.insert(0,"توضیحی قرار دهید" )
comment.place(x=40,y=100)
ttk.Label(tab1,text =": توضــــــــــــــیحات").place(x=500,y=100)

type = ttk.Entry(tab1 , width= 70 ,foreground="gray",justify=CENTER)
type.bind("<FocusIn>" , del3)
type.insert(0,"نوع کار را وارد کنید" )
type.place(x=40,y=150)
ttk.Label(tab1,text =": نـــــــــــــــــــــــــــوع*").place(x=500,y=150)

date = ttk.Entry(tab1 , width= 70 ,foreground="gray",justify=CENTER)
date.bind("<FocusIn>" , del4)
date.insert(0,"(1400/5/23)تاریخ را وارد کنید" )
date.place(x=40,y=200)
ttk.Label(tab1,text =": تاریـــــــــــــــــــــــــخ").place(x=500,y=200)




def save_data(values) :

    new_data = {"money" : int(values[0]) , "comment" : values[1] , "type" : values[2] , "date" : values[3]}       
    with open(filename, "r") as file_object:  
      data = json.load(file_object) 
      length = len(data)
      length+=1
      data[length] = new_data       
    file = open(filename,"w")
    file.close()           
    with open(filename, "w") as file_object:  
      json.dump(data, file_object) 
    messagebox.showinfo("صحت عملیات", "اطلاعات با موفقیت ثبت شد")
    update_read_data()
    widget_list = all_children(tab3)
    for item in widget_list:
      item.pack_forget()
    chart_data()
    

def check_values() :
     check = [money.get(),comment.get(),type.get(),date.get()]
     one_money = True
     two_comment = True
     three_type = True
     four_date = True
     if len(check[0]) == 0 or check[0] == "مبلغ مورد نظر را وارد کنید" :
         one_money = False
         messagebox.showerror("خطا", "مبلغ را وارد کنید")
     elif check[0].isnumeric() == False :
         one_money = False
         messagebox.showerror("خطا", "مبلغ باید مقداری عددی باشد")

     if len(check[2]) == 0 or check[2] == "نوع کار را وارد کنید" :
         three_type = False
         messagebox.showerror("خطا", "نوع کار را مشخص کنید")

     
     if len(check[3]) > 0 and check[3] != "(1400/5/23)تاریخ را وارد کنید" :
        
        date_string = check[3]
        format = r"%Y/%m/%d"
        try:
          datetime.strptime(date_string, format)
        except ValueError:
          
          four_date = False
          messagebox.showerror("خطا", "(1400/5/23)تاریخ را با فرمت رو به رو وارد کنید ")

     if check[1] == "توضیحی قرار دهید" or check[1] == "":
         check[1] = "--------------"

     if check[3] == "" or check[3] == "(1400/5/23)تاریخ را وارد کنید" :
       sh_date = gregorian_to_jalali(time.localtime()[0], time.localtime()[1], time.localtime()[2])
       check[3] = str(sh_date[0])+"/"+str(sh_date[1])+"/"+str(sh_date[2])
     if one_money == True and two_comment==True and three_type==True and four_date==True :

        save_data(check)

     
     



submit = ttk.Button(tab1, width=70 ,text = "ثبت" , command = check_values)
submit.place(x=40,y=250)






def read_data(arg,value) :
# define columns
    columns = ('id', 'money', 'date' , 'type' , 'comment' )

    tree = ttk.Treeview(tab2, columns=columns, show='headings', height=15 )

    # define headings
    tree.heading('id', text='کد' )
    tree.column("# 1", anchor=CENTER , width=60)
    tree.heading('money', text='مبلغ')
    tree.column("# 2", anchor=CENTER , width=80)
    tree.heading('type', text='نوع')
    tree.column("# 3", anchor=CENTER , width=80)
    tree.heading('comment', text='توضیحات')
    tree.column("# 4", anchor=CENTER , width=125)
    tree.heading('date', text='تاریخ')
    tree.column("# 5", anchor=CENTER , width=255)


    
    # generate sample data
    contacts = []
    with open(filename, "r") as file_object:  
        data = json.load(file_object)
        delete = []
        for key in data:
            if selectoption.get() != "انتخاب نوع" and data[key]["type"] != selectoption.get():
              delete.append(key)  
             
            if arg == "all"  :
               contacts.append((f'{key}', f'{data[key]["money"]}' , f'{data[key]["date"]}', f'{data[key]["type"]}', f'{data[key]["comment"]}'  ))
            elif arg == "date" and key not in delete :
                jalali_database =str(data[key]["date"])
                sep_data = jalali_database.split("/")
                jalali = str(int(sep_data[0]))+"/"+str(int(sep_data[1]))+"/"+str(int(sep_data[2]))
                if jalali == value :
                    contacts.append((f'{key}', f'{data[key]["money"]}' , f'{data[key]["date"]}', f'{data[key]["type"]}', f'{data[key]["comment"]}' ))
            elif arg == "dates" and key not in delete:
                jalali_database =str(data[key]["date"])
                sep_data = jalali_database.split("/")
                gregorian_list = jalali_to_gregorian(int(sep_data[0]),int(sep_data[1]),int(sep_data[2]))
                gregorian = str(gregorian_list[0])+"/"+str(gregorian_list[1])+"/"+str(gregorian_list[2])
                time = datetime.strptime(gregorian, r"%Y/%m/%d").timestamp()
                if time >= value[0] and time <= value[1] :
                    contacts.append((f'{key}', f'{data[key]["money"]}' , f'{data[key]["date"]}', f'{data[key]["type"]}', f'{data[key]["comment"]}' ))
            elif arg == "number" and key not in delete :
                money_database =int(data[key]["money"])
                if money_database == value or str(value) == key :
                    contacts.append((f'{key}', f'{data[key]["money"]}' , f'{data[key]["date"]}', f'{data[key]["type"]}', f'{data[key]["comment"]}' ))
            elif arg == "numbers" and key not in delete :
                money_database =int(data[key]["money"])
                if money_database >= value[0] and money_database <= value[1] :
                    contacts.append((f'{key}', f'{data[key]["money"]}' , f'{data[key]["date"]}', f'{data[key]["type"]}', f'{data[key]["comment"]}'  ))              
            elif arg == "free" and key not in delete :
                 type_database =data[key]["type"]
                 comment_database =data[key]["comment"]
                 if value in type_database or value in comment_database  :
                    contacts.append((f'{key}', f'{data[key]["money"]}' , f'{data[key]["date"]}', f'{data[key]["type"]}', f'{data[key]["comment"]}'  ))              




    contacts.reverse()    
   
    def item_selected(event):
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            openNewWindow(item)


    tree.bind('<<TreeviewSelect>>', item_selected)

    for contact in contacts:
        tree.insert('', END, values=contact )




    tree.grid(row=0, column=0, sticky='nsew')

    # add a scrollbar
    scrollbar = ttk.Scrollbar(tab2, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

read_data(arg ="all" , value="1")



reload = ttk.Button(tab2, width=8  ,text = "تازه سازی" , command=update_read_data )
reload.place(x=546,y=335)


def search():
    string = str(search_data_entry.get())
    if string.count("/") == 2 :

        sep_data = string.split("/") 
        jalali = str(int(sep_data[0]))+"/"+str(int(sep_data[1]))+"/"+str(int(sep_data[2]))
        read_data(arg="date" , value=jalali)
        messagebox.showinfo("صحت عملیات","جستجو با موفقیت انجام شد")

    elif string.count("/") == 4 :

        sep_data = string.split("-") 
        date_one = str(sep_data[0]).split("/")
        date_two = str(sep_data[1]).split("/")
  

        gregorian_list_one = jalali_to_gregorian(int(date_one[0]),int(date_one[1]),int(date_one[2]))
        gregorian_one = str(gregorian_list_one[0])+"/"+str(gregorian_list_one[1])+"/"+str(gregorian_list_one[2])
        time_one = datetime.strptime(gregorian_one, r"%Y/%m/%d").timestamp()

        gregorian_list_two = jalali_to_gregorian(int(date_two[0]),int(date_two[1]),int(date_two[2]))
        gregorian_two = str(gregorian_list_two[0])+"/"+str(gregorian_list_two[1])+"/"+str(gregorian_list_two[2])
        time_two = datetime.strptime(gregorian_two, r"%Y/%m/%d").timestamp()

        print(time_one,time_two)

        read_data(arg="dates" , value=[time_one,time_two])
        messagebox.showinfo("صحت عملیات","جستجو با موفقیت انجام شد")
       
    
    elif string.isnumeric() == True :
        read_data(arg="number", value=int(string))
        messagebox.showinfo("صحت عملیات","جستجو با موفقیت انجام شد")
       

    elif string.count("-") == 1 and string.count("/") == 0 :
        sep_data = string.split("-")
        read_data(arg="numbers", value=[int(sep_data[0]),int(sep_data[1])])
        messagebox.showinfo("صحت عملیات","جستجو با موفقیت انجام شد")
       
    else :
        read_data(arg="free" , value=string)
        messagebox.showinfo("صحت عملیات","جستجو با موفقیت انجام شد")
       


    

    





search_data_entry = ttk.Entry(tab2 , width= 30   ,foreground="gray",justify=CENTER)
search_data_entry.bind("<FocusIn>" , del6)
search_data_entry.insert(0,"عبارت خود را برای جستجو وارد کنید" )
search_data_entry.place(x=274,y=336 ,height=23)
search_data_button = ttk.Button(tab2, width=7 ,text = "جستجو" , command = search)
search_data_button.place(x=108,y=335)

def show(self):
   messagebox.showinfo("راهنمای جستجو", """
   برای جستجو، عبارت را به شیوه های زیر وارد کنید \n
 👇اگر به دنبال قیمتی مشخص هستید \n
مثال : 20000 \n
👇اگر به دنبال قیمتی در بازه ای مشخص هستید \n
مثال : 20000-10000 \n
👇اگر به دنبال تاریخی مشخص هستید \n
مثال : 1400/3/8 \n
👇اگر به دنبال تاریخی در بازه ای مشخص هستید \n
مثال 1400/10/4-1400/5/5 \n
اگر هم به دنبال عبارتی در ستون نوع ، توضیحات و کد هستید تنها کافیست عبارت را وارد کنید  \n

در صورت انتخاب نوع ، تمامی موارد بالا در نوع انتخاب شده جستجو می شود """)

help = ttk.Label(tab2,text ="راهنمای جستجو" , foreground="blue"  , font=('tahoma',7 , "underline") )
help.bind("<Button-1>" , show)
help.place(x=362,y=360)

help = ttk.Label(tab2,text="برای حذف یا ویرایش بر روی سطر کلیک کنید", foreground="gray"  , font=('tahoma',7) )
help.place(x=432,y=360)






chart_data()



















tk.mainloop()

