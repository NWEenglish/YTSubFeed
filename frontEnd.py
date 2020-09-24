import tkinter
from tkinter import Menu

class frontEnd(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        
        #The container holds frames of each screen to be shown.
        #Frames are stacked on top of each other with the visible
        #one placed on top.
        container = tkinter.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames={}
        for f in (homePage, creatorPage):
            pageName = f.__name__
            frame = f(parent=container, controller=self)
            self.frames[pageName]=frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.showFrame("homePage")
    
    #Raised the selected page to the top of the container
    #so that it is visible    
    def showFrame(self, pageName):
        frame = self.frames[pageName]
        frame.tkraise()

#Home page for the application        
class homePage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        
        menubar = Menu(self)
        
        #Settings options
        settingsMenu = Menu(menubar, tearoff=0)
        settingsMenu.add_command(label="Add/Remove Creator",
                                 command=lambda:controller.showFrame("creatorPage"))
        settingsMenu.add_command(label="Reset Default")
        settingsMenu.add_command(label="Retrieve Last 10 Videos")
        menubar.add_cascade(label="Settings", menu=settingsMenu)
        
        #Pull videos button
        menubar.add_command(label="Pull Videos")
        
        #Delete videos button
        menubar.add_command(label="Delete Selected")
        
        #Sort options
        sortMenu = Menu(menubar, tearoff=0)
        sortMenu.add_command(label="Creator")
        sortMenu.add_command(label="Title")
        sortMenu.add_command(label="Date")
        sortMenu.add_command(label="Video Count")
        menubar.add_cascade(label="Sort By", menu=sortMenu)
        
#        menubar.pack()

#Add / Remove creator page for the application
class creatorPage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        
        menubar = Menu(self)
        
        #Back to home button
        menubar.add_command(label="Home Screen", command=lambda:
            controller.showFrame("homePage"))
        
        #Save changes button
        menubar.add_command(label="Save Changes")
        
        #Sort options
        sortMenu = Menu(menubar, tearoff=0)
        sortMenu.add_command(label="Creator Name")
        sortMenu.add_command(label="Video Count")
        sortMenu.add_command(label="Date Added")
        menubar.add_cascade(label="Sort By", menu=sortMenu)
        
#        menubar.pack()

if __name__ == "__main__":
    app = frontEnd()
    app.mainloop()