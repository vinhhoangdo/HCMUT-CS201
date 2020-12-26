import PySimpleGUI as sg
import cv2
import os
import numpy as np

"""
Big project's program that displays a image||(webcam) using Opencv and appling some very basic image functions
We using this file for checking our function written.  

none:       no processing, just show Origin Image

threshold:  simple b/w-threshold on the luma channel, slider sets the threshold value (BONUS)

canny:      edge finding with canny, sliders set the two threshold values for the function => edge sensitivity

blur:       simple Gaussian blur, slider sets the sigma, i.e. the amount of blur smear (BONUS)

hue:        moves the image hue values by the amount selected on the slider (BONUS)

enhance:    applies local contrast enhancement on the luma channel to make the image fancier - slider controls fanciness. (BONUS)
"""

def main():
    # Create the GUI with PySmpleGUI's library
    sg.theme('LightBlue')

    # Define the window's contents
    """
    Text is name of showing project
    """
    layout = [
      [sg.Text('Project of Computer Vison', size=(60, 1), justification='center')],
      [sg.Image(filename='', key='-IMAGE-')],
      [sg.Radio('None', 'Radio', True, size=(10, 1))],
      [sg.Radio('threshold', 'Radio', size=(10, 1), key='-THRESH-'),
       sg.Slider((0, 255), 128, 1, orientation='h', size=(40, 15), key='-THRESH SLIDER-')],
      [sg.Radio('canny', 'Radio', size=(10, 1), key='-CANNY-'),
       sg.Slider((0, 255), 128, 1, orientation='h', size=(20, 15), key='-CANNY SLIDER A-'),
       sg.Slider((0, 255), 128, 1, orientation='h', size=(20, 15), key='-CANNY SLIDER B-')],
      [sg.Radio('blur', 'Radio', size=(10, 1), key='-BLUR-'),
       sg.Slider((1, 11), 1, 3, orientation='h', size=(40, 15), key='-BLUR SLIDER-')],
      [sg.Radio('hue', 'Radio', size=(10, 1), key='-HUE-'),
       sg.Slider((0, 225), 0, 1, orientation='h', size=(40, 15), key='-HUE SLIDER-')],
      [sg.Radio('enhance', 'Radio', size=(10, 1), key='-ENHANCE-'),
       sg.Slider((1, 255), 128, 1, orientation='h', size=(40, 15), key='-ENHANCE SLIDER-')],
      [sg.Button('Exit', size=(10, 1))],
    ]

    # Create the window and show it without the plot
    width, height = 640, 320
    window = sg.Window('OpenCV Integration', layout, location=(width, height))
    # Create button "Browse", "OK", "Cancel" for choosing image locate in your PC
    event_img, values_img = window.Layout([[sg.Input(key='-FILES-'), sg.FilesBrowse()],[sg.OK(), sg.Cancel()]]).Read()
    #If you want to show webcam, please adjust here.
    # cap = cv2.VideoCapture(0)


    while True:
        event, values = window.read(timeout=20)
        # Statement breaks program!!!
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        # If you want to read frame of webcam, please adjust here.
        # ret, frame = cap.read() # it returns 2 params and frame is the images with default FPS
        # When turning on the webcam, please comment 1 line below.
        frame = cv2.imread(values_img['-FILES-']) # Read image when you choose on GUI
        """ Task1: Threshold"""
        """ Task2: Canny Edge Detection"""
        """ Task3: Filter with Gaussian Blur"""
        """ Task4: Convert frame/image BGR to HSV """
        """ Task5: Basically, Enhance image"""
        if values['-THRESH-']:
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)  # bgr2grayscale(frame)
            frame = cv2.threshold(frame, values['-THRESH SLIDER-'], 255, cv2.THRESH_BINARY)[1]
        elif values['-CANNY-']:
            frame = cv2.Canny(frame, values['-CANNY SLIDER A-'], values['-CANNY SLIDER B-'])
        elif values['-BLUR-']:
            frame = cv2.GaussianBlur(frame, (21, 21), values['-BLUR SLIDER-'])
        elif values['-HUE-']:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            frame[:, :, 0] += int(values['-HUE SLIDER-'])
            frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
        elif values['-ENHANCE-']:
            enh_val = values['-ENHANCE SLIDER-'] / 40
            clahe = cv2.createCLAHE(clipLimit=enh_val, tileGridSize=(8, 8))
            lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
            lab[:, :, 0] = clahe.apply(lab[:, :, 0])
            frame = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        # For updating statement above when it actives. Display in GUI
        imgbytes = cv2.imencode('.png', frame)[1].tobytes()
        window['-IMAGE-'].update(data=imgbytes)
    #Just close the GUI when we click button "Exit" on GUI  or close GUI tab!!!
    window.close()

main()
