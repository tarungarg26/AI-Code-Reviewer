def compare_code(code1, code2):

    code1 = code1 or ""
    code2 = code2 or ""

    chars1 = len(code1)
    chars2 = len(code2)

    lines1 = len(code1.splitlines())
    lines2 = len(code2.splitlines())

    words1 = len(code1.split())
    words2 = len(code2.split())

    char_difference = chars2 - chars1
    line_difference = lines2 - lines1

    if chars1 > 0:
        char_change_percent = ((chars2 - chars1) / chars1) * 100
    else:
        char_change_percent = 0.0

    return {
        "version_1": {
            "characters": chars1,
            "lines": lines1,
            "words": words1
        },
        "version_2": {
            "characters": chars2,
            "lines": lines2,
            "words": words2
        },
        "difference": {
            "characters": char_difference,
            "lines": line_difference,
            "words": words2 - words1
        },
        "character_change_percent": round(char_change_percent, 2)
    }