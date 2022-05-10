from sources.debugger_print import *


def add_std_operation(driver, xpaths, gui):
    from sources.variables import increase_index, op_vars, op_widgets

    xpath_section = 'add_std_operation'

    debugger_print("\n******** Adding Standard Operation ********\n")
    # Perform entire Try statement for every operation
    if(len(op_vars)-1) >= 0:
        debugger_print(len(op_vars))
        for op_index in range(0, (len(op_vars))):
            section_index = -1
            try:
                # Wait for the RELATED LISTS tab to appear and click on it
                section_index = increase_index(section_index, xpaths.items_len(xpath_section))
                elem_xpath = xpaths.get_xpath(xpath_section, section_index)
                click_element(driver, elem_xpath, "Opening RELATED LISTS tab")

                # Click the OPERATIONS tab
                section_index = increase_index(section_index, xpaths.items_len(xpath_section))
                elem_xpath = xpaths.get_xpath(xpath_section, section_index)
                click_element(driver, elem_xpath, "Clicking OPERATIONS tab")

                # Click ADD STANDARD OPERATIONS button
                section_index = increase_index(section_index, xpaths.items_len(xpath_section))
                elem_xpath = xpaths.get_xpath(xpath_section, section_index)
                click_element(driver, elem_xpath, "Clicking ADD STANDARD OPERATIONS button")

                # Wait for std operations window to open
                str_temp = op_widgets[op_index]['Process'].get().__str__()
                str_index = str_temp.find(" ")
                if str_index != -1:
                    s_keys = str_temp[0:(str_index)]

                debug_message = "Wait for std operations window to open"
                section_index = increase_index(section_index, xpaths.items_len(xpath_section))
                elem_xpath = xpaths.get_xpath(xpath_section, section_index)
                input_text(driver, elem_xpath, s_keys, debug_message)

                # Select 30 for the PROCESS options
                str_temp = op_widgets[op_index]['Process'].get().__str__()
                section_index = increase_index(section_index, xpaths.items_len(xpath_section))
                elem_xpath = xpaths.get_xpath(xpath_section, section_index)
                select_option(driver, elem_xpath, str_temp, "Select " + str_temp + "for the PROCESS option")

                # Select DLFT for WORK CENTER options
                section_index = increase_index(section_index, xpaths.items_len(xpath_section))
                elem_xpath = xpaths.get_xpath(xpath_section, section_index)
                select_option(driver, elem_xpath, "DFLT", "Select DFLT for WORK CENTER options")

                # Select correct name form ASSIGNED TO options
                temp = gui.get_user_info_combo_boxes('Name')
                temp = temp.__str__()
                section_index = increase_index(section_index, xpaths.items_len(xpath_section))
                elem_xpath = xpaths.get_xpath(xpath_section, section_index)
                select_option(driver, elem_xpath, temp, "Select correct name form ASSIGNED TO options")

                # Click the LABOR STDS tab
                # /html/body/div[1]/div[2]/table/tbody/tr/td[2]/form/div[1]/div/div/div/div[2]/table/tbody/tr[1]/td/table/tbody/tr/td[6]/table/tbody/tr/td[2]/table/tbody/tr/td
                section_index = increase_index(section_index, xpaths.items_len(xpath_section))
                elem_xpath = xpaths.get_xpath(xpath_section, section_index)
                click_element(driver, elem_xpath, "Click the LABOR STDS tab")

                # Select PER PIECE from the SET UP TYPE options
                option = "Piece"
                section_index = increase_index(section_index, xpaths.items_len(xpath_section))
                elem_xpath = xpaths.get_xpath(xpath_section, section_index)
                select_option(driver, elem_xpath, option, "Select PER PIECE from the SET UP TYPE options")

                # Select REPAIR from the SETUP LABOR GRADE options
                option = "Repair"
                section_index = increase_index(section_index, xpaths.items_len(xpath_section))
                elem_xpath = xpaths.get_xpath(xpath_section, section_index)
                select_option(driver, elem_xpath, option, "Select REPAIR from the SETUP LABOR GRADE options")

                # Select PER PIECE from the RUN TYPE options
                option = "Piece"
                section_index = increase_index(section_index, xpaths.items_len(xpath_section))
                elem_xpath = xpaths.get_xpath(xpath_section, section_index)
                select_option(driver, elem_xpath, option, "Select PER PIECE from the RUN TYPE options")

                # Select REPAIR from the RUN LABOR GRADE options
                option = "Repair"
                section_index = increase_index(section_index, xpaths.items_len(xpath_section))
                elem_xpath = xpaths.get_xpath(xpath_section, section_index)
                select_option(driver, elem_xpath, option, "Select REPAIR from the RUN LABOR GRADE options")

                # Enter SETUP STANDARD HOURS filed
                if op_vars[op_index]['Expected Hours'].get().__str__() != "":
                    i_txt = op_vars[op_index]['Expected Hours'].get().__str__()
                else:
                    i_txt = "2.0"

                debug_message = "Enter SETUP STANDARD HOURS filed"
                section_index = increase_index(section_index, xpaths.items_len(xpath_section))
                elem_xpath = xpaths.get_xpath(xpath_section, section_index)
                input_text_delete(driver, elem_xpath, i_txt, 9, debug_message)

                # Enter RUN STANDARD HOURS filed
                debug_message = "Enter RUN STANDARD HOURS filed"
                section_index = increase_index(section_index, xpaths.items_len(xpath_section))
                elem_xpath = xpaths.get_xpath(xpath_section, section_index)
                input_text_delete(driver, elem_xpath, i_txt, 9, debug_message)

                # Save the STANDARD OPERATION
                debug_message = "Saved the STANDARD OPERATION"
                section_index = increase_index(section_index, xpaths.items_len(xpath_section))
                elem_xpath = xpaths.get_xpath(xpath_section, section_index)
                click_element(driver, elem_xpath, debug_message)

            except NoSuchWindowException:
                debugger_print("window was closed manually")
    else:
        debugger_print("No operations have been entered")

    debugger_print("\n******** Standard Operation complete ********\n")
    return
