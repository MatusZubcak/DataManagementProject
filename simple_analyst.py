#! /usr/bin/python3
from collections import Counter, OrderedDict

def load(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        nonempty_lines = [line.strip() for line in lines if line.strip() and ".2024" not in line]

        return nonempty_lines


filename = "horoscopes.txt"
horoscopes = load(filename)
counts = Counter(horoscopes).most_common()
occurrences = []
for (item, count) in counts:
    occurrences.append(count)

occurrences_counter = Counter(occurrences).most_common()

print("number of horoscopes: " + str(len(horoscopes)))

for (count, occurrence) in occurrences_counter:
    print(str(count) + " " + str(occurrence))
