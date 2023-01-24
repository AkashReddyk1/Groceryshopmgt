####################################################Before Running the code ensure that following libraries are installed on your python 3.8 and with add to path enabled=======================================================
#1)reportlab  2)mysql.connector-python  3)pandas  #4)matplotlib    #5)IPython           #6)PDFNetPython3  7)sqlalchemy
#########################If above libraries go to command prompt  execute the following commands one after one with internet connection ##############################################################
#1)pip install reportlab   #2)pip install mysql.connector-python  3)#pip install IPython #4)pip install PDFNetPython3 #5)pip install matplotlib    #6)pip install pandas  #7)pip install sqlalchemy
#======================================================================================All import Statements============================================
from reportlab.platypus import Table
from tkinter import *
from PIL import Image as pilimage, ImageTk
from tkinter import messagebox
from tkinter import ttk
import site
site.addsitedir("../../../PDFNetC/Lib")
import sys
from PDFNetPython3 import *
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import mysql.connector as sql
import sqlalchemy as alsql
from datetime import date
from datetime import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
#=================================================================================Preparation of Mysql =====================================================================================================================
cnx =sql.connect(user='root', password='danger',host='localhost')
alsqlengine=alsql.create_engine('mysql+mysqlconnector://root:danger@localhost/project')
cursor=cnx.cursor()
try:
    cursor.execute('use project')
except:
    cursor.execute('create database project')
    cursor.execute('use project')
try:
    cursor.execute('select * from credentials')
    s=cursor.fetchall()
    for x in s:
        print(x[0],'\t',x[1],'\t',x[2],'\t',x[3])
except:
    cursor.execute(
        'create table credentials(sno integer,username varchar(100),usertype varchar(100),password varchar(100))')
    cursor.execute('alter table credentials add primary key(username)')
    cursor.execute("insert into credentials values (1,'1','testing','1'),(2,'user1','employee','password1'),(3,'user2','employee','password2'),(4,'user3','employee','password3'),(5,'admin','owner','admin')")
    cursor.execute('select * from credentials')
    s=cursor.fetchall()
    for x in s:
        print(x[0],'\t',x[1],'\t',x[2],'\t',x[3])
try:
    cursor.execute('select * from olditems')
    data=cursor.fetchall()
    print(data)
except:
    csvfile=os.getcwd()+'\\resources\Itemsdata.csv'
    itemsdataframe=pd.read_csv(csvfile)
    print(itemsdataframe)
    alsqlcn=alsqlengine.connect()
    itemsdataframe.to_sql('olditems',alsqlcn)
    alsqlcn.close()
    alsqlengine.dispose()
    cursor.execute('drop table if exists items ')
    cursor.execute('CREATE TABLE items(select sno,itemname,itemcode,quantity,price,company from project.olditems)')
    cnx.commit()
try:
    cursor.execute('use orders')
except:
    cursor.execute('create database orders')
    cnx.commit()
cnx.close()
#==========================================================================================Initialising mainwindow=============================================================
ifc = Tk()
#ifc.resizable(width=FALSE, height=FALSE)
# ======================================================================Strings and StringVars=======================================================================#################
todaysdate = str(date.today().strftime('%d-%m-%Y'))
datewithouthyphens = todaysdate.replace('-', '_')
print(datewithouthyphens)
user = StringVar()
password = StringVar()
################==========================================================All images=============================================================####################
img_submit = PhotoImage(file=os.getcwd()+'\\resources\submit.png')
img_back = PhotoImage(file=os.getcwd()+'\\resources\\back.png')
img_logout = PhotoImage(file=os.getcwd()+'\\resources\logout.png')
img_changepassword = PhotoImage(file=os.getcwd()+'\\resources\changepassword.png')
img_viewitems = PhotoImage(file=os.getcwd()+'\\resources\\viewitems.png')
img_orderitems = PhotoImage(file=os.getcwd()+'\\resources\orderitems.png')
img_changeprices = PhotoImage(file=os.getcwd()+'\\resources\changeprices.png')
img_manageitems = PhotoImage(file=os.getcwd()+'\\resources\manageitems.png')
img_analyzedata = PhotoImage(file=os.getcwd()+'\\resources\\analyzedata.png')
img_viewandmanageitems = PhotoImage(file=os.getcwd()+'\\resources\\viewandmanageitems.png')
img_manageusers = PhotoImage(file=os.getcwd()+'\\resources\manageusers.png')
LOGIN = PhotoImage(file=os.getcwd()+'\\resources\\newlogin.png')
EXIT = PhotoImage(file=os.getcwd()+'\\resources\\newexit.png')
#=========================================================================================Mainexit button====================================================
def mainexit():
    os._exit(0)
##########################################################################All the Classes i.e frames+++++++++++=============================================================================================================
class orderhistory():
    def __init__(self,ifc):
        self.ifc=ifc
        ifc.geometry('1200x700')
        ifc.title('Order History')
        ifc.configure(bg='green')
        def back1dashboard():
            mainhistoryframe.pack_forget()
            for widget in mainhistoryframe.winfo_children():
                widget.pack_forget()
            Dashboard(ifc)
        def insert_allorders():
            cn = sql.connect(host='localhost', user='root', password='danger', database='orders')
            c = cn.cursor()
            c.execute('select table_name,date_format(create_time,\'%d%m%y%h%m%s\') from information_schema.tables where table_schema=\'orders\'')
            table_names=[]
            table_times=[]
            amounts=[]
            historydata=[]
            for ordertuple in list(c.fetchall()):
                historydata.append(list(ordertuple))
            print(historydata)
            for order in historydata:
                table_names.append(order[0])
                entryatetime=str(order[1])
                table_times.append(entryatetime[0:2]+'-'+entryatetime[2:4]+'-'+entryatetime[4:6]+'  '+entryatetime[6:8]+':'+entryatetime[8:10]+':'+entryatetime[10:12])
            print(table_times)
            print(table_names)
            for table in table_names:
                c.execute('select sum(price) from '+str(table))
                amounts.append(int(str(c.fetchall()).replace('[(Decimal(\'', '').replace('\'),)]', '')))
            print(amounts)
            for info in range(0,len(table_names)):
                ordervalue=(table_names[info],table_times[info],amounts[info])
                records_orders.insert('',END,values=ordervalue)
            cn.commit()
            cn.close()
        def order_info(ev):
            records_orderinfo.delete(*records_orderinfo.get_children())
            cn = sql.connect(host='localhost', user='root', password='danger', database='orders')
            c = cn.cursor()
            view_orderinfo = records_orders.focus()
            getorderinfo = records_orders.item(view_orderinfo)
            ordernoinfo= list(getorderinfo['values'])
            c.execute('select * from '+str(ordernoinfo[0]))
            order_data=c.fetchall()
            print(order_data)
            for itemdetail in order_data:
                itemdetailtuple=(itemdetail[0],itemdetail[1],itemdetail[2],itemdetail[3],itemdetail[4],itemdetail[5],itemdetail[6])
                records_orderinfo.insert('',END,values=itemdetailtuple)
            cn.commit()
            cn.close()
        def order_reciept(ev):
            view_orderinfo = records_orders.focus()
            getorderinfo = records_orders.item(view_orderinfo)
            ordernoinfo= list(getorderinfo['values'])
            print('ordernoinfo',ordernoinfo)
            entryate=str(ordernoinfo[0])[-10:]
            print('entryate',entryate)
            recieptfile=str(os.getcwd())+'\Order_Reciepts\Reciepts_dated_'+str(entryate)+'\Reciept_of_'+str(ordernoinfo[0])+'.pdf'
            os.startfile(recieptfile)

        mainhistoryframe=Frame(ifc,bd=10,bg='blue')
        mainhistoryframe.pack(fill=BOTH,expand=YES)
        topframeforhistory=Frame(mainhistoryframe,bd=10,bg='red',width=1200,height=600)
        topframeforhistory.pack(fill=BOTH,expand=YES)
        bottomframeforhistory=Frame(mainhistoryframe,bd=10,bg='pink',width=1200,height=100)
        bottomframeforhistory.pack(fill=BOTH,expand=YES)
        leftframeforhistory=Frame(topframeforhistory,width=450,height=600,bd=10,bg='gold')
        leftframeforhistory.pack(fill=BOTH,expand=YES,side=LEFT)
        orderinfoframe=Frame(topframeforhistory,width=720,height=600,bd=10,bg='brown')
        orderinfoframe.pack(fill=BOTH,expand=YES,side=RIGHT)
        instruction='''Double Click To view Order Details ,Right Click To View Order Reciept'''

        historyframe=Frame(leftframeforhistory,width=440,height=590,bd=10,bg='gold')
        historyframe.pack(fill=BOTH,expand=YES,side=BOTTOM)
        label_instructions=Label(leftframeforhistory,text=instruction,font='rockwell 10 bold')
        label_instructions.pack(side=TOP)

        button_back = Button(bottomframeforhistory, text='Back to Dashboard', font='comicsansms 14 bold', bg='gold',
                             fg='blue', bd=10, command=back1dashboard)
        button_back.pack(side=LEFT)
        button_exit = Button(bottomframeforhistory, text='     Exit      ', bg='green',fg='blue', font='segoeuiblack 14 bold italic', bd=10,
                             command=mainexit)
        button_exit.pack(side=RIGHT)
        global records_orders
        records_orders = ttk.Treeview(historyframe, height=24,columns=('Orderno','Order Date and Time','Order Amount'))
        scroll_x = ttk.Scrollbar(historyframe, orient=HORIZONTAL, command=records_orders.xview)
        scroll_y = ttk.Scrollbar(historyframe, orient=VERTICAL, command=records_orders.yview)
        records_orders.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        records_orders.heading('Orderno', text='Orderno')
        records_orders.heading('Order Date and Time', text='Order DateTime')
        records_orders.heading('Order Amount', text='Order Amount')

        records_orders['show'] = 'headings'
        records_orders.column('#0', width=150, minwidth=120)
        records_orders.column('#1', width=150, minwidth=120)
        records_orders.column('#2', width=90, minwidth=85)
        records_orders.pack(fill=BOTH, expand=YES, side=BOTTOM)
        insert_allorders()
        records_orders.bind('<Double-1>',order_info)
        records_orders.bind('<Button-3>',order_reciept)

        ############################################################Another Treeview for Order Details###########################################################
        records_orderinfo = ttk.Treeview(orderinfoframe, height=24,columns=('Itemno','Sno', 'Item Name', 'Item Code', 'Quantity', 'Price', 'Brand'))
        scrollr_x = ttk.Scrollbar(orderinfoframe, orient=HORIZONTAL, command=records_orderinfo.xview)
        scrollr_y = ttk.Scrollbar(orderinfoframe, orient=VERTICAL, command=records_orderinfo.yview)
        records_orderinfo.configure(yscrollcommand=scrollr_y.set, xscrollcommand=scrollr_x.set)
        scrollr_x.pack(side=BOTTOM, fill=X)
        scrollr_y.pack(side=RIGHT, fill=Y)
        records_orderinfo.heading('Itemno', text='Item No')
        records_orderinfo.heading('Sno', text='Sno')
        records_orderinfo.heading('Item Name', text='Item Name')
        records_orderinfo.heading('Item Code', text='Item Code')
        records_orderinfo.heading('Quantity', text='Quantity')
        records_orderinfo.heading('Price', text='Price')
        records_orderinfo.heading('Brand', text='Brand')
        records_orderinfo['show'] = 'headings'

        records_orderinfo.column('#0', width=50, minwidth=30)
        records_orderinfo.column('#1', width=30, minwidth=30)
        records_orderinfo.column('#2', width=90, minwidth=90)
        records_orderinfo.column('#3', width=90, minwidth=90)
        records_orderinfo.column('#4', width=90, minwidth=90)
        records_orderinfo.column('#5', width=90, minwidth=90)
        records_orderinfo.column('#6', width=90, minwidth=90)
        records_orderinfo.pack(fill=BOTH, expand=YES)

