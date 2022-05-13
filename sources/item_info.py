from sources.debugger_print import *


def get_item_info(driver, xpaths, gui):
    from sources.variables import item_info, increase_index

    xpath_section = 'get_item_info'
    section_index = -1

    debugger_print("\n******** Getting Item Info ********\n")
    # Search for the dps
    try:
        # Xpath - search bar
        section_index = increase_index(section_index, xpaths.items_len(xpath_section))
        elem_xpath = xpaths.get_xpath(xpath_section, section_index)
        elem = driver.find_element_by_xpath(elem_xpath)
        elem.clear()
        u_info = gui.get_unit_info_entry_box_text_vars('Serial Number')
        u_info_str = u_info.__str__()
        elem.send_keys(u_info_str)
        elem.send_keys(Keys.ENTER)
        debugger_print('Searching for the serial number...')
    except NoSuchElementException:
        debugger_print('Error: Search box not found.')
        # update_status_box('Error:   Search box not found.')
        # driver.close()
        # return

    # Find information for
    exit_flag = 0
    try:
        header_wanted = "Inventory Items by Serial Number"
        for indx in range(20):
            if exit_flag == 1:
                break

            list_text = "list" + indx.__str__()
            # debugger_print(list_text)
            list_eles = driver.find_elements_by_class_name(list_text)
            for ind, list_ele in enumerate(list_eles):
                debugger_print("\nind = " + ind.__str__())
                # debugger_print(list_ele.text)
                # debugger_print(list_ele)

                headers = list_ele.find_element_by_class_name("pbHeader")
                header_text = headers.text
                # debugger_print(headers)
                debugger_print(header_text)

                if header_text is not None and header_wanted in header_text:
                    debugger_print("Header Found: Inventory Items by Serial Number")
                    data_body = list_ele.find_element_by_class_name("pbBody")
                    data_sections = data_body.find_elements_by_tag_name("tr")
                    debugger_print(data_sections)
                    debugger_print("sorting through unit rows")

                    for sec_index, section in enumerate(data_sections):
                        debugger_print("\n")
                        debugger_print(section.text)
                        if sec_index != 0:
                            data_cells = section.find_elements_by_class_name("dataCell  ")
                            debugger_print(data_cells)
                            cell_text = data_cells[0].text
                            cell_str = cell_text.__str__()
                            if gui.get_unit_info_entry_box_text_vars('Part Number') in cell_str and \
                                    gui.get_unit_info_entry_box_text_vars('Serial Number') in cell_str:
                                for cell, data_cells in enumerate(data_cells):
                                    if cell < len(item_info):
                                        item_info[cell] = data_cells.text
                                        debugger_print("data_cell[" + cell.__str__() + "] = " + item_info[cell].__str__())
                                    else:
                                        break

                    exit_flag = 1
                    break

    except NoSuchElementException:
        debugger_print('Error: No Item Number found for this DPS.')
        # update_status_box('Error: No Item Number found for this DPS.')
        # driver.close()
    debugger_print("\n******** Item Info Stored ********\n")
    return


def get_wo_page(driver, xpaths):
    from sources.variables import wo_data, increase_index

    xpath_section = 'get_wo_page'
    section_index = -1

    debugger_print("\n******** Opening WO ********\n")
    # Search for the dps
    try:
        # Xpath - search bar
        section_index = increase_index(section_index, xpaths.items_len(xpath_section))
        elem_xpath = xpaths.get_xpath(xpath_section, section_index)
        elem = driver.find_element_by_xpath(elem_xpath)
        elem.clear()
        elem.send_keys(wo_data['number'])
        elem.send_keys(Keys.ENTER)
        debugger_print('\nSearching for the WO NUMBER...')
    except NoSuchElementException:
        debugger_print('\nError: Search box not found.')
        # update_status_box('Error:   Search box not found.')
        driver.close()
        # return

    # Find information for rs_item_info[]
    exit_flag = 0
    try:
        header_wanted = "Work Orders"
        for indx in range(20):
            if exit_flag == 1:
                break

            list_text = "list" + indx.__str__()
            debugger_print(list_text)
            list_eles = driver.find_elements_by_class_name(list_text)
            for ind, list_ele in enumerate(list_eles):
                debugger_print("\nind = " + ind.__str__())
                debugger_print(list_ele.text)
                debugger_print(list_ele)

                headers = list_ele.find_element_by_class_name("pbHeader")
                header_text = headers.text
                debugger_print(headers)
                debugger_print(header_text)

                # Found the right table with the header wanted
                if header_text is not None and header_wanted in header_text:
                    datacells = list_ele.find_element_by_class_name("pbBody")
                    data = datacells.find_elements_by_class_name("dataCell")
                    '''
                    print("Sorting through cells\n")
                    for indication, datum in enumerate(data):
                        print(indication)
                        print(datum.text)
                    '''
                    # Work order is closed and a new work order needs to be placed
                    if data[9].text is not None and "9" in data[9].text:
                        debugger_print("New work order will be made")
                        wo_data['status'] = "0"
                        return True

                    elif data[9].text is not None and "7" in data[9].text:
                        debugger_print("New work order will be made")
                        wo_data['status'] = "0"
                        return True

                    else:
                        debugger_print("Found existing work order.")
                        wo_data['status'] = data[9].text
                        debugger_print(wo_data['status'])
                        d = data[0].find_element_by_tag_name("a")
                        d.click()
                        exit_flag = 1
                        break

    except NoSuchElementException:
        debugger_print('Error: No WO found for this DPS.')
        # update_status_box('Error: No Item Number found for this DPS.')
        # driver.close()

    section_index = increase_index(section_index, xpaths.items_len(xpath_section))
    elem_xpath = xpaths.get_xpath(xpath_section, section_index)
    wait = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, elem_xpath)))
    debugger_print("\n******** Existing WO is open ********\n")
    return False


