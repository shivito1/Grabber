from Tkinter import *
import os,subprocess,threading,ttk, tkFileDialog, win32api
from os import environ
from os import walk
from threading import Thread
class Bkgrabber:
	def __init__(self,root):
		self.root = root
		root.wm_title("JSPrograms")
		
		w = 350 # width for the Tk root
		h = 250 # height for the Tk root
		
		# get screen width and height
		ws = root.winfo_screenwidth() # width of the screen
		hs = root.winfo_screenheight() # height of the screen

		# calculate x and y coordinates for the Tk root window
		x = (ws) / (3)
		y = (hs) / (3)

		# set the dimensions of the screen 
		# and where it is placed
		root.geometry('%dx%d+%d+%d' % (w, h, x, y))
		root.configure(background="#4d4dff")
		
		# If this value is set to 1 then C:Drive will be added to backup
		self.Scanc = 0
		self.formtable()#main application GUI
		self.root.mainloop()

	def callback(self,*args):   # Checks Grabber fields and changes input
		
		ut = self.cbox.get()
		ut = ut.replace("\\", "")
		switchit = self.e2.get()
		self.e2.delete(0, END)
		self.e2.insert(END, switchit.replace('/','\\'))

		self.e.delete(0, END)
		self.e.insert(END, ut)
		
		self.Combo_e1()
		
	def Combo_e1(self,*args):
		try:				
			ut = self.cbox1.get()
			self.e1.delete(0, END)
			self.e1.insert(END, ut)
		except AttributeError:
			print "No user selected"
			pass
		
		try:
			pc = "\\\\" + self.e.get() + "\\C$\\users"
			if os.path.isdir(pc):
				# Usernames for e1 textbox
				get_e = self.e.get()
				pc = "\\\\" + get_e + "\\C$\\users"
				self.usernames = os.walk(pc).next()[1]
				#Combobox for entry 2	
				self.cbox1 = ttk.Combobox(self.root,value=self.usernames, textvariable=self.var2)
				self.cbox1.bind("<Button-1>", self.Clearentry)
				self.cbox1.grid(row=2,column=0,columnspan=5,sticky="w",padx=20)
				
			else:
				pc = self.e.get()
				if os.path.isdir(pc):
					self.usernames = os.walk(pc).next()[1]

					print "yes"
				else:
					print "no"
		except UnboundLocalError:
			print "No path found"
			pass

	def formtable(self):
		self.network = subprocess.Popen('net view', stdout=subprocess.PIPE).communicate()
		self.device = str(self.network)
		self.device1 = []
		self.device2 =[]
		
		self.device = tuple(filter(None, self.device.split('\\n')))
		for item in self.device:		# Removes new line and other unwanted charicters "\n","\r"," "	
			self.device1.append(item.replace('\n', '').replace('\\r', '').replace(' ',''))
			self.device = self.device1
		
