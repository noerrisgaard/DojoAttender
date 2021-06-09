"""Classes for handling members in DojoAttender."""
import os
import pickle
import time

import cv2
import face_recognition
from imutils import paths
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QHeaderView, QLabel, QPushButton, QScroller,
                             QTableWidgetItem, QWidget)

from db_handler import DatabaseManager


class RegisterMemberWorker(QThread):
    """Worker for registering new members, analyzing faces etc."""

    update_text_signal = pyqtSignal(str)
    take_picture_signal = pyqtSignal(int)
    analyze_done_signal = pyqtSignal(list)

    def run(self):
        """To be run when worker is started."""
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self._countdown()
        self._take_pictures()
        self._analyze_picture_endocings()

    def _countdown(self):
        """Countdown method for taking pictures."""
        for _i in reversed(range(5)):
            self.update_text_signal.emit(f"Taking pictures in {str(_i)}")
            time.sleep(1)
        self.update_text_signal.emit("")

    def _take_pictures(self):
        """Grab frames from videobuffer."""
        text = "Taking pictures"
        self.update_text_signal.emit(text)
        for _i in range(5):
            self.update_text_signal.emit(text)
            time.sleep(1)
            self.take_picture_signal.emit(_i)
            text = text + "."
        self.update_text_signal.emit("")

    def _analyze_picture_endocings(self):
        """Get the members face encodings for facial recognition."""
        text = "Analyzing pictures"

        known_encodings = []
        imagePaths = list(paths.list_images(f"{self.dir_path}/../data"))
        for (i, imagePath) in enumerate(imagePaths):
            text = text + "."
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(rgb, model="hog")
            encodings = face_recognition.face_encodings(rgb, boxes)

            # loop over the encodings
            for encoding in encodings:
                # add each encoding + name to our set of known names and
                # encodings
                known_encodings.append(encoding)
            self.update_text_signal.emit(text)
        self.update_text_signal.emit("")
        self.analyze_done_signal.emit(known_encodings)


class RegisterMemberHandler(QWidget):
    """Handle registering new members."""

    def __init__(self, video_enginge, regmem_btn, return_btn, mem_name_input):
        """Init RegisterMemberHandler and connect signals etc."""
        super().__init__()
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.video_enginge = video_enginge
        self.regmem_btn = regmem_btn
        self.return_btn = return_btn
        self.mem_name_input = mem_name_input

        self.regmem_worker = RegisterMemberWorker()
        self.regmem_worker.update_text_signal.connect(self._update_text)
        self.regmem_worker.take_picture_signal.connect(self._take_picture)
        self.regmem_worker.analyze_done_signal.connect(self._save_new_member)
        self.regmem_worker.finished.connect(self._toggle_btns)

    def _take_picture(self, _iter):
        ret, cv_img = self.video_enginge.thread.cap.read()
        if ret:
            cv_img = cv2.rotate(cv_img, cv2.ROTATE_90_CLOCKWISE)
            img_name = f"{self.dir_path}/../data/image_{_iter}.jpg"
            cv2.imwrite(img_name, cv_img)

    def _update_text(self, text):
        if "Taking pictures in" in text:
            self.video_enginge.text2[0] = "Place face in front of the camera"
        else:
            self.video_enginge.text2[0] = ""
        self.video_enginge.text1[0] = text

    def _toggle_btns(self):
        toggle = not self.regmem_btn.isEnabled()
        self.regmem_btn.setEnabled(toggle)
        self.return_btn.setEnabled(toggle)
        self.mem_name_input.setEnabled(toggle)
        if toggle and self.mem_name_input.isModified():
            self.mem_name_input.setText("")

    def _save_new_member(self, encodings):
        with open(f'{self.dir_path}/../data/image_0.jpg', 'rb') as data:
            image = data.read()
            member_to_be_added = {"name": self.mem_name_input.text(),
                                  "encodings": pickle.dumps(encodings),
                                  "picture": image}

            with DatabaseManager() as db:
                db.add_member(member_to_be_added)

        image_paths = list(paths.list_images(f"{self.dir_path}/../data"))
        for (i, imagePath) in enumerate(image_paths):
            os.remove(imagePath)

    def register_new_member(self):
        """Register new members, toggle button and start RegisterMemberWorker."""
        self._toggle_btns()
        self.regmem_worker.start()


class EditMembersHandler(QWidget):
    """Use to handle editing members."""

    def __init__(self):
        """Initiate EditMembersHandler."""
        super().__init__()
        self.table = None
        self.centralwidget = None

    def populate_members_table(self, table, centralwidget):
        """Populate the members table in the UI."""
        self.centralwidget = centralwidget
        self.table = table
        QScroller.grabGesture(self.table, QScroller.TouchGesture)
        self.table.setColumnHidden(3, True)

        with DatabaseManager() as db:
            members = db.get_members()
            for row_number, row_data in enumerate(members):
                self.table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    if column_number == 0:
                        self.table.setItem(row_number, 3,
                                           QTableWidgetItem(str(data)))
                        self.table.item(row_number, 3)
                    if column_number == 1:
                        self.table.setItem(row_number, 1,
                                           QTableWidgetItem(str(data)))
                    if column_number == 3:
                        item = self.convert_img_to_label(data)
                        self.table.setCellWidget(row_number, 0, item)
                    btn = QPushButton('Delete')
                    btn.clicked.connect(self.handle_button_clicked)
                    self.table.setCellWidget(row_number, 2, btn)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.horizontalHeader().setSectionResizeMode(1,
                                                           QHeaderView.Stretch)

    def convert_img_to_label(self, img):
        """Convert image from the video framebuffer to a QPixmap to be loaded in the UI."""
        image_label = QLabel(self.centralwidget)
        image_label.setText("")
        image_label.setScaledContents(True)
        pixmap = QPixmap()
        pixmap.loadFromData(img, 'jpg')
        pixmap = pixmap.scaled(120, 280, Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
        return image_label

    def handle_button_clicked(self):
        """Call when a user clicks delete on a member."""
        button = self.centralwidget.focusWidget()
        index = self.table.indexAt(button.pos())
        if index.isValid():
            with DatabaseManager() as db:
                db.delete_member(self.table.item(index.row(), 3).text())
        self.table.setRowCount(0)
        self.populate_members_table(self.table, self.centralwidget)
