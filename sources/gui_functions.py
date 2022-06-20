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

    # google chromedriver.exe auto installer
    cdai = chromedriver_autoinstaller.install(True)
    # Load cookies created in start_up.py: If user cannot log in, run start_up.py
    cookie_dir = os.path.abspath("chrome-data")
    cookie_dir_text = str(cookie_dir)
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=" + cookie_dir_text)
    main_driver = webdriver.Chrome(cdai, options=chrome_options)
    try:
        try:
            try:
                # set up directory and file name for logging information
                error_log_dir, track_str = get_files_dir()
                error_log_unit_name = "\\unit.txt"
                error_log_unit = error_log_dir + error_log_unit_name

                # check if 'Customer Property' is checked.
                cancel_flag = False
                if main_gui.get_unit_info_check_box_vars('Customer Property') is False:
                    prompt = messagebox.askyesno(title="Customer Property", message="Is this unit customer property?")

                    if prompt is True:
                        # Unit is customer property but checkbox is not checked.
                        cancel_flag = True
                        debugger_print("Pop-up: customer property checkbox needs to be checked.")
                        messagebox.showinfo(title="Customer Property", message="Please check the 'Customer Property' checkbox and select the correct location if applicable.")
                        raise ValueError("\ngui_functions.py: Customer Property not checked.")

                    elif prompt is False:
                        # Continue program
                        debugger_print("Pop-up: unit is not customer property")

                if cancel_flag is False:
                    main_gui.get_gui_entries()  # prints user input to log file or console.
                    # get the unit information to use for the file name
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

                    # If all checkboxes are unchecked, user is setting up browser cookies. Increase waiting time.
                    if main_gui.get_perform_tasks_check_box_values('Location Transfer') is False \
                            and main_gui.get_perform_tasks_check_box_values('Create and Assign WO') is False \
                            and main_gui.get_perform_tasks_check_box_values('DM Repair Information') is False \
                            and main_gui.get_perform_tasks_check_box_values('Add Standard Operations and Booking') is False \
                            and main_gui.get_perform_tasks_check_box_values('WO Receipt') is False:
                        main_driver.implicitly_wait(150)

                    # Log-in to Salesforce
                    error_flag = login_init(main_driver, main_xpaths, main_gui)
                    if error_flag is True:
                        raise ValueError("\nlogin_init.py: something went wrong.")

                    # get the item info
                    error_flag = get_item_info(main_driver, main_xpaths, main_gui)
                    if error_flag is True:
                        raise ValueError("\nget_item_info.py: something went wrong.")

                    # CHECK IF THE COIL IS CUSTOMER PROPERTY
                    # set variables for Location to Location function.
                    ret_list = set_previous_location()
                    debugger_print("ret_list = " + ret_list.__str__())
                    error_flag = ret_list[0]
                    if error_flag is True:
                        raise ValueError("\nlocations.py: set_previous_location() malfunction")
                    original_location['id'] = ret_list[1]
                    original_location['key'] = ret_list[2]
                    original_location['no'] = set_inventory_location()

                    if main_gui.get_perform_tasks_check_box_values('Location Transfer') is True:
                        # Override location if flag is True
                        error_flag = loc_to_loc_transfer(main_driver, main_xpaths, main_gui)
                        if error_flag is True:
                            raise ValueError("\nlocations.py: set_previous_location() malfunction")

                    """Initialize the Work Order and Enter the relevant data """
                    # check if there is a pre-existing WO and prompt the user if they would like to user that WO instead
                    if main_gui.get_perform_tasks_check_box_values('Create and Assign WO') is True:

                        # check if there is a work order associated with this item
                        if item_info[7] is not None and "WO" in item_info[7]:
                            # if a WO is found, prompt the user if they would like to open it.
                            wo_data['number'] = item_info[7].replace("WO-", "")
                            error_flag, new_wo_flag = get_wo_page(main_driver, main_xpaths)
                            if error_flag is True:
                                raise ValueError("\nitem_info.py: get_wo_page() malfunction")

                            elif new_wo_flag is True:
                                # Previous WO found has been completed. Open a new WO.
                                debugger_print("No Previous WO has been created.")
                                error_flag, wo_data['number'] = work_order_init(main_driver, main_xpaths, main_gui)
                                if error_flag is True:
                                    raise ValueError("\nwo_init.py: work_order_init() malfunction")
                                elif wo_data['number'] is not None:
                                    wo_data['number'] = wo_data['number'].replace("WO-", "")
                                    if test_flag is False:
                                        # Generate the PickList
                                        debugger_print("Generating Pick List")
                                        error_flag, wo_data['number'] = generate_picklist(main_driver, main_xpaths)
                                        if error_flag is True:
                                            raise ValueError("\ngen_picklist.py: generate_picklist() malfunction")
                                        elif wo_data['number'] is not None:
                                            wo_data['number'] = wo_data['number'].replace("WO-", "")
                                            wo_page_flag = True
                                            debugger_print("wo_page_fag set True")
                                        else:
                                            raise ValueError(
                                                "wo_data['number'] = None\nSomething went wrong creating WO.")
                                    # wo_page_flag = True
                                    # debugger_print("wo_page_fag set True")
                                else:
                                    raise ValueError("wo_data['number'] = None\nSomething went wrong opening existing WO.")
                        else:
                            # No WO has been found. A new WO will be created.
                            debugger_print("No Previous WO has been created.")
                            error_flag, wo_data['number'] = work_order_init(main_driver, main_xpaths, main_gui)
                            if error_flag is True:
                                raise ValueError("\nwo_init.py: work_order_init() malfunction")
                            elif wo_data['number'] is not None:
                                wo_data['number'] = wo_data['number'].replace("WO-", "")
                                if test_flag is False:
                                    # Generate the PickList
                                    debugger_print("Generating Pick List")
                                    error_flag, wo_data['number'] = generate_picklist(main_driver, main_xpaths)
                                    if error_flag is True:
                                        raise ValueError("\ngen_picklist.py: generate_picklist() malfunction")
                                    elif wo_data['number'] is not None:
                                        wo_data['number'] = wo_data['number'].replace("WO-", "")
                                        wo_page_flag = True
                                    else:
                                        raise ValueError("wo_data['number'] = None\nSomething went wrong creating WO.")

                            # Issue the work order to the correct serial number
                            debugger_print("Issuing WO to given Serial Number.")
                            error_flag = wo_issue(main_driver, main_xpaths, main_gui)
                            if error_flag is True:
                                raise ValueError("\nissue_wo.py: wo_issue() malfunction")

                    elif main_gui.get_unit_info_check_box_vars('Use Previous WO') is True:
                        # open existing WO
                        wo_data['number'] = main_gui.get_unit_info_entry_box_text_vars('Previous WO Number')
                        wo_data['number'] = wo_data['number'].replace("WO-", "")
                        error_flag = open_wo_page(main_driver, main_xpaths, main_gui)
                        if error_flag is True:
                            raise ValueError("\nissue_wo.py: wo_issue() malfunction")
                        else:
                            # WO is now open
                            wo_page_flag = True

                    # automatically open any open WO associated with this unit.
                    elif main_gui.get_perform_tasks_check_box_values('Location Transfer') is True \
                            or main_gui.get_perform_tasks_check_box_values('Create and Assign WO') is True \
                            or main_gui.get_perform_tasks_check_box_values('DM Repair Information') is True \
                            or main_gui.get_perform_tasks_check_box_values('Add Standard Operations and Booking') is True \
                            or main_gui.get_perform_tasks_check_box_values('WO Receipt') is True:
                        wo_data['number'] = item_info[7].__str__()
                        debugger_print("run_wo_maker: wo_data['number'] = " + wo_data['number'])
                        error_flag = get_wo_page(main_driver, main_xpaths)
                        if error_flag is True:
                            raise ValueError("\nissue_wo.py: wo_issue() malfunction. Tried to open WO automatically.")
                        else:
                            # WO is now open
                            wo_page_flag = True

                    if test_flag is False and wo_page_flag is True:
                        # Add DM Repair Info, wo required
                        if main_gui.get_perform_tasks_check_box_values('DM Repair Information') is True:
                            error_flag = dm_repair_info(main_driver, main_xpaths, main_gui)
                            if error_flag is True:
                                raise ValueError("\ndm_repair.py: dm_repair_info() malfunction.")

                        # Add standard Operations, wo required
                        if main_gui.get_perform_tasks_check_box_values('Add Standard Operations and Booking') is True:
                            error_flag = add_std_operation(main_driver, main_xpaths, main_gui)
                            if error_flag is True:
                                raise ValueError("\nstd_operations.py: add_std_operation() malfunction")

                        # Perform the TQ Booking, wo required
                        # if main_gui.get_perform_tasks_check_box_values('Add Booking') is True:
                            error_flag = tq_booking(main_driver, main_xpaths, main_gui)
                            if error_flag is True:
                                raise ValueError("\ntime_booking.py: tq_booking() malfunction")

                        # Perform WO Receipt and change final loaction.
                        if main_gui.get_perform_tasks_check_box_values('WO Receipt') is True:
                            wo_receipt(main_driver, main_xpaths, main_gui)
                            if error_flag is True:
                                raise ValueError("\nreceipt_wo.py: wo_receipt() malfunction")

                        # close WO
                        """
                        if main_gui.get_perform_tasks_check_box_values('Close WO') is True:
                            wo_data['status'] = check_wo_page_status(main_driver, main_xpaths)
                            if wo_data['status'] is not None and wo_data['status'] == "8":
                                close_wo(main_driver, main_xpaths)
                        """

                    try:
                        main_driver.close()
                        if wo_page_flag is True:
                            box_message = "Your Work Order is: WO-" + wo_data['number'].__str__()
                            main_gui.set_unit_info_entry_box_text_vars('Previous WO Number', wo_data['number'].__str__())
                        elif main_gui.get_perform_tasks_check_box_values('Create and Assign WO') is False and main_gui.get_unit_info_check_box_vars('Use Previous WO') is False:
                            box_message = "Task performed successfully."
                            debugger_print("Task performed successfully.")
                        else:
                            box_message = "No Work Order was available for this Run."
                            debugger_print("WO page is not open.")

                        messagebox.showinfo(title="Run is Complete", message=box_message)

                    except Exception as e:
                        debugger_print("No browser was open.")
                        debugger_print(traceback.format_exc())
            except NoSuchWindowException:
                debugger_print("Browser was closed manually.")

        except ValueError as exp:
            debugger_print('\n\n\nError:  ' + exp.__str__())
            try:
                main_driver.close()
            except Exception as e:
                debugger_print("No browser was open.")
                debugger_print(traceback.format_exc())

    except Exception as e:
        debugger_print("\n\n\n********** Exception Called **********")
        debugger_print(traceback.format_exc())
        try:
            main_driver.close()
        except Exception as e:
            debugger_print("No browser was open.")
            debugger_print(traceback.format_exc())


if __name__ == "__main__":
    print("Hello world!")