class analysedata():
    def __init__(self, ifc):
        cn = sql.connect(host='localhost', user='root', password='danger', database='orders')
        c = cn.cursor()
        maindataframe = pd.DataFrame()
        tablelist = []
        c.execute("select table_name from information_schema.tables where table_schema=\'orders\'")
        for table in c.fetchall():
            tablelist += table
        for tablename in tablelist:
            query_todf = 'select * from ' + str(tablename)
            tempdf = pd.read_sql(query_todf, cn)
            maindataframe = pd.concat([tempdf, maindataframe], axis=0, ignore_index=True)
        cn.commit()
        cn.close()
        print('maindataframe', maindataframe)
        maindataframe['count'] = 1
        print('maindataframe', maindataframe)
        items = list(maindataframe['itemname'])
        print(items)
        itemcount = {}
        # itemcount=dict(zip(items,list(maindataframe['count'])))
        print(itemcount)
        print(len(items))
        for i in range(0, len(items)):
            itemcount[str(items[i])] = int(items.count(items[i]))
        print(itemcount)

        profitlist = maindataframe[['itemname', 'price']]
        profitlist.loc[:, 'profitperitem'] = round((0.1) * profitlist.loc[:, 'price'])
        print('profitlist', profitlist)
        profitlist = profitlist.drop(index=profitlist[profitlist.duplicated(['itemname'])].index)
        print('profitlist')
        print(profitlist)
        profitlist['itemcount']=itemcount.values()
        profitlist['totalprofitfromitem']=profitlist['profitperitem']*profitlist['itemcount']
        print('profitlist')
        print(profitlist)
        print('Duplicate values', profitlist[profitlist.duplicated(['itemname'])])
        def analysefrequentitems():
            itemsx=list(range(0,len(itemcount.keys())))
            plt.bar(itemsx, itemcount.values(), color='green')
            plt.xticks(itemsx,itemcount.keys(),rotation='vertical')
            plt.title('Items Analysis')
            plt.margins(0.2)
            plt.ylabel('-----Number of times it has been orderd ---------')
            plt.xlabel('-----------Item------------------')
            # Tweak spacing to prevent clipping of tick-labels
            plt.subplots_adjust(bottom=0.30)
            plt.show()
        def analyseprofitperitem():
            plt.bar(profitlist['itemname'],profitlist['totalprofitfromitem'], color='green')
            plt.xticks(profitlist['itemname'],profitlist['itemname'],rotation='vertical')
            plt.title('Items Analysis')
            plt.margins(0.2)
            plt.ylabel('-----Profit per unit item---------')
            plt.xlabel('-----------Item------------------')
            # Tweak spacing to prevent clipping of tick-labels
            plt.subplots_adjust(bottom=0.30)
            plt.show()
        def backdashboard():
            frameforanalysis.pack_forget()
            for widget in frameforanalysis.winfo_children():
                widget.pack_forget()
            Dashboard(ifc)
        ifc.geometry('1200x700')
        ifc.configure(bg='red')
        ifc.title('DataAnalysis')
        global frameforanalysis
        frameforanalysis = Frame(ifc, bg='brown', bd=10)
        frameforanalysis.pack(fill=BOTH, expand=YES)
        button_mostlysolditems = Button(frameforanalysis,
                                        text='Analyze which items are mostly sold out from orders till now',
                                        font='comicsansms 14 bold', bg='gold', fg='blue', bd=10,
                                        command=analysefrequentitems)
        button_mostlysolditems.pack()
        button_profitperitem = Button(frameforanalysis,
                                        text='Analyze which items are profit per item',
                                        font='comicsansms 14 bold', bg='gold', fg='blue', bd=10,
                                        command=analyseprofitperitem)
        button_profitperitem.pack()
        button_back = Button(frameforanalysis, text='Back to Dashboard', font='comicsansms 14 bold', bg='gold',
                             fg='blue', bd=10, command=backdashboard)
        button_back.pack(side=LEFT)
        button_exit = Button(frameforanalysis, text='Exit', bg='green',fg='blue', font='segoeuiblack 14 bold italic', bd=10,
                             command=mainexit)
        button_exit.pack(side=RIGHT)
