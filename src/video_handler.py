"""Classes for handling of video in DojoAttender."""
import os
import pickle
import time

import cv2
import face_recognition
import imutils
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget

from db_handler import DatabaseManager


class RegMemVideoThread(QThread):
    """Video thread for registering new members window."""

    update_label_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        """Init videothread, start capturing frames."""
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self._run_flag = True

    def run(self):
        """Run loop for videothread."""
        while self._run_flag:
            ret, cv_img = self.cap.read()
            if ret:
                cv_img = cv2.rotate(cv_img, cv2.ROTATE_90_CLOCKWISE)
                self.update_label_signal.emit(cv_img)
        self.cap.release()

    def stop(self):
        """Stop videothread and wait for exit."""
        self._run_flag = False
        self.wait()


class FaceDetectionVideoThread(QThread):
    """Video thread for detecting faces when making a new training session/class."""

    update_label_signal = pyqtSignal(np.ndarray)
    detected_face_signal = pyqtSignal(int)
    class_timer_reached = pyqtSignal()

    def __init__(self, encodings, names):
        """Init videothread."""
        super().__init__()
        self.encodings = encodings
        self.names = names
        self.cap = cv2.VideoCapture(0)
        self._run_flag = True
        self.analyze_frame = True
        self.detector = cv2.CascadeClassifier(f"{os.path.dirname(os.path.realpath(__file__))}/haarcascade_frontalface_default.xml")
        self.detected_person = 0

    def run(self):
        """Run face detection."""
        _i = 0
        time_done = int(time.time()) + 1800
        while self._run_flag:
            if int(time.time()) > time_done:
                self.class_timer_reached.emit()
            ret, cv_img = self.cap.read()
            if ret:
                cv_img = cv2.rotate(cv_img, cv2.ROTATE_90_CLOCKWISE)
                if _i == 10:
                    frame = imutils.resize(cv_img, width=500)
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale for face detection
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB for face recognition

                    rects = self.detector.detectMultiScale(gray,  # Detect face in frame
                                                           scaleFactor=1.1,
                                                           minNeighbors=5,
                                                           minSize=(30, 30),
                                                           flags=cv2.CASCADE_SCALE_IMAGE)
                    boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]  # (x, y, w, h) to (top, right, botton, left)
                    encodings = face_recognition.face_encodings(rgb, boxes)
                    for encoding in encodings:
                        matches = face_recognition.compare_faces(self.encodings,  # Loop over all member face encodings
                                                                 encoding)        # and compare with detected face
                        person = 0
                        if True in matches:
                            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                            counts = {}
                            for i in matchedIdxs:
                                person = self.names[i][1]
                                counts[person] = counts.get(person, 0) + 1

                            person = max(counts, key=counts.get)  # Get the person which matches best
                            if self.detected_person != person:
                                self.detected_person = person
                                self.detected_face_signal.emit(int(self.detected_person))
                    _i = 0
                self.update_label_signal.emit(cv_img)
                _i += 1
        self.cap.release()

    def stop(self):
        """Stop videothread and wait for exit."""
        self._run_flag = False
        self.wait()


class TrainingSesVideoEngine(QWidget):
    """Handle new training session, communication with videothread and UI."""

    def __init__(self, label):
        """Init videoe engine."""
        super().__init__()
        self.encodings = []
        self.names_ids = []
        self.get_member_encodings()

        self.thread = FaceDetectionVideoThread(self.encodings, self.names_ids)
        self.thread.update_label_signal.connect(self.process_image)
        self.thread.start()
        self.label = label

    def get_member_encodings(self):
        """Get all members face encodings."""
        with DatabaseManager() as db:
            members = db.get_members()
            for member in members:
                name = str(member[1]).split(" ")[0]
                encodings = pickle.loads(member[2])
                for encoding in encodings:
                    self.encodings.append(encoding)
                    self.names_ids.append((name, str(member[0])))

    def process_image(self, cv_img):
        """Convert image and update UI label with converted image."""
        qt_img = self.convert_cv_qt(cv_img)
        self.label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap."""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QtGui.QImage(rgb_image.data, w, h,
                                            bytes_per_line,
                                            QtGui.QImage.Format_RGB888)
        p = convert_to_qt_format.scaled(self.label.width(),
                                        self.label.height(),
                                        Qt.KeepAspectRatioByExpanding)
        return QPixmap.fromImage(p)


class RegNewMemVideoEnginge(QWidget):
    """Handle registering, communication with videothread and UI."""

    def __init__(self, label):
        """Init video engine."""
        super().__init__()
        self.text1 = ["", (0, 0, 255)]
        self.text2 = ["", (0, 0, 255)]
        self.label = label
        self.thread = RegMemVideoThread()
        self.thread.update_label_signal.connect(self.update_image)
        self.thread.start()

    def update_image(self, cv_img):
        """Update the image_label with a new opencv image."""
        ft = cv2.freetype.createFreeType2()
        ft.loadFontData(fontFileName='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                        id=0)
        ft.putText(img=cv_img,
                   text=self.text1[0],
                   org=(10, 55),
                   fontHeight=25,
                   color=self.text1[1],
                   thickness=-1,
                   line_type=cv2.LINE_AA,
                   bottomLeftOrigin=True)

        ft.putText(img=cv_img,
                   text=self.text2[0],
                   org=(10, 85),
                   fontHeight=25,
                   color=self.text2[1],
                   thickness=-1,
                   line_type=cv2.LINE_AA,
                   bottomLeftOrigin=True)

        qt_img = self.convert_cv_qt(cv_img)
        self.label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap."""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QtGui.QImage(rgb_image.data, w, h,
                                            bytes_per_line,
                                            QtGui.QImage.Format_RGB888)
        p = convert_to_qt_format.scaled(self.label.width(),
                                        self.label.height(),
                                        Qt.KeepAspectRatioByExpanding)
        return QPixmap.fromImage(p)
