from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
import pathlib

import glob


class MemoModules:
    def __init__(self):
        super().__init__()

    def load_initial_memos(self, tree_widget=None):
        print('load initial memos')
        file_arr = glob.glob('memos/*.txt')

        file_info = []

        for file in file_arr:
            fname = pathlib.Path(file)


        file_arr = [QTreeWidgetItem(file_name.replace('memos\\', '') for file_name in file_arr)]


        tree_widget.addTopLevelItems(file_arr)
