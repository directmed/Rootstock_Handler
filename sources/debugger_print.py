from sources.all_imports import *


def debugger_print(message):
    from sources.variables import debug

    if debug is True:
        print(message)
        return
    else:
        return


def click_element(driver, xpath, msg):
    from sources.variables import wait_time

    debugger_print(msg)
    try:
        wait = WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        debugger_print("TimeoutException triggered.")
        pass
    try:
        el = driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        debugger_print("Element Not Found: Could not click element.")
    try:
        el.click()
    except ElementClickInterceptedException:
        pass
    return


def select_option(driver, xpath, opt, msg):
    from sources.variables import wait_time

    debugger_print(msg)
    try:
        wait = WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        debugger_print("TimeoutException triggered.")
        pass
    try:
        el = driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        debugger_print("Element Not Found: Could not find options element.")

    all_options = el.find_elements_by_tag_name("option")
    for option in all_options:
        option_text = option.text
        if option_text is not None and opt in option_text:
            option.click()
            return
            break

    return


def select_option_el(el, opt, msg):
    debugger_print(msg)
    all_options = el.find_elements_by_tag_name("option")
    for option in all_options:
        option_text = option.text
        if option_text is not None and opt in option_text:
            option.click()
            return
            break

    return


def is_option_available(el, opt, msg):
    debugger_print(msg)
    all_options = el.find_elements_by_tag_name("option")
    for option in all_options:
        option_text = option.text
        if option_text is not None and opt in option_text:
            return True
            break

    return False


def input_text(driver, xpath, txt, msg):
    from sources.variables import wait_time

    debugger_print(msg)
    try:
        wait = WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        debugger_print("TimeoutException triggered.")
        pass
    try:
        el = driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        debugger_print("Element Not Found: Could not input text.")

    el.clear()
    el.send_keys(txt)
    return


def input_letters(driver, xpath, txt, msg):
    debugger_print(msg)
    el = driver.find_element_by_xpath(xpath)
    el.clear()
    for letter in txt:
        el.send_keys(letter)

    return


def input_text_delete(driver, xpath, txt, del_num, msg):
    from sources.variables import wait_time

    debugger_print(msg)
    try:
        wait = WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        debugger_print("TimeoutException triggered.")
        pass
    try:
        el = driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        debugger_print("Element Not Found: Could not delete characters in element.")

    for index in range(del_num):
        el.send_keys(Keys.BACKSPACE)

    el.send_keys(txt)
    return


def input_text_delete_by_element(el, txt, del_num, msg):
    debugger_print(msg)
    for index in range(del_num):
        el.send_keys(Keys.BACKSPACE)

    el.send_keys(txt)
    return


def find_element(driver, xpath, msg):
    from sources.variables import wait_time

    debugger_print(msg)
    try:
        wait = WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        debugger_print("TimeoutException triggered.")
        pass
    try:
        el = driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        debugger_print("Element Not Found")
        return False

    return el


def move_page_down(driver, xpath, msg):
    from sources.variables import wait_time

    debugger_print(msg)
    try:
        wait = WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        debugger_print("TimeoutException triggered.")
        pass
    try:
        el = driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        debugger_print("Element Not Found: Could not input text.")

    el.send_keys(Keys.PAGE_DOWN)
    return
