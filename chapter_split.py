import re
chapter_pattern = re.compile(r"\*\*[0-9]+\*\*")
for i in range(1, 29):
    with open(f"book_{i}.txt", "r") as f:
        text = f.read()
        chapters = chapter_pattern.split(text)
        for j, chapter in enumerate(chapters):
            with open(f"book_{i}_chapter_{j}.txt", "w") as f:
                f.write(chapter)


