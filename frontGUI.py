import tkinter
from io import BytesIO
from tkinter import scrolledtext, ttk
from tkinter import Menu
from urllib.request import urlopen
from PIL import Image
from PIL import ImageTk

import CreatorAndVideoObjects
# from backEndMain import allCreatorsList, allVideosList
import backEndMain

#################### GUI Setup ####################
class YouTubeApp(tkinter.Tk):
    #__init__ function for YouTubeApp
    def __init__(self, *args, **kwargs):
        #__init__ function for Tk class
        tkinter.Tk.__init__(self, *args, **kwargs)
        
        #Create container
        container = tkinter.Frame(self)
        # container.pack(side="top", fill="both", expand=True)
        container.grid(column=0, row=0)
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
        self.frame = tkinter.Frame.__init__(self, parent)
        self.controller = controller
        
        #################### Text Area ####################
        textAreaLabel = tkinter.Label(self, text="Videos", font = ('-weighted bold', 10))
        textAreaLabel.grid(column=0, row=0, pady=1, padx=1, sticky='W')

        self.contentFrame = ScrollableFrame(self.frame)

        displayedCreatorsList = []
        row = 5
        backEndMain.load()
        for c in backEndMain.allVideosList:
            ttk.Label(self.contentFrame.scrollable_frame, text=c.title, font=('-weighted bold', 10)).grid(column=0, row=row, sticky='nw')
            ttk.Label(self.contentFrame.scrollable_frame, text=c.userName, font=('-weighted bold', 10)).grid(column=0, row=row+1, sticky='nw')
            ttk.Label(self.contentFrame.scrollable_frame, text=c.dateUploaded, font=('-weighted bold', 10)).grid(column=0, row=row+2, sticky='nw')

            # Image thumbnail
            url = urlopen(c.imageURL)
            raw_data = urlopen(c.imageURL).read()
            url.close()

            img = Image.open(BytesIO(raw_data))
            photo = ImageTk.PhotoImage(img)

            label = tkinter.Label(self.contentFrame.scrollable_frame , image=photo)
            label.image = photo
            label.grid(column=0, row=row+3, sticky='nw')

            ttk.Label(self.contentFrame.scrollable_frame, text="", font=('-weighted bold', 10)).grid(column=0, row=row+4, sticky='nw')
            row = row + 5

            # displayedCreatorsList.append(ttk.Label(videoFrame.scrollable_frame, text=c.title, font=('-weighted bold', 10)))
            # displayedCreatorsList.append(ttk.Label(videoFrame.scrollable_frame, text=c.videoID, font=('-weighted bold', 10)))

            # displayedCreatorsList[len(displayedCreatorsList)-2].grid(column=0, row=row, pady=5, padx=10, sticky='W')
            # displayedCreatorsList[len(displayedCreatorsList)-1].grid(column=0, row=row+1, pady=5, padx=10, sticky='W')

        self.contentFrame.grid(column=0, row=1)


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

        # textArea = tkinter.scrolledtext.ScrolledText(self, width=45, height=11)
        # textArea.grid(column=0, row=1, padx=10, columnspan=5, rowspan=5)
        
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


# Credit and appreciation out to Jose Salvatierra! This helped us get the major front end feature working.
# https://blog.tecladocode.com/tkinter-scrollable-frames/
class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tkinter.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # canvas.pack(side="left", fill="both", expand=True)
        # scrollbar.pack(side="right", fill="y")

        canvas.grid(column=0, row=0, rowspan=20)
        scrollbar.grid(column=0, row=0, rowspan=20, columnspan=20, sticky="e")


#################### Driver Code ####################
app = YouTubeApp()
app.title("YouTube SubFeed")
app.geometry("600x500")
app.mainloop()