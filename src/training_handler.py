"""Classes for handling editing of class/training session history and for starting new sessions."""
from datetime import datetime

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QHeaderView, QListWidgetItem, QPushButton,
                             QScroller, QTableWidgetItem, QWidget)

from db_handler import DatabaseManager
from video_handler import TrainingSesVideoEngine


class ClassManager(QWidget):
    """Handle editing classes/training session history."""

    def __init__(self, table, centralwidget, attendee_list, group_box):
        """Init ClassManager, connect signals etc."""
        super().__init__()
        self.table = table
        self.attendee_list = attendee_list
        self.group_box = group_box
        QScroller.grabGesture(self.attendee_list, QScroller.TouchGesture)
        font = self.table.font()
        font.setPointSize(12)
        self.table.setFont(font)
        self.centralwidget = centralwidget
        self.table.clicked.connect(self.training_selected)
        self.attendee_list.setFocus()

    def populate_classes_table(self):
        """Populate the classes table im the UI."""
        QScroller.grabGesture(self.table, QScroller.TouchGesture)

        with DatabaseManager() as db:
            classes = db.get_training_sessions()
            for row_number, row_data in enumerate(classes):
                self.table.insertRow(0)
                self.table.setItem(0, 0, QTableWidgetItem(str(row_data[0])))
                btn = QPushButton('Delete')
                btn.clicked.connect(self.handle_delete_button_clicked)
                self.table.setCellWidget(0, 1, btn)
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setSectionResizeMode(0,
                                                           QHeaderView.Stretch)

    def populate_attendees_list(self, training_session):
        """Populate the attendees list on the right side of UI."""
        self.group_box.setTitle(training_session)
        self.attendee_list.clear()
        with DatabaseManager() as db:
            attendees = db.get_training_session_attendees(training_session)
            for attendee in attendees:
                item = QListWidgetItem(attendee[0])
                item.setForeground(QColor('#168b44'))
                self.attendee_list.addItem(item)

    def handle_delete_button_clicked(self):
        """Handle when user clicks delete on a class."""
        button = self.centralwidget.focusWidget()
        index = self.table.indexAt(button.pos())
        if index.isValid():
            with DatabaseManager() as db:
                db.delete_class(self.table.item(index.row(), 0).text())
        self.table.setRowCount(0)
        self.populate_classes_table()

    def training_selected(self, first_load=False):
        """Handle when user selects a class, load the attendees."""
        index = self.table.selectionModel().currentIndex()
        if index.column() == 0:
            self.populate_attendees_list(self.table.item(index.row(),
                                                         0).text())


class TrainingSessionManager(QWidget):
    """Handle creation of a new training session, scan for member faces etc."""

    def __init__(self, class_label, class_type, label, attendee_list, return_btn):
        """Init TrainingSessionManager."""
        super().__init__()
        timestamp = datetime.now().strftime('%Y-%d-%m %H:%M')
        self.return_btn = return_btn
        self.video_enginge = TrainingSesVideoEngine(label)
        self.attendee_list = attendee_list
        QScroller.grabGesture(self.attendee_list, QScroller.TouchGesture)
        self.attendees = []
        self.class_session = f"{class_type} {timestamp}"
        class_label.setTitle(self.class_session)

        self.video_enginge.thread.detected_face_signal.connect(self.member_detected)
        self.video_enginge.thread.class_timer_reached.connect(self.end_session_registering)

    def member_detected(self, member_id):
        """Call when a members face is recognized."""
        if member_id not in self.attendees:
            self.attendees.append(member_id)
            with DatabaseManager() as db:
                item = QListWidgetItem(db.get_member_name(member_id)[0])
                item.setForeground(QColor('#168b44'))
                self.attendee_list.addItem(item)

    def save_session(self):
        """Save the traning session and it's attendees."""
        if len(self.attendees) > 0:
            with DatabaseManager() as db:
                db.save_training_session(self.class_session, self.attendees)

    def end_session_registering(self):
        """Stop scanning for faces and save the recorded session, return to main."""
        self.return_btn.click()
