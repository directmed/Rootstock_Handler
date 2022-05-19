from sources.all_imports import *


def autocomplete_example(ws):
    selections = ['--None--', 'countries', 'continents', 'oceans', 'planets']
    none_array = ['--None--']
    countries = [
            '-- None --', 'Antigua and Barbuda', 'Bahamas','Barbados','Belize', 'Canada',
            'Costa Rica ', 'Cuba', 'Dominica', 'Dominican Republic', 'El Salvador ',
            'Grenada', 'Guatemala ', 'Haiti', 'Honduras ', 'Jamaica', 'Mexico',
            'Nicaragua', 'Saint Kitts and Nevis', 'Panama ', 'Saint Lucia',
            'Saint Vincent and the Grenadines', 'Trinidad and Tobago', 'United States of America'
            ]
    continents = ['-- None --', 'Asia', 'Europe', 'North America', 'South America', 'Africa', 'Australia', 'Antarctica']
    oceans = ['-- None --', 'Pacific', 'Atlantic', 'Arctic', 'Indian', 'Antarctic']
    planets = ['-- None --', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'X']
    all_arrays = [none_array, countries, continents, oceans, planets]
    selection_combo_box_options = {}
    current_selection = StringVar()
    current_selection.set("--None--")

    for ind, selection in enumerate(selections):
        selection_combo_box_options[selection] = all_arrays[ind]

    def accept_input(self, sel_box, cur_sel, event):
        print("selection identifier: " + cur_sel.get())
        # print(event)
        # print(self.get())
        match_flag = False
        new_sel = ' '
        for sel in selections:
            if self.get() in sel:
                new_sel = sel
                match_flag = True
                break

        if match_flag is False:
            self.set(self.current(0))
            print("no match found")
        else:
            if cur_sel.get() != new_sel:
                self.autocomplete()
                sel_box[cur_sel.get()].pack_forget()
                cur_sel.set(new_sel)
                sel_box[cur_sel.get()].set(sel_box[cur_sel.get()].current(0))
                sel_box[new_sel].pack()
                print("NEW selection identifier: " + current_selection.get())
                print("found a match")

    def accept_input2(self, event):
        print("binding works!")
        # print(event)
        # print(self.get())
        match_flag = False
        for sel in selection_combo_box_options[current_selection.get()]:
            if self.get() in sel:
                match_flag = True
                break

        if match_flag is False:
            self.set(self.current(0))
            print("no match found")
        else:
            self.autocomplete()
            print("found a match")

    ws.title('PythonGuides')
    ws.geometry('400x300')   # set window size
    ws.config(bg='#F2F6FC')  # sets color of background

    frame = LabelFrame(ws, bg='#8DBF5A', text="test label frame")
    frame.pack(expand=True)

    Label(
        frame,
        bg='#8DBF5A',
        font=('Times', 21),
        text='Countries in North America '
        ).pack()

    entry1 = AutocompleteCombobox(
        frame,
        width=30,
        font=('Times', 18),
        completevalues=selections
        )

    selection_combo_boxes = {}
    for selection in selections:
        selection_combo_boxes[selection] = AutocompleteCombobox(frame, width=30, font=('Times', 18), completevalues=selection_combo_box_options[selection])
        selection_combo_boxes[selection].bind('<Return>', partial(accept_input2, selection_combo_boxes[selection]))
        selection_combo_boxes[selection].bind('<FocusOut>', partial(accept_input2, selection_combo_boxes[selection]))

    entry1.bind('<Return>', partial(accept_input, entry1, selection_combo_boxes, current_selection))
    entry1.bind('<FocusOut>', partial(accept_input, entry1, selection_combo_boxes, current_selection))

    entry1.pack()
    selection_combo_boxes[current_selection.get()].pack()


if __name__ == "__main__":
    print("Hello world!")
