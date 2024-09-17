import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font, colorchooser
import configparser
import ast
from contextualhelp import ContextualHelp
import json

help_system = ContextualHelp("help_generator.ftxt")


def show_help(event):
    focused_widget = event.widget
    element_id = focused_widget.winfo_name()
    print(f"Element ID: {element_id}")  # Print to debug
    help_system.display_help(element_id, "tkinter")


class FormattedTextEditor:
    def __init__(self, master):
        self.master = master

        self.create_widgets()
        self.create_toolbar()

    def create_widgets(self):
        self.text_widget = tk.Text(self.master, wrap="word", undo=True)
        self.text_widget.pack(expand=True, fill="both")

        default_font = font.nametofont(self.text_widget.cget("font"))
        self.current_font_family = default_font.actual()["family"]
        self.current_font_size = default_font.actual()["size"]

        bold_font = font.Font(self.text_widget, self.text_widget.cget("font"))
        bold_font.configure(weight="bold")
        self.text_widget.tag_configure("bold", font=bold_font)

        italic_font = font.Font(self.text_widget, self.text_widget.cget("font"))
        italic_font.configure(slant="italic")
        self.text_widget.tag_configure("italic", font=italic_font)

        self.text_widget.tag_configure("underline", underline=True)

    def create_toolbar(self):
        toolbar = ttk.Frame(self.master)
        toolbar.pack(side="top", fill="x")

        ttk.Button(toolbar, text="Bold", command=self.toggle_bold).pack(side="left", padx=2, pady=2)
        ttk.Button(toolbar, text="Italic", command=self.toggle_italic).pack(side="left", padx=2, pady=2)
        ttk.Button(toolbar, text="Underline", command=self.toggle_underline).pack(side="left", padx=2, pady=2)

        font_families = font.families()
        self.font_family_var = tk.StringVar(value=self.current_font_family)
        font_family_combo = ttk.Combobox(toolbar, textvariable=self.font_family_var, values=font_families, width=15)
        font_family_combo.pack(side="left", padx=2, pady=2)
        font_family_combo.bind("<<ComboboxSelected>>", self.change_font_family)

        font_sizes = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 36, 48, 72]
        self.font_size_var = tk.StringVar(value=self.current_font_size)
        font_size_combo = ttk.Combobox(toolbar, textvariable=self.font_size_var, values=font_sizes, width=5)
        font_size_combo.pack(side="left", padx=2, pady=2)
        font_size_combo.bind("<<ComboboxSelected>>", self.change_font_size)

        ttk.Label(toolbar, text="Font Color:").pack(side="left", padx=2, pady=2)
        self.create_color_dropdown(toolbar)

    def create_color_dropdown(self, parent):
        self.colors = [
            ('#000000', 'Black'), ('#800000', 'Maroon'), ('#008000', 'Green'), ('#808000', 'Olive'),
            ('#000080', 'Navy'), ('#800080', 'Purple'), ('#008080', 'Teal'), ('#C0C0C0', 'Silver'),
            ('#808080', 'Gray'), ('#FF0000', 'Red'), ('#00FF00', 'Lime'), ('#FFFF00', 'Yellow'),
            ('#0000FF', 'Blue'), ('#FF00FF', 'Fuchsia'), ('#00FFFF', 'Aqua'), ('#FFFFFF', 'White')
        ]

        self.color_var = tk.StringVar()
        self.color_var.set(self.colors[0][1])  # Set default value

        color_menu = ttk.OptionMenu(
            parent,
            self.color_var,
            self.colors[0][1],
            *[color[1] for color in self.colors],
            command=self.on_color_select
        )
        color_menu.pack(side="left", padx=2, pady=2)

        # Configure the dropdown list
        color_menu["menu"].configure(bg="white", fg="black")
        for i, (hex_color, color_name) in enumerate(self.colors):
            color_menu["menu"].entryconfigure(
                i,
                background=hex_color,
                foreground=self.get_contrast_color(hex_color),
                activebackground=hex_color,
                activeforeground=self.get_contrast_color(hex_color)
            )

    def get_contrast_color(self, hex_color):
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return "#000000" if luminance > 0.5 else "#FFFFFF"

    def on_color_select(self, color_name):
        hex_color = next(color[0] for color in self.colors if color[1] == color_name)
        self.apply_color(hex_color)

    def toggle_bold(self):
        self.toggle_tag("bold")

    def toggle_italic(self):
        self.toggle_tag("italic")

    def toggle_underline(self):
        self.toggle_tag("underline")

    def toggle_tag(self, tag):
        if self.text_widget.tag_ranges(tk.SEL):
            current_tags = self.text_widget.tag_names("sel.first")
            if tag in current_tags:
                self.text_widget.tag_remove(tag, "sel.first", "sel.last")
            else:
                self.text_widget.tag_add(tag, "sel.first", "sel.last")
        else:
            current_tags = self.text_widget.tag_names("insert")
            if tag in current_tags:
                self.text_widget.tag_remove(tag, "insert", "insert+1c")
            else:
                self.text_widget.tag_add(tag, "insert", "insert+1c")

    def apply_color(self, color):
        color_tag = f"color_{color}"
        self.text_widget.tag_configure(color_tag, foreground=color)
        if self.text_widget.tag_ranges(tk.SEL):
            self.text_widget.tag_add(color_tag, "sel.first", "sel.last")
        else:
            self.text_widget.tag_add(color_tag, "insert", "insert+1c")

    def change_font_family(self, event):
        new_family = self.font_family_var.get()
        if self.text_widget.tag_ranges(tk.SEL):
            start, end = self.text_widget.tag_ranges(tk.SEL)
            self.text_widget.tag_remove("family_" + self.current_font_family, start, end)
            self.text_widget.tag_add("family_" + new_family, start, end)
        else:
            self.text_widget.tag_remove("family_" + self.current_font_family, "insert", "insert+1c")
            self.text_widget.tag_add("family_" + new_family, "insert", "insert+1c")
        self.current_font_family = new_family

    def change_font_size(self, event):
        new_size = int(self.font_size_var.get())
        if self.text_widget.tag_ranges(tk.SEL):
            start, end = self.text_widget.tag_ranges(tk.SEL)
            self.text_widget.tag_remove("size_" + str(self.current_font_size), start, end)
            self.text_widget.tag_add("size_" + str(new_size), start, end)
        else:
            self.text_widget.tag_remove("size_" + str(self.current_font_size), "insert", "insert+1c")
            self.text_widget.tag_add("size_" + str(new_size), "insert", "insert+1c")
        self.current_font_size = new_size

    def encode_formatted_text(self):
        encoded_content = []
        for index in range(1, int(self.text_widget.index(tk.END).split('.')[0])):
            line_start = f"{index}.0"
            line_end = f"{index}.end"
            line_text = self.text_widget.get(line_start, line_end)
            line_tags = {}
            for tag in self.text_widget.tag_names(line_start):
                if tag.startswith(("color_", "family_", "size_", "bold", "italic", "underline")):
                    line_tags[tag] = True
            # Keep only the last font family and size
            font_families = [tag for tag in line_tags if tag.startswith("family_")]
            font_sizes = [tag for tag in line_tags if tag.startswith("size_")]
            if font_families:
                line_tags = {tag: line_tags[tag] for tag in line_tags if not tag.startswith("family_") or tag == font_families[-1]}
            if font_sizes:
                line_tags = {tag: line_tags[tag] for tag in line_tags if not tag.startswith("size_") or tag == font_sizes[-1]}
            encoded_content.append({"text": line_text, "tags": line_tags})
        return encoded_content

    def decode_formatted_text(self, encoded_content):
        self.text_widget.delete("1.0", tk.END)
        for line in encoded_content:
            self.text_widget.insert(tk.END, line["text"] + "\n")
            line_start = self.text_widget.index(f"end-2c linestart")
            line_end = self.text_widget.index(f"end-1c")
            for tag, _ in line["tags"].items():
                if tag.startswith("color_"):
                    self.text_widget.tag_configure(tag, foreground=tag[6:])
                elif tag.startswith("family_"):
                    family = tag[7:]
                    self.text_widget.tag_configure(tag, font=(family, self.current_font_size))
                elif tag.startswith("size_"):
                    size = int(tag[5:])
                    self.text_widget.tag_configure(tag, font=(self.current_font_family, size))
                self.text_widget.tag_add(tag, line_start, line_end)

class HelpFileGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Help File Generator")
        self.master.geometry("1100x800")

        self.gui_elements = {
            "General": {
                "title": "",
                "description": ""
            },
            "MainWindow": {
                "elements": {}
            }
        }

        self.element_info = {}  # Store element name and type information
        self.current_element = None
        self.temp_data = {}  # Temporary storage for unsaved changes
        self.gui_framework = None  # Will hold detected framework name

        # Create and arrange widgets
        self.create_widgets()

        # Bind F1 key to show help
        self.master.bind_all('<F1>', show_help)

    def exit_application(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.master.destroy()

    def create_widgets(self):
        # Create main frame
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # File selection frame
        self.file_frame = ttk.Frame(self.main_frame)
        self.file_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(self.file_frame, text="Python file:").pack(side=tk.TOP, anchor=tk.W)
        self.file_entry = ttk.Entry(self.file_frame, width=50, name="file_entry")
        self.file_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        # Buttons
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Button(self.button_frame, text="Browse", name="browse_button", command=self.browse_file).pack(side=tk.LEFT)
        self.open_help_file_button = ttk.Button(self.button_frame, text="Open Help File", name="open_help_file_button",
                                                command=self.load_help_file, state=tk.DISABLED)
        self.open_help_file_button.pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Analyze", name="analyze_button", command=self.analyze_file).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Help", name="help_button", command=self.show_help_window).pack(side=tk.LEFT,
                                                                                                           padx=5)
        self.save_help_file_button = ttk.Button(self.button_frame, text="Save Help File", name="save_help_file_button",
                                                command=self.save_help_file, state=tk.DISABLED)
        self.save_help_file_button.pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Exit", name="exit_button", command=self.exit_application).pack(
            side=tk.RIGHT, padx=5)

        # Split view
        self.paned_window = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Element tree frame
        self.tree_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.tree_frame, weight=1)
        self.element_tree = ttk.Treeview(self.tree_frame, columns=("Type"), show="tree headings")
        self.element_tree.heading("Type", text="Type")
        self.element_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.element_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.element_tree.config(yscrollcommand=scrollbar.set)
        self.element_tree.bind("<<TreeviewSelect>>", self.on_element_select)

        # Help text frame
        self.text_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.text_frame, weight=2)
        ttk.Label(self.text_frame, text="Help Text:").pack(anchor=tk.W)
        self.help_text = FormattedTextEditor(self.text_frame)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)
            self.open_help_file_button.config(state=tk.NORMAL)  # Enable "Open Help File" button

    def analyze_file(self):
        file_path = self.file_entry.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a Python file.")
            return

        with open(file_path, 'r') as file:
            content = file.read()

        tree = ast.parse(content)
        self.gui_elements["MainWindow"]["elements"] = {}
        self.element_info = {}
        self.temp_data = {}

        self.detect_gui_framework(tree)
        if self.gui_framework:
            messagebox.showinfo("Framework Detected", f"Detected GUI framework: {self.gui_framework}")
        else:
            messagebox.showerror("Error", "No supported GUI framework detected.")
            return

        self.extract_gui_elements(tree)
        self.update_element_tree()
        self.save_help_file_button.config(state=tk.NORMAL)  # Enable the Save Help File button

    def detect_gui_framework(self, tree):
        for node in tree.body:
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    if alias.name in ['tkinter', 'Tkinter']:
                        self.gui_framework = 'Tkinter'
                    elif alias.name == 'PySimpleGUI':
                        self.gui_framework = 'PySimpleGUI'
                    elif alias.name.startswith('PyQt'):
                        self.gui_framework = 'PyQt'

    def extract_gui_elements(self, node):
        if isinstance(node, ast.Assign):
            if self.gui_framework == 'PyQt' and isinstance(node.value, ast.Call):
                element_name = node.targets[0].id  # Variable name
                element_type = node.value.func.attr  # Widget type (e.g., QPushButton)
                self.add_element(element_name, element_type)
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                element_type = node.func.attr
                element_name = self.get_element_name(node)
                if self.is_gui_element(element_type):
                    self.add_element(element_name, element_type)

        for child in ast.iter_child_nodes(node):
            self.extract_gui_elements(child)

    def get_element_name(self, node):
        if self.gui_framework == 'Tkinter':
            for kw in node.keywords:
                if kw.arg == 'name':
                    return ast.literal_eval(kw.value)
        elif self.gui_framework == 'PySimpleGUI':
            for kw in node.keywords:
                if kw.arg == 'key':
                    return ast.literal_eval(kw.value)
        return None

    def is_gui_element(self, element_type):
        gui_elements = ['Button', 'Label', 'Entry', 'Text', 'Listbox', 'Combobox', 'InputText', 'Combo', 'Multiline']
        return element_type in gui_elements

    def add_element(self, element_name, element_type):
        base_name = element_name
        counter = 1
        original_name = element_name

        # Ensure unique names
        while element_name in self.gui_elements["MainWindow"]["elements"]:
            element_name = f"{base_name}_{counter}"
            counter += 1

        if original_name not in self.element_info:
            self.gui_elements["MainWindow"]["elements"][element_name] = ""
            self.element_info[element_name] = element_type

    def update_element_tree(self):
        self.element_tree.delete(*self.element_tree.get_children())

        # Insert "General" section
        general_node = self.element_tree.insert("", "end", text="General", open=True)
        general = self.gui_elements.get("General", {})
        self.element_tree.insert(general_node, "end", text="Title", values=(general.get("title", "")))
        self.element_tree.insert(general_node, "end", text="Description", values=(general.get("description", "")))

        # Insert "MainWindow" elements
        main_window_node = self.element_tree.insert("", "end", text="MainWindow", open=True)
        main_window = self.gui_elements.get("MainWindow", {}).get("elements", {})
        for name, description in main_window.items():
            self.element_tree.insert(main_window_node, "end", text=f"{name} ({self.element_info.get(name, 'Unknown')})",
                                     values=(description))

    def update_element_tree(self):
        self.element_tree.delete(*self.element_tree.get_children())

        # Insert "General" section
        general_node = self.element_tree.insert("", "end", text="General", open=True)
        general = self.gui_elements.get("General", {})
        self.element_tree.insert(general_node, "end", text="Title", values=("",))
        self.element_tree.insert(general_node, "end", text="Description", values=("",))

        # Insert "MainWindow" elements
        main_window_node = self.element_tree.insert("", "end", text="MainWindow", open=True)
        main_window = self.gui_elements.get("MainWindow", {}).get("elements", {})
        for name, description in main_window.items():
            self.element_tree.insert(main_window_node, "end", text=f"{name} ({self.element_info.get(name, 'Unknown')})",
                                     values=("",))

    def on_element_select(self, event):
        self.save_current_element_to_temp()
        selected_item = self.element_tree.selection()
        if not selected_item:
            return

        selected_item = selected_item[0]
        parent = self.element_tree.parent(selected_item)
        if parent:
            section = self.element_tree.item(parent)['text']
            element_name = self.element_tree.item(selected_item)['text'].split('(')[0].strip()

            if section == "General":
                self.current_element = (section, element_name.lower())
                content = self.temp_data.get((section, element_name.lower()),
                                             self.gui_elements[section].get(element_name.lower(), []))
            else:
                self.current_element = (section, element_name.lower())
                content = self.temp_data.get((section, element_name.lower()),
                                             self.gui_elements[section]["elements"].get(element_name.lower(), []))

            self.help_text.text_widget.delete("1.0", tk.END)
            if isinstance(content, list):
                self.help_text.decode_formatted_text(content)
            elif isinstance(content, str):
                self.help_text.text_widget.insert(tk.END, content)
            else:
                messagebox.showwarning("Warning", "The content for this element seems to be corrupted.")

    def save_current_element_to_temp(self):
        if self.current_element:
            section, element_name = self.current_element
            content = self.help_text.encode_formatted_text()
            if section == "General":
                self.temp_data[(section, element_name)] = content
            else:
                self.temp_data[(section, element_name)] = content

    def show_help_window(self):
        help_text = "Press F1 while button is in focus to see detailed help."
        messagebox.showinfo("Help", help_text)

    def load_help_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Formatted Text Files", "*.ftxt")])
        if not file_path:
            return

        with open(file_path, "r") as file:
            content = json.load(file)

        self.gui_elements = {
            "General": {
                "title": content.get("General", {}).get("title", []),
                "description": content.get("General", {}).get("description", [])
            },
            "MainWindow": {
                "elements": content.get("MainWindow", {}).get("elements", {})
            }
        }

        # Convert string content to list format for compatibility
        for key, value in self.gui_elements["MainWindow"]["elements"].items():
            if isinstance(value, str):
                self.gui_elements["MainWindow"]["elements"][key] = [{"text": value, "tags": {}}]

        self.temp_data = {}  # Clear temp data
        self.update_element_tree()

    def save_help_file(self):
        self.save_current_element_to_temp()  # Save any unsaved changes

        file_path = filedialog.asksaveasfilename(defaultextension=".ftxt", filetypes=[("Formatted Text Files", "*.ftxt")])
        if not file_path:
            return

        content = {
            "General": {
                "title": self.temp_data.get(("General", "title"), self.gui_elements["General"]["title"]),
                "description": self.temp_data.get(("General", "description"), self.gui_elements["General"]["description"])
            },
            "MainWindow": {
                "elements": {}
            }
        }

        # Update content with temp_data
        for (section, element), data in self.temp_data.items():
            if section == "MainWindow":
                content["MainWindow"]["elements"][element] = data

        # Add any elements from gui_elements that are not in temp_data
        for element, data in self.gui_elements["MainWindow"]["elements"].items():
            if ("MainWindow", element) not in self.temp_data:
                content["MainWindow"]["elements"][element] = data

        with open(file_path, "w") as file:
            json.dump(content, file, indent=2)

        messagebox.showinfo("Success", "Help file saved successfully.")


if __name__ == "__main__":
    root = tk.Tk()
    s = ttk.Style()
    s.theme_use('classic')
    # help_file = "help_generator.ftxt"

    app = HelpFileGenerator(root)
    root.mainloop()
