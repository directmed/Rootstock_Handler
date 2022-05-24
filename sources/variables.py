from sources.all_imports import *

debug = False
test_flag = False
background_color = '#fafcfc'
button_color = '#42a2fc'

'''
root = Tk()
root.iconbitmap('DM_icon.ico')
root.title('Rootstock Work Order Handler')
root.config(bg=background_color)
root.geometry("1200x600")
main_menu_bar = Menu(root)
root.config(menu=main_menu_bar)
'''

all_col_width = 75
max_col = 6
user_info_row = 4
unit_info_row = 7
location_info_row = 11
repair_info_row = 17
repair_text_input_width = 45
auto_entry_input_width = 25
button_width = 20
operations_width = 12

# options
message_box_width = max_col * 21
wait_time = 60
wait_till_absence = 60

'''
@item_info - array to hold information extracted from the LOCATION TO LOCATION page in rootstock
[NAME, DIVISION, ITEM NUMBER, SERIAL NUMBER, LOCATION ID, STOCK LOC NO, STOCK ADD DATE, ORDER NUMBER, ORDER LINE, LAST MODIFIED DATE] - array order
Array order is determined according to the order that the 'dataCells' are extracted from the list of elements from the search results.

'''
item_info = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
item_info_location = {'id': 3, 'no': 5}
wo_data = {'number': ' ', 'status': ' '}
original_location = {'id': '', 'no': ''}

user_info_engineer_names = ["Daniel Perri", "Enrique Castillo Cruz", "Enrique Sosa", "Joseph Lindsay", "Kevin Derby", "Miguel Rojo", "Tim Kearney"]
user_info_combo_box_options = {'Name': user_info_engineer_names}

# location info id options will be the location IDs for initial and final palcements
location_info_id_options = []
# location info no options by id will be the location number options assigned to a particular ID
location_info_no_options_by_id = {}

op_combo_box_options = ["10 (Initial Test / Inspection)", "20 (Diagnose / Troubleshoot)",
                        "30 (Repair)",
                        "35 (External Vendor Repair)", "40 (Assembly / Reassembly)",
                        "50 (Final Bench Test)",
                        "60 (Final System Test)", "110 (Scrap / Component Harvest)", ]
op_labels = []
op_widgets = []
op_vars = []
op_label_names = ['Expected Hours', 'Total Hours', 'Process']


def increase_index(section_ind, total_len):
    from sources.debugger_print import debugger_print

    if section_ind < total_len:
        section_ind = section_ind + 1
    else:
        debugger_print("Index is out of range")
    return section_ind


class Xpaths:
    xpath_sections = {}

    def __inti__(self):
        from sources.debugger_print import debugger_print
        debugger_print("Initializing Xpaths")

    def get_xpaths(self):
        from sources.debugger_print import debugger_print, get_dir
        import pandas as pds

        xpath_headers = ['login_init', 'get_item_info', 'get_wo_page', 'check_wo_page_status', 'open_wo_page',
                         'loc_to_loc_transfer', 'work_order_init', 'generate_picklist', 'wo_issue', 'dm_repair_info',
                         'add_std_operation', 'tq_booking', 'wo_receipt', 'close_wo', 'tq_rows']
        data_flag = False  # true if CSV file is found
        try:
            this_dir = get_dir()
            xpath_data = pds.read_csv(this_dir + '\\xpaths.csv')  # read csv file
            if xpath_data.empty:  # check if csv file is empty
                debugger_print('CSV file is empty.')  # print out message on status box
                data_flag = False  # set flag false
            else:
                data_flag = True  # set flag true b/c csv file is not empty

        except FileNotFoundError:  # handle if file is not found in ROG folder.
            self.load_xpaths_github()  # search on github for default data.
            debugger_print("Get data from Github")
            pass

        if data_flag is True:  # csv file is found in ROG folder
            # obtain all of the location number headers

            for header in xpath_headers:
                xpath_options_temp = xpath_data[header].astype(str)
                xpath_sections_temp = []
                for option in xpath_options_temp:
                    if option != 'nan':
                        xpath_sections_temp.append(option.__str__())
                    else:
                        continue

                self.xpath_sections[header] = xpath_sections_temp.copy()

    def load_xpaths_github(self):
        from sources.debugger_print import debugger_print
        data_flag = False  # true if csv file is found in github

        xpath_headers = ['login_init', 'get_item_info', 'get_wo_page', 'check_wo_page_status', 'open_wo_page',
                         'loc_to_loc_transfer', 'work_order_init', 'generate_picklist', 'wo_issue', 'dm_repair_info',
                         'add_std_operation', 'tq_booking', 'wo_receipt', 'close_wo', 'tq_rows']

        # github url where default csv file is found.
        xpath_url = 'https://raw.githubusercontent.com/directmed/Rootstock_Handler/main/xpaths.csv'
        xpath_data = pd.read_csv(xpath_url)  # read csv file
        if xpath_data.empty:  # check if csv file is empty
            # update_status_box('Github CSV file is empty.')
            data_flag = False
        else:
            data_flag = True

        if data_flag is True:  # csv file is found in ROG folder
            # obtain all of the location number headers

            for header in xpath_headers:
                xpath_options_temp = xpath_data[header].astype(str)
                xpath_sections_temp = []
                for option in xpath_options_temp:
                    if option != 'nan':
                        xpath_sections_temp.append(option.__str__())
                    else:
                        continue

                self.xpath_sections[header] = xpath_sections_temp.copy()

        debugger_print("xpath headers = " + xpath_headers.__str__())

        xpath_sections_data = []
        for index1, val1 in enumerate(self.xpath_sections):
            xpath_sections_data.append([])
            debugger_print("xpath data index = " + index1.__str__())
            for val2 in self.xpath_sections[val1]:
                xpath_sections_data[index1].append(val2)

        df = pd.DataFrame(xpath_sections_data, index=xpath_headers).transpose()
        df.to_csv('xpaths.csv', index=False)  # save CSV file

    def get_xpath(self, key, xpath_index):
        return self.xpath_sections[key][xpath_index]

    def get_items(self, key):
        return self.xpath_sections[key]

    def keys_len(self):
        return len(self.xpath_sections)

    def items_len(self, key):
        return len(self.xpath_sections[key])

    def print_all(self):
        from sources.debugger_print import debugger_print

        for key, values in self.xpath_sections.items():
            for value_index, value in enumerate(values):
                debugger_print(key + '[' + value_index.__str__() + '] = ' + value)


if __name__ == "__main__":
    print("Hello world!")
