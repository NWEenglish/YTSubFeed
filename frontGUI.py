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
window_height = 600
window_col0_width = window_width - 100


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
        for f in self.frames:
            if f is not cont:
                self.frames[f].grid_hide()

        frame = self.frames[cont]
        frame.tkraise()
        menubar = frame.menubar(self)
        self.configure(menu=menubar)
        try:
            self.frames[cont].grid_show()
        except AttributeError:
            pass


#################### Home Screen ####################
class homePage(tkinter.Frame):
    def __init__(self, parent, controller):
        self.frame = tkinter.Frame.__init__(self, parent)
        self.controller = controller
        self.contentFrame = ScrollableFrame(self.frame)
        self.parent = parent
        self.controller = controller

        row = 1
        for v in backEndMain.allVideosList:
            if v not in backEndMain.deletableVideosList:

                # Video info
                ttk.Label(self.contentFrame.scrollable_frame, text=v.title, font=('-weighted bold', 12),
                          wraplength=window_col0_width).grid(column=0, row=row, padx=10, sticky='w')
                ttk.Label(self.contentFrame.scrollable_frame, text=v.userName, font=('-weighted bold', 10),
                          wraplength=window_col0_width).grid(column=0, row=row+1, padx=10, sticky='w')
                ttk.Label(self.contentFrame.scrollable_frame, text=v.dateUploaded, font=('-weighted bold', 10),
                          wraplength=window_col0_width).grid(column=0, row=row+2, padx=10, sticky='w')

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

                # Button for deletion
                ttk.Button(self.contentFrame.scrollable_frame, text="Delete",
                           command=lambda widget=v: [self.contentFrame.grid_forget(),
                                                     backEndMain.deleteVideo(widget),
                                                     self.__init__(self.parent, self.controller)])\
                    .grid(column=1, row=row, sticky='nw')

                row += 6

        self.contentFrame.grid(column=0, row=1, sticky="ns")

    def menubar(self, root):
        menubar = tkinter.Menu(root)
        
        # Options menu
        optionsMenu = Menu(menubar, tearoff=0)
        optionsMenu.add_command(label="Save")##, command=backEndMain.save)

        optionsMenu.add_command(label="Reload", command=lambda: [self.contentFrame.grid_forget(),
                                                                 backEndMain.load(),
                                                                 self.__init__(self.parent, self.controller)])

        optionsMenu.add_command(label="Pull Videos")##, command=backEndMain.pullVideos)
        menubar.add_cascade(label="Options", menu=optionsMenu)
        
        # Settings options
        settingsMenu = Menu(menubar, tearoff=0)
        settingsMenu.add_command(label="Creators Page", command=lambda: self.controller.showFrame(cPage))
        settingsMenu.add_command(label="Reset Default")##, command=backEndMain.resetToDefault)
        menubar.add_cascade(label="Settings", menu=settingsMenu)
        
        # Sort options
        sortMenu = Menu(menubar, tearoff=0)
        sortMenu.add_command(label="Creator", command=lambda: [self.contentFrame.grid_forget(),
                                                               backEndMain.sortVideoByCreator(),
                                                               self.__init__(self.parent, self.controller)])

        sortMenu.add_command(label="Title", command=lambda: [self.contentFrame.grid_forget(),
                                                             backEndMain.sortVideoByTitle(),
                                                             self.__init__(self.parent, self.controller)])

        sortMenu.add_command(label="Date", command=lambda: [self.contentFrame.grid_forget(),
                                                            backEndMain.sortVideoByDate(),
                                                            self.__init__(self.parent, self.controller)])

        menubar.add_cascade(label="Sort By", menu=sortMenu)
        
        #Return the menubar
        return menubar

    def grid_hide(self):
        self.grid_remove()
        self.contentFrame.grid_remove()

    def grid_show(self):
        self.grid()
        self.contentFrame.grid()


