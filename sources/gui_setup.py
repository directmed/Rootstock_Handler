from sources.gui_functions import *


class GuiSetup:
    from sources.variables import location_info_id_options, Xpaths

    xpaths = Xpaths()

    def __init__(self):
        from sources.variables import location_info_id_options, location_info_no_options_by_id, \
            current_initial_location_no_option, current_final_location_no_option, root, \
            user_info_combo_box_options, message_box_width, main_menu_bar, repair_text_input_width, \
            auto_entry_input_width, button_width, background_color, button_color

        debugger_print("Initializing GUI setup")
        self.data_info_headers = ['user', 'unit']
        self.edit_menu_option_names = ['size', 'font']
        self.edit_menu_options = {}
        self.edit_menu_option_vars = {}
        self.text_font_size = {'frame': 9, 'label': 9, 'input': 9, 'text': 9, 'output': 11}
        self.text_font_selection = {'frame': 'Audiowide', 'label': 'Consolas', 'input': 'Times', 'text': 'Inconsolata',
                                    'output': 'Consolas'}
        self.available_options = [self.text_font_size, self.text_font_selection]

        for opt_index, name in enumerate(self.edit_menu_option_names):
            self.edit_menu_options[name] = {}
            self.edit_menu_option_vars[name] = {}
            for key in self.available_options[opt_index]:
                if opt_index == 0:
                    # use only options var to set the font size and font type
                    self.edit_menu_option_vars[name][key] = IntVar()
                elif opt_index == 1:
                    self.edit_menu_option_vars[name][key] = StringVar()

        self.saved_user_data = {}
        """ Page Creation """
        # Create the main frame of the page
        self.main_frame = Frame(root)
        self.main_frame.config(bg=background_color)
        self.main_frame.pack(fill=BOTH, expand=1)

        # Create a canvas to fill the frame. Can attach multiple frames to canvas.
        self.main_canvas = Canvas(self.main_frame)
        self.main_canvas.config(bg=background_color)
        self.main_canvas.pack(side=LEFT, fill=BOTH, expand=1)
        self.main_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Create and attach vertical scrollbar on main frame. Scroll for canvas.
        self.vertical_scrollbar = Scrollbar(self.main_frame, orient=VERTICAL, command=self.main_canvas.yview)
        self.vertical_scrollbar.pack(side=RIGHT, fill=Y)
        self.main_canvas.configure(yscrollcommand=self.vertical_scrollbar.set)

        # Create and attach horizontal scrollbar on main frame. Scroll for canvas.
        self.horizontal_scrollbar = Scrollbar(self.main_frame, orient=HORIZONTAL, command=self.main_canvas.xview)
        self.horizontal_scrollbar.pack(side=BOTTOM, fill=X)
        self.main_canvas.configure(xscrollcommand=self.horizontal_scrollbar.set)

        # Create the inner frame in the canvas.
        self.wo_frame = Frame(self.main_canvas)
        self.wo_frame.config(bg=background_color)
        self.main_canvas.create_window((0, 0), window=self.wo_frame, anchor="nw")

        """ Widgets """
        # Label Frames / Frames
        self.perform_tasks_frame = LabelFrame(self.wo_frame, text='PERFORM TASKS', bg=background_color,
                                              font=(
                                              self.text_font_selection['frame'], self.text_font_size['frame'], 'bold'))
        self.user_info_frame = LabelFrame(self.wo_frame, text='USER INFORMATION', bg=background_color,
                                          font=(
                                          self.text_font_selection['frame'], self.text_font_size['frame'], 'bold'))
        self.unit_info_frame = LabelFrame(self.wo_frame, text='UNIT INFORMATION', bg=background_color,
                                          font=(
                                          self.text_font_selection['frame'], self.text_font_size['frame'], 'bold'))
        self.location_info_frame = LabelFrame(self.wo_frame, text='LOCATION INFORMATION', bg=background_color,
                                              font=(
                                              self.text_font_selection['frame'], self.text_font_size['frame'], 'bold'))
        self.repair_info_frame = LabelFrame(self.wo_frame, text='REPAIR INFORMATION', bg=background_color,
                                            font=(
                                            self.text_font_selection['frame'], self.text_font_size['frame'], 'bold'))
        self.operations_info_frame = LabelFrame(self.wo_frame, text='OPERATIONS INFORMATION', bg=background_color,
                                                font=(self.text_font_selection['frame'], self.text_font_size['frame'],
                                                      'bold'))
        self.message_box_frame = LabelFrame(self.wo_frame, text='CONSOLE', font=(self.text_font_selection['frame'], self.text_font_size['frame'], 'bold'), bg=background_color)
        self.all_frames = [self.perform_tasks_frame, self.user_info_frame, self.unit_info_frame,
                           self.location_info_frame, self.repair_info_frame,
                           self.operations_info_frame, self.message_box_frame]

        self.main_canvas.bind('<Configure>',
                              lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all")))
        self.main_canvas.bind('<Configure>',
                              lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all")))
        """ Labels according to LabelFrame """
        # User info frame
        self.user_info_labels = {}
        self.user_info_label_names = ['Name',  # combo box.
                                      'SalesForce User Name',  # entry box.
                                      'SalesForce Password'  # entry box.
                                      ]
        for name in self.user_info_label_names:
            self.user_info_labels[name] = Label(self.user_info_frame, text=name, bg=background_color, font=(self.text_font_selection['label'], self.text_font_size['label']))

        # unit info frame
        self.unit_info_label_names = ['Part Number',  # entry box.
                                      'Serial Number',  # entry box.
                                      'Previous WO Number'  # entry box.
                                      ]
        self.unit_info_labels = {}
        for name in self.unit_info_label_names:
            self.unit_info_labels[name] = Label(self.unit_info_frame, text=name, bg=background_color, font=(self.text_font_selection['label'], self.text_font_size['label']))

        # location transfer frame
        self.location_info_label_names = ['Transfer Location ID',  # combo box.
                                          'Transfer Location No.',  # combo box.
                                          'WO Receipt Location ID',  # combo box.
                                          'WO Receipt Location No.'  # combo box.
                                          ]
        self.location_info_labels = {}
        for name in self.location_info_label_names:
            self.location_info_labels[name] = Label(self.location_info_frame, text=name, bg=background_color, font=(self.text_font_selection['label'], self.text_font_size['label']))

        # repair info frame
        self.repair_info_label_names = ['OEM Number',  # entry box
                                        'Customer Complaint',  # text box.
                                        'Initial Condition',  # text box.
                                        'Initial Failure',  # text box.
                                        'Internal Repair',  # text box.
                                        'Testing Notes',  # text box.
                                        'External Repair',  # text box.
                                        ]
        self.repair_info_labels = {}
        for name in self.repair_info_label_names:
            self.repair_info_labels[name] = Label(self.repair_info_frame, text=name, bg=background_color, font=(self.text_font_selection['label'], self.text_font_size['label']))

        # Operations Info Frame
        self.operations_info_label_names = ['Expected Hours', 'Total Hours', 'Process']
        self.operations_info_labels = {}
        for name in self.operations_info_label_names:
            self.operations_info_labels[name] = Label(self.operations_info_frame, text=name, bg=background_color, font=(self.text_font_selection['label'], self.text_font_size['label']))

        """ Entries, combo boxes, text boxes, check boxes by LableFrame """
        # all values
        self.all_input_values = {}
        # tasks frame
        self.perform_tasks_check_box_names = ['Location Transfer',  # check box.
                                              'Create and Assign WO',  # check box.
                                              'DM Repair Information',  # check box.
                                              'Add Standard Operations and Booking',  # check box.
                                              # 'Add Booking',   # check box.
                                              'WO Receipt',  # check box.
                                              'Close WO'  # check box.
                                              ]
        self.perform_tasks_check_box_values = {}
        self.perform_tasks_check_boxes = {}
        # make sure these check boxes are checked when starting program
        for name in self.perform_tasks_check_box_names:
            self.perform_tasks_check_box_values[name] = BooleanVar()
            self.perform_tasks_check_box_values[name].set(True)
            self.perform_tasks_check_boxes[name] = Checkbutton(self.perform_tasks_frame, text=name,
                                                               var=self.perform_tasks_check_box_values[name],
                                                               onvalue=True, bg=background_color,
                                                               offvalue=False,
                                                               command=partial(self.is_checked,
                                                                               self.perform_tasks_check_box_values[
                                                                                   name]), font=(self.text_font_selection['label'], self.text_font_size['label']))

        self.perform_tasks_check_boxes['DM Repair Information'].config(
            command=partial(self.hide_frame_input, self.perform_tasks_check_box_values['DM Repair Information'],
                            self.repair_info_frame, 300))
        self.perform_tasks_check_boxes['Add Standard Operations and Booking'].config(
            command=partial(self.hide_frame_input, self.perform_tasks_check_box_values['Add Standard Operations and Booking'],
                            self.operations_info_frame,
                            400))
        self.all_input_values = self.perform_tasks_check_box_values.copy()

        # User info frame
        self.user_info_combo_box_names = ['Name']
        self.user_info_combo_boxes = {}
        for name in self.user_info_combo_box_names:
            self.user_info_combo_boxes[name] = AutocompleteCombobox(self.user_info_frame,
                                                                    completevalues=user_info_combo_box_options[name],
                                                                    width=auto_entry_input_width, font=(self.text_font_selection['label'], self.text_font_size['label']))

        self.all_input_values.update(self.user_info_combo_boxes)

        self.user_info_entry_box_names = ['SalesForce User Name', 'SalesForce Password']
        self.user_info_entry_boxes = {}
        self.user_info_entry_box_text_vars = {}
        for name in self.user_info_entry_box_names:
            self.user_info_entry_box_text_vars[name] = StringVar()
            self.user_info_entry_boxes[name] = Entry(self.user_info_frame,
                                                     textvariable=self.user_info_entry_box_text_vars[name], width=auto_entry_input_width, font=(self.text_font_selection['label'], self.text_font_size['label']))

        self.all_input_values.update(self.user_info_entry_box_text_vars)
        self.user_info_entry_boxes['SalesForce Password'].config(show='*')

        # Unit info frame
        self.unit_info_entry_box_names = ['Part Number', 'Serial Number', 'Previous WO Number']
        self.unit_info_entry_boxes = {}
        self.unit_info_entry_box_text_vars = {}
        for name in self.unit_info_entry_box_names:
            self.unit_info_entry_box_text_vars[name] = StringVar()
            self.unit_info_entry_boxes[name] = Entry(self.unit_info_frame,
                                                     textvariable=self.unit_info_entry_box_text_vars[name], width=auto_entry_input_width, font=(self.text_font_selection['label'], self.text_font_size['label']))

        self.all_input_values.update(self.unit_info_entry_box_text_vars)

        self.unit_info_check_box_names = ['Use Previous WO', 'Customer Property']
        self.unit_info_check_boxes = {}
        self.unit_info_check_box_vars = {}
        for name in self.unit_info_check_box_names:
            self.unit_info_check_box_vars[name] = BooleanVar()
            self.unit_info_check_box_vars[name].set(False)
            self.unit_info_check_boxes[name] = Checkbutton(self.unit_info_frame, text=name, bg=background_color,
                                                           var=self.unit_info_check_box_vars[name],
                                                           onvalue=True, offvalue=False, font=(self.text_font_selection['label'], self.text_font_size['label']))

        self.unit_info_check_boxes['Customer Property'].config(
            command=partial(self.is_checked, self.unit_info_check_box_vars['Customer Property']))
        self.unit_info_check_boxes['Use Previous WO'].config(
            command=partial(self.previous_wo_input, self.unit_info_check_box_vars['Use Previous WO'],
                            self.unit_info_labels['Previous WO Number'],
                            self.unit_info_entry_boxes['Previous WO Number'], 3))
        self.all_input_values.update(self.unit_info_check_box_vars)

        # location transfer frame
        self.location_info_check_box_names = ['change Initial Location']
        self.location_info_check_boxes = {}
        self.location_info_check_box_vars = {}
        for name in self.location_info_check_box_names:
            self.location_info_check_box_vars[name] = BooleanVar()
            self.location_info_check_boxes[name] = Checkbutton(self.location_info_frame, text=name,
                                                               var=self.location_info_check_box_vars[name],
                                                               onvalue=True, offvalue=False, bg=background_color,
                                                               command=partial(self.is_checked,
                                                                               self.location_info_check_box_vars[name]), font=(self.text_font_selection['label'], self.text_font_size['label']))

        self.all_input_values.update(self.location_info_check_box_vars)

        # initial location options
        self.dummy = 0
        self.get_location_ids()
        # populate all of the different combo boxes available for each location ID
        self.location_info_initial_no_combo_boxes = {}
        for option in location_info_id_options:
            self.location_info_initial_no_combo_boxes[option] = AutocompleteCombobox(self.location_info_frame,
                                                                                     completevalues=
                                                                                     location_info_no_options_by_id[
                                                                                         option], width=auto_entry_input_width, font=(self.text_font_selection['label'], self.text_font_size['label']))
            self.location_info_initial_no_combo_boxes[option].bind('<Return>', partial(self.autocorrect_no,
                                                                                       self.location_info_initial_no_combo_boxes[
                                                                                           option],
                                                                                       current_initial_location_no_option,
                                                                                       location_info_no_options_by_id[
                                                                                           option]))
            self.location_info_initial_no_combo_boxes[option].bind('<FocusOut>', partial(self.autocorrect_no,
                                                                                         self.location_info_initial_no_combo_boxes[
                                                                                             option],
                                                                                         current_initial_location_no_option,
                                                                                         location_info_no_options_by_id[
                                                                                             option]))

        self.all_input_values.update(self.location_info_initial_no_combo_boxes)

        # autocorrect_id(self, sel_box, cur_sel, sel_options, row)
        # initial location ID
        self.location_info_initial_id_combo_box = {}
        self.location_info_initial_id_combo_box['Initial'] = AutocompleteCombobox(self.location_info_frame,
                                                                                  completevalues=location_info_id_options,
                                                                                  width=auto_entry_input_width, font=(self.text_font_selection['label'], self.text_font_size['label']))
        self.location_info_initial_id_combo_box['Initial'].bind('<Return>', partial(self.autocorrect_id,
                                                                                    self.location_info_initial_id_combo_box[
                                                                                        'Initial'],
                                                                                    self.location_info_initial_no_combo_boxes,
                                                                                    current_initial_location_no_option,
                                                                                    location_info_id_options, 2))
        self.location_info_initial_id_combo_box['Initial'].bind('<FocusOut>', partial(self.autocorrect_id,
                                                                                      self.location_info_initial_id_combo_box[
                                                                                          'Initial'],
                                                                                      self.location_info_initial_no_combo_boxes,
                                                                                      current_initial_location_no_option,
                                                                                      location_info_id_options, 2))

        self.all_input_values.update(self.location_info_initial_id_combo_box)

        # final location options
        # populate all of the different combo boxes available for each location ID
        self.location_info_final_no_combo_boxes = {}
        for option in location_info_id_options:
            self.location_info_final_no_combo_boxes[option] = AutocompleteCombobox(self.location_info_frame,
                                                                                   completevalues=
                                                                                   location_info_no_options_by_id[
                                                                                       option], width=auto_entry_input_width, font=(self.text_font_selection['label'], self.text_font_size['label']))
            self.location_info_final_no_combo_boxes[option].bind('<Return>',
                                                                 partial(self.autocorrect_no,
                                                                         self.location_info_final_no_combo_boxes[
                                                                             option],
                                                                         current_final_location_no_option,
                                                                         location_info_no_options_by_id[option]))
            self.location_info_final_no_combo_boxes[option].bind('<FocusOut>',
                                                                 partial(self.autocorrect_no,
                                                                         self.location_info_final_no_combo_boxes[
                                                                             option],
                                                                         current_final_location_no_option,
                                                                         location_info_no_options_by_id[option]))

        self.all_input_values.update(self.location_info_final_no_combo_boxes)

        # final location ID
        self.location_info_final_id_combo_box = {}
        self.location_info_final_id_combo_box['Final'] = AutocompleteCombobox(self.location_info_frame,
                                                                              completevalues=self.location_info_id_options,
                                                                              width=auto_entry_input_width, font=(self.text_font_selection['label'], self.text_font_size['label']))
        self.location_info_final_id_combo_box['Final'].bind('<Return>',
                                                            partial(self.autocorrect_id,
                                                                    self.location_info_final_id_combo_box['Final'],
                                                                    self.location_info_final_no_combo_boxes,
                                                                    current_final_location_no_option,
                                                                    location_info_id_options, 3, ))
        self.location_info_final_id_combo_box['Final'].bind('<FocusOut>',
                                                            partial(self.autocorrect_id,
                                                                    self.location_info_final_id_combo_box['Final'],
                                                                    self.location_info_final_no_combo_boxes,
                                                                    current_final_location_no_option,
                                                                    location_info_id_options, 3))

        self.location_info_initial_id_combo_box['Initial'].current(0)
        current_initial_location_no_option.set('--None--')
        self.location_info_final_id_combo_box['Final'].current(0)
        current_final_location_no_option.set('--None--')

        self.perform_tasks_check_boxes['Location Transfer'].config(
            command=partial(self.location_transfer_input,
                            self.perform_tasks_check_box_values['Location Transfer'],
                            self.location_info_labels['Transfer Location ID'],
                            self.location_info_initial_id_combo_box['Initial'],
                            self.location_info_labels['Transfer Location No.'],
                            self.location_info_initial_no_combo_boxes,
                            current_initial_location_no_option,
                            2))
        self.perform_tasks_check_boxes['WO Receipt'].config(
            command=partial(self.location_transfer_input,
                            self.perform_tasks_check_box_values['WO Receipt'],
                            self.location_info_labels['WO Receipt Location ID'],
                            self.location_info_final_id_combo_box['Final'],
                            self.location_info_labels['WO Receipt Location No.'],
                            self.location_info_final_no_combo_boxes,
                            current_final_location_no_option,
                            3))

        self.all_input_values.update(self.location_info_final_id_combo_box)

        # repair info frame
        self.repair_info_entry_box_names = ['OEM Number']
        self.repair_info_entry_boxes = {}
        self.repair_info_entry_box_vars = {}
        for name in self.repair_info_entry_box_names:
            self.repair_info_entry_box_vars[name] = StringVar()
            self.repair_info_entry_boxes[name] = Entry(self.repair_info_frame, width=auto_entry_input_width,
                                                       textvariable=self.repair_info_entry_box_vars[name], font=(self.text_font_selection['label'], self.text_font_size['label']))

        self.all_input_values.update(self.repair_info_entry_box_vars)

        self.repair_info_text_box_names = ['Customer Complaint', 'Initial Condition', 'Initial Failure',
                                           'Internal Repair',
                                           'Testing Notes', 'External Repair']
        self.repair_info_text_boxes = {}
        for name in self.repair_info_text_box_names:
            self.repair_info_text_boxes[name] = Text(self.repair_info_frame, height=4, width=repair_text_input_width, font=(self.text_font_selection['text'], self.text_font_size['text']))

        self.all_input_values.update(self.repair_info_text_boxes)

        self.repair_info_check_box_names = ['Tested On Bench', 'Tested On Live MRI', 'Repair Is Finalized', 'Append']
        self.repair_info_check_boxes = {}
        self.repair_info_check_box_vars = {}
        for name in self.repair_info_check_box_names:
            self.repair_info_check_box_vars[name] = BooleanVar()
            self.repair_info_check_boxes[name] = Checkbutton(self.repair_info_frame, text=name,
                                                             var=self.repair_info_check_box_vars[name],
                                                             onvalue=True, offvalue=False, bg=background_color,
                                                             command=partial(self.is_checked,
                                                                             self.repair_info_check_box_vars[name]), font=(self.text_font_selection['label'], self.text_font_size['label']))

        self.all_input_values.update(self.repair_info_check_box_vars)

        # repair_info_var_values should have .get() for all of its contents.
        self.repair_info_var_values = self.repair_info_entry_box_vars.copy()
        self.repair_info_var_values.update(self.repair_info_text_boxes)
        self.repair_info_var_values.update(self.repair_info_check_box_vars)

        # Operations Info Frame
        self.operations_info_button_names = ["Add Operation", "Delete Operation"]
        self.operations_info_buttons = {}
        for name in self.operations_info_button_names:
            self.operations_info_buttons[name] = Button(self.operations_info_frame, text=name, bg=button_color, fg="#FFFFFF",
                                                        width=button_width, font=(self.text_font_selection['label'], self.text_font_size['label'], 'bold'))

        self.operations_info_buttons["Add Operation"].config(command=self.add_std_op)
        self.operations_info_buttons["Delete Operation"].config(command=self.delete_std_op)

        self.operations_info_combo_box_options = ["10 (Initial Test / Inspection)", "20 (Diagnose / Troubleshoot)",
                                                  "30 (Repair)",
                                                  "35 (External Vendor Repair)", "40 (Assembly / Reassembly)",
                                                  "50 (Final Bench Test)",
                                                  "60 (Final System Test)", "110 (Scrap / Component Harvest)"]
        self.operations_info_combo_box_names = ["Process"]
        self.operations_info_combo_boxes = {}
        for name in self.operations_info_combo_box_names:
            self.operations_info_combo_boxes[name] = AutocompleteCombobox(self.operations_info_frame,
                                                                          completevalues=self.operations_info_combo_box_options,
                                                                          width=button_width, font=(self.text_font_selection['label'], self.text_font_size['label']))

        self.all_input_values.update(self.operations_info_combo_boxes)

        self.operations_info_entry_box_names = ['Expected Hours', 'Total Hours']
        self.operations_info_entry_boxes = {}
        self.operations_info_entry_box_vars = {}
        for name in self.operations_info_entry_box_names:
            self.operations_info_entry_box_vars[name] = StringVar()
            self.operations_info_entry_boxes[name] = Entry(self.operations_info_frame,
                                                           textvariable=self.operations_info_entry_box_vars[name],
                                                           width=button_width, font=(self.text_font_selection['label'], self.text_font_size['label']))

        self.all_input_values.update(self.operations_info_entry_box_vars)

        # Message box frame
        self.message_box = Text(self.message_box_frame, height=5, width=message_box_width, font=(self.text_font_selection['text'], self.text_font_size['text']))

        """ File Menu Options """
        # save/load options
        # exit option
        """ Edit Menu Options """
        # xpaths
        """ Update Menu Options """

        # File menu
        self.file_menu = Menu(main_menu_bar, tearoff=0)
        main_menu_bar.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label='Load Info', command=self.get_user_data)
        self.file_menu.add_command(label='Save Info', command=self.save_user_data)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=root.quit)
        # Edit menu
        self.edit_menu = Menu(main_menu_bar, tearoff=0)
        main_menu_bar.add_cascade(label='Update', menu=self.edit_menu)
        # self.edit_menu.add_command(label='Options', command=self.is_checked)
        # self.edit_menu.add_command(label='Xpath', command=self.is_checked)
        self.edit_menu.add_command(label='Xpaths', command=self.xpaths.load_xpaths_github)
        self.edit_menu.add_command(label='Locations', command=self.load_locations_github)

    def start_gui(self):
        from sources.variables import max_col, all_col_width, current_initial_location_no_option, \
            current_final_location_no_option, background_color, button_color

        """ Placing elements on grid """
        # grid will have 8 columns
        pad_label = Label(self.wo_frame, text=" ", bg=background_color)
        pad_label.grid(row=0, column=0, pady=100, padx=25, sticky=W, rowspan=30)
        Grid.columnconfigure(self.wo_frame, 0, weight=1)

        # establish order in which sections will be arranged
        # -column, -columnspan, -in, -ipadx, -ipady, -padx, -pady, -row, -rowspan, or -sticky
        self.perform_tasks_frame.grid(row=1, column=1, columnspan=max_col, sticky=W, pady=5)
        self.user_info_frame.grid(row=10, column=1, columnspan=max_col, sticky=W, pady=5)
        self.unit_info_frame.grid(row=100, column=1, columnspan=max_col, sticky=W, pady=5)
        self.location_info_frame.grid(row=200, column=1, columnspan=max_col, sticky=W, pady=5)
        self.repair_info_frame.grid(row=300, column=1, columnspan=max_col, sticky=W, pady=5)
        self.operations_info_frame.grid(row=400, column=1, columnspan=max_col, sticky=W, pady=5)
        # self.message_box_frame.grid(row=500, column=1, columnspan=max_col, sticky=W, pady=5)

        # widgets for perform_tasks_frame
        row_start = 0
        col_start = 0
        for index in range(0, len(self.perform_tasks_check_box_names) - 1):
            if (index % 3) == 0:
                row_start = row_start + 1
                col_start = 0
            self.perform_tasks_check_boxes[self.perform_tasks_check_box_names[index]].grid(row=row_start,
                                                                                           column=col_start, sticky=NW,
                                                                                           pady=5, columnspan=2, padx=10)
            col_start = col_start + 2

        # widgets for user_info_frame
        col_start = 0
        row_start = 1
        for index in range(0, len(self.user_info_combo_box_names)):
            self.user_info_labels[self.user_info_combo_box_names[index]].grid(row=row_start, column=col_start,
                                                                              sticky=NE, pady=5)
            col_start = col_start + 1
            self.user_info_combo_boxes[self.user_info_combo_box_names[index]].grid(row=row_start, column=col_start,
                                                                                   sticky=NW, pady=5,
                                                                                   columnspan=2)
            col_start = col_start + 2

        col_start = 0
        row_start = row_start + 1
        for index in range(0, len(self.user_info_entry_box_names)):
            self.user_info_labels[self.user_info_entry_box_names[index]].grid(row=row_start, column=col_start,
                                                                              sticky=NE, pady=5)
            col_start = col_start + 1
            self.user_info_entry_boxes[self.user_info_entry_box_names[index]].grid(row=row_start, column=col_start,
                                                                                   sticky=W, pady=5,
                                                                                   columnspan=2)
            col_start = col_start + 2

        # widgets for Unit_info_frame
        col_start = 0
        row_start = 1
        for index in range(0, len(self.unit_info_entry_box_names) - 1):
            if (index % 2) == 0:
                row_start = row_start + 1
                col_start = 0

            self.unit_info_labels[self.unit_info_entry_box_names[index]].grid(row=row_start, column=col_start, sticky=E,
                                                                              pady=5)
            col_start = col_start + 1
            self.unit_info_entry_boxes[self.unit_info_entry_box_names[index]].grid(row=row_start, column=col_start,
                                                                                   sticky=W, pady=5,
                                                                                   columnspan=2)
            col_start = col_start + 2

        col_start = 0
        row_start = row_start + 2
        for index in range(0, len(self.unit_info_check_box_names)):
            self.unit_info_check_boxes[self.unit_info_check_box_names[index]].grid(row=row_start, column=col_start,
                                                                                   sticky=E, pady=5)
            col_start = col_start + 2

        # widgets for location_info_frame
        col_start = 1
        row_start = 1
        for index in range(0, len(self.location_info_label_names)):
            if (index % 2) == 0:
                row_start = row_start + 1
                col_start = 0

            self.location_info_labels[self.location_info_label_names[index]].grid(row=row_start, column=col_start,
                                                                                  sticky=E, pady=5)
            col_start = col_start + 3

        current_initial_location_no_option.set('--None--')
        current_final_location_no_option.set('--None--')
        col_start = 1
        row_start = 2
        self.location_info_initial_id_combo_box['Initial'].grid(row=row_start, column=col_start, sticky=W, pady=5,
                                                                columnspan=2)
        col_start = col_start + 3
        self.location_info_initial_no_combo_boxes[current_initial_location_no_option.get()].grid(row=row_start,
                                                                                                 column=col_start,
                                                                                                 sticky=W, pady=5,
                                                                                                 columnspan=2)
        col_start = 1
        row_start = 3
        self.location_info_final_id_combo_box['Final'].grid(row=row_start, column=col_start, sticky=W, pady=5,
                                                            columnspan=2)
        col_start = col_start + 3
        self.location_info_final_no_combo_boxes[current_final_location_no_option.get()].grid(row=row_start,
                                                                                             column=col_start,
                                                                                             sticky=W, pady=5,
                                                                                             columnspan=2)

        # widgets for repair_info_frame
        col_start = 0
        row_start = 1
        for index in range(0, len(self.repair_info_entry_box_names)):
            self.repair_info_labels[self.repair_info_entry_box_names[index]].grid(row=row_start, column=col_start,
                                                                                  sticky=E, pady=5)
            col_start = col_start + 1
            self.repair_info_entry_boxes[self.repair_info_entry_box_names[index]].grid(row=row_start, column=col_start,
                                                                                       sticky=W, pady=5,
                                                                                       columnspan=2)
            col_start = col_start + 2

        col_start = 0
        row_start = row_start + 1
        for index in range(0, len(self.repair_info_text_box_names)):
            if (index % 2) == 0:
                col_start = 0
                row_start = row_start + 1

            self.repair_info_labels[self.repair_info_text_box_names[index]].grid(row=row_start, column=col_start,
                                                                                 sticky=NE, pady=5)
            col_start = col_start + 1
            self.repair_info_text_boxes[self.repair_info_text_box_names[index]].grid(row=row_start, column=col_start,
                                                                                     sticky=W, pady=5,
                                                                                     columnspan=2)
            col_start = col_start + 2

        col_start = 0
        row_start = row_start + 1
        for index in range(0, len(self.repair_info_check_box_names) - 1):
            self.repair_info_check_boxes[self.repair_info_check_box_names[index]].grid(row=row_start, column=col_start,
                                                                                       sticky=E, pady=5)
            col_start = col_start + 1

        self.repair_info_check_boxes['Append'].grid(row=0, column=0, sticky=E, pady=5)

        # widgets for operations frame
        col_start = 1
        for name in self.operations_info_button_names:
            self.operations_info_buttons[name].grid(row=0, column=col_start, pady=5, sticky=E)
            col_start = col_start + 1

        # widgets for message_box
        # self.message_box.grid(row=1, column=0, sticky=W, pady=5, columnspan=7)
        # Set all frames to have the same col width
        for frame in self.all_frames:
            for index in range(0, max_col):
                temp = Label(frame, text="    ", bg=background_color)
                temp.grid(row=8, column=index, padx=all_col_width, sticky=W)
                frame.grid_columnconfigure(index, weight=1, uniform="fred")

        # Run Button
        run_button = Button(self.wo_frame, text="Run", width=20, fg="#FFFFFF", bg=button_color, command=partial(run_wo_maker, self), font=(self.text_font_selection['label'], self.text_font_size['label'], 'bold'))
        run_button.grid(row=650, column=3, pady=5, sticky=E)
        # test Button
        # test_button = Button(self.wo_frame, text="Test Values", width=20, command=partial(variable_tester, self.all_input_values))
        # test_button.grid(row=650, column=2, pady=5, sticky=E)

    def _on_mousewheel(self, event):  # change this self
        self.main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def window_size_update(self, event):  # change this self
        from sources.variables import root
        debugger_print('updating window.')
        window_width = root.winfo_width()
        window_height = root.winfo_height()
        if (window_width != event.width) or (window_height != event.heigth):
            root.update()
            self.grid(row=0, column=1, sticky=W, columnspan=8, padx=int(0.05 * root.winfo_width()),
                      pady=int(0.05 * root.winfo_height()))

    def is_checked(self, var):
        debugger_print(var.get())
        if var.get() is True:
            debugger_print("check box is checked")
        else:
            debugger_print("check box is not checked.")

    def autocorrect_id(self, ele, sel_box, cur_sel, sel_options, row, event):  # change this self
        # debugger_print("selection identifier: ")
        # debugger_print(cur_sel)
        # debugger_print(self.get())
        match_flag = False
        new_sel = ' '
        for sel in sel_options:
            if ele.get() in sel:
                new_sel = sel
                match_flag = True
                break

        if match_flag is False:
            ele.set(ele.current(0))
            # debugger_print("no match found")
        else:
            ele.autocomplete()
            if cur_sel.get() != new_sel:
                sel_box[cur_sel.get()].grid_remove()
                sel_box[new_sel].grid(row=row, column=4, sticky=W, pady=5, columnspan=2)
                cur_sel.set(new_sel)
                # debugger_print("NEW selection identifier: " + cur_sel.get())

            debugger_print("found a match")

    def autocorrect_no(self, ele, cur_sel, sel_options, event):  # change this self
        debugger_print("selection identifier: " + cur_sel.get())
        # print(self.get())
        match_flag = False
        new_sel = ' '
        for sel in sel_options:
            if ele.get() in sel:
                new_sel = sel
                match_flag = True
                break

        if match_flag is False:
            ele.set(ele.current(0))
            debugger_print("no match found")
        else:
            ele.autocomplete()
            debugger_print("NEW selection identifier: " + cur_sel.get())
            debugger_print("found a match")

    def previous_wo_input(self, var, wid1, wid2, row_ind):
        if var.get() is True:
            wid1.grid(row=row_ind, column=0, sticky=E, pady=5)
            wid2.grid(row=row_ind, column=1, sticky=W, pady=5, columnspan=2)
        else:
            wid1.grid_remove()
            wid2.grid_remove()

    def location_transfer_input(self, var, wid1, wid2, wid3, wid4, current_loc, row_ind):
        if var.get() is True:
            wid1.grid(row=row_ind, column=0, sticky=E, pady=5)
            wid2.grid(row=row_ind, column=1, sticky=W, pady=5, columnspan=2)
            wid3.grid(row=row_ind, column=3, sticky=E, pady=5)
            wid4[current_loc.get()].grid(row=row_ind, column=4, sticky=W, pady=5, columnspan=2)
        else:
            wid1.grid_remove()
            wid2.grid_remove()
            wid3.grid_remove()
            wid4[current_loc.get()].grid_remove()

    def hide_frame_input(self, var, input_frame, row_ind):
        from sources.variables import max_col, root
        if var.get() is True:
            input_frame.grid(row=row_ind, column=1, columnspan=max_col, sticky=W, pady=5)
        else:
            input_frame.grid_remove()

        root.update()

    def add_std_op(self):
        from sources.variables import op_combo_box_options, op_labels, op_widgets, op_vars, op_label_names, root, \
            operations_width, background_color

        # Operations Info Frame
        # Labels

        op_index = len(op_labels) - 1

        if op_index < 0:
            op_labels_temp = {}
            op_labels.append(op_labels_temp)
            op_widgets_temp = {}
            op_widgets.append(op_widgets_temp)
            op_vars_temp = {}
            op_vars.append(op_vars_temp)
            op_index = op_index + 1
            # widget creation
            for op_name in op_label_names:
                op_labels[op_index][op_name] = Label(self.operations_info_frame, text=op_name, bg=background_color, font=(self.text_font_selection['label'], self.text_font_size['label']))
                if op_name == 'Process':
                    op_widgets[op_index][op_name] = AutocompleteCombobox(self.operations_info_frame,
                                                                         completevalues=op_combo_box_options, width=operations_width*2, font=(self.text_font_selection['label'], self.text_font_size['label']))
                else:
                    op_vars[op_index][op_name] = DoubleVar()
                    op_widgets[op_index][op_name] = Entry(self.operations_info_frame,
                                                          textvariable=op_vars[op_index][op_name], width=operations_width, font=(self.text_font_selection['label'], self.text_font_size['label']))
                    op_vars[op_index][op_name].set(0)

            # Widget Placement on Grid
            for op_name in op_label_names:
                if op_name == 'Process':
                    op_labels[op_index][op_name].grid(row=(op_index + 1), column=0, sticky=E, pady=5)
                    op_widgets[op_index][op_name].grid(row=(op_index + 1), column=1, sticky=W, pady=5, columnspan=2)

                elif op_name == 'Expected Hours':
                    op_labels[op_index][op_name].grid(row=(op_index + 1), column=2, sticky=E, pady=5)
                    op_widgets[op_index][op_name].grid(row=(op_index + 1), column=3, sticky=W, pady=5)

                elif op_name == 'Total Hours':
                    op_labels[op_index][op_name].grid(row=(op_index + 1), column=4, sticky=E, pady=5)
                    op_widgets[op_index][op_name].grid(row=(op_index + 1), column=5, sticky=W, pady=5)

        root.update()

    def delete_std_op(self):
        from sources.variables import op_labels, op_widgets, op_vars, op_label_names, root
        op_index = len(op_labels) - 1
        if op_index >= 0:
            for op_name in op_label_names:
                op_labels[op_index][op_name].grid_remove()
                op_widgets[op_index][op_name].grid_remove()

            op_labels.pop(op_index)
            op_widgets.pop(op_index)
            op_vars.pop(op_index)

        root.update()

    def get_location_ids(self):
        from sources.variables import location_info_id_options, location_info_no_options_by_id
        data_flag = False  # true if CSV file is found
        try:
            location_data = pd.read_csv('locations.csv')  # read csv file
            if location_data.empty:  # check if csv file is empty
                debugger_print('CSV file is empty.')  # print out message on status box
                data_flag = False  # set flag false
            else:
                data_flag = True  # set flag true b/c csv file is not empty

        except FileNotFoundError:  # handle if file is not found in ROG folder.
            self.load_locations_github()  # search on github for default data.
            debugger_print("Get data from Github")

        if data_flag is True:  # csv file is found in ROG folder
            # obtain all of the location number headers
            location_info_id_options_temp = location_data['Location ID'].astype(str)  # convert dataframe to string
            location_info_no_options_by_id_temp = {}
            for header in location_info_id_options_temp:
                if header != 'nan':
                    location_info_no_options_by_id_temp[header] = location_data[header].astype(str)

            for option in location_info_id_options_temp:
                if option != 'nan':
                    location_info_id_options.append(option.__str__())  # place xpath info into xpath_options
                    location_info_no_options_by_id[option] = []
                    for opt in location_info_no_options_by_id_temp[option]:
                        if opt != 'nan':
                            opt_str = opt.__str__()
                            # print('opt str: ' + opt_str)
                            parenthesis_init = opt_str.find('(')
                            # print('par init: ' + parenthesis_init.__str__())
                            parenthesis_final = opt_str.find(')')
                            # print('par final: ' + parenthesis_final.__str__())
                            if (parenthesis_final != -1) and (parenthesis_init != -1):
                                sub_opt_str = opt_str[0:parenthesis_init - 1]
                                # print('final str: ' + sub_opt_str)
                                location_info_no_options_by_id[option].append(sub_opt_str)
                            else:
                                # print('final str: ' + opt_str)
                                location_info_no_options_by_id[option].append(opt_str)

                else:
                    continue

    def load_locations_github(self):
        import os
        from sources.variables import location_info_id_options, location_info_no_options_by_id
        data_flag = False  # true if csv file is found in github

        if os.path.exists('locations.csv'):
            os.remove('locations.csv')
        else:
            debugger_print("The file does not exist")

        location_info_id_options.clear()
        location_info_no_options_by_id.clear()

        # github url where default csv file is found.
        locations_url = 'https://raw.githubusercontent.com/directmed/Rootstock_Handler/main/locations.csv'
        location_data = pd.read_csv(locations_url)  # read csv file
        if location_data.empty:  # check if csv file is empty
            # update_status_box('Github CSV file is empty.')
            data_flag = False
        else:
            data_flag = True

        if data_flag is True:  # csv file is found in ROG folder
            # obtain all of the location number headers
            location_info_id_options_temp = location_data['Location ID'].astype(str)  # convert dataframe to string
            location_info_no_options_by_id_temp = {}
            for header in location_info_id_options_temp:
                if header != 'nan':
                    location_info_no_options_by_id_temp[header] = location_data[header].astype(str)

            for option in location_info_id_options_temp:
                if option != 'nan':
                    location_info_id_options.append(option.__str__())  # place xpath info into xpath_options
                    location_info_no_options_by_id[option] = []
                    for opt in location_info_no_options_by_id_temp[option]:
                        if opt != 'nan':
                            opt_str = opt.__str__()
                            # print('opt str: ' + opt_str)
                            parenthesis_init = opt_str.find('(')
                            # print('par init: ' + parenthesis_init.__str__())
                            parenthesis_final = opt_str.find(')')
                            # print('par final: ' + parenthesis_final.__str__())
                            if (parenthesis_final != -1) and (parenthesis_init != -1):
                                sub_opt_str = opt_str[0:parenthesis_init - 1]
                                # print('final str: ' + sub_opt_str)
                                location_info_no_options_by_id[option].append(sub_opt_str)
                            else:
                                # print('final str: ' + opt_str)
                                location_info_no_options_by_id[option].append(opt_str)

                else:
                    continue

        locations_header = []
        locations_header.append('Location ID')
        for loc_index in range(0, len(location_info_id_options)):
            locations_header.append(location_info_id_options[loc_index])
        debugger_print("headers = " + locations_header.__str__())

        locations_data = [[]]
        locations_data[0] = location_info_id_options.copy()
        for key_index, key in enumerate(location_info_no_options_by_id):
            locations_data.append([])
            debugger_print("locations data index = " + (key_index + 1).__str__())
            for data in location_info_no_options_by_id[key]:
                locations_data[key_index + 1].append(data)

        df = pd.DataFrame(locations_data, index=locations_header).transpose()
        df.to_csv('locations.csv', index=False)  # save CSV file

    # Function saves all user data to csv file in ROG folder.
    def save_user_data(self):
        # user_name, user_password, engineer_name, directory
        data_info_headers = ['user', 'unit']  # add 'options'
        user_info_headers = [self.user_info_entry_box_names, self.unit_info_entry_box_names]
        user_info_header_values = [self.user_info_entry_box_text_vars, self.unit_info_entry_box_text_vars]
        info_str = [[], []]
        headers = []
        for header_index, header in enumerate(data_info_headers):
            headers.append(header.__str__())
            debugger_print("saving info: header = " + header)
            for entry in user_info_headers[header_index]:
                debugger_print("entry = " + entry)
                debugger_print(
                    "info_str[" + header + "] = " + user_info_header_values[header_index][entry].get().__str__())
                info_str[header_index].append("\'" + user_info_header_values[header_index][entry].get().__str__())

        df = pd.DataFrame(info_str, index=headers).transpose()
        df.to_csv('user_data.csv', index=False)  # save CSV file

    def get_user_data(self):
        data_flag = False  # true if CSV file is found

        try:
            user_data = pd.read_csv('user_data.csv')  # read csv file
            if user_data.empty:  # check if csv file is empty
                # update_status_box('CSV file is empty.')  # print out message on status box
                data_flag = False  # set flag false
            else:
                data_flag = True  # set flag true b/c csv file is not empty

        except FileNotFoundError:  # handle if file is not found in ROG folder.
            debugger_print("No user data available.")
            return

        if data_flag is True:  # csv file is found in ROG folder
            user_info = user_data['user'].astype(str)
            unit_info = user_data['unit'].astype(str)
            data_info = [user_info, unit_info]
            for info_index in range(0, len(data_info)):
                self.saved_user_data[self.data_info_headers[info_index]] = []
                for data_index, data in enumerate(data_info[info_index]):
                    if data != 'nan':
                        data = data.__str__().replace("\'", "")
                        self.saved_user_data[self.data_info_headers[info_index]].append(
                            data.__str__())  # place xpath info into xpath_options
                        debugger_print("data = " + data.__str__())
                        debugger_print(self.saved_user_data)
                        debugger_print("getting user info from file")
                    else:
                        continue
            # show data
            self.update_loaded_data()
            self.save_user_data()  # save all the data.

    def update_loaded_data(self):
        from sources.variables import root
        # data_info_headers = ['user', 'unit']  # add 'options'
        user_info_headers = [self.user_info_entry_box_names, self.unit_info_entry_box_names]
        user_info_header_values = [self.user_info_entry_box_text_vars, self.unit_info_entry_box_text_vars]

        for header_index, header in enumerate(self.saved_user_data):
            debugger_print("updating info: header = " + header)
            for entry_index, entry in enumerate(user_info_headers[header_index]):
                debugger_print("updating entry = " + entry)
                if entry_index <= (len(self.saved_user_data[header]) - 1):
                    debugger_print(self.saved_user_data[header][entry_index])
                    user_info_header_values[header_index][entry].set(
                        self.saved_user_data[header][entry_index].__str__())
                else:
                    continue

        root.update()

    def get_user_info_entry_box_text_vars(self, name):
        return self.user_info_entry_box_text_vars[name].get().__str__()

    def get_user_info_combo_boxes(self, name):
        return self.user_info_combo_boxes[name].get()

    def get_unit_info_entry_box_text_vars(self, name):
        return self.unit_info_entry_box_text_vars[name].get().__str__()

    def get_unit_info_check_box_vars(self, name):
        return self.unit_info_check_box_vars[name].get()

    def get_location_info_final_id_combo_box(self, name):
        return self.location_info_final_id_combo_box[name].get().__str__()

    def get_location_info_final_no_combo_boxes(self, name):
        return self.location_info_final_no_combo_boxes[name].get().__str__()

    def get_location_info_initial_id_combo_box(self, name):
        return self.location_info_initial_id_combo_box[name].get().__str__()

    def get_location_info_initial_no_combo_boxes(self, name):
        return self.location_info_initial_no_combo_boxes[name].get().__str__()

    def pull_repair_info_var_values(self, name):
        return self.repair_info_var_values[name]

    def get_repair_info_check_box_vars(self, name):
        return self.repair_info_check_box_vars[name].get()

    def get_perform_tasks_check_box_values(self, name):
        return self.perform_tasks_check_box_values[name].get()
