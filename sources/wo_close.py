from sources.debugger_print import *


def close_wo(driver, xpaths):
    from sources.variables import increase_index, wait_till_absence

    xpath_section = 'close_wo'
    section_index = -1

    debugger_print("\n******** Closing WO ********\n")
    try:
        # Press the CLOSE WORK ORDER button
        debug_message = "Press the CLOSE WORK ORDER button"
        section_index = increase_index(section_index, xpaths.items_len(xpath_section))
        elem_xpath = xpaths.get_xpath(xpath_section, section_index)
        click_element(driver, elem_xpath, debug_message)
        sleep(10)
        # Wait for the page to return to normal. You may need to click the OK button
        section_index = increase_index(section_index, xpaths.items_len(xpath_section))
        elem_xpath = xpaths.get_xpath(xpath_section, section_index)
        try:
            wait = WebDriverWait(driver, wait_till_absence, ignored_exceptions=UnexpectedAlertPresentException).until_not(EC.presence_of_element_located((By.XPATH, elem_xpath)))
        except TimeoutException:
            pass

    except NoSuchWindowException:
        debugger_print("window was closed manually")

    debugger_print("\n******** WO is now closed ********\n")
    return
