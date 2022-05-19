from sources.all_imports import *


class Handler:
    def __init__(self):
        from sources.debugger_print import debugger_print_gui_setup
        self.root = Tk()
        debugger_print_gui_setup("initialized Handler")

    def start_tk(self):
        self.root.iconbitmap('DM_icon.ico')
        self.root.title('Rootstock Work Order Handler')
        self.root.geometry("1200x600")

    def root(self):
        return self.root


if __name__ == "__main__":
    print("Hello world!")
