from sources.all_imports import *


class Handler:
    def __init__(self):
        from sources.debugger_print import debugger_print
        self.root = Tk()
        debugger_print("initialized Handler")

    def start_tk(self):
        self.root.iconbitmap('DM_icon.ico')
        self.root.title('Rootstock Work Order Handler')
        self.root.geometry("1200x600")

    def root(self):
        return self.root
