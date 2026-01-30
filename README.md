# Lipimerge

A Python application that merges multiple LipidQuant Excel files and generates a combined output file.  

The merge algorithm preserves all records for every lipid class found in any of the input files.
If a particular lipid class is missing in some files, the algorithm inserts empty columns in their place
to maintain a consistent structure across the merged output.

Basic sanity check is provided that there are no missing data in a column or 
a row in an input file; **completely** empty columns or rows are allowed and removed
from the final merge.

Supports both command-line and graphical user interface (GUI) usage.

    If the same lipid class is present in both `source` and `destination`,
    the data from `source` are placed into the correct column in `destination`
    according to the class name (class names are looked up in the first row).

    If a lipid class is present only in `destination` but is not present in `source`,
    empty cells are placed into the `destination`.

    If a lipid class is present only in `source` but is not present in `destination`,
    a new column is appended to the data in `destination` with empty cells for old
    records (rows) and 
    
## 🚀 Features

- Accepts multiple `.xls`, `.xlsx`, or `.xlsm` files as input
- Requires one output file (`-o output.xlsm`)
- Launches a GUI if run without arguments
- Remembers last used directory across sessions
- Drag and drop support for input files in the GUI

## 🛠️ Usage

### Initialization

Run `setup.bat` on Windows or `setup.sh` on Linux. This:
- Creates python virtual environment (`.venv`)
- Installs dependencies

### Command Line

```bash
python lipimerge.py input1.xlsm input2.xlsm -o output.xlsm
```

### GUI Mode

Simply run:

```bash
python lipimerge.py
```

Then use the GUI to select input and output files.

### Help & Version

```bash
python lipimerge.py -h      # show help
python lipimerge.py -v      # show version
```

## 📦 Non-Standard Dependencies

See `requirements.txt`

## 🤖 AI Assistance

Much of the development work for this project was supported by [ChatGPT](https://chatgpt.com/) and [GitHub Copilot](https://github.com/features/copilot).

From design decisions to implementation and testing, these tools played a key role in boosting productivity and code quality.
