#!/usr/bin/env python3

import argparse
import itertools
from pathlib import Path
import re
from rules import rules

class Colors:
    CONTENT = '\033[94m'
    PATH = '\033[93m'
    MESSAGE = '\033[91m'
    ENDC = '\033[0m'

def files_to_lint():
    return list(Path(".").glob("**/*.tex"))

def line_number(newline_indices, index):
    for line_i, char_i in enumerate(newline_indices):
        if (index <= char_i): return line_i
    return None

def lint(lines):

    results = []

    for rule in rules:
        # ruleRE = compile…
        for line_index, line in enumerate(lines):
            for match in re.finditer(rule['regex'], line, re.IGNORECASE):
                results.append({
                'message': rule['message'],
                'line_index': line_index,
                # 'char_index_in_line': match.start(),
                })

    return results

def group_warnings(lst):
    # keyfunc = lambda d: next(iter(d.values()))
    keyfunc = lambda d: d['message']
    return itertools.groupby(sorted(lst, key=keyfunc), key=keyfunc)
    # return {k: [x for d in g for x in d] for k, g in itertools.groupby(sorted(lst, key=keyfunc), key=keyfunc)}

parser = argparse.ArgumentParser()
parser.add_argument('-c', "--ignore-comments", help="ignore lines starting with a percent sign (including preceding whitespace)", action="store_true")
parser.add_argument('-l', "--show-lines", help="show lines producing warnings", action="store_true")
args = parser.parse_args()

summary_chars = 0
summary_lines = 0
summary_lines_with_error = 0

for path in files_to_lint():
    with open(path, 'r') as f:
        text = f.read()
        lines = text.split('\n')

        summary_chars += len(text)
        summary_lines += len(lines)

        results = lint(lines)

        if args.ignore_comments:
            results = [r for r in results if not lines[r['line_index']].strip().startswith('%')]

        if results:
            total_unique_lines = len(set([r['line_index'] for r in results]))
            summary_lines_with_error += total_unique_lines
            print(f"{Colors.PATH}*** {path}: {len(results)} Warnung(en) in {total_unique_lines} Zeile(n){Colors.ENDC}")
            # print(colored(f"*** {path}: {len(results)} warnings", 'yellow'))
            grouped = group_warnings(results)
            for message, items in grouped:
                print(Colors.MESSAGE + message + Colors.ENDC)
                unique_lines = sorted(set([i['line_index'] for i in items]))
                if args.show_lines:
                    for i_l, l in enumerate(unique_lines):
                        # if not first line and previous line index isn't one before current line index
                        if (i_l != 0 and unique_lines[i_l-1] != l-1):
                            print('–')
                        # lines are zero-indexed, but the user expects them to be one-indexed
                        print(l+1, Colors.CONTENT + lines[l].strip() + Colors.ENDC)
                else:
                    print("Z. " + ','.join([str(l+1) for l in unique_lines]))


print('\n')
print(f"Insgesamt {summary_lines} Zeile(n), davon {summary_lines_with_error} mit Warnungen")
print(f"→ {(100*summary_lines_with_error/summary_lines):.2f}%")
