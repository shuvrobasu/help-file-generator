#The ContextualHelp class is responsible for displaying help information for the different elements of the application.
#The load_help_info method reads the help information from a JSON file and restructures it for easier access.
#The display_help method is used to display the help information for a specific element.
#The help information is displayed in a Toplevel window with a Text widget.

import json
from tkinter import Tk, Toplevel, Text, END, messagebox, font


class ContextualHelp:
    def __init__(self, help_file):
        self.help_info = self.load_help_info(help_file)

    def load_help_info(self, help_file):
        try:
            with open(help_file, 'r') as file:
                content = json.load(file)

            # Restructure the content for easier access
            help_info = {}
            if "General" in content:
                help_info["title"] = content["General"].get("title", [])
                help_info["description"] = content["General"].get("description", [])

            if "MainWindow" in content and "elements" in content["MainWindow"]:
                for element, data in content["MainWindow"]["elements"].items():
                    help_info[element] = data if isinstance(data, list) else [{"text": data, "tags": {}}]

            return help_info
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format in help file.")
            return {}
        except FileNotFoundError:
            messagebox.showerror("Error", f"Help file not found: {help_file}")
            return {}

    def display_help(self, element_id, platform):
        if element_id in self.help_info:
            help_data = self.help_info[element_id]

            root = Tk()
            root.withdraw()  # Hide the root window
            help_window = Toplevel(root)
            help_window.title(f"Help - {element_id.capitalize()}")
            text_widget = Text(help_window, wrap="word")
            text_widget.pack(expand=True, fill="both")

            self.apply_formatting(text_widget, help_data)
            help_window.mainloop()
        else:
            messagebox.showinfo("Help", "No help available for this element.")

    def apply_formatting(self, text_widget, help_data):
        default_font = font.nametofont(text_widget.cget("font"))
        current_font_family = default_font.actual()["family"]
        current_font_size = default_font.actual()["size"]

        for line in help_data:
            text_widget.insert(END, line["text"] + "\n")
            line_start = text_widget.index(f"end-2c linestart")
            line_end = text_widget.index(f"end-1c")

            for tag, _ in line["tags"].items():
                if tag.startswith("color_"):
                    text_widget.tag_configure(tag, foreground=tag[6:])
                elif tag.startswith("family_"):
                    family = tag[7:]
                    text_widget.tag_configure(tag, font=(family, current_font_size))
                elif tag.startswith("size_"):
                    size = int(tag[5:])
                    text_widget.tag_configure(tag, font=(current_font_family, size))
                elif tag == "bold":
                    text_widget.tag_configure(tag, font=(current_font_family, current_font_size, "bold"))
                elif tag == "italic":
                    text_widget.tag_configure(tag, font=(current_font_family, current_font_size, "italic"))
                elif tag == "underline":
                    text_widget.tag_configure(tag, underline=True)

                text_widget.tag_add(tag, line_start, line_end)

    def show_general_help(self):
        root = Tk()
        root.withdraw()  # Hide the root window
        help_window = Toplevel(root)
        help_window.title("General Help")
        text_widget = Text(help_window, wrap="word")
        text_widget.pack(expand=True, fill="both")

        # Display title
        self.apply_formatting(text_widget, self.help_info.get("title", []))
        text_widget.insert(END, "\n\n")  # Add some space between title and description

        # Display description
        self.apply_formatting(text_widget, self.help_info.get("description", []))

        help_window.mainloop()
