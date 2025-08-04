import sys
import argparse

def process(input_files, output_file):
    print("This function is not implemented in this context. Please implement the processing logic.")

def runGUI(): 
    print("This function is not implemented in this context. Please implement the GUI logic.")

def print_help():
    help_text = """
Usage:
  script.py input1 [input2 ...] -o output_file

Description:
  - Provide one or more input files followed by -o and exactly one output file.
  - If run with no arguments, a GUI will launch for file selection.
  - Use -h for help, -v for version.

Examples:
  script.py data1.xlsm data2.xlsm -o result.xlsm
"""
    print(help_text.strip())

def main():
    parser = argparse.ArgumentParser(
        description="Process Excel files and write to an output file.",
        usage="%(prog)s input1 [input2 ...] -o output"
    )
    parser.add_argument(
        'input_files',
        nargs='*',
        help='Input Excel files'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file',
        required=False
    )
    parser.add_argument(
        '-v', '--version',
        action='store_true',
        help='Show version and exit'
    )

    args = parser.parse_args()

    if args.version:
        print(f"Version: {0}")
        sys.exit(0)

    if not args.input_files and not args.output:
        runGUI()
        return

    # Valid if and only if: input files given AND exactly one output
    if args.input_files and args.output:
        process(args.input_files, args.output)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()