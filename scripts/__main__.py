import sys
import os
from scripts.cleaner import main

if __name__ == "__main__":
    assert (
        len(sys.argv) == 4
    ), "PLEASE INCLUDE: PATH TO FILE DIRECTORY, FILENAME, and SOURCE (QUALTRICS/SURVEY MONEKY)"

    # Grab cleaned file
    fullpath, filename, source = sys.argv[1:4]
    rec = main(fullpath, filename, source)

    # Export file
    ext = filename.split(".")[-1]
    ext = "." + ext
    new_filename = filename.split(ext)[0] + "_cleaned" + ".xlsx"

    rec.to_excel(os.path.join(fullpath, new_filename), index=False)
    print("FILE SAVED TO:", os.path.join(fullpath, new_filename))
