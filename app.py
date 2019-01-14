import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time, os, random, string, argparse
from pathlib import Path
import numpy as np
from PIL import ImageTk, Image
import cv2
import pytesseract as tess


class Page(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("OCR Using Tesseract")
        
        container=tk.Frame(self)
        container.grid()

        # menu
        self.option_add('*tearOff', False)
        menubar = tk.Menu(self)
        self.config(menu = menubar)
        file = tk.Menu(menubar)
        help_ = tk.Menu(menubar)

        menubar.add_cascade(menu = file, label = "File")
        file.add_command(label = 'Open...', command=lambda:self.show_image())
        menubar.add_cascade(menu = help_, label = "Help")
        help_.add_command(label = 'About', command=lambda:self.about())

        # title
        self.empty_name=tk.Label(self, text="OCR Using Tesseract - Version 0.5", font=("Arial", 16))
        self.empty_name.grid(row=0, column=0, pady=5, padx=10, sticky="sw")

        # intro
        self.intro_lbl = tk.Label(self, text="Demonstration of using Python and Pytesseract in a desktop application for OCR.",
                                  font=("Arial", 11), fg="#202020")
        self.intro_lbl.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nw")

        # select image                          
        self.browse_lbl = tk.Label(self, text="Select Image :", font=("Arial", 10), fg="#202020")
        self.browse_lbl.grid(row=4, column=0, columnspan=3, padx=24, pady=10, sticky="w")

        self.browse_entry=tk.Entry(self, text="", width=30)
        self.browse_entry.grid(row=4, column=0, columnspan=3, padx=120, pady=10, sticky="w")

        self.browse_btn = tk.Button(self, text="     Browse     ", bg="#ffffff", relief="flat", width=10,
                                    command=lambda:self.show_image())
        self.browse_btn.grid(row=4, column=0, padx=310, pady=10, columnspan=3, sticky="w")
        
        # file info
        self.lbl_filename = tk.Label(self, text="File Name: ", font=("Arial", 10), fg="#202020")
        self.lbl_filesize = tk.Label(self, text="File Size: ", font=("Arial", 10), fg="#202020") 

        self.label_text_x = tk.StringVar()
        self.lbl_filename_01 = tk.Label(self, textvariable=self.label_text_x, font=("Arial", 10),fg="#202020")
        
        self.text_file_size=tk.StringVar()
        self.lbl_filesize_01 = tk.Label(self, textvariable=self.text_file_size, font=("Arial", 10), fg="#202020")
        
        # place holder for document thumbnail
        self.lbl_image = tk.Label(self, image="")
        self.lbl_image.grid(row=8, column=0, pady=25, padx=10, columnspan=3, sticky="nw")

        # status text
        self.label_text_progress = tk.StringVar()
        self.scan_progress = tk.Label(self, textvariable=self.label_text_progress, font=("Arial", 10),fg="#0000ff")
        
        # scan button
        self.scan_btn = tk.Button(self, text="     Process     ", bg="#ffffff", relief="flat",
                                 width=10, command=lambda:self.ocr())
        # clear ocr text button
        self.clear_btn = tk.Button(self, text="     Clear      ", bg="#ffffff", relief="flat",
                                  width=10, command=lambda:self.clearOcr())
        # text area to place text
        self.ocr_text = tk.Text(self, height=25, width=38)  
       
    
    def show_image(self):
        global path
        
        # open file dialog
        self.path = filedialog.askopenfilename(defaultextension="*.jpg", filetypes = (("JPG", "*.jpg"),("PNG","*.png")))
        self.browse_entry.delete(0, tk.END)
        self.browse_entry.insert(0, self.path)
        
        self.label_text_progress.set("Image loaded - ready to be processed.");
        self.scan_progress.grid(row=18, column=0, padx=10, pady=0,
                           columnspan=3, sticky="w")

        # resize image
        cv_img = cv2.cvtColor(cv2.imread(self.path), cv2.COLOR_BGR2RGB)
        height, width, no_channels = cv_img.shape

        HEIGHT = 400   
        imgScale = HEIGHT/height
        newX, newY = cv_img.shape[1]*imgScale, cv_img.shape[0]*imgScale
        newimg = cv2.resize(cv_img, (int(newX), int(newY)))
        photo = ImageTk.PhotoImage(image = Image.fromarray(newimg))
        
        # show image
        self.lbl_image.configure(image=photo)
        self.lbl_image.image=photo

        # show file information
        self.lbl_filename.grid(row=5, column=0, pady=0, padx=10, columnspan=3, sticky="nw")
        self.lbl_filename_01.grid(row=5, column=0, pady=0, padx=85, columnspan=3, sticky="nw")
        self.lbl_filesize.grid(row=6, column=0, pady=0, padx=10, sticky="nw")
        self.lbl_filesize_01.grid(row=6, column=0, pady=0, padx=75, columnspan=3, sticky="nw")

        # add scan button
        scan_btn_mid = int(newX/2) - 40;       
        self.scan_btn.grid(row=17, column=0, padx=scan_btn_mid, pady=10,
                           columnspan=3, sticky="w")
        self.ocr_text.grid(row=8, column=0, padx=350, pady=26, columnspan=3, sticky="w")
        
        # set the filename
        self.label_text_x.set(os.path.basename(self.path))
        
        # set the filesize
        self.text_file_size.set(os.path.getsize(self.path))
        

    def ocr(self):
        self.label_text_progress.set("Image processing complete.");
        
        # load the example image and convert it to grayscale
        self.ocr_image = cv2.imread(self.path)
        gray = cv2.cvtColor(self.ocr_image, cv2.COLOR_BGR2GRAY)
      
        # apply thresholding to preprocess the image
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # apply median blurring to remove any blurring
        gray = cv2.medianBlur(gray, 3)

        # save the processed image in the /static/uploads directory
        ofilename = os.path.join('./scans',"{}.png".format(os.getpid()))
        cv2.imwrite(ofilename, gray)

        # create a thumbnail of processed image
        corrected_img = cv2.cvtColor(cv2.imread(ofilename), cv2.COLOR_BGR2RGB)
        cheight, cwidth, cno_channels = corrected_img.shape

        # resize image
        HEIGHT = 400
        cimgScale = HEIGHT/cheight
        cnewX, cnewY = corrected_img.shape[1]*cimgScale, corrected_img.shape[0]*cimgScale
        cnewimg = cv2.resize(corrected_img, (int(cnewX), int(cnewY)))
        cphoto = ImageTk.PhotoImage(image = Image.fromarray(cnewimg))

        # replace the unprocessed thumbnail
        self.lbl_image.configure(image=cphoto)
        self.lbl_image.image=cphoto

        # perform OCR on the processed image
        ocrtext = tess.image_to_string(Image.open(ofilename))

        # add text to end of textbox
        self.ocr_text.insert(tk.END,ocrtext)
        self.clear_btn.grid(row=17, column=0, padx=440, pady=10,
                           columnspan=3, sticky="w")

    def clearOcr(self):
        # clear the textbox
        self.ocr_text.delete(1.0, tk.END)

    def about(self):
        # show about message
        messagebox.showinfo(title = 'About', message = 'This is a demo Tkinter project by Rick Torzynski')
        

if __name__ == "__main__":
    app = Page()
    app.geometry("700x725+100+100")
    app.mainloop()

        
                                 
