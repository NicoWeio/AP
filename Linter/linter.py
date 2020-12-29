#!/usr/bin/env python3

import argparse
import itertools
import json
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
                'importance': rule['importance'],
                'line_index': line_index,
                # 'char_index_in_line': match.start(),
                })

    return results

def group_warnings(lst):
    keyfunc = lambda d: d['message']
    return itertools.groupby(sorted(lst, key=keyfunc), key=keyfunc)

def group_lines(lst):
    # lst has to be filtered by message for correct output!
    lst = list(lst)
    startLine = None
    result = []
    for i, item in enumerate(lst):
        currentLine = item['line_index']
        nextLine = lst[i+1]['line_index'] if (i < len(lst) - 1) else None
        if (currentLine + 1 == nextLine):
            # print("MULTI", currentLine)
            if not startLine:
                startLine = currentLine
        elif startLine:
            # print("MULTI_END", currentLine)
            item['line_index'] = (startLine, currentLine)
            result.append(item)
            startLine = None
        else:
            # print("SINGLE", currentLine, nextLine)
            item['line_index'] = (currentLine, currentLine)
            result.append(item)
    return result

def output_json():
    allResults = []
    for path in files_to_lint():
        with open(path, 'r') as f:
            text = f.read()
            lines = text.split('\n')

            def get_annotation_level(importance):
                # if importance > 8:
                #     return 'failure'
                if importance > 4:
                    return 'warning'
                return 'notice'

            def resultify(w):
                return {
                    'file': str(path),
                    'start_line': w['line_index'][0] + 1, # index shift from 0 to 1
                    'end_line': w['line_index'][1] + 1, # index shift from 0 to 1
                    # 'title': 'Lint',
                    'message': w['message'],
                    'annotation_level': get_annotation_level(w['importance'])
                }

            # [warning]
            raw_result = lint(lines)
            # [(message, [warning])]
            grouped_result = group_warnings(raw_result)
            # [warning]
            line_grouped_result = []
            for message, items in grouped_result:
                line_grouped_result += group_lines(items)

            results = [resultify(warning) for warning in line_grouped_result]
            allResults += results

    allResultsJson = json.dumps(allResults, indent=4)
    print(allResultsJson)

def output_human_readable():
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


parser = argparse.ArgumentParser()
parser.add_argument('-c', "--ignore-comments", help="ignore lines starting with a percent sign (including preceding whitespace)", action="store_true")
parser.add_argument('-l', "--show-lines", help="show lines producing warnings", action="store_true")
parser.add_argument("--json", help="export as JSON", action="store_true")
args = parser.parse_args()


if args.json:
    output_json()
else:
    output_human_readable()
