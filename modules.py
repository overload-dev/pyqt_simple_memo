from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QTextEdit
import pathlib
import os.path, time
from PyQt5.QtCore import Qt

import glob


class Modules(QTreeWidget, QTextEdit):
    def __init__(self, memo_tree, memo_content):
        super().__init__()
        self.memo_tree = memo_tree
        self.memo_content = memo_content

        self._flag_change = False

    def parse_memo_content(self, fname):
        try:
            f = open('memos\\' + fname + '.txt', 'r')
            data = f.read()
            f.close()
            self.memo_content.setText(data)
        except TypeError:
            print('팝업 처리 필요')

    def on_double_click_tree_item(self, item, column_no):
        clicked_memo_name = item.data(0, Qt.UserRole)
        # 기존 작성 내용이 저장되었는지 체크필요
        self.parse_memo_content(clicked_memo_name)

    def load_initial_memos(self):
        print('load initial memos')
        file_arr = glob.glob('memos/*.txt')

        for file_dir in file_arr:
            file_name = (file_dir.replace('memos\\', '')).replace('.txt', '')
            item = QTreeWidgetItem(self.memo_tree)
            item.setText(0, file_name)
            item.setText(1, time.ctime(os.path.getmtime(file_dir)))
            item.setData(0, Qt.UserRole, file_name)

        self.memo_tree.itemDoubleClicked.connect(self.on_double_click_tree_item)

