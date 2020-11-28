from PyQt5.QtWidgets import QMenu, QAction


class CreateMenuRC():
    def __init__(self, parent=None, options={}):
        self.parent = parent
        self.options = options
        self.menu = QMenu(parent)

    def effectsButtonMenu(self, style_sheet):
        self.menu.addAction(QAction('test', self.parent))
        self.menu.addAction(QAction('test', self.parent))
        self.menu.addAction(QAction('test', self.parent))
        self.menu.addAction(QAction('test', self.parent))
        self.menu.addAction(QAction('test', self.parent))
        self.menu.addAction(QAction('test', self.parent))

        for entry_name, entry_payload in self.options.items():
            self.menu.addAction(QAction(entry_name, entry_payload))
            self.menu.action.triggered.connect(lambda: print('pressed'))

        # Set style
        with open(style_sheet) as style_file:
            print(style_sheet)
            self.menu.setStyleSheet(style_file.read())

        return self.menu
