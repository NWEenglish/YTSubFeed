import tkinter
from tkinter import Menu

gui = tkinter.Tk()
gui.title("YouTube Sub Feeder")
gui.geometry("600x250")

#################### MENU ROW #######################
menubar = Menu(gui)

#Settings - ADD COMMANDS
settingsMenu = Menu(menubar, tearoff=0)
settingsMenu.add_command(label="Add/Remove Creator")
settingsMenu.add_command(label="Reset Default")
settingsMenu.add_command(label="Retrieve Last 10 Videos")
menubar.add_cascade(label="Settings", menu=settingsMenu)

#Pull video option - ADD COMMAND
menubar.add_command(label="Pull Videos")

#Delete videos option - ADD COMMAND
menubar.add_command(label="Delete Selected")

#Sort by - ADD COMMANDS
sortMenu = Menu(menubar, tearoff=0)
sortMenu.add_command(label="Creator")
sortMenu.add_command(label="Title")
sortMenu.add_command(label="Date")
sortMenu.add_command(label="Video Count")
menubar.add_cascade(label="Sort By", menu=sortMenu)

gui.config(menu=menubar)
gui.mainloop()