#################### Creator's Page ####################
class cPage(tkinter.Frame):
    def __init__(self, parent, controller):
        self.frame = tkinter.Frame.__init__(self, parent)
        self.controller = controller
        self.contentFrame = ScrollableFrame(self.frame)
        self.parent = parent
        self.controller = controller
        
        row = 1
        for c in backEndMain.allCreatorsList:
            if c not in backEndMain.deletableCreatorsList:

                # Creator info
                ttk.Label(self.contentFrame.scrollable_frame, text=c.name, font=('-weighted bold', 12),
                          wraplength=window_col0_width).grid(column=0, row=row, padx=10, sticky='w')
                ttk.Label(self.contentFrame.scrollable_frame, text="Videos: {}".format(c.videoCounter),
                          font=('-weighted bold', 10),
                          wraplength=window_col0_width).grid(column=0, row=row+1, padx=10, sticky='w')
                ttk.Label(self.contentFrame.scrollable_frame, text="Added on: {}".format(c.dateAdded),
                          font=('-weighted bold', 10),
                          wraplength=window_col0_width).grid(column=0, row=row+2, padx=10, sticky='w')

                # Get image thumbnail
                url = urlopen(c.imageURL)
                raw_data = urlopen(c.imageURL).read()
                url.close()
                img = Image.open(BytesIO(raw_data))
                photo = ImageTk.PhotoImage(img)

                # Make thumbnail into a clickable hyperlink
                label = tkinter.Button(self.contentFrame.scrollable_frame, image=photo,
                                       command=lambda widget=c.channelURL: webbrowser.open_new(widget))
                label.image = photo
                label.grid(column=0, row=row+3, padx=10, sticky='w')

                # Break between entries
                ttk.Label(self.contentFrame.scrollable_frame, text="",
                          font=('-weighted bold', 10)).grid(column=0, row=row + 4, padx=10, sticky='w')
                ttk.Label(self.contentFrame.scrollable_frame, text="-" * 100,
                          font=('-weighted bold', 10)).grid(column=0, row=row + 5, padx=10, sticky='w')

                # Button for deletion
                ttk.Button(self.contentFrame.scrollable_frame, text="Delete",
                           command=lambda widget=c: [self.contentFrame.grid_forget(),
                                                     backEndMain.deleteCreator(widget),
                                                     self.__init__(self.parent, self.controller)])\
                    .grid(column=2, row=row, sticky='nw')

                row += 6

        self.contentFrame.grid(column=0, row=1, sticky="ns")
        
    def menubar(self, root):
        menubar = Menu(root)
        
        #Return to home screen button
        menubar.add_command(label="Home Screen", command=lambda:self.controller.showFrame(homePage))
        
        #Save changes button
        menubar.add_command(label="Save Changes")##, command=backEndMain.save)
    
        #Sort options
        sortMenu = Menu(menubar, tearoff=0)
        sortMenu.add_command(label="Creator Name", command=lambda: [self.contentFrame.grid_forget(),
                                                                    backEndMain.sortCreatorByName(),
                                                                    self.__init__(self.parent, self.controller)])

        sortMenu.add_command(label="Video Count", command=lambda: [self.contentFrame.grid_forget(),
                                                                   backEndMain.sortCreatorByVideos(),
                                                                   self.__init__(self.parent, self.controller)])

        sortMenu.add_command(label="Date Added", command=lambda: [self.contentFrame.grid_forget(),
                                                                  backEndMain.sortCreatorByDate(),
                                                                  self.__init__(self.parent, self.controller)])

        menubar.add_cascade(label="Sort By", menu=sortMenu)

        menubar.add_command(label="Add Creator", command=lambda: self.addCreatorScreen())
            
        #Return the menubar
        return menubar

    def grid_hide(self):
        self.grid_remove()
        self.contentFrame.grid_remove()

    def grid_show(self):
        self.grid()
        self.contentFrame.grid()

    def addCreatorScreen(self):
        window = tkinter.Tk()
        frame = tkinter.Frame(window, width=window_width, height=window_height)

        selection = tkinter.IntVar(frame)

        tkinter.Radiobutton(frame, text="Username", variable=selection, value=1).grid(row=0, column=0, sticky="w")
        tkinter.Radiobutton(frame, text="Channel ID", variable=selection, value=2).grid(row=1, column=0, sticky="w")
        selection.set(1)

        tkinter.Label(frame, text=" " * 5).grid(row=0, column=1)
        tkinter.Label(frame, text=" " * 5).grid(row=1, column=1)

        userInput = tkinter.Entry(frame, width=30)
        userInput.grid(row=0, column=2, sticky="e")
        tkinter.Button(frame, text="Submit", width=10,
                       command=lambda widget=userInput, widget2=selection:
                       self.addCreator(widget.get(), widget2.get())).grid(row=1, column=2, sticky="e")

        frame.grid()

    def addCreator(self, creator, value):
        inListFlag = False

        if value is 1:
            for c in backEndMain.allCreatorsList:
                if c not in backEndMain.deletableCreatorsList:
                    if creator is c.userName:
                        inListFlag = True

            if not inListFlag:
                self.contentFrame.grid_forget()
                backEndMain.addCreator(creator)
                self.__init__(self.parent, self.controller)

        elif value is 2:
            for c in backEndMain.allCreatorsList:
                if c not in backEndMain.deletableCreatorsList:
                    if creator is c.creatorID:
                        inListFlag = True

            if not inListFlag:
                self.contentFrame.grid_forget()
                backEndMain.addCreator_ByID(creator)
                self.__init__(self.parent, self.controller)


# Credit and appreciation out to Jose Salvatierra! This helped us get the major front end feature working.
# https://blog.tecladocode.com/tkinter-scrollable-frames/
class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tkinter.Canvas(self, width=window_width-10, height=window_height-10)
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
backEndMain.load()
app = YouTubeApp()
app.title("YouTube SubFeed")
app.geometry("{}x{}".format(window_width, window_height))
app.mainloop()