def check_wo_page_status(driver, xpaths):
    from sources.variables import increase_index
    from sources.debugger_print import find_element

    xpath_section = 'check_wo_page_status'
    section_index = -1
    status_numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    section_index = increase_index(section_index, xpaths.items_len(xpath_section))
    elem_xpath = xpaths.get_xpath(xpath_section, section_index)
    el = find_element(driver, elem_xpath, "Finding WO status.")
    el_text = el.text
    for number in status_numbers:
        if el_text is not None and number in el_text:
            debugger_print("\n******** Status Number = " + number)
            return number
            break

    return None


def open_wo_page(driver, xpaths, gui):
    from sources.variables import wo_data, increase_index

    xpath_section = 'open_wo_page'
    section_index = -1

    debugger_print("\n******** Opening WO ********\n")
    try:
        # Search for the dps
        try:
            # Xpath - search bar
            text_to_input = gui.get_unit_info_entry_box_text_vars('Previous WO Number')
            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            elem = find_element(driver, elem_xpath, '\nSearching for the WO NUMBER...')
            if elem is False:
                debugger_print("could not find element. stop 1.")
                return

            elem.clear()
            elem.send_keys(text_to_input)
            elem.send_keys(Keys.ENTER)
        except NoSuchElementException:
            debugger_print('\nError: Search box not found.')
            # update_status_box('Error:   Search box not found.')
            driver.close()
            # return
            # Find information for rs_item_info[]
        exit_flag = 0
        try:
            header_wanted = "Work Orders"
            for indx in range(20):
                if exit_flag == 1:
                    break

                list_text = "list" + indx.__str__()
                debugger_print(list_text)
                list_eles = driver.find_elements_by_class_name(list_text)
                for ind, list_ele in enumerate(list_eles):
                    debugger_print("\nind = " + ind.__str__())
                    debugger_print(list_ele.text)
                    debugger_print(list_ele)

                    headers = list_ele.find_element_by_class_name("pbHeader")
                    header_text = headers.text
                    debugger_print(headers)
                    debugger_print(header_text)

                    # Found the right table with the header wanted
                    if header_text is not None and header_wanted in header_text:
                        datacells = list_ele.find_element_by_class_name("pbBody")
                        data = datacells.find_elements_by_class_name("dataCell")
                        '''
                        print("Sorting through cells\n")
                        for indication, datum in enumerate(data):
                            print(indication)
                            print(datum.text)
                        '''
                        # Work order is closed and a new work order needs to be placed
                        if data[9].text is not None and "9" in data[9].text:
                            debugger_print("New work order will be made")
                            wo_data['status'] = "0"
                            return

                        elif data[9].text is not None and "7" in data[9].text:
                            debugger_print("New work order will be made")
                            wo_data['status'] = "0"
                            return

                        else:
                            debugger_print("Found existing work order.")
                            wo_data['status'] = data[9].text
                            debugger_print(wo_data['status'])
                            d = data[0].find_element_by_tag_name("a")
                            d.click()
                            exit_flag = 1
                            break

        except NoSuchElementException:
            debugger_print('Error: No WO found for this DPS.')
            # update_status_box('Error: No Item Number found for this DPS.')
            # driver.close()

        section_index = increase_index(section_index, xpaths.items_len(xpath_section))
        elem_xpath = xpaths.get_xpath(xpath_section, section_index)
        wait = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, elem_xpath)))

    except NoSuchWindowException:
        debugger_print("window was closed manually")

    debugger_print("\n******** Existing WO is open ********\n")
    return
