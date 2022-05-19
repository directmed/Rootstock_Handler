from sources.debugger_print import *


def tq_booking(driver, xpaths, gui):
    from sources.variables import wo_data, increase_index, op_vars, wait_till_absence

    xpath_section = 'tq_booking'
    section_index = -1
    xpath_subsection = 'tq_rows'
    subsection_index = -1

    debugger_print("\n******** Initializing TIME AND QUANTITY BOOKING ********\n")

    try:
        try:
            # Wait for the RELATED LISTS tab to appear and click on it
            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            click_element(driver, elem_xpath, "Opening RELATED LISTS tab")

            # Click the OPERATIONS tab
            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            click_element(driver, elem_xpath, "Clicking OPERATIONS tab")

            # Find all operation numbers to use in booking
            # /html/body/div[1]/div[2]/table/tbody/tr/td[2]/span[3]/div/div/div/div/div[1]/div/div[2]/table/tbody/tr/td/span/table/tbody/tr[2]/td[3]/table/tbody/tr/td/div/div/table/tbody/tr[2]/td/span/table/tbody
            debug_message = "Find all operation numbers to use in booking"
            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            elem = find_element(driver, elem_xpath, debug_message)
            if elem is False:
                debugger_print("Could not find element. Stop 1")
                return

            op_count = elem.find_elements_by_tag_name("tr")
            debugger_print(op_count)
            op_number = []
            debugger_print("\nfinding all operations")
            for count in range(0, len(op_count)):
                debugger_print("count = " + count.__str__())
                elem_data_cell = op_count[count].find_elements_by_class_name("dataCell")
                debugger_print("data cells")
                debugger_print(elem_data_cell[1].text)
                op_num_text = elem_data_cell[1].text
                op_number.append(op_num_text.__str__())
                debugger_print("op_number = " + op_number[count])
                debugger_print("op_count = " + count.__str__())

            try:
                # Open ROOTSTOCK SITE MAP in a new tab
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get("https://directmedparts--rstk.na159.visual.force.com/apex/Manufacturing?sfdc.tabName=01r0a000000qIJj")

                # Click on the TQ BOOKING button
                debug_message = "\nClick on the TQ BOOKING button"
                section_index = increase_index(section_index, xpaths.items_len(xpath_section))
                elem_xpath = xpaths.get_xpath(xpath_section, section_index)
                click_element(driver, elem_xpath, debug_message)

                # Wait for TQ BOOKING page to open and WORK ORDER options are available
                debug_message = "Selecting Name from options"
                section_index = increase_index(section_index, xpaths.items_len(xpath_section))
                elem_xpath = xpaths.get_xpath(xpath_section, section_index)
                select_option(driver, elem_xpath, gui.get_user_info_combo_boxes('Name'), debug_message)

                # Enter WO in SEARCH WORK ORDERS
                debug_message = "Enter WO in SEARCH WORK ORDERS"
                section_index = increase_index(section_index, xpaths.items_len(xpath_section))
                elem_xpath = xpaths.get_xpath(xpath_section, section_index)
                debugger_print(wo_data['number'])
                input_letters(driver, elem_xpath, wo_data['number'], debug_message)

                # wait for selection box
                debug_message = " Wait for selection box."
                section_index = increase_index(section_index, xpaths.items_len(xpath_section))  # index F
                elem_xpath = xpaths.get_xpath(xpath_section, section_index)
                elem = find_element(driver, elem_xpath, debug_message)  # check this xpath
                if elem is False:
                    debugger_print("Could not find element. Stop 2")
                    return

                try:
                    wait = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "li")))
                    all_tags = elem.find_elements_by_tag_name("li")  # program failed at this point
                    for index, tag in enumerate(all_tags):
                        try:
                            debugger_print(index)
                            debugger_print(tag.text)
                            if tag.text is not None and wo_data['number'] in tag.text:
                                tag.click()
                                # debugger_print(debug, "WO selected = " + tag.text)
                                break
                        except StaleElementReferenceException:
                            tag.send_keys(Keys.PAGE_DOWN)
                            debugger_print(index)
                            debugger_print(tag.text)
                            if tag.text is not None and wo_data['number'] in tag.text:
                                tag.click()
                                # debugger_print(debug, "WO selected = " + tag.text)
                                break

                except StaleElementReferenceException:
                    elem.click()

                # Press the LOAD ENTRIES button
                debug_message = "Loading Entries"
                section_index = increase_index(section_index, xpaths.items_len(xpath_section))
                elem_xpath = xpaths.get_xpath(xpath_section, section_index)
                click_element(driver, elem_xpath, debug_message)

                # del entries button
                debug_message = "Find Del Entries Button"
                section_index = increase_index(section_index, xpaths.items_len(xpath_section))
                del_button_xpath = xpaths.get_xpath(xpath_section, section_index)
                elem = find_element(driver, del_button_xpath, debug_message)
                if elem is False:
                    debugger_print("Could not find element. Stop 3")
                    return

                # Find body for booking options
                # loop through each booking entry
                debugger_print("\nSearching though operation input rows")
                for count in range(0, len(op_number)):
                    # extract all data cells
                    subsection_index = increase_index(subsection_index, xpaths.items_len(xpath_subsection))
                    elem_xpath = xpaths.get_xpath(xpath_subsection, subsection_index)
                    elem_span = find_element(driver, elem_xpath, "Finding booking options row")
                    if elem_span is False:
                        debugger_print("could not find booking row option. Stop 4")
                        return

                    elem_data_cells = elem_span.find_elements_by_class_name("dataCell")
                    # Fill out booking entry
                    elem_data_cells[0].click()      # check the 'Select' Checkbox
                    debugger_print("clicked select box")

                    # Input Total number of hours
                    debug_message = "Input Total number of hours"
                    data_cell = elem_data_cells[5].find_element_by_tag_name("input")
                    if count <= (len(op_vars)-1):
                        temp = op_vars[count]['Total Hours'].get()  # key error
                        if temp <= 0:
                            temp = 1.0
                    else:
                        temp = 1.0

                    temp = temp.__str__()
                    input_text_delete_by_element(data_cell, temp, 5, debug_message)

                    # select the correct WO
                    data_cell = elem_data_cells[6].find_element_by_tag_name("select")
                    debugger_print(wo_data['number'])
                    select_option_el(data_cell, wo_data['number'], debug_message)
                    debugger_print("selected WO")

                    # select the correct operation "5"
                    debug_message = "select the correct operation = " + op_number[count].__str__() + "\n"
                    data_cell = elem_data_cells[7].find_element_by_tag_name("select")
                    select_option_el(data_cell, op_number[count], debug_message)

                # Click the SUBMIT BOOKING button
                debug_message = "Click the SUBMIT BOOKING button"
                section_index = increase_index(section_index, xpaths.items_len(xpath_section))
                elem_xpath = xpaths.get_xpath(xpath_section, section_index)
                click_element(driver, elem_xpath, debug_message)

                # Wait for the page to return to normal. You may need to click the OK button
                wait = WebDriverWait(driver, wait_till_absence, ignored_exceptions=UnexpectedAlertPresentException).until_not(EC.presence_of_element_located((By.XPATH, elem_xpath)))

                # Return to original Tab
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                driver.refresh()

            except NoSuchWindowException:
                debugger_print("window was closed manually")

        except NoSuchWindowException:
            debugger_print("window was closed manually")

        debugger_print("\n******** TQ BOOKING COMPLETED ********\n")

    except Exception as e:
        debugger_print("\n\n\n********** Exception Called **********")
        debugger_print(traceback.format_exc())
    return


if __name__ == "__main__":
    print("Hello world!")