# Add attached drives
		drives = win32api.GetLogicalDriveStrings()
		drives = drives.split('\00')[:-1]
		for i in drives:
			self.device2.append(i)
			
		self.device2.append("localhost")
		for item in self.device:        # Removes unwanted "\\" this is added to the network location later.
			if item.startswith("\\\\"):	
				self.device2.append(re.sub('\\\\', '', item))
				self.device = self.device2
				
				
		
		
		
		
		
		self.var = StringVar()
		self.var.trace("w", self.callback)
		self.var2 = StringVar()
		self.var2.trace("w", self.callback)
		self.var3 = StringVar()
		self.var3.trace("w", self.callback)
		self.var4 = 1
		
		
		# Entry fields
		self.e = ttk.Entry(self.root,width=20,)
		self.e1 = ttk.Entry(self.root,width=20)
		self.e2 = ttk.Entry(self.root,width=35, textvariable=self.var3)
		
			
		
		lb = Label(text="Grabber",font="Comic 24",bg="#4d4dff")
		lb.grid(row=0,column=0,columnspan=5,sticky="w")
		
		self.e.grid(row=1,column=0,columnspan=1,sticky="w",padx=20)
		self.e.bind("<Button-1>", self.Clearentry)
		self.e.insert(END, "Select PC Name")
		
		#Combobox for entry 1	
		self.cbox = ttk.Combobox(self.root,value=self.device, textvariable=self.var)
		self.cbox.bind("<Button-1>", self.Clearentry)
		self.cbox.grid(row=1,column=0,columnspan=5,sticky="w",padx=20)
		
		# Set Var to Host Name/IP Address
		self.var.set("Select PC Name")
		
		
		self.e1.bind("<Button-1>", self.Clearentry2)
		self.e1.insert(END, "Select UserName")
		
		
		
		
		self.e2.bind("<Button-1>", self.Clearentry3)
		self.e2.insert(END, "Destination")
		self.e2.grid(row=3,column=0,columnspan=1,sticky="w",padx=20)
		# Remove or add network Combobox
		self.bt = ttk.Button(self.root, text="Browse", command=self.Filelookup)
		self.bt.grid(row=3,column=1,columnspan=2,sticky="w")
		self.b = ttk.Button(text="Backup",command=self.Varcomputer)
		
		b2 = ttk.Button(text="Get Folders",command=self.Scancdef)
		b2.grid(row=5,column=0,pady=5)
		
		
		
		self.listbox = Listbox(self.root,bg="gray",height=8,width=25)
	
		self.listbox.grid(row=5,rowspan=20,column=0,columnspan=5,sticky="e")
		
		self.listbox.insert(END, "Items in Backup:")

	def Netbox(self): # Remove or add network Combobox
		if self.var4 == 1:
			self.cbox.grid_forget()
		elif self.var4 == 2:
			self.cbox.grid(row=1,column=0,columnspan=5,sticky="w",padx=20)
		else:
			"this is bad"
		if self.var4 == 1:
			self.var4 = 2
		elif self.var4 == 2:
			self.var4 = 1
		else:
			"this is bad too"
		
		
	def Filelookup(self):
		self.e2.delete(0, END)
		self.dirpath = tkFileDialog.askdirectory()
		self.e2.insert(END, self.dirpath)
	def Clearentry(self,*args):
		if self.var.get() == "Select PC Name":
			self.var.set("")
		elif self.var.get() == "":
			self.var.set("Select PC Name")
		else:
			print "New entry found"
		
	def Clearentry2(self,*args):
		if self.e1.get() == "Select UserName":
			self.e1.delete(0, END)
		elif self.e1.get() == "":
			self.e1.insert(END, "Select UserName")
		else:
			print "New entry found2"
	def Clearentry3(self,*args):
		if self.e2.get() == "Destination":
			self.e2.delete(0, END)
		elif self.e2.get() == "":
			self.e2.insert(END, "Destination")
		else:
			print "New entry found3"
	def Varcomputer(self):
		self.Client = self.e.get()
		self.Username = self.e1.get()
		self.Destination = self.e2.get()
		
		self.Run_backup()

	def Run_backup(self):
		if os.path.isdir("\\\\" + self.Client + "\\C$\\users\\" + self.Username + '\\'):
			self.userpath = "\\\\" + self.Client + "\\C$\\users\\" + self.Username + '\\'
			path = "\\\\" + self.Client + "\\C$"
		else:
			self.userpath = self.Client
			path = self.Client

		for item in self.UserFiles:
			os.system(r"xcopy /E /Y /C /I " + self.userpath + "\\" + "\"" + item + "\"" + " " + "\"" + self.Destination + "\\" + "Userfiles\\" + item + "\"")
		if self.Scanc == 1:		
			for item in self.knockoutlist:
				os.system(r"xcopy /E /Y /C /I " + path + "\\" + "\"" + item + "\"" + " " + "\"" + self.Destination + "\\" + "C-drive\\" + item + "\"")
		else:
			pass
		
	
		print "-------------------------------- Backup Finished ---------------------"
		
		self.create_window()
	def Scancdef(self):
		def rmvlist(event):
			m = str(self.listbox.get(ACTIVE))
			self.listbox.delete(1,END)
			if m in self.knockoutlist:
				print "here1"
				self.listbox.delete(ANCHOR)
				self.knockoutlist
				new = []
				for i in self.knockoutlist:
					if i != m:
						new.append(i)
				self.knockoutlist = new
				print self.knockoutlist
			elif m in self.UserFiles:
				print "here2"
				self.listbox.delete(ANCHOR)
				self.UserFiles
				new = []
				for i in self.UserFiles:
					if i != m:
						new.append(i)
				self.UserFiles = new
				print self.UserFiles
			else:
				print "here3"
				pass
			for i in self.UserFiles:
				self.listbox.insert(END,i)
			for i in self.knockoutlist:
				self.listbox.insert(END,i)

		self.b.grid(row=6,column=0,pady=5)
		self.listbox.delete(1,END)
		self.Client = self.e.get()
		self.Username = self.e1.get()
		self.Destination = self.e2.get()
		try:
			path = "\\\\" + self.Client + "\\C$"
			userpath = "\\\\" + self.Client + "\\C$\\users\\" + self.Username
			path2 = ['Program Files (x86)', 'ProgramData', 'Windows', 'Users', 'Temp', 'Python27', 'eagle', '$Windows.~WS', '$Recycle.Bin']
			path3 = os.walk(path).next()[1]
		except StopIteration:
