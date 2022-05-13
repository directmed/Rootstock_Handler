from sources.debugger_print import *


def wo_issue(driver, xpaths, gui):
    from sources.variables import wo_data, test_flag, increase_index, wait_till_absence

    xpath_section = 'wo_issue'
    section_index = -1

    debugger_print("\n******** Initializing Work Order Issue ********\n")
    try:
        # Open ROOTSTOCK SITE MAP in a new tab
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get("https://directmedparts--rstk.na159.visual.force.com/apex/Manufacturing?sfdc.tabName=01r0a000000qIJj")

        # Click on the WO ISSUE button
        debug_message = "Click on the WO ISSUE button"
        section_index = increase_index(section_index, xpaths.items_len(xpath_section))
        elem_xpath = xpaths.get_xpath(xpath_section, section_index)
        click_element(driver, elem_xpath, debug_message)

        # Wait for WO ISSUE page to open and WORK ORDER options are available
        debug_message = "Selecting Work Order from options"
        section_index = increase_index(section_index, xpaths.items_len(xpath_section))
        elem_xpath = xpaths.get_xpath(xpath_section, section_index)
        select_option(driver, elem_xpath, wo_data['number'], debug_message)

        # Select the correct SERIAL COMPONENT using the part number
        temp = gui.get_unit_info_entry_box_text_vars('Part Number')
        temp = temp.__str__()
        debug_message = "Select the correct SERIAL COMPONENT"
        section_index = increase_index(section_index, xpaths.items_len(xpath_section))
        elem_xpath = xpaths.get_xpath(xpath_section, section_index)
        select_option(driver, elem_xpath, temp, debug_message)

        # Click on the DISPLAY COMPONENTS button
        debug_message = "Click on the DISPLAY COMPONENTS button"
        section_index = increase_index(section_index, xpaths.items_len(xpath_section))
        elem_xpath = xpaths.get_xpath(xpath_section, section_index)
        click_element(driver, elem_xpath, debug_message)

        # Search the component rows for the unit according to the serial number
        debug_message = "Searching the rows for the correct serial number."
        # xpath of the table containing the serial number
        section_index = increase_index(section_index, xpaths.items_len(xpath_section))
        elem_xpath = xpaths.get_xpath(xpath_section, section_index)
        elem = find_element(driver, elem_xpath, debug_message)
        if elem is False:
            debugger_print("could not find element. stop 2.")
            return

        try:
            # populate the rows that may contain the serial number
            new_loc_rows = elem.find_elements_by_tag_name("tr")
        except NoSuchElementException:
            debugger_print("Could not find rows or columns on the components table.")
            return

        debugger_print(new_loc_rows)
        indx = 0
        # Check each row for the serial number
        for ind, new_loc_row in enumerate(new_loc_rows):
            debugger_print(new_loc_row)
            try:
                # check if 'Select' is part of the columns
                new_loc_row.find_element_by_tag_name("select")
                temp = gui.get_unit_info_entry_box_text_vars('Serial Number')
                temp = temp.__str__()
                if is_option_available(new_loc_row, temp, "Searching for the Serial Number") is True:
                    indx = ind
                    debugger_print("This is the right row...")
                    debugger_print("data cell index = " + ind.__str__())
                    break
                else:
                    debugger_print("Not the right row...")

            except NoSuchElementException:
                debugger_print("Not the right row...")
                pass

        # Uncheck the first cell of the first row
        data_cells = new_loc_rows[0].find_elements_by_class_name("dataCell")
        debugger_print(new_loc_rows[0].text)
        sel_chk_box = data_cells[0].find_element_by_tag_name("input")
        sel_chk_box.click()

        # Proceed to find the correct row with the serial number and select it.
        data_cells = new_loc_rows[indx].find_elements_by_class_name("dataCell")
        debugger_print(data_cells)
        sel_chk_box = data_cells[0].find_element_by_tag_name("input")
        if sel_chk_box.get_attribute("checked") != "true":
            debugger_print("Clicked the SELECT box")
            sel_chk_box.click()

        # select the correct serial number
        debug_message = "selecting the serial number"
        temp = gui.get_unit_info_entry_box_text_vars('Serial Number')
        temp = temp.__str__()
        select_option_el(data_cells[6], temp, debug_message)

        section_index = increase_index(section_index, xpaths.items_len(xpath_section))
        elem_xpath = xpaths.get_xpath(xpath_section, section_index)
        section_index = increase_index(section_index, xpaths.items_len(xpath_section))
        section_index1 = section_index
        elem_xpath1 = xpaths.get_xpath(xpath_section, section_index1)
        if test_flag is False:
            # Click the ISSUE COMPONENTS BUTTON
            debug_message = "Click the ISSUE COMPONENTS BUTTON"
            click_element(driver, elem_xpath, debug_message)

        # Wait for the page to return to normal. You may need to click the OK button
        try:
            wait = WebDriverWait(driver, wait_till_absence, ignored_exceptions=UnexpectedAlertPresentException).until_not(EC.presence_of_element_located((By.XPATH, elem_xpath1)))
        except TimeoutException:
            pass

        # Return to original Tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.refresh()

    except NoSuchWindowException:
        debugger_print("window was closed manually")

    debugger_print("\n******** WO ISSUE COCMPLETED ********\n")
    return
