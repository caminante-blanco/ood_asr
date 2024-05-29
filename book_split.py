import os
import sys

file_path = sys.argv[1]
delimiter = sys.argv[2]

with open(file_path, 'r') as f:
    text = f.read()

books = text.split(delimiter)

for i, book in enumerate(books):
    with open(f'book_{i}.txt', 'w') as f:
        f.write(book)

