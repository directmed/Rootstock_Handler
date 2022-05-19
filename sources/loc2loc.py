from sources.debugger_print import *


def loc_to_loc_transfer(driver, xpaths, gui):
    from sources.variables import original_location, increase_index, wait_till_absence

    xpath_section = 'loc_to_loc_transfer'
    section_index = -1

    debugger_print("\n******** Performing Location to Location Transfer. ********\n")
    try:
        try:
            # Open Location to Location transfer page
            driver.get("https://directmedparts--rstk.na159.visual.force.com/apex/Stocklocmove?sfdc.tabName=01r0a000000qIJD")

            # Cycle through the STOCK LOC ID options
            debug_message = "Finding original location."
            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            elem = find_element(driver, elem_xpath, debug_message)
            debugger_print("xpath[" + section_index.__str__() + "] = " + elem_xpath)
            if elem is False:
                debugger_print("Could not find element. Stop 1.")
                return

            all_options = elem.find_elements_by_tag_name("option")
            for option in all_options:
                option_text = option.text
                if option_text is not None and original_location['key'] in option_text:
                    # Click on the option that matches the previous_location
                    debugger_print("Previous location found.")
                    option.click()
                    break

            # check the MOVE SERIAL ITEMS box
            debug_message = "Checked MOVE SERIAL ITEMS box."
            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            debugger_print("xpath[" + section_index.__str__() + "] = " + elem_xpath)
            click_element(driver, elem_xpath, debug_message)

            # Enter the  ITEM NUMBER in the SEARCH ITEM field
            temp = gui.get_unit_info_entry_box_text_vars('Part Number')
            temp = temp.__str__() + ' '

            debug_message = "Enter the  ITEM NUMBER in the SEARCH ITEM field"
            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            input_text(driver, elem_xpath, temp, debug_message)
            debugger_print("xpath[" + section_index.__str__() + "] = " + elem_xpath)

            # Click on drop autocomplete menu
            debug_message = "Click on drop autocomplete menu"
            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            click_element(driver, elem_xpath, debug_message)
            debugger_print("xpath[" + section_index.__str__() + "] = " + elem_xpath)

            # Find the current INVENTORY LOCATION of the item
            debug_message = "Find the current INVENTORY LOCATION of the item"
            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            elem = find_element(driver, elem_xpath, debug_message)
            debugger_print("xpath[" + section_index.__str__() + "] = " + elem_xpath)
            if elem is False:
                debugger_print("Could not find element. Stop 2.")
                return

            all_options = elem.find_elements_by_tag_name("option")
            # setup xpaths for loops
            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            section_index1 = section_index
            elem_xpath1 = xpaths.get_xpath(xpath_section, section_index1)

            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            section_index2 = section_index
            elem_xpath2 = xpaths.get_xpath(xpath_section, section_index2)

            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            section_index3 = section_index
            elem_xpath3 = xpaths.get_xpath(xpath_section, section_index3)

            options_exit_flag = False
            try:
                for option in all_options:
                    # check if the serial_number has been found. If so, exit loop. If not, continue to the next option.
                    option_text = option.text
                    if options_exit_flag is True:
                        break

                    if option_text is not None and original_location['no'] in option_text:
                        # Click the option that matches the inventory_location
                        option.click()
                        debugger_print("Inventory location match...")

                        debugger_print("xpath[" + section_index1.__str__() + "] = " + elem_xpath1)
                        debugger_print("selection options")
                        sec_elem = find_element(driver, elem_xpath1, debug_message)
                        sec_options = sec_elem.find_elements_by_tag_name("option")
                        for sec_option in sec_options:
                            sec_option_text = sec_option.text
                            if sec_option_text is not None and gui.get_unit_info_entry_box_text_vars('Serial Number') in sec_option_text:
                                # The Unit has been found in the right location. Now we can move it to a different location
                                options_exit_flag = True
                                sec_option.click()
                                # continue_flag = False
                                # while continue_flag is False:
                                # Click the SELECT SERIALS button and click it
                                debugger_print("xpath[" + section_index2.__str__() + "] = " + elem_xpath2)
                                debug_message = "Select the correct serial to be moved."
                                click_element(driver, elem_xpath2, debug_message)
                                # make sure the serial has been selected and placed in the box adjacent
                                debugger_print("xpath[" + section_index3.__str__() + "] = " + elem_xpath3)
                                debug_message = "make sure the serial has been selected and placed in the box adjacent"
                                elem = find_element(driver, elem_xpath3, debug_message)
                                elem_text = elem.text
                                elem_str = elem_text.__str__()
                                debugger_print(elem_str)

                                debugger_print("Found the current inventory location of the item.")
                                break

            except NoSuchElementException:
                debugger_print("Could not find the Serial Number in Locations.")

            # Click the DISPLAY LOC MOVE ENTRIES button and click it
            debug_message = "Clicked DISPLAY LOC MOVE ENTRIES."
            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            debugger_print("xpath[" + section_index.__str__() + "] = " + elem_xpath)
            click_element(driver, elem_xpath, debug_message)

            debug_message = "Move page down if all entries are not populated."
            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            debugger_print("xpath[" + section_index.__str__() + "] = " + elem_xpath)
            move_page_down(driver, elem_xpath, debug_message)

            # Set the new location of the unit
            debug_message = "Searching the rows for the new location."
            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            elem = find_element(driver, elem_xpath, debug_message)
            if elem is False:
                debugger_print("Could not find element")
                return

            debugger_print("xpath[" + section_index.__str__() + "] = " + elem_xpath)
            try:
                new_loc_rows = elem.find_elements_by_tag_name("tr")
            except NoSuchElementException:
                debugger_print("Could not find rows or columns on new location table.")
                return

            indx = 0
            debugger_print(new_loc_rows)
            for ind, new_loc_row in enumerate(new_loc_rows):
                debugger_print(new_loc_row)
                try:
                    new_loc_row.find_element_by_tag_name("select")
                    indx = ind
                    debugger_print(all_options)
                    debugger_print("This is the right row...")
                    debugger_print("data cell index = " + ind.__str__())
                    break

                except NoSuchElementException:
                    debugger_print("Not the right row...")
                    pass

            # Obtain all of the columns in the data row
            data_cells = new_loc_rows[indx].find_elements_by_class_name("dataCell")
            # Click the SELECT checkbox
            data_cells[0].find_element_by_tag_name("input").click()
            # Set the TO LOC ID option to 'Lab'
            all_options = data_cells[1].find_elements_by_tag_name("option")
            destination = gui.get_location_info_initial_id_combo_box('Initial')
            debugger_print(all_options)
            for option in all_options:
                option_text = option.text
                if option_text is not None and destination in option_text:
                    debugger_print("Lab option has been found in the TO LOC ID column.")
                    option.click()
                    break

            loc_no = data_cells[2].find_element_by_tag_name("input")
            loc_no.send_keys(gui.get_location_info_initial_no_combo_boxes(gui.get_current_initial_location_no_option().__str__()))

            # Click the MOVE SELECTED ITEMS BUTTON
            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            debugger_print("xpath[" + section_index.__str__() + "] = " + elem_xpath)
            click_element(driver, elem_xpath, "Click the MOVE SELECTED ITEMS BUTTON")
            wait = WebDriverWait(driver, wait_till_absence, ignored_exceptions=UnexpectedAlertPresentException).until_not(EC.presence_of_element_located((By.XPATH, elem_xpath)))

        except NoSuchWindowException:
            debugger_print("window was closed manually")

    except Exception as e:
        debugger_print("\n\n\n********** Exception Called **********")
        debugger_print(traceback.format_exc())

    debugger_print("\n******** Location Transfer Complete ********\n")
    return


if __name__ == "__main__":
    print("Hello world!")
