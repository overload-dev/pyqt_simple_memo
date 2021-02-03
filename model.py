import xml.etree.ElementTree as ET
import uuid

class MemoModel:
    def __init__(self):
        super().__init__()
        self.memo_elements = None
        self.load_memos()

    def load_memos(self):
        f = open('memos/memos.xml', 'r+', encoding='UTF-8')
        self.memo_elements = ET.parse(f)

    def get_all(self):
        return self.memo_elements.getroot()

    def get_one(self, no):
        return self.memo_elements.getroot().find('./memo[@no=\'%s\']' % no)

    def update(self, no, title, content, m_date):
        origin = self.memo_elements.getroot().find('./memo[@no=\'%s\']' % no)
        origin.attrib['title'] = title
        origin.attrib['m_date'] = m_date
        origin.find('./content').text = content
        self.memo_elements.write('memos/memos.xml')

    def insert(self, title, content, c_date, m_date):
        no = str(uuid.uuid4())
        origin = self.memo_elements.getroot()
        node_memo = ET.Element('memo')
        node_memo.attrib['no'] = no
        node_memo.attrib['title'] = title
        node_memo.attrib['c_date'] = c_date
        node_memo.attrib['m_date'] = m_date

        node_content = ET.Element('content')
        node_content.text = content

        node_memo.append(node_content)
        origin.append(node_memo)
        self.memo_elements.write('memos/memos.xml')
        return no

    def delete(self, no):
        origin = self.memo_elements.getroot()
        del_memo = self.memo_elements.getroot().find('./memo[@no=\'%s\']' % no)
        origin.remove(del_memo)
        self.memo_elements.write('memos/memos.xml')
