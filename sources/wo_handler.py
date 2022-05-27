# Import all files in this folder
from sources.handler import Handler
from sources.gui_setup import GuiSetup
from updater import Updater
from sources.debugger_print import setup_files

setup_files()
main_updater = Updater()
main_updater.start_updater()
if main_updater.load_updater_github() is True:
    main_updater.overwrite_files()

main_handler = Handler()
main_handler.start_tk()
main_root = main_handler.root
gui = GuiSetup(main_handler)
gui.start_gui()
main_root.mainloop()
