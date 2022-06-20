from sources.all_imports import *


def debugger_print(message):
    from sources.variables import debug

    error_log_dir, track_str = get_files_dir()

    if debug is True:
        print(message)
        return
    else:
        with open(error_log_dir + '\\unit.txt', 'r') as f:
            unit_str = f.read()

        error_log_track_file = error_log_dir + '\\' + track_str + '_unit_' + unit_str + '.txt'
        # check if 'track' file exists.
        track_exists = os.path.exists(error_log_track_file)
        if not track_exists:
            with open(error_log_track_file, 'x') as f:
                f.write(message.__str__() + '\n')
        # if file exists, get current iteration and update for next iteration.
        else:
            with open(error_log_track_file, 'a') as f:
                f.write(message.__str__() + '\n')
        return


def debugger_print_updater(message):
    from sources.variables import debug

    error_log_dir, track_str = get_files_dir()

    if debug is True:
        print(message)
        return
    else:
        error_log_track_file = error_log_dir + '\\' + track_str + '_updater.txt'
        # check if 'track' file exists.
        track_exists = os.path.exists(error_log_track_file)
        if not track_exists:
            with open(error_log_track_file, 'x') as f:
                f.write(message.__str__() + '\n')
        # if file exists, get current iteration and update for next iteration.
        else:
            with open(error_log_track_file, 'a') as f:
                f.write(message.__str__() + '\n')
        return


def debugger_print_gui_setup(message):
    from sources.variables import debug

    error_log_dir, track_str = get_files_dir()

    if debug is True:
        print(message)
        return
    else:
        error_log_track_file = error_log_dir + '\\' + track_str + '_gui_setup.txt'
        # check if 'track' file exists.
        track_exists = os.path.exists(error_log_track_file)
        if not track_exists:
            with open(error_log_track_file, 'x') as f:
                f.write(message.__str__() + '\n')
        # if file exists, get current iteration and update for next iteration.
        else:
            with open(error_log_track_file, 'a') as f:
                f.write(message.__str__() + '\n')
        return


def setup_files():
    # set up directory path and file path.
    error_log_dir_name = "\\errorlog"
    error_log_track_name = "\\track.txt"
    cw = os.getcwd()
    cw_temp = cw.__str__()
    cw_str = cw_temp
    # cw_str = cw_temp.replace("\\dist\\wo_handler", "")

    # create strings for both paths.
    error_log_dir = cw_str + error_log_dir_name
    error_log_track = error_log_dir + error_log_track_name

    # Check whether the specified path exists or not
    dir_exists = os.path.exists(error_log_dir)

    if not dir_exists:
        # Create a new directory because it does not exist
        os.makedirs(error_log_dir)

    # check if 'track' file exists.
    track_exists = os.path.exists(error_log_track)
    if not track_exists:
        with open(error_log_track, 'x') as f:
            f.write('0')
    # if file exists, get current iteration and update for next iteration.
    else:
        with open(error_log_track, 'r') as f:
            track_str = f.read()
            if track_str == '':
                track_int = 0
            else:
                track_int = int(track_str)

        with open(error_log_track, 'w') as f:
            track_int = track_int + 1
            f.write(track_int.__str__())


def get_files_dir():
    # set up directory path and file path.
    error_log_dir_name = "\\errorlog"
    error_log_track_name = "\\track.txt"
    cw = os.getcwd()
    cw_temp = cw.__str__()
    # cw_str = cw_temp.replace("\\dist\\wo_handler", "")
    cw_str = cw_temp

    # create strings for both paths.
    error_log_dir = cw_str + error_log_dir_name
    error_log_track = error_log_dir + error_log_track_name
    # if file exists, get current iteration and update for next iteration.
    with open(error_log_track, 'r') as f:
        track_str = f.read()

    return error_log_dir, track_str


def get_dir():
    # set up directory path and file path.
    cw = os.getcwd()
    cw_temp = cw.__str__()
    cw_str = cw_temp.replace("\\dist\\wo_handler", "")
    return cw_str


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
        try:
            el.click()
        except ElementClickInterceptedException:
            debugger_print("ElementClickInterceptedException exception was called.")
            pass
    except NoSuchElementException:
        debugger_print("Element Not Found: Could not click element.")
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
        all_options = el.find_elements_by_tag_name("option")
        for option in all_options:
            option_text = option.text
            if option_text is not None and opt in option_text:
                option.click()
                return
    except NoSuchElementException:
        debugger_print("Element Not Found: Could not find options element.")

    return


def select_option_el(el, opt, msg):
    debugger_print(msg)
    all_options = el.find_elements_by_tag_name("option")
    for option in all_options:
        option_text = option.text
        if option_text is not None and opt in option_text:
            option.click()
            return
    return


def select_option_el_nonzero(el, el_index, opt, msg):
    debugger_print(msg)
    all_options = el.find_elements_by_tag_name("option")
    for opt_index, option in enumerate(all_options):
        option_text = option.text
        if option_text is not None and opt in option_text:
            if el_index != 0:
                # Option is not in the first row. It must be selected.
                option.click()
                return
            else:
                if opt_index != 0:
                    all_options[0].click()  # deselect the first option and select the correct option.
                    option.click()
                else:
                    # option is already selected and no need for clicking.
                    return

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


if __name__ == "__main__":
    print("Hello world!")
