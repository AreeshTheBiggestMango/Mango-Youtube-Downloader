from tkinter import *
from tkinter import filedialog
from pytube import YouTube
import threading
import os
from os import path
from functools import partial

# This class runs the main program itself with all of the respective widgets


class Main():
    def __init__(self, parent):
        # Frame Setup
        background_color = "#282828"
        ytred = "#8a1111"
        self.downloader_frame = Frame(
            parent, bg=background_color, padx=10, pady=10)
        self.downloader_frame.grid(sticky=NSEW)

        # Downloader Heading
        self.heading_label = Label(self.downloader_frame, text="Youtube Downloader",
                                   font=("arial", "18", "bold"), bg=ytred, fg="white",
                                   padx=10, pady=10, justify=CENTER, borderwidth=4, relief="solid")
        self.heading_label.grid(
            row=0, columnspan=2, column=0, padx=10, pady=10)
        # Button to toggle between light/dark mode

        # URL Box
        self.url_box = Entry(self.downloader_frame, width=50,
                             bg=ytred, fg="white", font="arial 12", borderwidth=2, relief="solid")
        self.url_box.bind("<Button-1>", lambda e: self.url_box.delete(0, END))
        self.url_box.insert(0, "  Insert URL Here:  ")
        self.url_box.grid(row=1, sticky=W, padx=10, pady=10)

        # Menu to allow right click context menu
        self.m = Menu(self.downloader_frame, tearoff=0)

        # For cut, copy and paste
        self.m.add_command(label="Cut", command=lambda: cut_text(self))
        self.m.add_command(label="Copy", command=lambda: copy_text(self))
        self.m.add_command(label="Paste", command=lambda: paste_text(self))

        # Generates the event which opens the context menu on right click
        def do_popup(event):
            try:
                self.m.tk_popup(event.x_root, event.y_root)
            finally:
                self.m.grab_release()
        self.url_box.bind("<Button-3>", do_popup)

        # Download Button
        self.download_button = Button(
            self.downloader_frame, text="Download", padx=5, pady=5, bg=ytred, fg="white", font="arial 12",
            command=lambda: startThreadProcess(self),
            borderwidth=4, relief="solid", activebackground=ytred, activeforeground="white")
        self.download_button.grid(
            row=1, column=1, sticky=W, padx=10, pady=10)

        # Selection Dropdown Menu
        file_types = ["MP4", "MP3"]
        tkvarq = StringVar(self.downloader_frame)

        # Generates a generic variable which can be assigned to the first variable in the dropdown menu
        tkvarq.set(file_types[0])

        # Sets up the OptionMenu widget
        self.drop_menu = OptionMenu(
            self.downloader_frame, tkvarq, *file_types)
        self.drop_menu.config(bg=ytred, fg="white",
                              font="arial 12", relief="solid", activebackground="#323232")
        self.drop_menu["menu"].config(
            bg=ytred, font="arial 12", relief="solid", fg="white", )
        self.drop_menu["borderwidth"] = 0
        self.drop_menu.grid(row=2, sticky=W, padx=10, pady=10)

        # Widget for the url box
        path = StringVar()
        self.file_directory = Entry(self.downloader_frame, bg=ytred, fg="white",
                                    font="arial 12", borderwidth=2, relief="solid", textvariable=path)
        self.file_directory.grid(row=3, sticky=W, padx=10, pady=10)

        # Help Button
        self.help_button = Button(self.downloader_frame, text="Help", padx=5, pady=5,
                                  bg=ytred, fg="white", font="arial 12",
                                  borderwidth=2, relief="solid", command=lambda: get_help(self),
                                  activebackground=ytred, activeforeground="white")
        self.help_button.grid(row=3, column=1, padx=0, pady=10)

        # Terms and Conditions Button
        self.TNC_button = Button(self.downloader_frame, text="T & C", padx=5, pady=5,
                                 bg=ytred, fg="white", font="arial 12",
                                 borderwidth=2, relief="solid", command=lambda: get_tnc(self),
                                 activebackground=ytred, activeforeground="white")
        self.TNC_button.grid(row=3, sticky=E, padx=0, pady=10)

        # Explore button
        self.explore_button = Button(self.downloader_frame, text="Browse", padx=5, pady=5,
                                     bg=ytred, fg="white", font="arial 12",
                                     borderwidth=2, relief="solid", height=1, command=lambda: find_directory(self),
                                     activebackground=ytred, activeforeground="white")
        self.explore_button.grid(row=3, sticky=W, padx=215, pady=0)

        # Configurable text
        self.progress_label = Label(self.downloader_frame, text="",
                                    bg=background_color, padx=0, pady=5, fg="white", font="arial 12", wraplength=450)
        self.progress_label.grid(row=4, sticky=W, padx=5, pady=5)

        # Downloading Functions
        def onClick():
            # Grabs the URL from the entry box for the URL, and also\
            # Grabs the file directory the user entered that they want to download to
            urlname = self.url_box.get()
            got_path = self.file_directory.get()
            try:
                # Checks if the Youtube URL is valid and configures text
                yt = YouTube(str(urlname))
                self.progress_label.configure(
                    text="Now downloading: " + yt.title, fg="white")
            except:
                # If the URL is invalid, prompts the user
                print("Fail")
                self.progress_label.configure(
                    text="Could not find video, Please try again!", fg="red")
            else:
                # If the try loop passes and URL is valid, then downlaods video
                # Grabs the file format from the dropmenu
                file_format = tkvarq.get()
                print(file_format)
                # Downloads file as MP4
                if file_format == "MP4":
                    # Gets the highest stream quality
                    vid = yt.streams.get_highest_resolution()
                    _destination = str(got_path)
                    # Downloads the video to the respective destination
                    vid.download(_destination)
                    self.progress_label.configure(
                        text="Downloading: " + yt.title + "\t", fg="white")
                    # Opens the directory the file has been downloaded to
                    os.startfile(got_path)
                    print('"', yt.title, '"', "has finished downloading")
                    self.progress_label.configure(
                        text=yt.title + " has finished downloading!" "\t", fg="green")
                # Downloads file as MP3
                elif file_format == "MP3":
                    # Filters YT streams by audio only
                    vid = yt.streams.filter(only_audio=True).first()
                    _destination = str(got_path)
                    # Sets the output to the file destination
                    output = vid.download(_destination)
                    # Downloads the video to the destination
                    vid.download(_destination)
                    # Opens the directory the file has been downloaded to
                    os.startfile(got_path)
                    # Changes the file format from MP4 to MP3
                    base, ext = os.path.splitext(output)
                    new_file = base + '.mp3'
                    os.rename(output, new_file)
                    print('"', yt.title, '"', "has finished downloading")
                    self.progress_label.configure(
                        text=yt.title + " has finished downloading!" "\t", fg="green")

        # Function to start the threading process\
        # to allow the program to run the GUI and Download functions simultaneously
        def startThreadProcess(self):
            myNewThread = threading.Thread(target=onClick)
            myNewThread.start()
            print("Threading Started")

        # Function to grab the inputted file directory
        def find_directory(self):
            open_file = filedialog.askdirectory()
            print(open_file)
            if os.path.isdir(open_file) == True:
                self.file_directory.insert(0, open_file)
            else:
                self.progress_label.configure(
                    text="Inputted directory is not valid!", fg=ytred)

        # Function to execute the help class window
        def get_help(self):
            get_help = Help(self)
            get_help.help_text.configure(
                text="Enter the URL of the video you wish to download into the URL box,\
                     then select the file format you wish to download as, select the directory by clicking browse, and click Download.", font="arial 12", fg="white")

        # Function to execute the terms and conditions class window
        def get_tnc(self):
            get_tnc = Terms(self)
            get_tnc.tnc_text.configure(
                text="I respect the intellectual property rights of others. You may infringe copyright or trademark laws if you were to download contentthat does not belong to you, and in this event, I am not to be held liable. This program should not use used as a means for piracy, and should only be used to download ones own content from the YouTube platform,which I have no affiliation with. ",
                font="arial 12", fg="white")

        # Allows user to paste text using context menu
        def paste_text(self):
            my_text = root.clipboard_get()
            self.url_box.delete(0, "end")
            self.url_box.insert(0, my_text)

        # Allows user to copy text using context menu
        def copy_text(self):
            root.clipboard_clear()
            my_text = self.url_box.selection_get()
            root.clipboard_append(my_text)

        # Allows user to cut text using context menu
        def cut_text(self):
            root.clipboard_clear()
            my_text = self.url_box.selection_get()
            if my_text == "":
                print("No text to cut")
            root.clipboard_append(my_text)
            self.url_box.delete(0, "end")

