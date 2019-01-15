# OCR Tesseract OpenCV Tkinter
Allows upload of an image for OCR using Tesseract and deployed using Tkinter.  This uses Tkinter, a Python GUI framework based on Tcl/Tkl.   OpenCV is used to reduce noise in the image for better processing by pytesseract. Below are 3 images of a job posting taken on a Pixel 2XL phone, and reduced in size using Gimp by adjusting quality. 

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
For Windows 10, Tesseract must be installed - you can find installer here:
* [Tesseract Window 10 Installers](https://github.com/UB-Mannheim/tesseract/wiki)


### Installing and Running
```
For ImageTk
$ sudo apt-get update
Install OpenCV
$ sudo apt-get install python3-pil.imagetk
$ pip install opencv-python 
$ pip install opencv-contrib-python
Install Tesseract/Pytesseract
$ sudo apt install tesseract-ocr
$ sudo apt install libtesseract-dev
$ pip install pytesseract
```

Also, see requirements.txt file produced using 
$ pip freeze > requirements.txt

You can use these images to test it - these are photos of a job posting:

* [Job Posting 1](https://www.torzyn.com/ocr/senior_python_developer_nlplogix1_sm.jpg)
* [Job Posting 2](https://www.torzyn.com/ocr/senior_python_developer_nlplogix2_sm.jpg)
* [Job Posting 3](https://www.torzyn.com/ocr/senior_python_developer_nlplogix3_sm.jpg)


## Built With
```
Python
Tkinter
Pytesseract
OpenCV
```

## Resources

Here are some helpful resources on the web that I used for this project. 

* [Deep Learning based Text Recognition (OCR) using Tesseract and OpenCV](https://www.learnopencv.com/deep-learning-based-text-recognition-ocr-using-tesseract-and-opencv/)
* [Using Tesseract OCR with Python](https://www.pyimagesearch.com/2017/07/10/using-tesseract-ocr-python/)


## Acknowledgments


