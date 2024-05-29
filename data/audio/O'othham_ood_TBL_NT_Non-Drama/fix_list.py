def clean_listtxt(filename="list.txt"):
    """Cleans a 'list.txt' file for FFmpeg, replacing non-standard spaces.

    Args:
        filename: The name of the 'list.txt' file to process.
    """

    with open(filename, 'r') as infile, open('new_' + filename, 'w') as outfile:
        for line in infile:
            cleaned_line = line.replace('\u00a0', ' ')  # Replace non-breaking space
            outfile.write("file '" + cleaned_line.strip() + "'\n")

if __name__ == "__main__":
    clean_listtxt()  # Will process the 'list.txt' file