class items_management():
    def __init__(self, ifc):
        self.ifc = ifc
        ifc.title('Items Management')
        ifc.geometry('1200x700+0+100')
        ifc.configure(bg='black')

        # ======================================Variables=============================================#
        sno = StringVar()
        itemname = StringVar()
        itemcode = StringVar()
        quantity = StringVar()
        price = StringVar()
        brand = StringVar()
        searchwith = StringVar()
        searchtext = StringVar()
        searchorder = StringVar()

        # ==================================functions================================================#
        def back5():
            mainframeforitems.place_forget()
            for widget in mainframeforitems.winfo_children():
                widget.place_forget()
            ifc.title('ShopKeeper Dashboard')
            ifc.geometry('1200x700')
            # ifc.geometry('800x600')
            # Dashboard(ifc)
            # optional if u use keeperdashboard.pack_forget() in command_itemsmgt()

        def clear():
            sno.set('')
            itemname.set('')
            itemcode.set('')
            quantity.set('')
            price.set('')
            brand.set('')
            searchwith.set('itemname')
            searchtext.set('')
            searchorder.set('asc')
            search()

        def add_item():
            if sno.get() == '' or itemname.get() == '' or itemcode == '':
                messagebox._show(message='Few Entries are Empty')
            else:
                cn = sql.connect(host='localhost', user='root', password='danger', database='project')
                c = cn.cursor()
                query_add = 'insert into items values (%s,%s,%s,%s,%s,%s)'
                tuple_add = (sno.get(), itemname.get(), itemcode.get(), quantity.get(), price.get(), brand.get())
                c.execute(query_add, tuple_add)
                cn.commit()
                records_items.delete(*records_items.get_children())
                insert_items()
                cn.close()
                messagebox._show(message='Record Added Successfully')
                clear()

        def delete_item():
            cn = sql.connect(host='localhost', user='root', password='danger', database='project')
            c = cn.cursor()
            query_delete = 'delete from items where sno=' + str(sno.get())
            c.execute(query_delete)
            cn.commit()
            records_items.delete(*records_items.get_children())
            insert_items()
            cn.close()
            messagebox._show(message='Record Deleted Successfully')

            clear()

        def update_item():
            cn = sql.connect(host='localhost', user='root', password='danger', database='project')
            c = cn.cursor()
            query_update = 'update items set itemname=%s,itemcode=%s,quantity=%s,price=%s,company=%s where sno=%s'
            tuple_update = (itemname.get(), itemcode.get(), quantity.get(), price.get(), brand.get(), sno.get())
            c.execute(query_update, tuple_update)
            cn.commit()
            records_items.delete(*records_items.get_children())
            insert_items()
            cn.close()
            messagebox._show(message='Record Updated Successfully')
            clear()

        global insert_items

        def insert_items():
            cn = sql.connect(host='localhost', user='root', password='danger', database='project')
            c = cn.cursor()
            c.execute('select * from items')
            rows = c.fetchall()
            for row in rows:
                records_items.insert('', END, values=row)
                cn.commit()
            cn.close()

        def item_info(ev):
            view_iteminfo = records_items.focus()
            getiteminfo = records_items.item(view_iteminfo)
            record = getiteminfo['values']
            sno.set(record[0])
            itemname.set(record[1])
            itemcode.set(record[2])
            quantity.set(record[3])
            price.set(record[4])
            brand.set(record[5])

        def delete_all():
            cn = sql.connect(host='localhost', user='root', password='danger', database='project')
            c = cn.cursor()
            c.execute('delete from items')
            cn.commit()
            cn.close()
            records_items.delete(*records_items.get_children())

        def search():
            cn = sql.connect(host='localhost', user='root', password='danger', database='project')
            c = cn.cursor()
            query_search = 'select * from items where ' + str(searchwith.get()) + ' like ' + '\'%' + str(
                searchtext.get()) + '%\'' + ' order by ' + str(searchwith.get()) + ' ' + str(entry_searchorder.get())
            if len(str(searchwith)) != 0 or len(str(searchorder)) != 0:
                if len(str(searchtext)) != 0:
                    c.execute(query_search)
                    searched_rows = c.fetchall()
                    records_items.delete(*records_items.get_children())
                    for searchedrow in searched_rows:
                        records_items.insert('', END, values=searchedrow)
                else:
                    c.execute(query_search)
                    searched_rows = c.fetchall()
                    records_items.delete(*records_items.get_children())
                    for searchedrow in searched_rows:
                        records_items.insert('', END, values=searchedrow)
            cn.commit()
            cn.close()

        # =================================Frames=====================================================#
        mainframeforitems = Frame(ifc, bg='gold', width=1200, height=700, bd=10, relief=RIDGE)
        mainframeforitems.place(x=0, y=0)
        leftframe = Frame(mainframeforitems, bg='white', width=400, height=600, bd=10, relief=RIDGE)
        leftframe.place(x=2, y=0)
        rightframe = Frame(mainframeforitems, bg='blue', width=800, height=590, bd=10, relief=RIDGE)
        rightframe.place(x=400, y=0)
        itemslabelframe = Frame(leftframe, width=200, height=600, relief=RIDGE, bg='brown', bd=8)
        itemslabelframe.grid(row=0, column=0,columnspan=1)
        itementriesframe = Frame(leftframe, width=200, height=600, relief=RIDGE, bg='darkviolet', bd=8)
        itementriesframe.grid(row=0, column=1,columnspan=1)
        recordsframe = Frame(rightframe, bg='darkgreen', width=800, height=600, bd=10, relief=RIDGE)
        recordsframe.place(x=0, y=100)
        searchframe = Frame(rightframe, bg='violet', width=1200, height=100, bd=10)
        searchframe.place(x=30, y=0)
        bottomframe = Frame(mainframeforitems, width=1200, height=100, bd=2, relief=RIDGE, bg='red')
        bottomframe.place(x=0, y=580)
        # ===================================Labels&Entries==============================================#
        lbl_sno = Label(itemslabelframe, text='Sno', font='segoeuiblack 12 bold', bd=10)
        lbl_sno.grid(row=0, column=0, padx=18, pady=23)
        entry_sno = Entry(itementriesframe, bd=10, width=16, font='rockwell 12', textvariable=sno)
        entry_sno.grid(row=0, column=0, padx=18, pady=23)
        lbl_itemname = Label(itemslabelframe, text='Item Name', font='segoeuiblack 12 bold', bd=10)
        lbl_itemname.grid(row=1, column=0, padx=18, pady=23)
        entry_itemname = Entry(itementriesframe, bd=10, width=16, font='rockwell 12', textvariable=itemname)
        entry_itemname.grid(row=1, column=0, padx=18, pady=23)
        lbl_itemcode = Label(itemslabelframe, text='Item Code', font='segoeuiblack 12 bold', bd=10)
        lbl_itemcode.grid(row=2, column=0, padx=18, pady=23)
        entry_itemcode = Entry(itementriesframe, bd=10, width=16, font='rockwell 12', textvariable=itemcode)
        entry_itemcode.grid(row=2, column=0, padx=18, pady=23)
        entry_quantity = ttk.Combobox(itementriesframe, width=16, font='rockwell 12', textvariable=quantity)
        entry_quantity['values'] = ('', '1kg', '1', '0.5 kg', '0.25kg', '100g', '1ltr', '0.5ltr')
        entry_quantity.grid(row=3, column=0, padx=18, pady=23)
        lbl_quantity = Label(itemslabelframe, text='Quantity', font='segoeuiblack 12 bold', bd=10)
        lbl_quantity.grid(row=3, column=0, padx=18, pady=23)
        lbl_price = Label(itemslabelframe, text='Price', font='segoeuiblack 12 bold', bd=10)
        lbl_price.grid(row=4, column=0, padx=18, pady=23)
        entry_price = Entry(itementriesframe, bd=10, width=16, font='rockwell 12', textvariable=price)
        entry_price.grid(row=4, column=0, padx=18, pady=23)
        lbl_brand = Label(itemslabelframe, text='Brand', font='segoeuiblack 12 bold', bd=10)
        lbl_brand.grid(row=5, column=0, padx=18, pady=23)
        entry_brand = Entry(itementriesframe, bd=10, width=16, font='rockwell 12', textvariable=brand)
        entry_brand.grid(row=5, column=0, padx=18, pady=23)
        lbl_searchwith = Label(searchframe, text='Search With', font='segoeuiblack 12 bold', bd=5)
        lbl_searchwith.grid(row=0, column=0)
        entry_searchwith = ttk.Combobox(searchframe, font='segoeuiblack 12 bold', textvariable=searchwith)
        entry_searchwith.grid(row=0, column=1)
        entry_searchwith['values'] = ('sno', 'itemname', 'itemcode', 'quantity', 'price', 'company')
        entry_searchwith.current(1)
        lbl_searchorder = Label(searchframe, text='Order By', font='segoeuiblack 12 bold', bd=5)
        lbl_searchorder.grid(row=0, column=2)
        entry_searchorder = ttk.Combobox(searchframe, font='segoeuiblack 12 bold')
        entry_searchorder.grid(row=0, column=3)
        entry_searchorder['values'] = ('asc', 'desc')
        entry_searchorder.current(0)
        lbl_searchtext = Label(searchframe, text='Search Text', font='segoeuiblack 12 bold', bd=5)
        lbl_searchtext.grid(row=1, column=0)
        entry_searchtext = Entry(searchframe, font='segoeuiblack 12 bold', textvariable=searchtext)
        entry_searchtext.grid(row=1, column=1)
        button_search = Button(searchframe, text='Search', bg='yellow', fg='blue', bd=6, command=search,
                               font='segoeuiblack 10 bold ')
        button_search.grid(row=1, column=2)
        # ==================================Buttons=====================================================#
        button_additem = Button(bottomframe, text='Add Item', bg='pink', font='segoeuiblack 14 bold italic', bd=8,width=22, command=add_item)
        button_additem.grid(row=0, column=1)
        button_deleteitem = Button(bottomframe, text='Delete Item', bg='pink', font='segoeuiblack 14 bold italic', bd=8,width=22, command=delete_item)
        button_deleteitem.grid(row=0, column=2)
        button_updateitem = Button(bottomframe, text='Update Item', bg='pink', font='segoeuiblack 14 bold italic', bd=8, width=22, command=update_item)
        button_updateitem.grid(row=0, column=3)
        button_clearitem = Button(bottomframe, text='Clear ', bg='pink', font='segoeuiblack 14 bold italic', bd=8,command=clear, width=22)
        button_clearitem.grid(row=0, column=4)
        button_delete_all = Button(bottomframe, text='Delete All', bg='pink', font='segoeuiblack 14 bold italic', bd=8,width=22, command=delete_all)
        button_delete_all.grid(row=1, column=2)
        button_back = Button(bottomframe, text='Back', bg='pink', font='segoeuiblack 14 bold italic', bd=8,command=back5, width=22)
        button_back.grid(row=1, column=1)
        button_exit = Button(bottomframe, text='Exit', bg='pink', font='segoeuiblack 14 bold italic', bd=8, command=mainexit, width=22, padx=50)
        button_exit.grid(row=1, column=4, columnspan=2)
        # =========================================Treeview for viewing items in records frame=======================

        records_items = ttk.Treeview(recordsframe, height=20,
                                     columns=('Sno', 'Item Name', 'Item Code', 'Quantity', 'Price', 'Brand'))
        scroll_x = ttk.Scrollbar(recordsframe, orient=HORIZONTAL, command=records_items.xview)
        scroll_y = ttk.Scrollbar(recordsframe, orient=VERTICAL, command=records_items.yview)
        records_items.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        records_items.heading('Sno', text='Sno')
        records_items.heading('Item Name', text='Item Name')
        records_items.heading('Item Code', text='Item Code')
        records_items.heading('Quantity', text='Quantity')
        records_items.heading('Price', text='Price')
        records_items.heading('Brand', text='Brand')
        records_items['show'] = 'headings'
        records_items.column('#0', width=80, minwidth=50)
        records_items.column('#1', width=110, minwidth=60)
        records_items.column('#2', width=110, minwidth=60)
        records_items.column('#3', width=110, minwidth=60)
        records_items.column('#4', width=100, minwidth=60)
        records_items.column('#5', width=100, minwidth=60)
        records_items.pack(fill=BOTH, expand=YES, side=BOTTOM)

        insert_items()
        records_items.bind('<ButtonRelease-1>', item_info)

        # records_items.bind('<ButtonRelease-1>',item_info)
        # records_items.bind('<Return>', item_info)


