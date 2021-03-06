import tkinter
from tkinter import Menu
from tkinter import scrolledtext
##import backEndMain


class frontEnd(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        
        # The container holds frames of each screen to be shown.
        # Frames are stacked on top of each other with the visible
        # one placed on top.
        container = tkinter.Frame(self)
        container.pack(side="top", fill="both")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames={}
        for f in (homePage, creatorPage):
            pageName = f.__name__
            frame = f(parent=container, controller=self)
            self.frames[pageName]=frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.showFrame("homePage")
    
    # Raised the selected page to the top of the container
    # so that it is visible
    def showFrame(self, pageName):
        frame = self.frames[pageName]
        frame.tkraise()
        menubar = frame.menubar(self)
        contentList = scrolledtext.ScrolledText(self)
        contentList.grid(row=0, column=0)
        self.configure(menu=menubar)


# Home page for the application
class homePage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        
    def menubar(self, root):
        menubar = tkinter.Menu(root)
        
        # Options menu
        optionsMenu = Menu(menubar, tearoff=0)
        optionsMenu.add_command(label="Save")##, command=backEndMain.save)
        optionsMenu.add_command(label="Reload")##, command=backEndMain.load)
        optionsMenu.add_command(label="Pull Videos")##, command=backEndMain.pullVideos)
        optionsMenu.add_command(label="Delete Selected")
        menubar.add_cascade(label="Options", menu=optionsMenu)
        
        # Settings options
        settingsMenu = Menu(menubar, tearoff=0)
        settingsMenu.add_command(label="Add/Remove Creator",
                             command=lambda:self.controller.showFrame("creatorPage"))
        settingsMenu.add_command(label="Reset Default")##, command=backEndMain.resetToDefault)
        menubar.add_cascade(label="Settings", menu=settingsMenu)
        
        # Sort options
        sortMenu = Menu(menubar, tearoff=0)
        sortMenu.add_command(label="Creator")##, command=backEndMain.sortVideoByCreator)
        sortMenu.add_command(label="Title")##, command=backEndMain.sortVideoByTitle)
        sortMenu.add_command(label="Date")##, command=backEndMain.sortVideoByDate)
        menubar.add_cascade(label="Sort By")##, menu=sortMenu)
            
        return menubar

    def contentList(self, root):
        contentList = scrolledtext.ScrolledText(root, width=300, height=200)
        contentList.focus()
        return contentList
        

# Add / Remove creator page for the application
class creatorPage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        
    def menubar(self, root):
        menubar = Menu(self)
        
        # Back to home button
        menubar.add_command(label="Home Screen", command=lambda:
            self.controller.showFrame("homePage"))
        
        # Save changes button
        menubar.add_command(label="Save Changes")##, command=backEndMain.save)
        
        # Sort options
        sortMenu = Menu(menubar, tearoff=0)
        sortMenu.add_command(label="Creator Name")##, command=backEndMain.sortCreatorByName)
        sortMenu.add_command(label="Video Count")##, command=backEndMain.sortCreatorByVideos)
        sortMenu.add_command(label="Date Added")##, command=backEndMain.sortCreatorByDate)
        menubar.add_cascade(label="Sort By", menu=sortMenu)
            
        return menubar
    
    def contentList(self, root):
        contentList = scrolledtext.ScrolledText(root)
        return contentList


if __name__ == "__main__":
    ##backEndMain.load()
    app = frontEnd()
    app.title("YouTube SubFeed")
    app.geometry("400x250")
    app.mainloop()