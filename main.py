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

try:
    from utils.search_cython import is_pattern_in_line_cy
    CYTHON_AVAILABLE = True
    static_logger.info("✓ Cython module loaded successfully. Using C-compiled functions")
except ImportError as e:
    static_logger.warning("✗ Cython module not available. Using pure Python implementation.")
    static_logger.warning("Compile first with: python utils/compile.py build_ext --inplace")
    CYTHON_AVAILABLE = False

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
    """
    Pure Python implementation of Boyer-Moore-Horspool algorithm
    (fallback when Cython is not available)
    """
    if ignore_case:
        line = line.lower()
        pattern = pattern.lower()

    # Boyer-Moore-Horspool
    line_len: int = len(line)
    pattern_len: int = len(pattern)

    if pattern_len == 0:
        return True

    if pattern_len > line_len:
        return False

    # jump table for bad character
    skip_table: dict[str, int] = {}
    for i in range(pattern_len - 1):
        skip_table[pattern[i]] = pattern_len - 1 - i

    # Actual search
    i: int = pattern_len - 1
    while i < line_len:
        j: int = pattern_len - 1
        k: int = i

        # Confronta dal fondo
        while j >= 0 and line[k] == pattern[j]:
            j -= 1
            k -= 1

        if j < 0:
            return True

        # Calcola il salto
        skip: int = skip_table.get(line[k], pattern_len)
        i += skip

    return False


def match_patterns_in_lines(
        lines: list[str],
        patterns: list[str],
        ignore_case: bool = False
    ) -> dict[str, dict[str, int | list[int]]]:

    results: dict[str, dict[str, int | list[int]]] = {
        pattern: {"occurrences": [], "counter": 0} for pattern in patterns
    }

    # Choose the best available pattern matching function
    pattern_func = is_pattern_in_line_cy if CYTHON_AVAILABLE else is_pattern_in_line

    for i, line in enumerate(lines, start=1):
        for pattern in patterns:
            if pattern_func(line=line, pattern=pattern, ignore_case=ignore_case):
                results[pattern]["occurrences"].append(i)
                results[pattern]["counter"] = len(results[pattern]["occurrences"])
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

    # Log which implementation is being used
    if CYTHON_AVAILABLE:
        logger.info("Using Cython optimized pattern matching")
    else:
        logger.info("Using Python fallback pattern matching")

    results = match_patterns_in_lines(lines, args.patterns, ignore_case=args.ignore_case)

    for pattern in args.patterns:
        pattern_data = results[pattern]
        if pattern_data["occurrences"]:
            logger.info(f"Pattern '{pattern}' found {pattern_data['counter']} times in the file at lines: {pattern_data['occurrences']}")
        else:
            logger.info(f"Pattern '{pattern}' not found in the file.")


if __name__ == "__main__":
    main()
