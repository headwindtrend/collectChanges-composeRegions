import sublime
import sublime_plugin
import re

# # # # # Add these 2 lines to your key bindings
#	{ "keys": ["ctrl+shift+."], "command": "collect_changes" },
#	{ "keys": ["ctrl+shift+,"], "command": "collect_changes", "args": {"addArbitraryRegions": true} },
# # # # #

class collectChangesCommand(sublime_plugin.TextCommand):
    my_collection_list = []
    my_quickpanel_list = []

    def run(self, edit, addArbitraryRegions=False):
        # Function to include the current selection into 'myCollection'
        def include_current_selection():
            self.my_collection_list = self.view.get_regions('myCollection')
            current_selection_list = list(self.view.sel())
            done_flag = "starts repeating"
            for region in current_selection_list:
                if region not in self.my_collection_list:
                    done_flag = "still uncertain"
            if done_flag == "still uncertain":
                self.my_collection_list += current_selection_list
                self.view.erase_regions('myCollection')
                self.view.add_regions('myCollection', self.my_collection_list)
                self.my_collection_list = self.view.get_regions('myCollection')
            return done_flag

        # Function to exhaust all modifications and add them to 'myCollection'
        def exhaust_modifications():
            self.view.erase_regions('myCollection')
            self.my_collection_list = []
            starting_point = self.view.sel()[0]
            self.view.sel().clear(); self.view.sel().add(starting_point)
            self.view.run_command('next_modification')
            if self.view.sel()[0] != starting_point:
                while True:
                    if include_current_selection() == "starts repeating": break
                    self.view.run_command('next_modification')

        # Main logic starts here
        self.view.erase_regions('saved_selection')
        self.view.add_regions('saved_selection', list(self.view.sel()))
        self.my_collection_list = self.view.get_regions('myCollection')

        if addArbitraryRegions:
            # This block of code is a quick-and-dirty way of adding these 4 minor features
            clpbrd = sublime.get_clipboard()
            if clpbrd == 'select myCollection':
                self.view.sel().clear(); self.view.sel().add_all(self.my_collection_list)
                self.view.window().status_message('The regions "myCollection" is selected.')
                return
            elif clpbrd == 'delete myCollection':
                self.view.erase_regions('myCollection')
                sublime.set_clipboard('done << delete myCollection')
                self.view.window().status_message('The regions "myCollection" is deleted.')
                return
            elif re.search(r"[\r\n]?\s*loadfrom\s*=\s*.+(?:[\r\n]|$)", clpbrd):
                match = re.search(r"[\r\n]?\s*loadfrom\s*=\s*(.+)(?:[\r\n]|$)", clpbrd)
                self.view.sel().clear(); self.view.sel().add_all(self.view.get_regions(match.group(1)))
                sublime.set_clipboard('loaded << ' + match.group(1))
                self.view.window().status_message('The regions "' + match.group(1) + '" is loaded.')
            elif re.search(r"[\r\n]?\s*saveto\s*=\s*.+(?:[\r\n]|$)", clpbrd):
                match = re.search(r"[\r\n]?\s*saveto\s*=\s*(.+)(?:[\r\n]|$)", clpbrd)
                self.view.erase_regions(match.group(1))
                self.view.add_regions(match.group(1), self.my_collection_list)
                sublime.set_clipboard('saved << ' + match.group(1))
                self.view.window().status_message('The collection of regions is saved as "' + match.group(1) + '".')
                return

            include_current_selection()
        else:
            exhaust_modifications()

        self.view.sel().clear(); self.view.sel().add(sublime.Region(0, 0))

        # Function to clean up and restore saved selection
        def clean_up():
            self.view.erase_regions('showScope')
            self.view.erase_regions('focusedRegions')
            self.view.sel().clear(); self.view.sel().add_all(self.view.get_regions('saved_selection'))
            self.view.erase_regions('saved_selection')

        # Function to highlight region when the user hovers over it in the quick panel
        def on_highlight(index):
            self.view.add_regions('focusedRegions', [self.my_collection_list[index]], "string", "dot")
            self.view.show_at_center(self.my_collection_list[index].a)

        # Function to handle selection in the quick panel
        def on_select(index):
            if index == -1: # Cancel operation
                clean_up()
                return
            yesno = sublime.yes_no_cancel_dialog("[Exit] to close the panel\n\n[Exclude] if you want to exclude " + str(self.my_collection_list[index]) + " from the collection of regions\n\n[Cancel] to dismiss this dialog and stay with the panel", "Exit", "Exclude")
            if yesno == sublime.DIALOG_YES: # to Exit
                clean_up()
                self.view.sel().clear(); self.view.sel().add_all(self.my_collection_list) # Select all the regions
                return
            elif yesno == sublime.DIALOG_NO: # to Exclude
                self.my_collection_list.pop(index)
                self.view.erase_regions('myCollection')
                self.view.add_regions('myCollection', self.my_collection_list)
                my_quickpanel(index)
            else: # to Dismiss the dialog and get back to the quick panel
                my_quickpanel(index, {'reload': False})

        # Function to prepare the quick panel list
        def prepare_the_show():
            self.view.erase_regions('showScope')
            self.view.add_regions('showScope', self.my_collection_list, "string", "", sublime.DRAW_NO_FILL)
            self.my_quickpanel_list = []
            for region in self.my_collection_list:
                row, col = self.view.rowcol(region.a)
                text = self.view.substr(region)
                text_to_show = text if len(text) < 66 else text[0:62] + "..."
                self.my_quickpanel_list.append(str(region) + " at Line " + str(row+1) + " Pos " + str(col+1) + ": " + text_to_show)
            return self.my_quickpanel_list

        # Function to show the quick panel
        def my_quickpanel(index, reload=True):
            if reload: self.my_quickpanel_list = prepare_the_show()
            self.view.window().show_quick_panel(self.my_quickpanel_list, on_select, 1, index, on_highlight)

        my_quickpanel(0)
