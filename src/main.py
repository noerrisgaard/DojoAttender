#!/usr/bin/python3
"""Main for DojoAttender."""
import sys
from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from pyudev import Context, Monitor
from pyudev.pyqt5 import MonitorObserver

from db_handler import DataTransferManager
from member_handler import EditMembersHandler, RegisterMemberHandler
from training_handler import ClassManager, TrainingSessionManager
from ui.ui_edit_classes__screen import Ui_EditClassesWindow
from ui.ui_edit_mem_screen import Ui_EditMemWindow
from ui.ui_main_screen import Ui_MainWindow
from ui.ui_reg_new_mem_screen import Ui_RegNewMemWindow
from ui.ui_start_class_screen import Ui_StartNewClassWindow
from video_handler import RegNewMemVideoEnginge


class MainWindow(QMainWindow):
    """Main window for DojoAttender."""

    def __init__(self):
        """Initiate Main window, register btn's and start monitor for USB events."""
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()
        self.ui.reg_new_mem_btn.clicked.connect(self.show_reg_new_mem_window)
        self.ui.view_edit_mem_btn.clicked.connect(self.show_edit_mem_window)
        self.ui.start_karate_btn.clicked.connect(partial(self.show_start_class_window, "Karate"))
        self.ui.start_kickboxing_btn.clicked.connect(partial(self.show_start_class_window, "Kickboxing"))
        self.ui.start_tai_btn.clicked.connect(partial(self.show_start_class_window, "Tai Chi"))
        self.ui.view_edit_session_btn.clicked.connect(self.show_edit_classes_window)
        self.ui.transfer_sessions_btn.clicked.connect(self.show_data_transfer)

        context = Context()
        monitor = Monitor.from_netlink(context)
        monitor.filter_by('block')
        self.observer = MonitorObserver(monitor)
        monitor.start()

    def show_reg_new_mem_window(self):
        """Show window for registering new members."""
        self.reg_new_mem_window = RegNewMemWindow()

    def show_edit_mem_window(self):
        """Show window for editing members."""
        self.edit_mem_window = EditMembersWindow()

    def show_edit_classes_window(self):
        """Show window for editing classes/training sessions."""
        self.edit_classes_window = EditClassesWindow()

    def show_start_class_window(self, classtype):
        """Show window for registering a new training session."""
        self.start_class_windows = StartNewClassWindow(classtype)

    def show_data_transfer(self):
        """Show dialog for data export/transfer."""
        dlg = DataTransferManager(self, self.observer)
        dlg.exec()


class StartNewClassWindow(QMainWindow):
    """Class for starting a new class/training session."""

    def __init__(self, classtype):
        """Initiate window and dependencies."""
        super(StartNewClassWindow, self).__init__()
        self.ui = Ui_StartNewClassWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()
        self.training_session_manager = TrainingSessionManager(self.ui.groupBox,
                                                               classtype,
                                                               self.ui.video_label,
                                                               self.ui.listWidget,
                                                               self.ui.return_btn)
        self.ui.return_btn.clicked.connect(self.close)

    def closeEvent(self, event):
        """Close event to run when window closes."""
        self.training_session_manager.save_session()
        self.training_session_manager.video_enginge.thread.stop()
        event.accept()


class EditMembersWindow(QMainWindow):
    """Class for starting window for editing members."""

    def __init__(self):
        """Initiate window and dependencies."""
        super(EditMembersWindow, self).__init__()
        self.ui = Ui_EditMemWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()
        self.member_handler = EditMembersHandler()
        self.member_handler.populate_members_table(self.ui.tableWidget,
                                                   self.ui.centralwidget)
        self.ui.return_btn.clicked.connect(self.close)


class EditClassesWindow(QMainWindow):
    """Class for starting window for editing classes/training sessions."""

    def __init__(self):
        """Initiate window and dependencies."""
        super(EditClassesWindow, self).__init__()
        self.ui = Ui_EditClassesWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()
        self.class_manager = ClassManager(self.ui.tableWidget,
                                          self.ui.centralwidget,
                                          self.ui.listWidget,
                                          self.ui.groupBox)
        self.class_manager.populate_classes_table()
        self.ui.return_btn.clicked.connect(self.close)


class RegNewMemWindow(QMainWindow):
    """Class for staring window for registering new members."""

    def __init__(self):
        """Initiate window and dependencies."""
        super(RegNewMemWindow, self).__init__()
        self.ui = Ui_RegNewMemWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()
        self.ui.return_btn.clicked.connect(self.close)
        self.video_enginge = RegNewMemVideoEnginge(self.ui.video_label)
        self.member_handler = RegisterMemberHandler(self.video_enginge,
                                                    self.ui.regmem_btn,
                                                    self.ui.return_btn,
                                                    self.ui.mem_name_input)
        self.ui.regmem_btn.clicked.connect(self.member_handler.register_new_member)

    def closeEvent(self, event):
        """Close event to run when window closes."""
        self.video_enginge.thread.stop()
        event.accept()


if __name__ == "__main__":
    App = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(App.exec_())
