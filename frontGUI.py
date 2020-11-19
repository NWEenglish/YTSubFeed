import tkinter
import webbrowser
from io import BytesIO
from tkinter import ttk
from tkinter import Menu
from urllib.request import urlopen
from PIL import Image, ImageTk

# from backEndMain import allCreatorsList, allVideosList
import backEndMain

window_width = 600
window_height = 500


#################### GUI Setup ####################
class YouTubeApp(tkinter.Tk):
    #__init__ function for YouTubeApp
    def __init__(self, *args, **kwargs):
        #__init__ function for Tk class
        tkinter.Tk.__init__(self, *args, **kwargs)
        
        #Create container
        container = tkinter.Frame(self)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid(column=0, row=0, sticky="nsew")

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
        textAreaLabel = tkinter.Label(self, text="Videos", font=('-weighted bold', 18))
        textAreaLabel.grid(column=0, row=0, pady=1, padx=10, sticky='nw')

        self.contentFrame = ScrollableFrame(self.frame)

        row = 1
        backEndMain.load()
        for v in backEndMain.allVideosList:
            ttk.Label(self.contentFrame.scrollable_frame, text=v.title, font=('-weighted bold', 12),
                      wraplength=window_width-50).grid(column=0, row=row, padx=10, sticky='w')
            ttk.Label(self.contentFrame.scrollable_frame, text=v.userName, font=('-weighted bold', 10),
                      wraplength=window_width-50).grid(column=0, row=row+1, padx=10, sticky='w')
            ttk.Label(self.contentFrame.scrollable_frame, text=v.dateUploaded, font=('-weighted bold', 10),
                      wraplength=window_width-50).grid(column=0, row=row+2, padx=10, sticky='w')

            # Get image thumbnail
            url = urlopen(v.imageURL)
            raw_data = urlopen(v.imageURL).read()
            url.close()
            img = Image.open(BytesIO(raw_data))
            photo = ImageTk.PhotoImage(img)

            # Make thumbnail into a clickable hyperlink
            label = tkinter.Button(self.contentFrame.scrollable_frame, image=photo,
                                   command=lambda widget=v.videoURL: webbrowser.open_new(widget))
            label.image = photo
            label.grid(column=0, row=row+3, padx=10, sticky='w')

            # Break between entries
            ttk.Label(self.contentFrame.scrollable_frame, text="",
                      font=('-weighted bold', 10)).grid(column=0, row=row + 4, padx=10, sticky='w')
            ttk.Label(self.contentFrame.scrollable_frame, text="-" * 100,
                      font=('-weighted bold', 10)).grid(column=0, row=row + 5, padx=10, sticky='w')

            row = row + 6

        self.contentFrame.grid(column=0, row=1, sticky="ns")

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
        canvas = tkinter.Canvas(self, width=window_width-10, height=window_height-50)
        vertical_scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        horizontal_scrollbar = ttk.Scrollbar(self, orient="horizontal", command=canvas.xview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=vertical_scrollbar.set)
        canvas.configure(xscrollcommand=horizontal_scrollbar.set)

        canvas.grid(column=0, row=0)
        vertical_scrollbar.grid(column=0, row=0, sticky="nse")
        # horizontal_scrollbar.grid(column=0, row=0, sticky="swe")


#################### Driver Code ####################
app = YouTubeApp()
app.title("YouTube SubFeed")
app.geometry("{}x{}".format(window_width, window_height))
app.mainloop()
