from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from imutils import face_utils
import cv2
import dlib
#import file

import sys
import datetime
import copy


# Main class
class MyWindow(QMainWindow):
    # var further used in the program

    # color selection
    r = 0
    b = 0
    g = 255

    # for loop
    counter = 1

    # Save the captured frame
    captureframeSq = 0
    captureframeDot = 0
    optio = ''

    # to define loop entry and exit point
    startind = 0
    endind = 68

    # couter for loop
    dotcount = 0

    # condition counter (ON/OFF)
    showsq = 0
    showdot = 0

    # initializing file to write in log.txt
    fi = open('D:/Folder/main/!!Nirma/Sem_4/PSC/project/log.txt', 'a')

    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(100, 100, 900, 700)
        self.setWindowTitle("Facial workspace")
        self.setWindowIcon(QtGui.QIcon('D:/Folder/main/!!Nirma/Sem_4/PSC/project/Icon/Project_icon.png'))
        self.initUI()
        # self.showfrm()
    def initUI(self):

        # initializing The elements
        self.bt1 = QtWidgets.QPushButton(self)
        self.bt1.setGeometry(100, 50, 300, 35)
        self.bt1.setText("Detect Face")
        self.bt1.clicked.connect(self.enableSQ)
        self.bt1.hide()

        self.bt2 = QtWidgets.QPushButton(self)
        self.bt2.setGeometry(100, 130, 300, 35)
        self.bt2.setText("Detect Separately")
        self.bt2.clicked.connect(self.enableDOT)
        self.bt2.hide()

        self.btstart = QtWidgets.QPushButton(self)
        self.btstart.setGeometry(375, 150, 100, 35)
        self.btstart.setText("Start")
        self.btstart.clicked.connect(self.showfrm)

        """
        self.bt3 = QtWidgets.QPushButton(self)
        self.bt3.setGeometry(480, 100, 100, 25)
        self.bt3.setText("Red It!")
        self.bt3.clicked.connect(self.redit)

        self.bt4 = QtWidgets.QPushButton(self)
        self.bt4.setGeometry(480, 150, 100, 25)
        self.bt4.setText("Blue It!")
        self.bt4.clicked.connect(self.blueit)
        """

        self.bt5 = QtWidgets.QPushButton(self)
        self.bt5.setGeometry(100, 280, 100, 35)
        self.bt5.setText("End")
        self.bt5.clicked.connect(self.endit)
        self.bt5.hide()

        self.btendsq = QtWidgets.QPushButton(self)
        self.btendsq.setGeometry(100, 50, 300, 35)
        self.btendsq.setText("STOP Facial Detection")
        self.btendsq.clicked.connect(self.endSQ)
        self.btendsq.hide()

        self.btenddot = QtWidgets.QPushButton(self)
        self.btenddot.setGeometry(100, 130, 300, 35)
        self.btenddot.setText("STOP Parts Detection")
        self.btenddot.clicked.connect(self.endDOT)
        self.btenddot.hide()

        self.bt6 = QtWidgets.QPushButton(self)
        self.bt6.setGeometry(100, 220, 93, 28)
        self.bt6.setText("Capture")
        self.bt6.setEnabled(False)
        self.bt6.clicked.connect(self.capture)
        self.bt6.hide()
        self.bt6.setEnabled(False)

        self.pbMouth = QtWidgets.QPushButton(self)
        self.pbMouth.setGeometry(500, 100, 93, 28)
        self.pbMouth.setText("Mouth")
        self.pbMouth.setEnabled(False)
        self.pbMouth.clicked.connect(self.Mouth)
        self.pbMouth.hide()

        self.pbEyeBrows = QtWidgets.QPushButton(self)
        self.pbEyeBrows.setGeometry(500, 140, 93, 28)
        self.pbEyeBrows.setText("EyeBrows")
        self.pbEyeBrows.setEnabled(False)
        self.pbEyeBrows.clicked.connect(self.EyeBrows)
        self.pbEyeBrows.hide()

        self.pbEyes = QtWidgets.QPushButton(self)
        self.pbEyes.setGeometry(500, 180, 93, 28)
        self.pbEyes.setText("Eyes")
        self.pbEyes.setEnabled(False)
        self.pbEyes.clicked.connect(self.Eyes)
        self.pbEyes.hide()

        self.pbNose = QtWidgets.QPushButton(self)
        self.pbNose.setGeometry(500, 220, 93, 28)
        self.pbNose.setText("Nose")
        self.pbNose.setEnabled(False)
        self.pbNose.clicked.connect(self.Nose)
        self.pbNose.hide()

        self.pbJaw = QtWidgets.QPushButton(self)
        self.pbJaw.setGeometry(500, 260, 93, 28)
        self.pbJaw.setText("Jaw")
        self.pbJaw.setEnabled(False)
        self.pbJaw.clicked.connect(self.Jaw)
        self.pbJaw.hide()

        self.sqRed = QtWidgets.QScrollBar(self)
        self.sqRed.setGeometry(100, 380, 30, 255)
        self.sqRed.sliderMoved.connect(self.redit)
        self.sqRed.setMinimum(0)
        self.sqRed.setMaximum(256)
        self.sqRed.setEnabled(False)
        self.sqRed.hide()

        self.sqGreen = QtWidgets.QScrollBar(self)
        self.sqGreen.setGeometry(170, 380, 30, 255)
        self.sqGreen.sliderMoved.connect(self.greenit)
        self.sqGreen.setMinimum(0)
        self.sqGreen.setMaximum(256)
        self.sqGreen.setEnabled(False)
        self.sqGreen.hide()

        self.sqBlue = QtWidgets.QScrollBar(self)
        self.sqBlue.setGeometry(240, 380, 30, 255)
        self.sqBlue.sliderMoved.connect(self.blueit)
        self.sqBlue.setMinimum(0)
        self.sqBlue.setMaximum(256)
        self.sqBlue.setEnabled(False)
        self.sqBlue.hide()

        self.labRed = QtWidgets.QLabel(self)
        self.labRed.setText("Red")
        self.labRed.move(100, 645)
        self.labRed.hide()

        self.labGreen = QtWidgets.QLabel(self)
        self.labGreen.setText("Green")
        self.labGreen.move(170, 645)
        self.labGreen.hide()

        self.labBlue = QtWidgets.QLabel(self)
        self.labBlue.setText("Blue")
        self.labBlue.move(240, 645)
        self.labBlue.hide()

        self.dialogue = QtWidgets.QFileDialog(self)

    '''
    def Square(self):
        # self.disable()
        # self.enableSq()
        self.counter = 0
        video = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # dshow means direct show
        face_cascade = cv2.CascadeClassifier(
            "C:/Users/dhruv/AppData/Local/Programs/Python/Python38/Cascade/haarcascade_frontalface_default.xml")  # contain features of face

        while True:
            check, frame = video.read()
            faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2,
                                                  minNeighbors=5)  # compare the image with the features
            print(faces)
            for x, y, w, h in faces:
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (self.b, self.g, self.r), 3)
            self.capturedframe = frame
            cv2.imshow('Capture', frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break

            if self.counter == 1:
                break

        video.release()
        cv2.destroyWindow('Capture')
        # self.disable()
        self.counter = 0

    def Dots(self):
        # self.disable()
        # self.enableMods()
        self.counter = 0
        p = "C:/Users/dhruv/AppData/Local/Programs/Python/Python38/shape_predictor_68_face_landmarks.dat"
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(p)
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

        while True:
            check, image = cap.read()
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            rects = detector(gray, 0)

            for (i, rect) in enumerate(rects):
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)

                for (x, y) in shape:

                    if self.startind < self.dotcount <= self.endind + 2:
                        cv2.circle(image, (x, y), 2, (self.b, self.g, self.r), -1)
                    else:
                        pass
                    self.dotcount += 1
                self.dotcount = 1

            cv2.imshow("Captures", image)
            self.captureframe = image

            key = cv2.waitKey(1)
            if key == ord('q'):
                break

            if self.counter == 1:
                break

        cap.release()
        cv2.destroyAllWindows()
        # self.disable()
        self.counter = 0

    '''

    # Method to Display Webcam and Detection
    def showfrm(self):
        # initializing file variable
        self.fi = open('D:/Folder/main/!!Nirma/Sem_4/PSC/project/log.txt', 'a')

        # Log entry
        x = datetime.datetime.now()
        ope = 'Started'
        stri = '\n' + str(x.date()) + ' ' + str(x.hour) + ':' + str(x.minute) + ':' + str(x.second) + ' ' + ope
        self.fi.write(stri)

        # Log Entry
        ope = 'WebCam On'
        stri = '\n' + str(x.date()) + ' ' + str(x.hour) + ':' + str(x.minute) + ':' + str(x.second) + ' ' + ope
        self.fi.write(stri)

        # Method call to make elements visible
        self.AllShow()

        # Hide the button which will not be in use now
        self.btstart.hide()

        # display the button which will be used now on
        self.bt5.show()

        # initializing the file to determine parts of face
        p = "C:/Users/dhruv/AppData/Local/Programs/Python/Python38/shape_predictor_68_face_landmarks.dat"

        # Returns Returns the default face detector.
        detector = dlib.get_frontal_face_detector()

        # take in the input of face image and returns the set of point locations that define the face
        predictor = dlib.shape_predictor(p)

        # cv2  method to access the WebCam, will not work if the WebCam is occupied
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        # haar file that contains the features of face
        face_cascade = cv2.CascadeClassifier("C:/Users/dhruv/AppData/Local/Programs/Python/Python38/Cascade/haarcascade_frontalface_default.xml")
        while True:
            #read the image from WebCam
            check, freeframe = cap.read()

            # use copy method to create the copy of the WebCam frame ; not using the '=' because,
            # the second variable is just pointing the address of the first variable
            frame = copy.copy(freeframe)

            # converting to gray image
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # returns the array that contain screen coordinates where face is detected
            rects = detector(gray, 0)
            # again copying the frame
            image = copy.copy(frame)

            # face detection by compare the image with the features
            # if you find the inaccuracy in detection of face, try re adjusting the scaleFactor between 1.0 to 2.0
            faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2,minNeighbors=5)

            # draw rectangle around the face
            for x, y, w, h in faces:
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (self.b, self.g, self.r), 3)

            for (i, rect) in enumerate(rects):
                shape = predictor(gray, rect)

                # this will convert the encoded facial landmarks from face_utils to numPy array
                shape = face_utils.shape_to_np(shape)
                # print(shape)

                for (x, y) in shape:

                    # as per the desired part to be detected, re format the startind & endind to specifically locate a part of list of array
                    if self.startind < self.dotcount <= self.endind:

                        # draw dot/point
                        cv2.circle(image, (x, y), 2, (self.b, self.g, self.r), -1)
                    else:
                        pass
                    #loop counter
                    self.dotcount += 1

                self.dotcount = 1

            # condition checking
            if self.showsq == 0 and self.showdot == 0:
                cv2.imshow("WebCam", freeframe)
                cv2.destroyWindow("Mapping")
                cv2.destroyWindow("Detection")
            else:
                cv2.destroyWindow("WebCam")
                if self.showdot == 1:
                    cv2.imshow("Mapping", image)  # face maping
                    self.captureframeDot = image

                    # enabling the required elements
                    self.pbMouth.setEnabled(True)
                    self.pbEyeBrows.setEnabled(True)
                    self.pbEyes.setEnabled(True)
                    self.pbNose.setEnabled(True)
                    self.pbJaw.setEnabled(True)
                    self.sqRed.setEnabled(True)
                    self.sqGreen.setEnabled(True)
                    self.sqBlue.setEnabled(True)

                else:
                    # disabling the non required elements
                    cv2.destroyWindow("Mapping")
                    self.pbMouth.setEnabled(False)
                    self.pbEyeBrows.setEnabled(False)
                    self.pbEyes.setEnabled(False)
                    self.pbNose.setEnabled(False)
                    self.pbJaw.setEnabled(False)
                    if self.showsq == 0:
                        self.sqRed.setEnabled(False)
                        self.sqGreen.setEnabled(False)
                        self.sqBlue.setEnabled(False)

                if self.showsq == 1:
                    cv2.imshow("Detection", frame)  # face detection
                    self.captureframeSq = frame

                    # enabling the required elements
                    self.sqRed.setEnabled(True)
                    self.sqGreen.setEnabled(True)
                    self.sqBlue.setEnabled(True)
                else:
                    cv2.destroyWindow("Detection")
                    if self.showdot == 0:
                        self.sqRed.setEnabled(False)
                        self.sqGreen.setEnabled(False)
                        self.sqBlue.setEnabled(False)

            if self.showsq == 0 and self.showdot == 0:
                # disabling the non required elements
                self.pbMouth.setEnabled(False)
                self.pbEyeBrows.setEnabled(False)
                self.pbEyes.setEnabled(False)
                self.pbNose.setEnabled(False)
                self.pbJaw.setEnabled(False)
                self.sqRed.setEnabled(False)
                self.sqGreen.setEnabled(False)
                self.sqBlue.setEnabled(False)

            # confirming for existence of window
            if cv2.getWindowProperty("Mapping", 0) == -1.0:
                self.showdot = 0

            if cv2.getWindowProperty("Detection", 0) == -1.0:
                self.showsq = 0

            cv2.waitKey(1)
            # exit condition
            if self.counter == 0:
                # print('Q pressed')
                break
        # releasing the window
        cap.release()
        cv2.destroyAllWindows()
        self.counter = 1

    def AllHide(self):
        # method to hide non usable elements
        self.bt1.hide()
        self.bt2.hide()
        self.bt5.hide()
        self.btendsq.hide()
        self.btenddot.hide()
        self.bt6.hide()
        self.pbMouth.hide()
        self.pbEyeBrows.hide()
        self.pbEyes.hide()
        self.pbNose.hide()
        self.pbJaw.hide()
        self.sqRed.hide()
        self.sqGreen.hide()
        self.sqBlue.hide()
        self.labRed.hide()
        self.labGreen.hide()
        self.labBlue.hide()

    def AllShow(self):
        # show the required elements
        self.bt5.show()
        # self.btendsq.show()
        # self.btenddot.show()
        self.bt6.show()
        self.pbMouth.show()
        self.pbEyeBrows.show()
        self.pbEyes.show()
        self.pbNose.show()
        self.pbJaw.show()
        self.sqRed.show()
        self.sqGreen.show()
        self.sqBlue.show()
        self.labRed.show()
        self.labGreen.show()
        self.labBlue.show()
        self.bt1.show()
        self.bt2.show()

    def redit(self):
        # the the value of Red
        self.r = self.sqRed.value()

    def blueit(self):
        # the the value of Blue
        self.b = self.sqBlue.value()

    def greenit(self):
        # # the the value of Green
        self.g = self.sqGreen.value()

    # method to save the frame
    def capture(self):
        # holds the various options that affect the look and feel of the dialog
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        # get the name of the destination and the name of file to be saved
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "", "Image (*.jpg)",
                                                  options=options)
        # Two variables with different extension according to the active window
        fileNameSq = fileName + '_FF.jpg'
        fileNameDot = fileName + '_Pt.jpg'

        # Check condition to save the frame or not
        if fileName != '':
            if self.showsq == 1:
                cv2.imwrite(fileNameSq, self.captureframeSq)

            if self.showdot == 1:
                cv2.imwrite(fileNameDot, self.captureframeDot)

        # log entry
        self.EnterLog('capture saved as {}'.format(fileName))

    # set the Startind and Endind as per the parts
    def Mouth(self):
        ope = 'Setting Parameters for MOUTH'
        self.EnterLog(ope)

        self.startind = 48
        self.endind = 68

    # set the Startind and Endind as per the parts
    def EyeBrows(self):
        ope = 'Setting Parameters for EYEBROWS'
        self.EnterLog(ope)

        self.startind = 17
        self.endind = 27

    # set the Startind and Endind as per the parts
    def Eyes(self):
        ope = 'Setting Parameters for EYES'
        self.EnterLog(ope)

        self.startind = 36
        self.endind = 48

    # set the Startind and Endind as per the parts
    def Nose(self):
        ope = 'Setting Parameters for NOSE'
        self.EnterLog(ope)

        self.startind = 27
        self.endind = 36

    # set the Startind and Endind as per the parts
    def Jaw(self):
        ope = 'Setting Parameters for JAW'
        self.EnterLog(ope)

        self.startind = 0
        self.endind = 17

    # set the var for detection to 1
    def enableSQ(self):
        self.EnterLog('Detecting FACE')

        self.showsq = 1
        self.bt1.hide()
        self.btendsq.show()
        self.bt6.setEnabled(True)

    # set the var for detection to 1
    def enableDOT(self):
        self.EnterLog('Detecting SEPARATE PARTS')
        self.showdot = 1
        self.bt2.hide()
        self.btenddot.show()
        self.bt6.setEnabled(True)

    # set the var for detector to 0
    def endDOT(self):
        self.EnterLog('Disabling SEPARATE PARTS')
        self.showdot = 0
        self.btenddot.hide()
        self.bt2.show()
        if self.showsq == 0:
            self.bt6.setEnabled(False)

    # set the var for detector to 0
    def endSQ(self):
        self.EnterLog('Disabling DETECT FACE')
        self.showsq = 0
        self.btendsq.hide()
        self.bt1.show()
        if self.showdot == 0:
            self.bt6.setEnabled(False)

    # End the window and go back to START
    def endit(self):
        self.counter = 0
        self.showsq = 0
        self.showdot = 0
        self.btenddot.hide()
        self.bt2.show()
        self.btendsq.hide()
        self.bt1.show()
        self.AllHide()
        self.bt5.hide()
        self.btstart.show()
        self.EnterLog('Closing Program')
        self.fi.close()

    # maintain the log file
    def EnterLog(self,strarg):
        x = datetime.datetime.now()
        stri = '\n' + str(x.date()) + ' ' + str(x.hour) + ':' + str(x.minute) + ':' + str(x.second) + ' ' + strarg
        self.fi.write(stri)

# initiating method
def wind():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

wind()