# Class for help window


class Help:
    def __init__(self, parent):
        # Disabling the state of buttons
        parent.help_button.configure(state=DISABLED)
        parent.download_button.configure(state=DISABLED)
        parent.TNC_button.configure(state=DISABLED)
        parent.explore_button.configure(state=DISABLED)

        # Variables for colour palettes
        background_color = "#282828"
        ytred = "#8a1111"

        # Sets the help box as a window above the main window
        self.help_box = Toplevel()

        # Allows the window to be proportional if stretched
        self.help_box.columnconfigure(0, weight=1)
        self.help_box.rowconfigure(0, weight=1)
        self.help_frame = Frame(
            self.help_box, width=300, bg=background_color)
        self.help_frame.grid(sticky=NSEW)

        # Allows the window to be proportional if stretched
        self.help_frame.columnconfigure(0, weight=1)
        self.help_frame.rowconfigure(0, weight=1)

        # For closing unnecessary windows
        self.help_box.protocol(
            'WM_DELETE_WINDOW', partial(self.close_help, parent))

        # Instructions Heading
        self.how_heading = Label(
            self.help_frame, text="Help / Instructions", font="arial 12 bold",
            bg=ytred, fg="white", borderwidth=4, relief=SOLID, padx=10, pady=10)
        self.how_heading.grid(row=0, padx=10, pady=10)

        # Help Text
        self.help_text = Label(self.help_frame, text="",
                               justify=CENTER, width=40, bg=background_color, wrap=250)
        self.help_text.grid(column=0, row=1)

        # Dismiss Button
        self.dismiss_btn = Button(self.help_frame, text="Dismiss", width=10,
                                  bg=ytred, fg="white", font="arial 12 bold",
                                  command=partial(self.close_help, parent), relief=SOLID,
                                  borderwidth=2, activebackground=ytred, activeforeground="white")
        self.dismiss_btn.grid(row=2, pady=10)

    # Closes the help box once dismiss has been clicked
    def close_help(self, parent):
        parent.help_button.configure(state=NORMAL)
        parent.download_button.configure(state=NORMAL)
        parent.TNC_button.configure(state=NORMAL)
        parent.explore_button.configure(state=NORMAL)
        self.help_box.destroy()

