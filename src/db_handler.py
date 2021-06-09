"""
This file contains classes for handling the database connection inDojoAttender.

Does also contain classes for handling data export to USB from the database.
"""

import os
import shutil
import sqlite3
import time
from pathlib import Path

import pandas as pd
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog
from sh import pumount

from ui.ui_transfer_dialog import Ui_DataTransfer


class DatabaseManager(object):
    """Class for handling connection to sqlite db."""

    def __init__(self):
        """Initiate DB."""
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.conn = sqlite3.connect(f"{dir_path}/../data/data.db")
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS "members" (
                "member_id"	INTEGER UNIQUE,
                "name"	TEXT,
                "encodings"	BLOB,
                "picture"	BLOB,
                PRIMARY KEY("member_id" AUTOINCREMENT)
                );''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS "attendance" (
                "class"	TEXT,
                "member_id"	INTEGER,
                FOREIGN KEY (member_id)
                REFERENCES members (member_id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
                );''')

    def __enter__(self):
        """Needed for class to be used in a context."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close DB connection on destruction of class."""
        self.conn.close()

    def add_member(self, member_dict):
        """Add new member to DB."""
        member = (None, member_dict['name'], member_dict['encodings'],
                  sqlite3.Binary(member_dict['picture']))
        self.cur.execute('''INSERT INTO members VALUES (?, ?, ?, ?)''', member)
        self.conn.commit()

    def get_member_name(self, member_id):
        """Get members name from DB."""
        self.cur.execute('''SELECT name FROM members WHERE member_id = ?''',
                         [str(member_id)])
        return self.cur.fetchall()[0]

    def get_members(self):
        """Get all members."""
        return self.cur.execute('SELECT * FROM members')

    def get_members_names(self):
        """Get all members names."""
        query = self.cur.execute('SELECT name FROM members')
        members = []
        for member in query:
            members.append(member[0])
        return members

    def delete_member(self, member_id):
        """Delete a member from the DB."""
        self.cur.execute('''DELETE FROM members WHERE member_id = ?;''',
                         [str(member_id)])
        self.conn.commit()

    def save_training_session(self, session, attendees):
        """Save a new training session."""
        for attendee in attendees:
            session_save = (session, attendee)
            self.cur.execute('''INSERT INTO attendance VALUES (?, ?)''',
                             session_save)
            self.conn.commit()

    def get_training_sessions(self):
        """Get a specific class/training session."""
        return self.cur.execute('SELECT DISTINCT class FROM attendance')

    def get_training_session_attendees(self, class_id):
        """Get attendees of a specific class/training session."""
        self.cur.execute('''SELECT m.name FROM members AS m
                            INNER JOIN attendance AS a
                            ON a.member_id = m.member_id
                            WHERE a.class = ?''', [str(class_id)])
        fetched = self.cur.fetchall()
        return fetched

    def get_all_training_sessions_and_attendees(self):
        """Get all training sessions and their attendees."""
        sessions = []
        for session in self.get_training_sessions():
            sessions.append(session[0])
        attendees = []
        for session in sessions:
            res = self.cur.execute('''SELECT m.name FROM members AS m
                                   INNER JOIN attendance AS a
                                   ON a.member_id = m.member_id
                                   WHERE a.class = ?''',
                                   [str(session)]).fetchall()
            _attendees = []
            for a in res:
                _attendees.append(a[0])
            attendees.append(_attendees)
        return [sessions, attendees]

    def delete_class(self, class_id):
        """Delete a specific class from the DB."""
        self.cur.execute('''DELETE FROM attendance WHERE class = ?;''',
                         [str(class_id)])
        self.conn.commit()


class WorksheetGenerator(QThread):
    """Worker for generating worksheet and transfering to USB."""

    update_label_signal = pyqtSignal(str)

    def __init__(self, usb_device):
        """Initiate worker."""
        super().__init__()
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.usb_device = usb_device

    def run(self):
        """Will be when starting worker."""
        dataframe = self.generate_dataframe()
        self.generate_worksheet(dataframe)
        self.save_to_usb()
        self.update_label_signal.emit("Data transfer done, remove USB device")

    def close(self):
        """Will be called when stopping worker."""
        self.quit()
        self.wait()

    def generate_dataframe(self):
        """Generate Pandas dataframe with classes/training sessions from Database."""
        og_text = "Generating excel file"
        text = "Generating excel file"
        with DatabaseManager() as db:
            members = db.get_members_names()
            members.insert(0, 'Training session')
            df = pd.DataFrame(columns=members)

            data = db.get_all_training_sessions_and_attendees()
            to_append = []
            for i, training in enumerate(data[0]):
                if len(text) > 25:
                    text = og_text
                else:
                    text = text + "."
                self.update_label_signal.emit(text)

                _dict = {'Training session': training}
                for attendee in data[1][i]:
                    _dict[attendee] = "✔"
                to_append.insert(0, _dict)
                time.sleep(0.5)

            final_df = pd.concat([pd.DataFrame(to_append), df],
                                 ignore_index=True).fillna("X")
        return final_df

    def str_len(self, str):
        """Get correct length of worksheet strings."""
        row_l = len(str)
        utf8_l = len(str.encode('utf-8'))
        return (utf8_l-row_l)/2+row_l

    def generate_worksheet(self, final_df):
        """Generate worksheet."""
        writer = pd.ExcelWriter(f'{self.dir_path}/../data/DojoAttendance.xlsx',
                                engine='xlsxwriter')
        final_df.to_excel(writer, sheet_name='Attendance', index=False)
        workbook = writer.book
        worksheet = writer.sheets['Attendance']
        end_row = final_df.shape[0]
        end_col = final_df.shape[1] - 1
        red_format = workbook.add_format({'bg_color':   '#FFC7CE',
                                          'font_color': '#9C0006'})
        green_format = workbook.add_format({'bg_color':   '#C6EFCE',
                                            'font_color': '#006100'})
        alignment = workbook.add_format({
                                'valign': 'center',
                                'align': 'center'})

        worksheet.conditional_format(0, 0, end_row, end_col,
                                     {'type': 'cell',
                                      'criteria': 'equal to',
                                      'value': '"X"',
                                      'format': red_format})
        worksheet.conditional_format(0, 0, end_row, end_col,
                                     {'type': 'cell',
                                      'criteria': 'equal to',
                                      'value': '"✔"',
                                      'format': green_format})
        for idx, col in enumerate(final_df):
            series = final_df[col]
            max_len = max((
                series.astype(str).map(self.str_len).max(),
                self.str_len(str(series.name)))) + 2
            worksheet.set_column(idx, idx, max_len, alignment)
        writer.save()

    def save_to_usb(self):
        """Save worksheet to usb."""
        p = Path('/media/usb')
        while not p.is_mount():
            self.update_label_signal.emit("Transfering to USB")
            time.sleep(0.3)
        shutil.copy(src=f'{self.dir_path}/../data/DojoAttendance.xlsx',
                    dst='/media/usb/DojoAttendance.xlsx')
        os.sync()
        time.sleep(1)
        pumount(str(self.usb_device))
        os.remove(f"{self.dir_path}/../data/DojoAttendance.xlsx")


class DataTransferManager(QDialog):
    """Class for handling Data export to USB."""

    def __init__(self, parent, observer):
        """Initiate popup dialog and connect signals."""
        super().__init__(parent)
        self.dialog = Ui_DataTransfer()
        self.dialog.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.dialog.CancelBtn.clicked.connect(self.close)
        observer.deviceEvent.connect(self.usb_event)

    def usb_event(self, device):
        """To be called when a USB event is registered from monitor started in main."""
        if 'ID_FS_TYPE' in device:
            if device.action == "add":
                self.dialog.CancelBtn.setEnabled(False)
                self.generator = WorksheetGenerator(device.device_node)
                self.generator.update_label_signal.connect(self.update_label)
                self.generator.start()
            elif device.action == "remove":
                self.close()

    def closeEvent(self, event):
        """To be called when dialog closes."""
        self.generator.close()
        event.accept()

    def update_label(self, update_str):
        """Update text label in Dialog."""
        self.dialog.label.setText(update_str)