class orders_management():
    def __init__(self, ifc):
        self.ifc = ifc
        ifc.title('Orders Management')
        ifc.geometry('1200x700+0+100')
        ifc.configure(bg='black')
        #ifc.resizable(width=FALSE, height=FALSE)
        # =====================================================================Variables============================================================
        entry_sno = StringVar()
        entry_itemname = StringVar()
        entry_itemcode = StringVar()
        entry_quantity = StringVar()
        entry_price = StringVar()
        entry_brand = StringVar()

        # =======================================================================Functions============================================================

        def back_dashboard():
            mainframefororders.pack_forget()
            Dashboard(ifc)

        def frameforreciept():
            mainframefororders.pack_forget()
            for widget in mainframefororders.winfo_children():
                widget.pack_forget()
            print_reciept(ifc)

        def insert_items():
            cn = sql.connect(host='localhost', user='root', password='danger', database='project')
            c = cn.cursor()
            c.execute('select * from items order by itemname')
            rows = c.fetchall()

            for row in rows:
                records_items.insert('', END, values=row)
                cn.commit()
            cn.close()

        rows_of_order = []

        def order_item(ev):
            view_iteminfo = records_items.focus()
            getiteminfo = records_items.item(view_iteminfo)
            record = getiteminfo['values']
            print('record was in this format', record)
            entry_sno.set(record[0])
            entry_itemname.set(record[1])
            entry_itemcode.set(record[2])
            entry_quantity.set(record[3])
            entry_price.set(record[4])
            entry_brand.set(record[5])
            ordered_row = ((entry_sno.get()),
                           (entry_itemname.get()),
                           (entry_itemcode.get()),
                           (entry_quantity.get()),
                           (entry_price.get()),
                           (entry_brand.get()))

            rows_of_order.append(ordered_row)
            ordered_items.insert('', END, values=ordered_row)

        def ordereditem_remove():
            # view_iteminfo=records_items.focus()

            # ordered_items.delete(getiteminfo['values'])
            selected_item = ordered_items.selection()
            print(selected_item)
            getiteminfo = ordered_items.item(selected_item)['values']
            ordered_items.delete(selected_item)
            print(rows_of_order)

            getiteminfo = (
                str(getiteminfo[0]), getiteminfo[1], str(getiteminfo[2]), str(getiteminfo[3]), str(getiteminfo[4]),
                getiteminfo[5])
            print(type(getiteminfo))

            print('format igven to remove is', tuple(getiteminfo))

            rows_of_order.remove(tuple(getiteminfo))
            print('after removing', rows_of_order)

        def ordereditems_clear():
            # for orderedrow in rows_of_order:
            # rows_of_order.remove(orderedrow)
            rows_of_order.clear()
            ordered_items.delete(*ordered_items.get_children())

        def placeorder():
            cn = sql.connect(host='localhost', user='root', password='danger', database='orders')
            c = cn.cursor()
            c.execute('use orders')
            c.execute('show tables in orders')
            c.fetchall()
            c.execute(
                'SELECT count(*) AS TOTALNUMBEROFTABLES FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = \'orders\' and TABLE_NAME like ' + '\'%' + '_dated_' + str(
                    datewithouthyphens) + '%\'')
            ordertillnow = int(str(c.fetchall()).replace('[(', '').replace(',)]', ''))
            # print(ordertillnow)
            global orderno
            orderno = ordertillnow + 1
            print(orderno)
            c.execute('create table order' + str(orderno) + '_dated_' + str(
                datewithouthyphens) + '(itemno int auto_increment,sno int,itemname varchar(45),itemcode varchar(45),quantity varchar(45),price int,company varchar(45),unique(itemno))')
            for row in rows_of_order:
                query_insertorder = ('insert into Order' + str(
                    orderno) + '_dated_' + str(
                    datewithouthyphens) + '(sno,itemname,itemcode,quantity,price,company) values (%s,%s,%s,%s,%s,%s)')
                ordered_rowintomysql = (str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]))
                c.execute(query_insertorder, ordered_rowintomysql)
                cn.commit()
            cn.close()
            print('Ooder' + str(orderno) + '_dated_' + str(datewithouthyphens) + 'Placed Successfully')
            ordereditems_clear()
            frameforreciept()

        # =======================================================================Frames=================================================================
        global mainframefororders
        mainframefororders = Frame(ifc, bg='gold', bd=5, relief=RIDGE)
        mainframefororders.pack(fill=BOTH, expand=YES)
        Topframe = Frame(mainframefororders, width=1200, height=600, bg='red', bd=3, relief=RIDGE)
        Topframe.pack(side=TOP, fill=BOTH, expand=YES)  # grid(row=0,column=0,sticky=NSEW)
        Bottomframe = Frame(mainframefororders, width=1200, height=100, bg='blue', bd=3, relief=RIDGE)
        Bottomframe.pack(side=BOTTOM, fill=BOTH, expand=YES)  # grid(row=1,column=0,sticky='nsew')
        Bottommostframe = Frame(Bottomframe, width=1200, height=100, bg='silver', bd=3, relief=RIDGE)
        Bottommostframe.pack(fill=BOTH, expand=YES)
        leftframe = Frame(Topframe, bg='white', width=600, height=600, bd=10, relief=RIDGE)
        leftframe.pack(side=LEFT, fill=BOTH, expand=YES)
        recordsframe = Frame(leftframe, width=600, height=600, bd=10, relief=RIDGE)
        recordsframe.pack(fill=BOTH, expand=YES)
        rightframe = Frame(Topframe, bg='green', width=600, height=600, bd=10, relief=RIDGE)
        rightframe.pack(side=RIGHT, fill=BOTH, expand=YES)
        orderframe = Frame(rightframe, width=600, height=600, bd=8, relief=RIDGE)
        orderframe.pack(fill=BOTH, expand=YES)
        cartframe = Frame(orderframe, width=600, height=600, bd=10, relief=RIDGE)
        cartframe.grid(row=1, column=0, columnspan=3, sticky=NSEW)

        # Topframe.grid_columnconfigure(0, weight=1, uniform="group1")
        # Topframe.grid_columnconfigure(1, weight=1, uniform="group1")
        # Topframe.grid_rowconfigure(0,weight=1)
        # ======================================================================== General Buttons and Labels===================================================================
        button_back = Button(Bottommostframe, text='Back', font='comicsansms 12 bold', bd=5, command=back_dashboard)
        button_back.pack(side=LEFT, fill=BOTH, expand=YES)
        button_exit = Button(Bottommostframe, text='Exit', bg='pink', font='comicsansms 12 bold', bd=8,
                             command=mainexit)
        button_exit.pack(side=RIGHT, fill=BOTH, expand=YES)
        label_selectrecords = Label(recordsframe, text='Double Click To Add Items To Cart', font='comicsansms 12 bold',
                                    bd=5)
        label_selectrecords.pack(fill=X)
        label_selectedrecords = Label(orderframe, text='Items Added  To Cart', font='comicsansms 12 bold', bd=5)
        label_selectedrecords.grid(row=0, column=0, columnspan=3)
        # ==================================Buttons for orderframe==================================================================
        button_placeorder = Button(orderframe, text='Place Order', font='comicsansms 12 bold', bd=5, padx=40,
                                   command=placeorder)
        button_clear = Button(orderframe, text='Remove All', font='comicsansms 12 bold', bd=5, padx=25,
                              command=ordereditems_clear)
        button_remove = Button(orderframe, text='Remove Item', font='comicsansms 12 bold', bd=5, padx=25,
                               command=ordereditem_remove)
        button_placeorder.grid(row=2, column=1, sticky=NS)
        button_clear.grid(row=2, column=2, sticky=NS)
        button_remove.grid(row=2, column=0, sticky=NS)
        # =====================================================================Treeviews=======================================================================
        records_items = ttk.Treeview(recordsframe, height=20,
                                     columns=('Sno', 'Item Name', 'Item Code', 'Quantity', 'Price', 'Brand'))
        sty = ttk.Style()
        sty.configure('Treeview', rowheight=20)
        scroll_x = ttk.Scrollbar(recordsframe, orient=HORIZONTAL, command=records_items.xview)
        scroll_y = ttk.Scrollbar(recordsframe, orient=VERTICAL, command=records_items.yview)
        records_items.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        records_items.heading('Sno', text='Sno')
        records_items.heading('Item Name', text='Item Name')
        records_items.heading('Item Code', text='Item Code')
        records_items.heading('Quantity', text='Quantity')
        records_items.heading('Price', text='Price')
        records_items.heading('Brand', text='Brand')
        records_items['show'] = 'headings'
        records_items.column('#0', width=70, minwidth=30)
        records_items.column('#1', width=70, minwidth=30)
        records_items.column('#2', width=70, minwidth=30)
        records_items.column('#3', width=70, minwidth=30)
        records_items.column('#4', width=70, minwidth=30)
        records_items.column('#5', width=60, minwidth=30)
        insert_items()
        records_items.pack(fill=BOTH, expand=YES, side=LEFT)
        records_items.bind('<Double-1>', order_item)
        # ===============================Ordered items treeview================================================================
        global ordered_items
        ordered_items = ttk.Treeview(cartframe, height=20,
                                     columns=('Sno', 'Item Name', 'Item Code', 'Quantity', 'Price', 'Brand'))
        sty = ttk.Style()
        sty.configure('Treeview', rowheight=20)
        scroll_x = ttk.Scrollbar(cartframe, orient=HORIZONTAL, command=ordered_items.xview)
        scroll_y = ttk.Scrollbar(cartframe, orient=VERTICAL, command=ordered_items.yview)
        ordered_items.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X, expand=YES)
        scroll_y.pack(side=RIGHT, fill=Y, expand=YES)
        ordered_items.heading('Sno', text='Sno')
        ordered_items.heading('Item Name', text='Item Name')
        ordered_items.heading('Item Code', text='Item Code')
        ordered_items.heading('Quantity', text='Quantity')
        ordered_items.heading('Price', text='Price')
        ordered_items.heading('Brand', text='Brand')
        ordered_items['show'] = 'headings'
        ordered_items.column('#0', width=70, minwidth=30)
        ordered_items.column('#1', width=70, minwidth=30)
        ordered_items.column('#2', width=70, minwidth=30)
        ordered_items.column('#3', width=70, minwidth=30)
        ordered_items.column('#4', width=70, minwidth=30)
        ordered_items.column('#5', width=70, minwidth=30)
        ordered_items.pack(side=LEFT, fill=BOTH, expand=YES)


