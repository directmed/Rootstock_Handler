from sources.loc2loc import *
from sources.login import *
from sources.item_info import *
from sources.locations import *
from sources.wo_init import *
from sources.dm_repair import *
from sources.std_operations import *
from sources.gen_picklist import *
from sources.issue_wo import *
from sources.time_booking import *
from sources.receipt_wo import *
from sources.wo_close import *
from sources.debugger_print import *
from sources.variables import *


# perform an update on the drop down menu when an event happens
# Common events: '<Return>', '<FocusOut>'
def drop_menu_accept_input(self, event, options):
    debugger_print(event)
    debugger_print(self.get())
    match_flag = False
    for option in options:
        if self.get() in option:
            match_flag = True
            break

    if match_flag is False:
        self.set(self.current(0))
        debugger_print("no match found")
    else:
        self.autocomplete()
        debugger_print("found a match")

    return


def variable_tester(all_val):
    from sources.variables import Xpaths

    xpaths = Xpaths()
    xpaths.get_xpaths()
    xpaths.print_all()

    debugger_print(len(all_val))
    debugger_print(all_val)
    for key, val in all_val.items():
        try:
            if val.get() is True or val.get() is False:
                debugger_print(key + ' = ' + val.get().__str__())
            else:
                debugger_print(key + ' = ' + val.get().__str__())
        except TypeError:
            debugger_print(key + ' = ' + val.get("1.0", END).__str__())


