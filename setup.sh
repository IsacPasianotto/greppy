#!/bin/bash

# OUT_FILE="frankenstein.txt"
# IN_URL="https://www.gutenberg.org/cache/epub/84/pg84.txt"
OUT_FILE="divina_commedia.txt"
IN_URL="https://www.gutenberg.org/cache/epub/1000/pg1000.txt"


if command -v curl &> /dev/null; then
    curl -o "$OUT_FILE" "$IN_URL"
elif command -v wget &> /dev/null; then
    wget -O "$OUT_FILE" "$IN_URL"
else
    echo "Neither curl nor wget is installed. Please install one of them to proceed."
    exit 1
fi

if ! command -v awk &> /dev/null; then
    echo "awk is not installed. Please install awk to use this script."
    exit 1
fi

if ! command -v sponge &> /dev/null; then
    echo "sponge is not installed. Please install moreutils to use sponge."
    exit 1
fi

awk '{printf "%d. %s\n", NR, $0}' "$OUT_FILE" | sponge "$OUT_FILE"