class print_reciept():
    def __init__(self, ifc):
        self.ifc = ifc
        ifc.geometry('1200x700+10+100')
        ifc.title('Order Finalization')
        def backtoorders():
            mainframeforreciept.pack_forget()
            for widget in mainframeforreciept.winfo_children():
                widget.pack_forget()
            orders_management(ifc)
        def saveaspdf():
            Time = str(datetime.now())[11:]
            cn = sql.connect(host='localhost', user='root', password='danger', database='orders')
            c = cn.cursor()
            c.execute('use orders')
            c.execute('select * from order' + str(orderno) + '_dated_' + str(datewithouthyphens))
            data = [['Itemno', 'Sno', 'Itemname', 'Itemcode', 'Quantity', 'Price', 'Company']]
            for row in c.fetchall():
                data.append(row)
            print(data)
            global filename
            currentworkingdirectory = os.getcwd()
            recieptsfolder = currentworkingdirectory + '\Order_Reciepts'
            todaysfolder = recieptsfolder + '\Reciepts_dated_' + str(datewithouthyphens)
            if os.path.exists(recieptsfolder) == True:
                pass
            else:
                os.mkdir(recieptsfolder)
            if os.path.exists(todaysfolder) == True:
                pass
            else:
                os.mkdir(todaysfolder)

            filename = todaysfolder + '\Reciept_of_order' + str(orderno) + '_dated_' + str(datewithouthyphens)+ '.pdf'
            print(filename)
            pdf = SimpleDocTemplate(filename, pagesize=A4)
            width, height = A4
            # SubTables
            headingTable = Table([['AMBEDHKAR GROCERY STORE'], ['Peerzadiguda,Uppal-500039'] , ['Phone:9876543210'], ['-' * 177],['Date: ' + str(todaysdate) + '         Order Invoice           Time:' + Time],['-' * 177],
                                  ['Customer Name:' + str(entry_customername.get()) + '           Customer Phone:' + str(entry_customerphone.get())]], width)
            headingTableStyle = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold')
                                               ,
                                            ('BACKGROUND', (0, 0), (-1, -1), colors.green), ('FONTSIZE', (0, 0), (-1, 0), 19),('TOPPADDING', (0, 0), (-1, 0), 5),('BOTTOMPADDING', (0, 0), (-1, 0), 8)

                                               , ('TOPPADDING', (0, 1), (-1, 1), 2),('BOTTOMPADDING', (0, 1), (-1, 1), 2),('FONTSIZE', (0, 1), (-1, 2), 12),

                                            ('BOTTOMPADDING', (0, 2), (-1, 2), 0),('TOPPADDING', (0, 2), (-1, 2), 1),

                                            ('BOTTOMPADDING', (0, 3), (-1, 3), 0),('TOPPADDING', (0, 3), (-1, 3), 0),

                                            ('FONTSIZE', (0, 4), (-1, 4), 16),('BOTTOMPADDING', (0, 4), (-1, 4), 0),('TOPPADDING', (0, 4), (-1, 4), 0),

                                            ('FONTSIZE', (0, 6), (-1, 6), 14), ('BOTTOMPADDING', (0, 6), (-1, 6), 5)])
            headingTable.setStyle(headingTableStyle)
            order_details_table = Table(data)
            order_details_tableStyle = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                                   ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                                                   ('FONTSIZE', (0, 0), (-1, 0), 14),
                                                   ('BACKGROUND', (0, 0), (-1, 0), colors.brown),
                                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                                                   ('LEFTPADDING', (0, 0), (-1, -1), 16),
                                                   ('RIGHTPADDING', (0, 0), (-1, -1), 16),
                                                   ('GRID', (0, 0), (-1, -1), 2, colors.red),
                                                   ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
                                                   ('FONTSIZE', (0, 1), (-1, -1), 12),
                                                   ('BACKGROUND', (0, 1), (-1, -1), colors.gold),
                                                   ])
            order_details_table.setStyle(order_details_tableStyle)
            c.execute('select sum(price) from order' + str(orderno) + '_dated_' + str(datewithouthyphens))
            # print(c.fetchall())
            sum = (str(c.fetchall()).replace('[(Decimal(\'', '').replace('\'),)]', ''))
            print(type(sum))
            print(sum)
            cn.commit()
            cn.close()
            totalTable = Table([['-' * 177], ['Total Cost : Rupees ' + sum], ['-' * 177], ['Visit Again']])
            totalTableStyle = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                          ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold')])

            totalTable.setStyle(totalTableStyle)

            mainTable = Table([[headingTable], [order_details_table], [totalTable]])  # ,[orderTable],[order1Table]
            mainTableStyle = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                         ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                                         ('FONTSIZE', (0, 0), (-1, 0), 14),
                                         ('GRID', (0, 0), (-1, -1), 2, colors.black)
                                         ])

            mainTable.setStyle(mainTableStyle)

            elems = []
            elems.append(mainTable)
            pdf.build(elems)
            os.startfile(filename)
            messagebox._show(message='Opening Generated Reciept Which was saved at \n' + str(filename))
        def printpdf():
            PDFNet.Initialize()
            doc = PDFDoc(filename)
            doc.InitSecurityHandler()
            # Set our PrinterMode options
            printerMode = PrinterMode()
            printerMode.SetCollation(True)
            printerMode.SetCopyCount(1)
            printerMode.SetDPI(100);  # regardless of ordering, an explicit DPI setting overrides the OutputQuality setting
            printerMode.SetDuplexing(PrinterMode.e_Duplex_Auto)
            # If the XPS print path is being used, then the printer spooler file will
            # ignore the grayscale option and be in full color
            printerMode.SetOutputColor(PrinterMode.e_OutputColor_Grayscale)
            printerMode.SetOutputQuality(PrinterMode.e_OutputQuality_Medium)
            # printerMode.SetNUp(2,1)
            # printerMode.SetScaleType(PrinterMode.e_ScaleType_FitToOutPage)
            # Print the PDF document to the default printer, using "tiger.pdf" as the document
            # name, send the file to the printer not to an output file, print all pages, set the printerMode
            # and don't provide a cancel flag.
            Print.StartPrintJob(doc, "", doc.GetFileName(), "", None, printerMode, None)

        global mainframeforreciept
        mainframeforreciept = Frame(ifc, bg='gold', bd=5, relief=RIDGE)
        mainframeforreciept.pack(fill=BOTH, expand=YES)
        buttonsframe = Frame(mainframeforreciept, bg='white', width=400, height=900, bd=10, relief=RIDGE)
        buttonsframe.pack(fill=BOTH, expand=YES)
        label_customername = Label(buttonsframe, text='Enter Customername', font='sansberi 20 bold', bg='black',
                                   fg='violet',
                                   padx=50, pady=20)
        label_customerphone = Label(buttonsframe, text='Enter Customer PhoneNumber', font='sansberi 20 bold',
                                    bg='black',
                                    fg='violet', pady=20)
        entry_customername = Entry(buttonsframe, fg='green', bg='gold', font='sansberi 20 bold', width=30,
                                   borderwidth=5)
        entry_customerphone = Entry(buttonsframe, fg='green', font='sansberi 20 bold', bg='gold', width=30,
                                    borderwidth=10)
        label_customername.grid(row=0, column=0, columnspan=2)
        entry_customername.grid(row=1, column=0, columnspan=2)
        label_customerphone.grid(row=2, column=0, columnspan=2)
        entry_customerphone.grid(row=3, column=0, columnspan=2)
        label_space = Label(buttonsframe, text='-' * 150, font='sansberi 6 bold')
        label_space.grid(row=4, column=0, columnspan=2)
        button_saveaspdf = Button(buttonsframe, text='Generate Reciept as pdf and View', fg='green', bg='gold',
                                  font='sansberi 20 bold', borderwidth=5, padx=20, command=saveaspdf)
        button_saveaspdf.grid(row=6, column=0, columnspan=2)
        button_printpdf = Button(buttonsframe, text='Print Reciept as pdf', fg='green', bg='gold',
                                 font='sansberi 20 bold', borderwidth=5, padx=20, command=printpdf)
        button_printpdf.grid(row=7, column=0, columnspan=2)
        label_space = Label(buttonsframe, text='-' * 150, font='sansberi 6 bold')
        label_space.grid(row=8, column=0, columnspan=2)
        button_finaliseorder = Button(buttonsframe, text='Finalise Order', fg='green', bg='gold',
                                      font='sansberi 20 bold', borderwidth=5)
        button_finaliseorder.grid(row=9, column=0, columnspan=2)
        label_space = Label(buttonsframe, text='-' * 150, font='sansberi 6 bold')
        label_space.grid(row=10, column=0, columnspan=2)
        button_exit = Button(buttonsframe, image=EXIT, padx=80, pady=100, command=mainexit)
        button_exit.grid(row=11, column=0)
        button_back = Button(buttonsframe, text='Back', bg='Black', fg='Red', padx=90, pady=24, command=backtoorders)
        button_back.grid(row=11, column=1)