# Class for Terms and Conditions window


class Terms:
    def __init__(self, parent):
        # Disabling the state of buttons
        parent.help_button.configure(state=DISABLED)
        parent.download_button.configure(state=DISABLED)
        parent.TNC_button.configure(state=DISABLED)
        parent.explore_button.configure(state=DISABLED)

        # Colours
        background_color = "#282828"
        ytred = "#8a1111"

        # Main Frame
        self.tnc_box = Toplevel()

        # Allows the window to be proportional if stretched
        self.tnc_box.columnconfigure(0, weight=1)
        self.tnc_box.rowconfigure(0, weight=1)
        self.tnc_frame = Frame(
            self.tnc_box, bg=background_color)
        self.tnc_frame.grid(sticky=NSEW)

        # Allows the window to be proportional if stretched
        self.tnc_frame.columnconfigure(0, weight=1)
        self.tnc_frame.rowconfigure(0, weight=1)

        # Closing unnecessary windows
        self.tnc_box.protocol(
            'WM_DELETE_WINDOW', partial(self.close_tnc, parent))

        # Heading
        self.tnc_heading = Label(
            self.tnc_frame, text="Terms & Conditions", font="arial 12 bold",
            bg=ytred, fg="white", borderwidth=4, relief=SOLID, padx=10, pady=10)
        self.tnc_heading.grid(row=0, padx=10, pady=10)

        # Configurable Text
        self.tnc_text = Label(self.tnc_frame, text="",
                              justify=CENTER, width=40, bg=background_color, wrap=300)
        self.tnc_text.grid(column=0, row=1)

        # Dismiss Button
        self.dismiss_btn = Button(self.tnc_frame, text="Dismiss", width=10,
                                  bg=ytred, fg="white", font="arial 12 bold",
                                  command=partial(self.close_tnc, parent), relief=SOLID, borderwidth=2,
                                  activebackground=ytred, activeforeground="white")
        self.dismiss_btn.grid(row=2, pady=10)

    # Closes the terms box once dismiss has been clicked
    def close_tnc(self, parent):
        parent.help_button.configure(state=NORMAL)
        parent.download_button.configure(state=NORMAL)
        parent.TNC_button.configure(state=NORMAL)
        parent.explore_button.configure(state=NORMAL)
        self.tnc_box.destroy()


# Runs the Tkinter window
if __name__ == "__main__":
    root = Tk()
    root.resizable(False, False)
    root.title("Youtube Downloader")
    root.iconbitmap(r"C:\Users\flami\OneDrive\Documents\13PAD\Achievement Standard\Youtube Downloader\youtube-ico.ico")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    downloader = Main(root)
    root.mainloop()
