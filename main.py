"""A simple script to find patterns in a text in a given file."""
#
# Imports
#

import os
import sys
from utils.parser import setup_parser
from utils.logger import setup_logger, static_logger
from logging import Logger
from argparse import ArgumentParser


#
# Methods
#


def read_file(
        file_path: str,
        logger: Logger = static_logger
    ) -> list[str]:

    lg: Logger = logger if logger else static_logger
    if file_path is None:
        raise ValueError("File path cannot be None.")

    if not os.path.exists(file_path):
        raise ValueError(f"File '{file_path}' does not exist.")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.readlines()
    except UnicodeDecodeError:
        lg.error(f"File '{file_path}' is not a valid UTF-8 text file.")


def is_pattern_in_line(
        line: str,
        pattern: str,
        ignore_case: bool = False
    ) -> bool:

    if ignore_case:
        line = line.lower()
        pattern = pattern.lower()

    # Naive pattern matching algorithm
    for i in range(len(line) - len(pattern) + 1):
        match = True
        for j in range(len(pattern)):
            if line[i + j] != pattern[j]:
                match = False
                break
        if match:
            return True
    return False

def match_patterns_in_lines(
        lines: list[str],
        patterns: list[str],
        ignore_case: bool = False
    ) -> dict[str, list[int]]:

    results: dict[str, list[int]] = {pattern: [] for pattern in patterns}
    for i, line in enumerate(lines, start=1):
        for pattern in patterns:
            if is_pattern_in_line(line=line, pattern=pattern, ignore_case=ignore_case):
                results[pattern].append(i)
    return results

#
# Main function
#


def main() -> None:
    parser: ArgumentParser = setup_parser() ; args = parser.parse_args()
    logger: Logger = setup_logger(level="INFO")
    lines: list[str] = []

    try:
        lines = read_file(args.file, logger)
    except ValueError as e:
        logger.error(str(e))
        sys.exit(1)

    results = match_patterns_in_lines(lines, args.patterns, ignore_case=args.ignore_case)

    for pattern in args.patterns:
        lines_found = results[pattern]
        if lines_found:
            logger.info(f"Pattern '{pattern}' found in lines: {lines_found}")
        else:
            logger.info(f"Pattern '{pattern}' not found in the file.")


if __name__ == "__main__":
    main()