class changepasswordclass():
    def __init__(self,ifc):
        self.ifc=ifc
        ifc.geometry('1200x700')
        ifc.title('Change Password')
        def back3():
            passwordchangeframe.pack_forget()
            for widget in passwordchangeframe.winfo_children():
                widget.pack_forget()
            Dashboard(ifc)
        def changepassword():
            i=0

            for i in range(0,count):
                cn = sql.connect(host='localhost', user='root', password='danger', database='project')
                c = cn.cursor()
                c.execute('select username,usertype,password from credentials')
                userdata = []
                for row in c.fetchall():
                    userdata.append(row)
                credentials = pd.DataFrame(data=userdata, columns=['username', 'usertype', 'password'])
                cn.close()
                if credentials.loc[i,'username']==str(verify_username.get()):
                    if credentials.loc[i,'password']==str(verify_password.get()):
                        cn = sql.connect(host='localhost', user='root', password='danger', database='project')
                        c = cn.cursor()
                        query_changepassword='update credentials set password=%s where username=%s'
                        tuple_changepassword=(str(entry_newpassword.get()),str(verify_username.get()))
                        c.execute(query_changepassword,tuple_changepassword)
                        cn.commit()
                        cn.close()
                        messagebox._show(message='Password Change was Successful')
                        entry_newpassword.delete(0,END)
                        verify_username.delete(0,END)
                        verify_password.delete(0,END)
                        break
                    else:
                        i+=1
                else:
                    i+=1
                if i == count:
                    messagebox.showerror(message='Wrong Credentials Entered Verification Failed')
                    entry_newpassword.delete(0, END)
                    verify_username.delete(0, END)
                    verify_password.delete(0, END)
        passwordchangeframe=Frame(ifc,width=800,height=600)
        passwordchangeframe.pack(fill=BOTH,expand=YES)
        label_changepassword = Label(passwordchangeframe, text='Verify username and existing password',font='sansberi 28 bold', bg='black', fg='violet', bd=5, relief='sunken', padx=150, pady=8)
        label_changepassword.pack()
        global verify_username
        global verify_password
        verify_username = Entry(passwordchangeframe, fg='red', bg='pink', width=50, borderwidth=5)
        verify_password = Entry(passwordchangeframe, fg='red', bg='pink', width=50, borderwidth=5)
        global entry_newpassword
        entry_newpassword = Entry(passwordchangeframe, fg='red', bg='pink', width=50, borderwidth=5)
        label_username = Label(passwordchangeframe, text='Enter Username', font='sansberi 20 bold', bg='black', fg='violet')
        label_password = Label(passwordchangeframe, text='Enter Existing  Password', font='sansberi 20 bold', bg='black',
                               fg='violet')
        label_newpassword = Label(passwordchangeframe, text='Enter New Password', font='sansberi 20 bold', bg='black',
                                  fg='violet')
        button_change = Button(passwordchangeframe, image=img_changepassword, command=changepassword)
        button_back3 = Button(passwordchangeframe, image=img_back, border=0, command=back3)
        button_exit = Button(passwordchangeframe, image=EXIT, padx=80, pady=10, border=0, command=mainexit)
        label_username.pack()
        verify_username.pack()
        label_password.pack()
        verify_password.pack()
        label_newpassword.pack()
        entry_newpassword.pack()
        button_change.pack()
        button_back3.pack()
        button_exit.pack()
