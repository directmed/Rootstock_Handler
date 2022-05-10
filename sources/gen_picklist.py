from sources.debugger_print import *


def generate_picklist(driver, xpaths):
    from sources.variables import increase_index, wait_till_absence

    xpath_section = 'generate_picklist'
    section_index = -1

    debugger_print("\n******** Generating Picklist ********\n")
    try:
        # Wait for GENERATE PICKLIST button to appear and click on it
        section_index = increase_index(section_index, xpaths.items_len(xpath_section))
        elem_xpath = xpaths.get_xpath(xpath_section, section_index)
        click_element(driver, elem_xpath, "Clicked GENERATE PICKLIST button")

        # Click GENERATE PICKLIST popup
        debug_msg = "Click GENERATE PICKLIST popup"
        # Wait for the page to return to normal. You may need to click the OK button
        section_index = increase_index(section_index, xpaths.items_len(xpath_section))
        elem_xpath = xpaths.get_xpath(xpath_section, section_index)
        click_element(driver, elem_xpath, debug_msg)
        wait = WebDriverWait(driver, wait_till_absence, ignored_exceptions=UnexpectedAlertPresentException).until_not(EC.presence_of_element_located((By.XPATH, elem_xpath)))

        # Get WO number for future reference
        debug_msg = "Getting WO number"
        debugger_print(debug_msg)
        section_index = increase_index(section_index, xpaths.items_len(xpath_section))
        elem_xpath = xpaths.get_xpath(xpath_section, section_index)
        elem = find_element(driver, elem_xpath, debug_msg)
        wo_num = elem.text
        debugger_print("WO Number is " + wo_num)

        # Wait for the page to return to normal. You may need to click the OK button
        section_index = increase_index(section_index, xpaths.items_len(xpath_section))
        elem_xpath = xpaths.get_xpath(xpath_section, section_index)
        wait = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, elem_xpath)))

    except NoSuchWindowException:
        debugger_print("window was closed manually")

    debugger_print("\n******** Picklist Complete ********\n")
    return wo_num
