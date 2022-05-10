from sources.debugger_print import *


# Checks if popup comes up. Closes the popup if it does.
def check_for_popup(driver):

    try:
        driver.find_element_by_id('tryLexDialog').is_displayed()
        driver.find_element_by_id('tryLexDialogX').click()
    except NoSuchElementException:
        return
    except InvalidSessionIdException:
        # update_status_box('Window has been closed. Starting over.')
        debugger_print("\nPop-up error: window has been closed. Starting over.\n")


def login_init(driver, xpaths, gui):
    from sources.variables import increase_index

    xpath_section = 'login_init'
    section_index = -1

    # Log-in to Salesforce
    debugger_print("\n******** Log-in initiated. ********")
    try:
        driver.get("https://login.salesforce.com/")

        # Check if user info is saved
        debug_message = "Checking if user name is displayed"
        section_index = increase_index(section_index, xpaths.items_len(xpath_section))
        elem_xpath = xpaths.get_xpath(xpath_section, section_index)      # xpath 1
        elem = find_element(driver, elem_xpath, debug_message)
        section_index = increase_index(section_index, xpaths.items_len(xpath_section))
        if elem is False:
            # find the user name input box and enter the user name
            user_name = gui.get_user_info_entry_box_text_vars('SalesForce User Name')
            text_to_input = user_name.__str__()
            debug_message = "Inputting login user name"
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)      # xpath 2
            input_text(driver, elem_xpath, text_to_input, debug_message)
            debugger_print('user name NOT saved.')
        else:
            debugger_print('user name was saved.')

        # Entering user name and password
        user_password = gui.get_user_info_entry_box_text_vars('SalesForce Password')
        text_to_input = user_password.__str__()
        debug_message = "Inputting login user password"
        section_index = increase_index(section_index, xpaths.items_len(xpath_section))
        elem_xpath = xpaths.get_xpath(xpath_section, section_index)     # xpath 3
        input_text(driver, elem_xpath, text_to_input, debug_message)

        # click the login button
        debug_message = "Clicking login button"
        section_index = increase_index(section_index, xpaths.items_len(xpath_section))
        elem_xpath = xpaths.get_xpath(xpath_section, section_index)     # xpath 4
        click_element(driver, elem_xpath, debug_message)

        # check if salesforce is in classic mode
        debug_message = "Checking if SalesForce is in classic mode."
        section_index = increase_index(section_index, xpaths.items_len(xpath_section))
        elem_xpath = xpaths.get_xpath(xpath_section, section_index)        # xpath 5
        elem = find_element(driver, elem_xpath, debug_message)

        section_index = increase_index(section_index, xpaths.items_len(xpath_section))
        elem_xpath1 = xpaths.get_xpath(xpath_section, section_index)  # xpath 6

        section_index = increase_index(section_index, xpaths.items_len(xpath_section))
        elem_xpath2 = xpaths.get_xpath(xpath_section, section_index)  # xpath 7

        if elem is False:
            # change salesforce from Lightning to Classic
            debug_message = "clicking Lightning Icon"
            click_element(driver, elem_xpath1, debug_message)

            # click the 'switch to classic' button
            debug_message = "Switching to SalesForce Classic"
            click_element(driver, elem_xpath2, debug_message)
        else:
            debugger_print("Salesforce is in Classic mode")

        # Check if search bar is present
        debug_message = "checking for search bar in Classic mode"
        section_index = increase_index(section_index, xpaths.items_len(xpath_section))
        elem_xpath = xpaths.get_xpath(xpath_section, section_index)     # xpath 8
        elem = find_element(driver, elem_xpath, debug_message)
        if elem is False:
            debugger_print("searchbar was not found. Something went wrong.")

    except NoSuchWindowException:
        debugger_print("window was closed manually")

    debugger_print('\n******** Logged in successfully. ********\n')
    return