class usermanagementclass():
    def __init__(self,ifc):
        self.ifc=ifc
        ifc.title('User Management System')
        ifc.geometry('1200x700')
        ifc.configure(bg='black')
        usrmgt_username=StringVar()
        usrmgt_password=StringVar()
        usrmgt_usertype=StringVar()
        usrmgt_sno=StringVar()
        def back4():
            usermanagementframe.pack_forget()
            for widget in usermanagementframe.winfo_children():
                widget.pack_forget()
            Dashboard(ifc)
        def add_user():
            cn = sql.connect(host='localhost', user='root', password='danger', database='project')
            c = cn.cursor()
            insertquery = 'insert into credentials values (%s,%s,%s,%s)'
            # c.execute(+str(count+1)+','+str(entry_username.get())+','+str(entry_usertype.get()+','+str(entry_password.get())+')'))
            c.execute(insertquery,(str(count + 1),str(usrmgt_username.get()),str(usrmgt_usertype.get()),str(usrmgt_password.get())))
            cn.commit()
            cn.close()
            records_users.delete(*records_users.get_children())
            insert_users()
            messagebox._show(message='User Added Successfully')
        def delete_user():
            cn = sql.connect(host='localhost', user='root', password='danger', database='project')
            c = cn.cursor()
            c.execute('delete from credentials where username=' + '\'' + str(entry_username.get()) + '\'')
            cn.commit()
            cn.close()
            records_users.delete(*records_users.get_children())
            insert_users()
            messagebox._show(message='User Deleted Successfully')
        def update_user():
            cn = sql.connect(host='localhost', user='root', password='danger', database='project')
            c = cn.cursor()
            tuple_updateuser = (usrmgt_password.get(),usrmgt_username.get(),usrmgt_usertype.get(),usrmgt_sno.get())
            query_updateuser='update credentials set password=%s,username=%s,usertype=%s where sno=%s'
            c.execute(query_updateuser,tuple_updateuser)
            cn.commit()
            cn.close()
            records_users.delete(*records_users.get_children())
            insert_users()
            messagebox._show(message='User Credentials updated successfully')
        def insert_users():
            cn = sql.connect(host='localhost', user='root', password='danger', database='project')
            c = cn.cursor()
            c.execute('select * from credentials')
            userlist=c.fetchall()
            cn.commit()
            cn.close()
            for userdetail in userlist:
                records_users.insert('',END,values=userdetail)
        def usermgt_clear():
            entry_sno.delete(0,END)
            entry_username.delete(0,END)
            entry_password.delete(0,END)
            entry_usertype.delete(0,END)
        def userinfo(ev):
            view_userinfo = records_users.focus()
            getuserinfo = records_users.item(view_userinfo)
            record = getuserinfo['values']
            usrmgt_sno.set(str(record[0]))
            usrmgt_username.set(record[1])
            usrmgt_usertype.set(record[2])
            usrmgt_password.set(record[3])
        usermanagementframe=Frame(ifc,bd=10,bg='yellow')
        usermanagementframe.pack(fill=BOTH,expand=YES)
        usrmgtleftframe=Frame(usermanagementframe,bd=10,width=400,height=800,bg='blue')
        usrmgtleftframe.pack(fill=BOTH,expand=YES,side=LEFT)
        usrmgtrightframe=Frame(usermanagementframe,width=600,height=800,bg='green',bd=10)
        usrmgtrightframe.pack(fill=BOTH,expand=YES,side=RIGHT)
        instruction='''Double Click To view User Details in Fields'''
        label_instructions=Label(usrmgtleftframe,text=instruction,font='rockwell 14 bold')
        label_instructions.grid(row=0,column=0,columnspan=2)
        lbl_sno = Label(usrmgtleftframe, text='Sno', font='segoeuiblack 14 bold', bd=10)
        lbl_sno.grid(row=1, column=0, padx=18, pady=18)
        entry_sno = Entry(usrmgtleftframe, bd=10, width=16, font='rockwell 14',textvariable=usrmgt_sno)
        entry_sno.grid(row=1, column=1, padx=18, pady=18)
        lbl_username = Label(usrmgtleftframe, text='user Name', font='segoeuiblack 14 bold', bd=10)
        lbl_username.grid(row=2, column=0, padx=18, pady=18)
        entry_username = Entry(usrmgtleftframe, bd=10, width=16, font='rockwell 14 bold',textvariable=usrmgt_username)
        entry_username.grid(row=2, column=1, padx=18, pady=18)
        lbl_password = Label(usrmgtleftframe, text='Password', font='segoeuiblack 14 bold', bd=10)
        lbl_password.grid(row=3, column=0, padx=18, pady=18)
        entry_password = Entry(usrmgtleftframe, bd=10, width=16, font='rockwell 14',textvariable=usrmgt_password)
        entry_password.grid(row=3, column=1, padx=18, pady=18)
        entry_usertype = ttk.Combobox(usrmgtleftframe, width=16, font='rockwell 14',textvariable=usrmgt_usertype)
        entry_usertype['values'] = ('owner','employee')
        entry_usertype.grid(row=4, column=1, padx=18, pady=18)
        lbl_usertype = Label(usrmgtleftframe, text='usertype', font='segoeuiblack 14 bold', bd=10)
        lbl_usertype.grid(row=4, column=0, padx=18, pady=18)
        button_adduser = Button(usrmgtleftframe, text='Add User', bg='pink', font='segoeuiblack 14 bold italic', bd=8, command=add_user)
        button_adduser.grid(row=5, column=0)
        button_deleteuser = Button(usrmgtleftframe, text='Delete User', bg='pink', font='segoeuiblack 14 bold italic', bd=8, command=delete_user)
        button_deleteuser.grid(row=5, column=1)
        button_updateuser = Button(usrmgtleftframe, text='Update User', bg='pink', font='segoeuiblack 14 bold italic', bd=8, command=update_user)
        button_updateuser.grid(row=6, column=0)
        button_clearuser = Button(usrmgtleftframe, text='Clear ', bg='pink', font='segoeuiblack 14 bold italic', bd=8,command=usermgt_clear)
        button_clearuser.grid(row=6, column=1)
        button_exit = Button(usrmgtleftframe, image=EXIT, padx=40, pady=40, command=mainexit)
        button_exit.grid(row=7, column=0)
        button_back = Button(usrmgtleftframe, text='Back',font='segoeuiblack 14 bold italic', bg='Black', fg='Red',padx=60, pady=20, command=back4)
        button_back.grid(row=7, column=1)
        records_users = ttk.Treeview(usrmgtrightframe, height=35,columns=('Sno','Username','UserType','Password'))
        sty = ttk.Style()
        sty.configure('Treeview', rowheight=20)
        scroll_x = ttk.Scrollbar(usrmgtrightframe, orient=HORIZONTAL, command=records_users.xview)
        scroll_y = ttk.Scrollbar(usrmgtrightframe, orient=VERTICAL, command=records_users.yview)
        records_users.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        records_users.heading('Sno', text='Sno')
        records_users.heading('Username', text='User Name')
        records_users.heading('UserType', text='User Type')
        records_users.heading('Password', text='Password')
        records_users['show'] = 'headings'
        records_users.column('#0', width=100, minwidth=50)
        records_users.column('#1', width=150, minwidth=80)
        records_users.column('#2', width=150, minwidth=80)
        records_users.column('#3', width=150, minwidth=80)
        insert_users()
        records_users.pack(fill=BOTH, expand=YES,side=TOP)
        records_users.bind('<Double-1>',userinfo)

