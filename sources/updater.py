import urllib.request
import os

cwd = os.getcwd()
cwd_str = cwd.__str__()


class Updater:
    # initiate Updater and read csv file
    def __init__(self):
        self.updater_headers = ['revision', 'raw', 'file_name']
        self.updater_sections = {}
        self.csv_sections = {}

    def start_updater(self):
        from sources.debugger_print import debugger_print_updater
        import pandas as pd

        try:
            csv_data = pd.read_csv('updater.csv')  # read csv file
            if csv_data.empty:  # check if csv file is empty
                debugger_print_updater('CSV file is empty.')  # print out message on status box
                data_flag = False  # set flag false
            else:
                data_flag = True  # set flag true b/c csv file is not empty

        except FileNotFoundError:  # handle if file is not found in ROG folder.
            self.load_updater_github()
            debugger_print_updater("Get data from Github")
            pass

        if data_flag is True:  # csv file is found in ROG folder
            # obtain all of the location number headers

            for header in self.updater_headers:
                csv_options_temp = csv_data[header].astype(str)
                csv_sections_temp = []
                for option in csv_options_temp:
                    if option != 'nan':
                        csv_sections_temp.append(option.__str__())
                    else:
                        continue

                self.csv_sections[header] = csv_sections_temp.copy()

    def overwrite_files(self):
        from sources.debugger_print import debugger_print_updater
        # raw data files from github repository
        raw_urls = self.csv_sections['raw'].copy()
        for url_index, url in enumerate(raw_urls):
            debugger_print_updater("url[" + url_index.__str__() + "] = " + url)

        # wanted file names
        python_files = []
        url_filenames = self.csv_sections['file_name'].copy()
        for name_index, name in enumerate(url_filenames):
            debugger_print_updater("file_name[" + name_index.__str__() + "] = " + name)
            python_files.append(cwd_str + name)
            debugger_print_updater("internal_memory_location[" + name_index.__str__() + "] = " + python_files[name_index].__str__())

        for file_index in range(0, len(raw_urls)):
            debugger_print_updater("index = " + file_index.__str__())
            local_filename, headers = urllib.request.urlretrieve(raw_urls[file_index], filename=python_files[file_index])
            debugger_print_updater("download complete!")
            debugger_print_updater("download file location: " + local_filename.__str__())
            debugger_print_updater("download headers: " + headers.__str__())

    def load_updater_github(self):
        import pandas as pd
        from sources.debugger_print import debugger_print_updater

        self.updater_sections.clear()

        # github url where default csv file is found.
        updater_url = 'https://raw.githubusercontent.com/directmed/Rootstock_Handler/main/updater.csv'
        updater_data = pd.read_csv(updater_url)  # read csv file
        if updater_data.empty:  # check if csv file is empty
            # update_status_box('Github CSV file is empty.')
            data_flag = False
        else:
            data_flag = True

        if data_flag is True:  # csv file is found in ROG folder
            # obtain all of the location number headers

            for header in self.updater_headers:
                updater_options_temp = updater_data[header].astype(str)
                updater_sections_temp = []
                for option in updater_options_temp:
                    if option != 'nan':
                        updater_sections_temp.append(option.__str__())
                    else:
                        continue

                self.updater_sections[header] = updater_sections_temp.copy()

        """   Get version number from saved csv file in local drive and compare them   """
        updater_version = int(float(self.updater_sections['revision'][0]))
        csv_version = int(float(self.csv_sections['revision'][0]))

        # update csv file if version is higher
        if updater_version > csv_version:
            self.csv_sections.clear()
            self.csv_sections = self.updater_sections.copy()
            # Format data to be able to save to csv
            debugger_print_updater("updater headers = " + self.updater_headers.__str__())
            updater_sections_data = []
            for index1, val1 in enumerate(self.updater_sections):
                updater_sections_data.append([])
                debugger_print_updater("updater data index = " + index1.__str__())
                for val2 in self.updater_sections[val1]:
                    updater_sections_data[index1].append(val2)

            df = pd.DataFrame(updater_sections_data, index=self.updater_headers).transpose()
            df.to_csv('updater.csv', index=False)  # save CSV file
            debugger_print_updater("Files have been updated.")
            return True
        else:
            debugger_print_updater("Version is up to date.")
            return False
