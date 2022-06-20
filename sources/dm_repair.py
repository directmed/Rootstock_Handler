from sources.debugger_print import *


def dm_repair_info(driver, xpaths, gui):
    from sources.variables import increase_index

    # 14 xpaths total
    xpath_section = 'dm_repair_info'
    section_index = -1
    try:
        try:
            # Click 'edit' button
            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            click_element(driver, elem_xpath, "Clicking 'Edit' button.")

            # Click the DM tab
            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            debugger_print(elem_xpath)
            click_element(driver, elem_xpath, "Clicking the DM tab")

            # DM tab information
            elem_xpath_names = ['OEM Number', 'Initial Condition', 'Customer Complaint', 'Initial Failure',
                                'Internal Repair', 'External Repair', 'Tested On Bench', 'Tested On Live MRI',
                                'Testing Notes', 'Repair Is Finalized']
            elem_xpaths = {}
            for name in elem_xpath_names:
                section_index = increase_index(section_index, xpaths.items_len(xpath_section))
                elem_xpaths[name] = xpaths.get_xpath(xpath_section, section_index)

            debug_messages = {'OEM Number': "Set OEM NUMBER",
                              'Initial Condition': "Set INITIAL CONDITION OR DAMAGE",
                              'Customer Complaint': "Set CUSTOMER COMPLAINT",
                              'Initial Failure': "Set INITIAL FAILURE FINDINGS",
                              'Internal Repair': " Set INTERNAL REPAIR NOTES",
                              'External Repair': "Set EXTERNAL REPAIR NOTES",
                              'Tested On Bench': "Set TESTED ON BENCH CHECKBOX",
                              'Tested On Live MRI': "Set TESTED ON LIVE SYSTEM CHECKBOX",
                              'Testing Notes': "Set TESTING NOTES",
                              'Repair Is Finalized': "Set FINILIZED CHECKBOX"
                              }
            # Cycle though each item in elem_xpaths and apply the correct function
            debugger_print("\nDM xpaths --------")
            for key, val in elem_xpaths.items():
                debugger_print(debug_messages[key])
                debugger_print(val)
                elem = find_element(driver, elem_xpaths[key], "finding DM elements.")

                try:
                    if gui.pull_repair_info_var_values(key).get() is True and elem.get_attribute("checked") != "true":
                        # gui check box is True and webpage check box is False
                        debugger_print("Checking Box")
                        elem.click()
                    elif gui.pull_repair_info_var_values(key).get() is False and elem.get_attribute("checked") == "true":
                        # gui check box is False and webpage check box is True
                        debugger_print("Unchecking Box")
                        elem.click()
                    else:
                        # do nothing
                        debugger_print("Check boxes are up to date")

                except TypeError:
                    send_text_str = ""
                    if gui.get_repair_info_check_box_vars('Append') is True:
                        debugger_print(elem.text)
                        str_converter = elem.text
                        send_text_str = str_converter.__str__() + "\n" + gui.pull_repair_info_var_values(key).get("1.0", END).__str__()
                    else:
                        send_text_str = gui.pull_repair_info_var_values(key).get("1.0", END).__str__()

                    elem.clear()
                    elem.send_keys(send_text_str)

            # Press the SAVE button
            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            click_element(driver, elem_xpath, "Saving Work Order...")

            # Wait for the page to return to normal. You may need to click the OK button
            # Get WO number for future reference
            debug_msg = "Getting WO number"
            debugger_print(debug_msg)

            section_index = increase_index(section_index, xpaths.items_len(xpath_section))
            elem_xpath = xpaths.get_xpath(xpath_section, section_index)
            elem = find_element(driver, elem_xpath, "checking wo status.")

            debugger_print(section_index.__str__())
            debugger_print(xpaths.items_len(xpath_section))
            debugger_print(elem_xpath)
            wo_num = elem.text
            debugger_print("WO Number is " + wo_num)

        except NoSuchWindowException:
            debugger_print("window was closed manually")
            return True

    except Exception as e:
        debugger_print("\n\n\n********** Exception Called **********")
        debugger_print(traceback.format_exc())
        return True

    debugger_print("\n******** DM Repair Info Complete ********\n")
    return False


if __name__ == "__main__":
    print("Hello world!")
