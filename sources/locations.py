from sources.debugger_print import *


def set_previous_location():
    from sources.variables import item_info, location_info_id_options, item_info_location

    debugger_print("******** set_previous_location: Checking for previous WOs ********")
    try:
        location_key = [""]
        index_loc = 0
        for location in location_info_id_options:
            # debugger_print(location)
            space_index = location.find(" ")
            if space_index != -1:
                location_sub = location[0:space_index]
                location_key.append(location_sub)
                # debugger_print(location_key[index_loc])
                index_loc = index_loc + 1

        loc_index = 0
        for location in location_info_id_options:
            if item_info[item_info_location['id']] is not None and location in item_info[item_info_location['id']]:
                debugger_print(item_info[item_info_location['id']])
                debugger_print(location_key[loc_index])
                return False, location_key[loc_index], location

            loc_index = loc_index + 1
    except Exception as e:
        return True

    debugger_print("******** set_previous_location: Finalized ********")
    return


def set_inventory_location():
    from sources.variables import item_info, original_location, item_info_location
    temp = item_info[item_info_location['no']][0:4]
    total_str = original_location['id'].__str__() + ' / ' + temp
    return str(total_str)


if __name__ == "__main__":
    print("Hello world!")
