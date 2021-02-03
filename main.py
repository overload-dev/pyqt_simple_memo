import sys
import datetime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import Qt

from model import MemoModel

form_main = uic.loadUiType("views/main.ui")[0]


class WindowClass(QMainWindow, form_main):

    def __init__(self):
        super().__init__(flags=Qt.Window)
        self.setupUi(self)
        self._flag_memo_modified = False
        self._flag_savable = False
        self._is_new = True
        self._selected_memo = None
        self.memo_model = MemoModel()
        self.load_initial_memos()

    def load_initial_memos(self):
        # memo list parse
        self._parse_tree()
        self.memo_content.textChanged.connect(self._memo_modified)
        self.memo_title.textChanged.connect(self._memo_modified)

        self.btn_new.clicked.connect(self._new_memo_mode)

        self.btn_save.setDisabled(True)
        self.btn_save.clicked.connect(self._save_memo)
        self.btn_del.setDisabled(True)
        self._flag_savable = False
        self._flag_memo_modified = False

    def _new_memo_mode(self):
        self._is_new = True
        self._selected_memo = None
        self.memo_title.clear()
        self.memo_content.clear()

    def _save_memo(self):
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if self._is_new:
            no = self.memo_model.insert(
                self.memo_title.text(),
                self.memo_content.toPlainText(),
                date, date
            )
            memo = self.memo_model.get_one(no)
            item = QTreeWidgetItem(self.memo_tree)
            item.setText(0, memo.attrib['title'])
            item.setText(1, memo.attrib['m_date'])
            item.setText(2, memo.attrib['c_date'])
            item.setData(0, Qt.UserRole, memo.attrib['no'])
            self._change_memo(item)
        else:
            print(self._selected_memo.data(0, Qt.UserRole))

            self.memo_model.update(
                self._selected_memo.data(0, Qt.UserRole),
                self.memo_title.text(),
                self.memo_content.toPlainText(),
                date)

            self._selected_memo.setText(0, self.memo_title.text())
            self._selected_memo.setText(1, date)
            self._change_memo(self._selected_memo)

    def _parse_tree(self):
        self.memo_tree.clear()
        for memo in self.memo_model.get_all():
            item = QTreeWidgetItem(self.memo_tree)
            item.setText(0, memo.attrib['title'])
            item.setText(1, memo.attrib['m_date'])
            item.setText(2, memo.attrib['c_date'])
            item.setData(0, Qt.UserRole, memo.attrib['no'])

        self.memo_tree.itemClicked.connect(self._click_tree_item)

    # content or title changed flag
    def _memo_modified(self):
        self._flag_memo_modified = True

        title_len = len(self.memo_title.text().strip())
        content_len = len(self.memo_content.toPlainText().strip())

        # no content so can not save memo
        if title_len <= 0 or content_len <= 0:
            self._flag_savable = False
            self.btn_save.setDisabled(True)
        else:
            self._flag_savable = True
            self.btn_save.setDisabled(False)

    def _click_tree_item(self, item):
        if self._flag_memo_modified:
            result = QMessageBox.question(self, 'Memo', '저장하지 않은 문서가 있습니다. 메모를 바꿀까요?'
                                          , QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.Yes:
                self._change_memo(item)
            else:
                if self._selected_memo is not None:
                    self.memo_tree.clearSelection()
                    self._selected_memo.setSelected(True)
        else:
            self._change_memo(item)

    def _change_memo(self, item):
        content = self.memo_model.get_one(item.data(0, Qt.UserRole))
        self._selected_memo = item
        self._selected_memo.setSelected(True)
        self._is_new = False
        self.memo_content.setText(content.findtext('content'))
        self.memo_title.setText(content.attrib['title'])
        self._flag_savable = False
        self._flag_memo_modified = False
        self.btn_save.setDisabled(True)
        self.btn_del.setDisabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec_())
