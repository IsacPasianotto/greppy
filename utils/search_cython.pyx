# cython: language_level=3

cdef bint boyer_moore_horspool_cy(str line, str pattern):
    cdef int line_len = len(line)
    cdef int pattern_len = len(pattern)
    cdef int i, j, k, skip
    cdef dict skip_table = {}

    if pattern_len == 0:
        return True

    if pattern_len > line_len:
        return False

    # Costruisci la tabella di salto per i caratteri "cattivi"
    for i in range(pattern_len - 1):
        skip_table[pattern[i]] = pattern_len - 1 - i

    # Ricerca effettiva
    i = pattern_len - 1
    while i < line_len:
        j = pattern_len - 1
        k = i

        # Confronta dal fondo
        while j >= 0 and line[k] == pattern[j]:
            j -= 1
            k -= 1

        if j < 0:
            return True

        # Calcola il salto
        skip = skip_table.get(line[k], pattern_len)
        i += skip

    return False

def is_pattern_in_line_cy(str line, str pattern, bint ignore_case=False):
    cdef str line_processed, pattern_processed

    if ignore_case:
        line_processed = line.lower()
        pattern_processed = pattern.lower()
    else:
        line_processed = line
        pattern_processed = pattern

    return boyer_moore_horspool_cy(line_processed, pattern_processed)
