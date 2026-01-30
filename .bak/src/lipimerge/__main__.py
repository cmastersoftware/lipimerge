"""
lipimerge - A Python application that merges multiple LipidQuant Excel files and generates a combined output file.  

See the README for more details on how to use this script.

Usage:
    1) lipimerge
    2) lipimerge input1 [input2 ...] {-o | --output} output
    3) lipimerge {-d | --directory} directory [{-o | --output} output]
    4) lipimerge -v | --version
    5) lipimerge -h | --help
    
Description:
    1) If run with no arguments, a GUI will launch for file selection.
    2) If input files are provided, they will be processed and merged into the output file.
    3) If a directory is specified, all files in that directory will be processed.
       - If an output file is specified, its path is relative to the directory.
       - If no output file is specified, it defaults to './lipimerge.xlsx'.
    4) Use -v or --version to display the version of the script.
    5) Use -h or --help to display this help message.

Examples:
    py -m lipimerge data1.xlsm data2.xlsm -o result.xlsm

Note:
    Use run.bat from the root directory to run this script in a Windows environment.
    The run.bat file passes its arguments to this script as is, i.e.,
    use the same syntax as shown in the Usage section, only replacing
    "lipimerge" with "run.bat" in the command line.
"""

import sys
import os
import argparse
import lipimerge
import lipimerge.internal.console as console
import lipimerge.internal.exceptions as lipiex

def main():

    # Parse arguments
    
    # Use the unmodified docstring as the help message
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument(
        '-h', '--help',
        action='store_true',
        help='Show help message'
    )

    parser.add_argument(
        '-v', '--version',
        action='store_true',
        help='Show version information'
    )

    parser.add_argument(
        'input_files',
        nargs='*',
        help='Input Excel files'
    )

    parser.add_argument(
        '-o', '--output',
        dest='output_file',
        help='Output file',
    )

    parser.add_argument(
        '-d', '--directory',
        dest='directory',
        help='Directory',
    )

    args = parser.parse_args()

    # Validate the arguments

    def validate_args(args):
        if len(sys.argv) == 1:
            return True
        if args.help and len(sys.argv) != 2:
            return False
        if args.version and len(sys.argv) != 2:
            return False
        if args.input_files and args.directory:
            return False
        if args.input_files and not args.output_file:
            return False
        
        return True
    
    if not validate_args(args):
        raise lipiex.InvalidArguments()

    # Run

    if args.help:
        return lipiex.Success("Help", __doc__.splitlines())

    if args.version:
        return lipiex.Success(f"Version: {__package__}", [lipimerge.__version__])

    if len(sys.argv) == 1:
        args.input_files, args.output_file = lipimerge.runGUI()

    if args.directory:
        args.input_files = [os.path.join(args.directory, f) for f in os.listdir(args.directory) if os.path.isfile(os.path.join(args.directory, f))]
        if not args.output_file: args.output_file = os.path.join('lipimerge.xlsx')
        args.output_file = os.path.join(args.directory, args.output_file)

    return lipimerge.process(args.input_files, args.output_file)
    

if __name__ == "__main__":
    
    result = None

    try:
        result = main()
    except lipiex.LipimergeException as e:
        result = e
    except Exception as e:
        result = lipiex.ExternalError(e)

    console.print()
    if result.errcode == 0:
        console.print(f"[green]Done: {result}[/]")
    else:
        console.print(f"[red]Error: {result}[/]")

    console.print("----------------------------------------")
    console.print("Details:")
    for line in result.details:
        console.print(line)
    console.print("========================================")

    sys.exit(result.errcode)
