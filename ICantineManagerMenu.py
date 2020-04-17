from tkinter import ttk
from tkinter import *
from tkinter import filedialog
from shutil import copyfile
from PIL import Image, ImageTk 
import webbrowser
import sys
import os
from ICantineManagerDB import InfoStudentsDB

class ICantineManagerMenu:
    def __init__(self):
        self.root = Tk()
        self.Profile = {1:""}

    def DisplayAllData(self):
        # Display data in treeview object
        for i in self.tree.get_children():
            self.tree.delete(i)
        db = InfoStudentsDB()
        select = db.InfoStudentsQueryAll()
        for row in select:
            self.tree.insert('' , END , values = row)
    
    def SearchByFirstName(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        firstname = self.entryFirstName.get()
        # Initialize DB
        db = InfoStudentsDB()
        select = db.InfoStudentsSearchByFirstName(firstname)
        select = list(select)
        for row in select:
            self.tree.insert('' , END , values = row )
        db.InfoStudentsClose()

    def ResetSearchByFirstName(self):
        self.entryFirstName.delete(0, END)
        self.DisplayAllData()
        

    def SearchByLastName(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        lastname = self.entryLastName.get()
        # Initialize DB
        db = InfoStudentsDB()
        select = db.InfoStudentsSearchByLastName(lastname)
        select = list(select)
        for row in select:
            self.tree.insert('' , END , values = row )
        db.InfoStudentsClose()

    def ResetSearchByLastName(self):
        self.entryLastName.delete(0, END)
        self.DisplayAllData()

    def SearchByClass(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        SClass = self.entryClass.get()
        # Initialize DB
        db = InfoStudentsDB()
        select = db.InfoStudentsSearchByClass(SClass)
        select = list(select)
        for row in select:
            self.tree.insert('' , END , values = row )
        db.InfoStudentsClose()

    def ResetSearchByClass(self):
        self.entryClass.delete(0, END)
        self.DisplayAllData()

    def AddStudent(self):
        Firstname = self.entryFirstName.get()
        Lastname = self.entryLastName.get()
        SClass = self.entryClass.get()
        StudentInfo = (Firstname, Lastname, SClass, "", 0)
        # Initialize DB
        db = InfoStudentsDB()
        db.InfoStudentsAdd(StudentInfo)
        db.InfoStudentsCommit()
        select = db.InfoStudentsQueryAllDesc()
        select = list(select)

        PhotoFilename = self.entryPhoto.get()
        ext = PhotoFilename.split(".")
        id = select[0][0]
        copyfile(PhotoFilename, "images/profile_" +str(id) +"."+ext[len(ext)-1])
        im = Image.open("images/profile_" +str(id) +"."+ext[len(ext)-1])
        rgb_im = im.convert('RGB')
        rgb_im.save("images/profile_" +str(id) + ".jpg")
        PhotoFilename = "profile_" +str(id) + ".jpg"
        db.InfoStudentsModifyPhotoFile(PhotoFilename, id)
        db.InfoStudentsCommit()
        select = db.InfoStudentsQueryAllDesc()
        select = list(select)

        self.tree.insert('' , END , values = select[0] )
        self.entryFirstName.delete(0, END)
        self.entryLastName.delete(0, END)
        self.entryClass.delete(0, END)
        self.entryPhoto.delete(0, END)
        db.InfoStudentsClose()

    def DeleteStudent(self):
        # Initialize DB
        db = InfoStudentsDB()
        idSelect = self.tree.item(self.tree.selection())['values'][0]
        db.InfoStudentsDeleteRecordID(int(idSelect))
        db.InfoStudentsCommit()
        db.InfoStudentsClose()
        self.tree.delete(self.tree.selection())
        # destroy previous image
        self.label_image.destroy()
        # Load default Image
        self.load = Image.open("images/profile.png")
        self.load.thumbnail((130,130))
        self.photo = ImageTk.PhotoImage(self.load)
        self.label_image = Label(self.root,image=self.photo)
        self.label_image.place(x=10, y=350)

    def BrowsePhoto(self):
        self.entryPhoto.delete(0, END)
        filename = filedialog.askopenfilename(initialdir= "/",title="Select File")
        print(filename)  
        self.entryPhoto.insert(END , filename)

    def sortByLastName(self): 
        # clear the treeview
        for i in self.tree.get_children():
            self.tree.delete(i)
        # Initialize DB
        db = InfoStudentsDB()
        select = db.InfoStudentsQueryAllAsc()
        for row in select:
            self.tree.insert('' , END , values = row)
        db.InfoStudentsClose() 

    def treeActionSelect(self, event):
        # destroy previous image
        self.label_image.destroy()
        # load new image
        idSelect = self.tree.item(self.tree.selection())['values'][0]
        FirstnameSelect = self.tree.item(self.tree.selection())['values'][1]
        LastNameSelect = self.tree.item(self.tree.selection())['values'][2]
        ClassSelect = self.tree.item(self.tree.selection())['values'][3]
        NumEntries = self.tree.item(self.tree.selection())['values'][5]
        imgProfile = "images/profile_" + str(idSelect) + "." + "jpg"
        Iload = Image.open(imgProfile)
        Iload.thumbnail((100,100))
        Iphoto = ImageTk.PhotoImage(Iload)
        self.Profile[1] = Iphoto
        lblImage = Label(self.root ,  image = Iphoto)
        lblImage.place(x=10 , y=350)
        lid = Label(self.root, text = "ID : " + str(idSelect))
        lid.place(x = 150, y = 350 , width = 150)
        lfirstname = Label(self.root, text = "First Name: " + FirstnameSelect)
        lfirstname.place(x=150 , y = 380 , width = 150)
        llastname = Label(self.root, text = "Last Name: " + LastNameSelect)
        llastname.place(x = 150 , y = 400 , width = 150)
        lclass = Label(self.root, text="Class: " +  ClassSelect)
        lclass.place(x = 150 , y = 420 , width = 150)
        nentries = Label(self.root, text="Entries: " +  str(NumEntries))
        nentries.place(x = 150 , y = 440 , width = 150)

    #Help Menu
    def Apropos(self):
        webbrowser.open_new("https://websitemaker.fr")

    def Support(self):
        webbrowser.open_new("https://websitemaker.fr/Livechat.html")

    def DrawMenu(self):
        self.root.geometry("800x500")
        self.root.title("ICantine")
        self.root.minsize(800, 500)
        self.root.iconbitmap("Face-ID.ico")
        
        # Add Title
        self.lblTitle = Label(self.root , text = "ICantine Database Manager" , font = ("Arial" , 21) , bg="darkblue" , fg = "white")
        self.lblTitle.place(x=0 , y=0 , width=800)

        # Label & Entry FirstName
        self.lblFirstName = Label(self.root , text = "Firstname:" ,  bg="black" , fg = "white")
        self.lblFirstName.place(x=5 , y = 50 , width = 155)
        self.entryFirstName = Entry(self.root)
        self.entryFirstName.place(x = 170,  y =50 , width=380)
        self.bSearchFName = Button(self.root , text = "Search" , bg="darkblue" , fg = "white" ,  command = self.SearchByFirstName)
        self.bSearchFName.place(x= 560 ,  y = 50 , height = 25)
        self.bSearchFReset = Button(self.root , text = "Reset" , bg="darkblue" , fg = "white" ,  command = self.ResetSearchByFirstName)
        self.bSearchFReset.place(x= 610 ,  y = 50 , height = 25)

        # Label & Entry LastName
        self.lblLastName = Label(self.root , text = "Lastname:" , bg="black" , fg = "white")
        self.lblLastName.place(x=5 , y=80 ,  width = 155 )
        self.entryLastName = Entry(self.root)
        self.entryLastName.place(x = 170,  y =80 , width=380)
        self.bSearchLName = Button(self.root , text = "Search" , bg="darkblue" , fg = "white" ,  command = self.SearchByLastName)
        self.bSearchLName.place(x= 560 ,  y = 80 , height = 25)
        self.bSearchLReset = Button(self.root , text = "Reset" , bg="darkblue" , fg = "white" ,  command = self.ResetSearchByLastName)
        self.bSearchLReset.place(x= 610 ,  y = 80 , height = 25)

        # Label & Entry Class
        self.lblClass = Label(self.root , text = "Class:" , bg="black" , fg = "white")
        self.lblClass.place(x=5 , y=110 ,  width = 155 )
        self.entryClass = Entry(self.root)
        self.entryClass.place(x = 170,  y =110 , width=380)
        self.bSearchSClass = Button(self.root , text = "Search" , bg="darkblue" , fg = "white" ,  command = self.SearchByClass)
        self.bSearchSClass.place(x= 560 ,  y = 110 , height = 25)
        self.bSearchCReset = Button(self.root , text = "Reset" , bg="darkblue" , fg = "white" ,  command = self.ResetSearchByClass)
        self.bSearchCReset.place(x= 610 ,  y = 110 , height = 25)


        # Label & Entry Photo
        self.lblPhoto = Label(self.root , text = "Photo:" , bg="black" , fg = "white")
        self.lblPhoto.place(x=5 , y=140 ,  width = 155 )
        self.bPhoto = Button(self.root , text = "Browse" , bg="darkblue" , fg = "white" ,  command = self.BrowsePhoto )
        self.bPhoto.place(x= 500 ,  y = 140 , height = 25)
        self.entryPhoto = Entry(self.root)
        self.entryPhoto.place(x = 170,  y =143 , width=320)

        # Command Button
        self.bAdd = Button(self.root , text = "Add" , bg="darkblue" , fg = "white" , command = self.AddStudent)
        self.bAdd.place(x= 5 ,  y = 205 , width = 155)

        self.bDelete = Button(self.root , text = "Delete" , bg="darkblue" , fg = "white" , command = self.DeleteStudent)
        self.bDelete.place(x= 5 ,  y = 240 , width = 155)

        self.bExit= Button(self.root , text = "Exit" , bg="darkblue" , fg = "white" , command = quit)
        self.bExit.place(x= 5 ,  y = 275 , width = 155)

        # Load Image
        self.load = Image.open("images/profile.png")
        self.load.thumbnail((130,130))
        self.photo = ImageTk.PhotoImage(self.load)
        self.label_image = Label(self.root,image=self.photo)
        self.label_image.place(x=10, y=350)  

        # Add Treeview
        self.tree = ttk.Treeview(self.root, columns =(1,2,3,4,5,6), height = 5 , show ="headings")
        self.tree.place(x=170, y=170, width = 600, height = 175)
        self.tree.bind("<<TreeviewSelect>>", self.treeActionSelect)

        # Add scrollbar
        self.vsb = ttk.Scrollbar(self.root , orient="vertical",command=self.tree.yview)
        self.vsb.place(x=770, y=168, height=180)
        self.tree.configure(yscrollcommand=self.vsb.set)

        # Add headings
        self.tree.heading(1, text ="ID" )
        self.tree.heading(2, text = "First Name")
        self.tree.heading(3, text = "Last Name")
        self.tree.heading(4, text = "Class")
        self.tree.heading(5, text = "Picture File")
        self.tree.heading(6, text = "Entries")

        #Define column width
        self.tree.column(1, width=30)
        self.tree.column(2, width=100)
        self.tree.column(3, width=100)
        self.tree.column(4, width=30)
        self.tree.column(5, width=100)
        self.tree.column(6, width=30)

        # Display data in treeview object
        self.DisplayAllData()

        #Menu
        self.menubar = Menu(self.root)

        self.menu1 = Menu(self.menubar, tearoff=0)
        self.menu1.add_command(label="Quit", command = quit)
        self.menubar.add_cascade(label="File", menu=self.menu1)

        self.menu3 = Menu(self.menubar, tearoff=0)
        self.menu3.add_command(label="Sort by name", command = self.sortByLastName)
        self.menubar.add_cascade(label="Display", menu=self.menu3)

        self.menu2 = Menu(self.menubar, tearoff=0)
        self.menu2.add_command(label="Support", command = self.Support)
        self.menu2.add_separator()
        self.menu2.add_command(label="About us", command = self.Apropos)
        self.menubar.add_cascade(label="Help", menu=self.menu2)

        self.root.config(menu=self.menubar)
        self.root.mainloop()