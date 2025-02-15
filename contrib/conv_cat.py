import collections
import csv
import re
#import collections

import sys
#print(csv.list_dialects(), file=sys.stderr)

debug = True

paths = collections.defaultdict(lambda: list())
hints = dict()

# a few special ones, those from the spec are added from table input
main_cats = set() # "Accessibility", "Screensavers", "WINE"}


def add_edges(key :str, multicand :list):
    global edges
    print(f"{key} -> {multicand}", file=sys.stderr)
    edges[key] |= set(multicand)


with open('Main_Categories.csv', newline='') as csvfile:
    rdr = csv.reader(csvfile, dialect='unix')
    for row in rdr:
        #print(row)
        assert(len(row) == 3)
        if " " in row[0]:  # the header
            continue
        main_cats.add(row[0].strip())
        hints[row[0]] = row[1]

if debug:
    print(f"main cats: {main_cats}", file=sys.stderr)

with open('Additional_Categories.csv', newline='') as csvfile:
    rdr = csv.reader(csvfile, dialect='unix')
    for row in rdr:
        #print(row)
        assert(len(row) == 3)
        if " " in row[0]:  # the header
            continue
        # we don't care about "based on foo library", that is not a real section
        if "Application based on" in row[1]:
            continue
        hints[row[0]] = row[1]
        for m in re.split(r'\s+or\s+', row[2]):
            m = m.strip()
            paths[row[0]].append(list(m.split(';')))

# let's fixup references which are not leading to some main category directly
resolved = False
while not resolved:
    resolved = True
    for k, v in paths.items():
        for w in v:
            cat = w[0]
            if not cat or cat in main_cats:
                continue
            if cat not in paths:
                print(f"Warning, cannot resolve {cat}", file=sys.stderr)
                continue
            for more in paths[cat]:
                w[:0] = more
                resolved = False

print(f"{paths}", file=sys.stderr)

groupedByLength = collections.defaultdict(lambda: list())
for k, v in paths.items():
    for l in v:
        groupedByLength[1+len(l)].append(l + [k])

groupedByLength[1] = list(map(lambda x: [x], main_cats))

print(f"{groupedByLength}", file=sys.stderr)

#keysByLen = list(reversed(sorted(paths.keys())))

print(f"""/**
 * WARNING: this file is autogenerated! Any change might be overwritten!
 *
 * Content is created using conv_cat.py with input from
 * https://specifications.freedesktop.org/menu-spec/latest/additional-category-registry.html
 * (i.e. the table transformed with LibreOffice to CSV format).
 */ 

#ifndef FDO_GEN_MENU_STRUCTURE_H
#define FDO_GEN_MENU_STRUCTURE_H

#include <initializer_list>

using t_menu_path = std::initializer_list<const char*>;
using t_menu_path_table = std::initializer_list<t_menu_path>;
using t_menu_path_table_list = std::initializer_list<t_menu_path_table>;

constexpr t_menu_path_table_list valid_paths = {{""")

for k in reversed(sorted(groupedByLength.keys())):
    print(f"\n\t// menu locations of depth {k}\n\t{{")
    ways = groupedByLength[k]
    for v in sorted(ways, key=lambda x: x[-1]):
        print("\t\t{")
        for t in reversed(v):
            print("// TRANSLATORS: This is a SHORT category menu name from freedesktop.org. Please add compact punctuation if needed but no double-quotes! Hint for the content inside: " + hints.get(t, t))
            if t:
                print("\t\t\tN_(\"" + t + "\"),")
            else:
                print("\t\t\t\"" + t + "\",")
        print("\t\t},")
    print("\t},")

print(f"""}};

#endif // FDO_GEN_MENU_STRUCTURE_H""")
