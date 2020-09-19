import tkinter
from tkinter import Menu

gui = tkinter.Tk()
gui.title("Add / Remove Creator")
gui.geometry("600x150")

############# MENU ROW ##############
menubar = Menu(gui)

#Ignore option
menubar.add_command(label="Ignore Changes")

#Save option
menubar.add_command(label="Save Changes")

#Sort option
sortMenu = Menu(menubar, tearoff=0)
sortMenu.add_command(label="Creator Name")
sortMenu.add_command(label="Video Count")
sortMenu.add_command(label="Date Added")
menubar.add_cascade(label="Sort By", menu=sortMenu)

gui.config(menu=menubar)
gui.mainloop()