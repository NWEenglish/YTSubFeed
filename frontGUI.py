import tkinter
from tkinter import scrolledtext
from tkinter import Menu

#################### GUI Setup ####################
class YouTubeApp(tkinter.Tk):
    #__init__ function for YouTubeApp
    def __init__(self, *args, **kwargs):
        #__init__ function for Tk class
        tkinter.Tk.__init__(self, *args, **kwargs)
        
        #Create container
        container = tkinter.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        #Initialize frames in empty array
        self.frames = {}
        
        #Iterate through frame layouts
        for F in (homePage, cPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        #Initially show home screen
        self.showFrame(homePage)
        
    #Display desired frame by moving it to the front
    def showFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        menubar = frame.menubar(self)
        self.configure(menu=menubar)

#################### Home Screen ####################
class homePage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        
        #################### Text Area ####################
        textAreaLabel = tkinter.Label(self, text="Videos", font = ('-weighted bold', 10))
        textAreaLabel.grid(column=0, row=0, pady=10, padx=10, sticky='W')

        textArea = tkinter.scrolledtext.ScrolledText(self, width=45, height=11)
        textArea.grid(column=0, row=1, padx=10, columnspan=5, rowspan=5)
        
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
        settingsMenu.add_command(label="Add/Remove Creator", command=lambda: self.controller.showFrame(cPage))
        settingsMenu.add_command(label="Reset Default")##, command=backEndMain.resetToDefault)
        menubar.add_cascade(label="Settings", menu=settingsMenu)
        
        # Sort options
        sortMenu = Menu(menubar, tearoff=0)
        sortMenu.add_command(label="Creator")##, command=backEndMain.sortVideoByCreator)
        sortMenu.add_command(label="Title")##, command=backEndMain.sortVideoByTitle)
        sortMenu.add_command(label="Date")##, command=backEndMain.sortVideoByDate)
        menubar.add_cascade(label="Sort By", menu=sortMenu)
        
        #Return the menubar
        return menubar
        
#################### Creator's Page ####################
class cPage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        
        #################### Text Area ####################
        textAreaLabel = tkinter.Label(self, text="Videos", font = ('-weighted bold', 10))
        textAreaLabel.grid(column=0, row=0, pady=10, padx=10, sticky='W')

        textArea = tkinter.scrolledtext.ScrolledText(self, width=45, height=11)
        textArea.grid(column=0, row=1, padx=10, columnspan=5, rowspan=5)
        
    def menubar(self, root):
        menubar = Menu(root)
        
        #Return to home screen button
        menubar.add_command(label="Home Screen", command=lambda:self.controller.showFrame(homePage))
        
        #Save changes button
        menubar.add_command(label="Save Changes")##, command=backEndMain.save)
    
        #Sort options
        sortMenu = Menu(menubar, tearoff=0)
        sortMenu.add_command(label="Creator Name")##, command=backEndMain.sortCreatorByName)
        sortMenu.add_command(label="Video Count")##, command=backEndMain.sortCreatorByVideos)
        sortMenu.add_command(label="Date Added")##, command=backEndMain.sortCreatorByDate)
        menubar.add_cascade(label="Sort By", menu=sortMenu)
            
        #Return the menubar
        return menubar
        
#################### Driver Code ####################
app = YouTubeApp()
app.title("YouTube SubFeed")
app.geometry("400x250")
app.mainloop()