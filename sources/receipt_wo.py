from sources.debugger_print import *


def wo_receipt(driver, xpaths, gui):
    from sources.variables import wo_data, increase_index, wait_till_absence

    xpath_section = 'wo_receipt'
    section_index = -1

    debugger_print("\n******** Initializing WO RECEIPT ********\n")
    try:
        try:
            # Open ROOTSTOCK SITE MAP in a new tab
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get("https://directmedparts--rstk.na159.visual.force.com/apex/Manufacturing?sfdc.tabName=01r0a000000qIJj")

            # Click on the WO RECEIPT button
            debug_message = "Click on the WO RECEIPT button"
            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            click_element(driver, elem_xpath, debug_message)

            # Wait for WO RECEIPT page to open and WORK ORDER options are available
            debug_message = "Selecting WO number from options"
            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            select_option(driver, elem_xpath, wo_data['number'], debug_message)

            # Wait for WO RECEIPT page to open and WORK ORDER options are available
            debug_message = "Selecting STOCK from options"
            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            select_option(driver, elem_xpath, gui.get_location_info_final_id_combo_box('Final'), debug_message)

            #
            debug_message = "Enter INVENTORY LOCATION NUMBER"
            text_to_input = gui.get_location_info_final_no_combo_boxes(gui.get_current_final_location_no_option().__str__())
            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            input_text(driver, elem_xpath, text_to_input, debug_message)

            # Press the PERFORM WORK ORDER RECEIPT button
            debug_message = "Press the PERFORM WORK ORDER RECEIPT button"
            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            click_element(driver, elem_xpath, debug_message)

            # Wait for the page to return to normal. You may need to click the OK button
            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            wait = WebDriverWait(driver, wait_till_absence, ignored_exceptions=UnexpectedAlertPresentException).until_not(EC.presence_of_element_located((By.XPATH, elem_xpath)))

            # Return to original Tab
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            driver.refresh()

        except NoSuchWindowException:
            debugger_print("window was closed manually")
            return True

    except Exception as e:
        debugger_print("\n\n\n********** Exception Called **********")
        debugger_print(traceback.format_exc())
        return True

    debugger_print("\n******** WO RECEIPT COMPLETED ********\n")
    return False


if __name__ == "__main__":
    print("Hello world!")
