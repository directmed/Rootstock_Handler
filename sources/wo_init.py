from sources.debugger_print import *


def work_order_init(driver, xpaths, gui):
    from sources.variables import test_flag, increase_index

    xpath_section = 'work_order_init'
    section_index = -1

    debugger_print("\n******** Initializing Work Order Init ********\n")
    # Open ROOTSTOCK SITE MAP
    try:
        try:
            driver.get("https://directmedparts--rstk.na159.visual.force.com/apex/Manufacturing?sfdc.tabName=01r0a000000qIJj")

            # Press the + button on the Work Orders
            debug_message = "Creating a new Work order by pressing the + button."
            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            click_element(driver, elem_xpath, debug_message)

            # Input data to the ITEM NUMBER field
            debug_message = "Setting ITEM NUMBER field"
            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            elem = find_element(driver, elem_xpath, debug_message)
            # elem = driver.find_element_by_xpath(elem_xpath)

            temp = gui.get_unit_info_entry_box_text_vars('Part Number')
            temp = temp.__str__() + ' '
            if elem is not False:
                elem.send_keys(temp)
            else:
                debugger_print("Check xpath: stop 1")

            # Select option from automatic menu
            debug_message = "Selecting Part Number"
            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            click_element(driver, elem_xpath, debug_message)

            # Input the QTY REQUIRED field
            debug_message = "Setting QTY REQUIRED field"
            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            text_to_input = "1"
            input_text(driver, elem_xpath, text_to_input, debug_message)

            # Setting the date
            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            click_element(driver, elem_xpath, "Setting the date")

            # Checking the REWORK checkbox
            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            click_element(driver, elem_xpath, "Checking the REWORK box")

            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            temp = gui.get_unit_info_check_box_vars('Customer Property')
            if temp is True:
                debugger_print("wo_init: customer coil check box = ")
                debugger_print(temp)
                click_element(driver, elem_xpath, "Checking the CONS box")

            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)

            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            section_index1 = section_index
            elem_xpath1 = xpaths.get_xpath(xpath_section, section_index1)
            if test_flag is False:
                # Press the SAVE button
                click_element(driver, elem_xpath, "Saving Work Order...")
                debugger_print("Work Order Saved.")

                # Wait for the page to return to normal. You may need to click the OK button
                # Get WO number for future reference
                debug_msg = "Getting WO number"
                elem = find_element(driver, elem_xpath1, debug_msg)
                wo_num = elem.text
                debugger_print("WO Number is " + wo_num)
                debugger_print("\n******** Work Order Init Complete ********\n")
                return wo_num

        except NoSuchWindowException:
            debugger_print("window was closed manually")

    except Exception as e:
        debugger_print("\n\n\n********** Exception Called **********")
        debugger_print(traceback.format_exc())

    return None


if __name__ == "__main__":
    print("Hello world!")