class Dashboard():
    def __init__(self, ifc, *pargs):
        self.ifc = ifc
        ifc.title('Shopkeeper Dashboard')
        ifc.geometry('1200x700')
        #ifc.resizable(width=FALSE, height=FALSE)

        def command_orderhistory():
            keeperdashboard.pack_forget()
            for widget in keeperdashboard.winfo_children():
                widget.pack_forget()
            orderhistory(ifc)

        def back2():
            keeperdashboard.pack_forget()
            entry_username.delete(0, END)
            entry_password.delete(0, END)
            shopkeeperclass(ifc)

        def framefordataanalysis():
            keeperdashboard.pack_forget()
            for widget in keeperdashboard.winfo_children():
                widget.pack_forget()
            analysedata(ifc)
        def changepassword():
            keeperdashboard.pack_forget()
            for x in keeperdashboard.winfo_children():
                x.place_forget()
            changepasswordclass(ifc)
        def command_itemsmgt():
            # keeperdashboard.pack_forget()
            for widget in keeperdashboard.winfo_children():
                widget.place_forget()
            items_management(ifc)
        def command_order():
            for widget in keeperdashboard.winfo_children():
                widget.grid_forget()
            keeperdashboard.pack_forget()
            orders_management(ifc)
        def command_usermanagement():
            for widget in keeperdashboard.winfo_children():
                widget.grid_forget()
            keeperdashboard.pack_forget()
            usermanagementclass(ifc)
        global keeperdashboard
        keeperdashboard = Frame(ifc, bg='black')
        keeperdashboard.pack(fill=BOTH, expand=YES)
        button_back2 = Button(keeperdashboard, image=img_logout, bd=0, command=back2)
        button_back2.grid(row=0, column=0)
        button_exit = Button(keeperdashboard, image=EXIT, padx=80, pady=10, border=0, command=mainexit)
        button_exit.grid(row=0, column=3, sticky=NE)
        button_change = Button(keeperdashboard, image=img_changepassword, command=changepassword, bd=0)
        button_change.grid(row=0, column=2)
        button_orderitems = Button(keeperdashboard, image=img_orderitems, bd=0, command=command_order)
        button_orderitems.grid(row=1, column=2)
        button_manageitems = Button(keeperdashboard, image=img_viewandmanageitems, bd=0, command=command_itemsmgt)
        button_manageitems.grid(row=2, column=2)
        button_analyzedata = Button(keeperdashboard, image=img_analyzedata, bd=0, command=framefordataanalysis)
        button_analyzedata.grid(row=4, column=2)
        button_orderhistory= Button(keeperdashboard,text=' View Order History', bd=0, command=command_orderhistory,padx=60,pady=15,bg='green',fg='purple')
        button_orderhistory.grid(row=3, column=2)
        for x in range(0,len(usercredentials['username'])):
            if usercredentials.loc[x,'username']==str(user_name):
                if usercredentials.loc[x,'password']==str(pass_word):
                    if usercredentials.loc[x,'usertype']=='owner':
                        global button_manageusers
                        button_manageusers = Button(keeperdashboard, image=img_manageusers, font='rockwell 20 bold', bd=0, bg='gold',fg='violet',command=command_usermanagement)
                        button_manageusers.grid(row=5, column=2)
                    else:
                        x+=1
                else:
                    x+=1

class shopkeeperclass():
    def __init__(self,ifc):
        self.ifc=ifc
        ifc.title('ShopKeeper Login')

        def back1():
            shopmgt.pack_forget()
            entry_username.delete(0, END)
            entry_password.delete(0, END)
            homepage(ifc)
        def submit():
            global user_name
            global pass_word
            user_name = str(entry_username.get())
            pass_word = str(entry_password.get())
            if len(user_name) == 0:
                if len(pass_word) == 0:
                    label_error = Label(shopmgt, text='Please Enter Credentials', font='sansberi 18 bold', bg='violet',
                                        fg='pink')
                    label_error.pack()
            else:
                cn = sql.connect(host='localhost', user='root', password='danger', database='project')
                c = cn.cursor()
                c.execute('select username,usertype,password from credentials')
                data = []
                for row in c.fetchall():
                    data.append(row)
                global usercredentials
                usercredentials = pd.DataFrame(data, columns=['username', 'usertype', 'password'])
                display(usercredentials)
                global count
                count =usercredentials['username'].count()
                print(count)
                cn.close()
                i = 0
                for i in range(0, count):
                    if usercredentials.loc[i,'username']== user_name:
                        if usercredentials.loc[i,'password'] == pass_word:
                            shopmgt.pack_forget()
                            Dashboard(ifc)
                            break
                        else:
                            i += 1
                    else:
                        i += 1
                if i == count:
                    messagebox.showerror(message='Wrong credentials entered')
                    entry_username.delete(0, END)
                    entry_password.delete(0, END)
        global shopmgt
        shopmgt = Frame(ifc, bg='black')
        shopmgt.pack(fill=BOTH, expand=YES)
        global entry_username
        global entry_password
        entry_username = Entry(shopmgt, fg='red', bg='pink', width=50, borderwidth=5)
        entry_password = Entry(shopmgt, textvariable=password, show='*', fg='red', bg='pink', width=50, borderwidth=5)
        label_username = Label(shopmgt, text='Enter Username', font='sansberi 20 bold', bg='black', fg='violet')
        label_password = Label(shopmgt, text='Enter Password', font='sansberi 20 bold', bg='black', fg='violet')
        button_exit = Button(shopmgt, image=EXIT, padx=80, pady=10, border=0, command=mainexit)
        button_submit = Button(shopmgt, image=img_submit, border=0, command=submit)
        button_back = Button(shopmgt, image=img_back, border=0, command=back1)
        label_username.pack()
        entry_username.pack()
        label_password.pack()
        entry_password.pack()
        button_submit.pack()
        button_back.pack()
        button_exit.pack()
class homepage():
    def __init__(self,ifc):
        self.ifc=ifc
        ifc.geometry('1200x700+10+100')
        ifc.title('Grocery Trade')
        ifc.configure(bg='black')
        ifc.minsize(0, 0)
        ifc.maxsize(2000, 1200)

        def command_login():
            Home.pack_forget()
            for widget in Home.winfo_children():
                widget.pack_forget()
            shopkeeperclass(ifc)

        class Example(Frame):
            def __init__(self, master, *pargs):
                Frame.__init__(self, master, *pargs)
                self.image = pilimage.open(os.getcwd()+"\\resources\sum.png")
                self.img_copy = self.image.copy()
                self.background_image = ImageTk.PhotoImage(self.image)
                self.background = Label(self, image=self.background_image)
                self.background.pack(fill=BOTH, expand=YES)
                self.background.bind('<Configure>', self._resize_image)

            def _resize_image(self, event):
                new_width = event.width
                new_height = event.height
                self.image = self.img_copy.resize((new_width, new_height))
                self.background_image = ImageTk.PhotoImage(self.image)
                self.background.configure(image=self.background_image)

        global Home
        Home = Frame(ifc, bg='black')
        Home.pack(fill=BOTH, expand=YES)
        Head = Label(Home, text='Welcome to D-Mart  Shop Management', font='sansberi 28 bold', bg='black', fg='violet', bd=5,relief='sunken', padx=150, pady=8)
        Head.pack()
        shopkeeperlogin = Button(Home, image=LOGIN, border=0, command=command_login)
        shopkeeperlogin.pack()
        button_exit = Button(Home, image=EXIT, padx=80, pady=10, border=0, command=mainexit)
        button_exit.pack()
        imgfill = Example(Home)
        imgfill.pack(fill=BOTH, expand=YES)

################################################################Creating eventloop and entering into first frame+========================================================================================
homepage(ifc)
ifc.mainloop()

