# Help File Generator

## Overview

The Help File Generator is a powerful tool designed to create and manage help documentation for GUI applications. It allows developers to easily add, edit, and format help content for various UI elements, streamlining the process of creating user documentation. This application will help to provide contextual help for your GUI based Python applications.

## Features

- **GUI Element Analysis**: Automatically extracts GUI elements from Python source files.
- **Rich Text Editing**: Provides a user-friendly interface for formatting help content.
- **Contextual Help**: Supports F1 key functionality for instant help on focused elements.
- **Multiple GUI Framework Support**: Compatible with Tkinter, PySimpleGUI, and PyQt.
- **Formatted Text File (.ftxt) Support**: Saves and loads help content in a custom JSON-based format.

## Installation

1. Clone the repository
   <p>git clone https://github.com/shuvrobasu/help-file-generator.git

2.  Navigate to the project directory:
      <p>cd help-file-generator

3. Install required dependencies
   <p>NONE REQUIRED. USES TKINTER which should be installed by default for all Python installs. Tested with <ins>3.10.0</ins> on Windows 11.0

## Usage

1. Run the Help File Generator:

python helpfilegenerator.py

2. Use the "Browse" button to select a Python file containing GUI elements.
3. Click "Analyze" to extract GUI elements from the selected file.
4. Select an element from the tree view to edit its help content.
5. Use the rich text editor to format the help content as desired.
6. Click "Save Help File" to save the help content to a .ftxt file.
7. <ins>See Examples folder for TK, PySimpleGUI and PyQt scripts and usage</ins>

## File Structure

- `helpfilegenerator.py`: Main application file
- `contextualhelp.py`: Contains the ContextualHelp class for managing help content
- `helpfilegenerator_help.ftxt`: <i><b>Sample help file for the Help File Generator created with this app !</b></i>

## .ftxt File Format

The Help File Generator uses a custom .ftxt file format based on JSON. This format allows for rich text formatting and easy parsing. Here's a basic structure:

```json
{
"General": {
 "title": [{"text": "App Title", "tags": {...}}],
 "description": [{"text": "App Description", "tags": {...}}]
},
"MainWindow": {
 "elements": {
   "element_name": [
     {"text": "Element Title", "tags": {...}},
     {"text": "Element Description", "tags": {...}}
   ]
 }
}
}
````
## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Support
If you encounter any problems or have any questions, please open an issue on the GitHub repository.