def run_wo_maker(main_gui):
    from sources.variables import wo_data, original_location, item_info, test_flag
    from sources.variables import Xpaths
    from sources.debugger_print import get_files_dir

    try:
        try:
            error_log_dir, track_str = get_files_dir()

            error_log_unit_name = "\\unit.txt"
            error_log_unit = error_log_dir + error_log_unit_name

            main_gui.get_gui_entries()

            item = main_gui.get_unit_info_entry_box_text_vars('Part Number')
            serial = main_gui.get_unit_info_entry_box_text_vars('Serial Number')
            unit_str = item + '_' + serial

            # check if 'track' file exists.
            track_exists = os.path.exists(error_log_unit)
            if not track_exists:
                with open(error_log_unit, 'x') as f:
                    f.write(unit_str.__str__())
            # if file exists, get current iteration and update for next iteration.
            else:
                with open(error_log_unit, 'w') as f:
                    f.write(unit_str.__str__())

            wo_page_flag = False
            # set up xpaths from csv file
            main_xpaths = Xpaths()
            main_xpaths.get_xpaths()
            # main_xpaths.print_all()
            # google chromedriver.exe auto installer
            cdai = chromedriver_autoinstaller.install(True)

            # Load cookies created in start_up.py: If user cannot log in, run start_up.py
            cookie_dir = os.path.abspath("chrome-data")
            cookie_dir_text = str(cookie_dir)
            chrome_options = Options()
            chrome_options.add_argument("--user-data-dir=" + cookie_dir_text)
            main_driver = webdriver.Chrome(cdai, options=chrome_options)

            if main_gui.get_perform_tasks_check_box_values('Location Transfer') is False \
                    and main_gui.get_perform_tasks_check_box_values('Create and Assign WO') is False \
                    and main_gui.get_perform_tasks_check_box_values('DM Repair Information') is False \
                    and main_gui.get_perform_tasks_check_box_values('Add Standard Operations and Booking') is False \
                    and main_gui.get_perform_tasks_check_box_values('WO Receipt') is False:
                main_driver.implicitly_wait(150)

            # Log-in to Salesforce
            login_init(main_driver, main_xpaths, main_gui)
            # get the item info
            get_item_info(main_driver, main_xpaths, main_gui)

            # CHECK IF THE COIL IS CUSTOMER PROPERTY
            # set variables for Location to Location function.
            ret_list = set_previous_location()
            debugger_print("ret_list = " + ret_list.__str__())
            original_location['id'] = ret_list[0]
            original_location['key'] = ret_list[1]
            original_location['no'] = set_inventory_location()

            if main_gui.get_perform_tasks_check_box_values('Location Transfer') is True:
                # Override location if flag is True
                loc_to_loc_transfer(main_driver, main_xpaths, main_gui)

            """Initialize the Work Order and Enter the relevant data """
            # check if there is a pre-existing WO and prompt the user if they would like to user that WO instead.
            if main_gui.get_perform_tasks_check_box_values('Create and Assign WO') is True:

                # check if there is a work order associated with this item
                if item_info[7] is not None and "WO" in item_info[7]:
                    # if a WO is found, prompt the user if they would like to open it.
                    wo_data['number'] = item_info[7].replace("WO-", "")
                    new_wo_flag = get_wo_page(main_driver, main_xpaths)
                    if new_wo_flag is True:
                        # Previous WO found has been completed. Open a new WO.
                        debugger_print("No Previous WO has been created.")
                        wo_data['number'] = work_order_init(main_driver, main_xpaths, main_gui)
                        wo_data['number'] = wo_data['number'].replace("WO-", "")
                        wo_page_flag = True
                else:
                    # No WO has been found. A new WO will be created.
                    debugger_print("No Previous WO has been created.")
                    wo_data['number'] = work_order_init(main_driver, main_xpaths, main_gui)
                    wo_data['number'] = wo_data['number'].replace("WO-", "")

                    if test_flag is False:
                        # Generate the PickList
                        debugger_print("Generating Pick List")
                        wo_data['number'] = generate_picklist(main_driver, main_xpaths)
                        wo_data['number'] = wo_data['number'].replace("WO-", "")
                        wo_page_flag = True

                    # Issue the work order to the correct serial number
                    debugger_print("Issuing WO to given Serial Number.")
                    wo_issue(main_driver, main_xpaths, main_gui)

            elif main_gui.get_unit_info_check_box_vars('Use Previous WO') is True:
                wo_data['number'] = main_gui.get_unit_info_entry_box_text_vars('Previous WO Number')
                wo_data['number'] = wo_data['number'].replace("WO-", "")
                open_wo_page(main_driver, main_xpaths, main_gui)
                wo_page_flag = True
            elif main_gui.get_perform_tasks_check_box_values('DM Repair Information') is True \
                    or main_gui.get_perform_tasks_check_box_values('DM Repair Information') is True \
                    or main_gui.get_perform_tasks_check_box_values('DM Repair Information') is True \
                    or main_gui.get_perform_tasks_check_box_values('DM Repair Information') is True \
                    or main_gui.get_perform_tasks_check_box_values('DM Repair Information') is True:
                wo_data['number'] = item_info[7].__str__()
                debugger_print("run_wo_maker: wo_data['number'] = " + wo_data['number'])
                get_wo_page(main_driver, main_xpaths)
                wo_page_flag = True

            if test_flag is False and wo_page_flag is True:
                # Add DM Repair Info, wo required
                if main_gui.get_perform_tasks_check_box_values('DM Repair Information') is True:
                    dm_repair_info(main_driver, main_xpaths, main_gui)

                # Add standard Operations, wo required
                if main_gui.get_perform_tasks_check_box_values('Add Standard Operations and Booking') is True:
                    add_std_operation(main_driver, main_xpaths, main_gui)
                # Perform the TQ Booking, wo required
                # if main_gui.get_perform_tasks_check_box_values('Add Booking') is True:
                    tq_booking(main_driver, main_xpaths, main_gui)

                # Perform WO Receipt and change final loaction.
                if main_gui.get_perform_tasks_check_box_values('WO Receipt') is True:
                    wo_receipt(main_driver, main_xpaths, main_gui)

                # close WO
                """
                if main_gui.get_perform_tasks_check_box_values('Close WO') is True:
                    wo_data['status'] = check_wo_page_status(main_driver, main_xpaths)
                    if wo_data['status'] is not None and wo_data['status'] == "8":
                        close_wo(main_driver, main_xpaths)
                """
            elif wo_page_flag is False:
                debugger_print("WO page is not open")

            main_driver.close()
        except NoSuchWindowException:
            debugger_print("Browser was closed manually.")

    except Exception as e:
        debugger_print("\n\n\n********** Exception Called **********")
        debugger_print(traceback.format_exc())


if __name__ == "__main__":
    print("Hello world!")