# If Drive letter selected
			path = self.Client
			path3 = os.walk(path).next()[1]
		self.path3c = path3
		self.knockoutlist = []
		self.UserFiles = []
		
		try:
			Walkuser = os.walk(userpath).next()[1]
			for item in Walkuser:
				self.UserFiles.append(item)
		except StopIteration:
			pass

		
		for item in path3:
			if item not in path2:
				self.knockoutlist.append(item)
		print self.knockoutlist
				
		for f in self.UserFiles:
			self.listbox.insert(END,f)		
				
		for f in self.knockoutlist:
			self.listbox.insert(END, f)
			
		self.listbox.bind("<Double-Button-1>", rmvlist)
		self.Scanc = 1
		
		self.listbox.bind("<Control-backslash>",self.Open_destination)
		
	def Open_destination(self,event):
		subprocess.Popen('explorer ' + self.Destination)
		print self.Destination
	def create_window(self):
		self.Sourse = "\\\\" + self.Client + "\\C$\\users\\" + self.Username + "\\Documents"
		self.Sourse1 = "\\\\" + self.Client + "\\C$\\users\\" + self.Username + "\\Pictures"
		self.Sourse2 = "\\\\" + self.Client + "\\C$\\users\\" + self.Username + "\\Desktop"
		
		self.Nobk = []
		self.g = []
		self.h = []
		cfulldir = []
		fullpath1 = []
		self.fullpath2 = []

		for item in self.UserFiles:
			letitgo = os.walk(self.userpath + item)
			for root, dirs, files in letitgo:
				for f in files:
					fullpath1.append(os.path.join(root,f))
					self.h.append(f)
		if self.Scanc == 1:
			for item in self.knockoutlist:
				letitgo = os.walk("\\\\" + self.Client + "\\C$\\" + item)
				for root, dirs, files in letitgo:
					for f in files:
						fullpath1.append(os.path.join(root,f))
						self.h.append(f)
						
		else:
			pass

		list_files = os.walk(self.Destination)
		for root, dirs, files in list_files:
			for f in files:
				self.fullpath2.append(os.path.join(root,f))
				self.g.append(f)
				
		for item in fullpath1:
			head, tail = os.path.split(item)
			if tail not in self.g:
				if tail.endswith('.ini'):
					pass
				else:
					self.Nobk.append(item)
				
		self.Window()
	def Window(self):

		def listupdate(*args):

			listselect = str(listbox.get(ACTIVE))
			head, tail = os.path.split(listselect)
			subprocess.Popen('explorer /select, ' + listselect)
			print head
				
		top = Toplevel()
		top.title("Not in Backup")
		#top.geometry('100x150')
		w = 300 # width for the Tk root
		h = 100 # height for the Tk root
		# get screen width and height
		ws = top.winfo_screenwidth() # width of the screen
		hs = top.winfo_screenheight() # height of the screen

		# calculate x and y coordinates for the Tk root window
		x = (ws) / (3)
		y = (hs) / (2)

		# set the dimensions of the screen 
		# and where it is placed
		top.geometry('%dx%d+%d+%d' % (w, h, x, y))
		scrollbar = Scrollbar(top)
		scrollbar.pack(side=RIGHT, fill=Y)

		xscrollbar = Scrollbar(top, orient=HORIZONTAL)
		xscrollbar.pack(side=BOTTOM, fill=X)

		
		listbox = Listbox(top, yscrollcommand=scrollbar.set,xscrollcommand=xscrollbar.set,width=300)
		listbox.insert(END, '--------------Folders Backed up--------------')
		
		id1 = 1
		while True:
			if self.listbox.get(id1) != '':
				listbox.insert(END, '-' + self.listbox.get(id1))
				print listbox.get(id1)
			else:
				break
			id1 += 1
			
		listbox.insert(END, '--------------!Missing!--------------')
		for self.Nobk in self.Nobk:
			listbox.insert(END, self.Nobk)
		listbox.pack(side=LEFT, fill=BOTH)
		listbox.bind("<Double-Button-1>", lambda e: listupdate())
		listbox.bind("<Control-backslash>", lambda e: self.create_window())
		
		scrollbar.config(command=listbox.yview)
		xscrollbar.config(command=listbox.xview)
		
		
Bkgrabber(Tk())
