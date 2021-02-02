from PyQt5.QtWidgets import QTreeWidget
from os import listdir
import glob


class MemoModules:
    def __init__(self):
        super().__init__()

    def load_initial_memos(self, tree_widget=None):
        print('load initial memos')

        file_arr = glob.glob('memos/*.txt')

        print(file_arr)

