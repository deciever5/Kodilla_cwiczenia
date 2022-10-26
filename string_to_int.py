def parse_int(string):
    conversions = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
                   "ten": 10, "eleven":11,"twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16,
                   "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40,
                   "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90, "hundred": 100,
                   "thousand": 1000, "milion": 1000000}
    result, last_digits = 0, 0

    for i, word in enumerate(string.split(" ")):
        if "-" in word:
            no_dash = word.split("-")
            result += (conversions.get(no_dash[0]) + conversions.get(no_dash[1]))
            last_digits = (conversions.get(no_dash[0]) + conversions.get(no_dash[1]))
        elif "hundred" == word:
            result += last_digits * 99
        elif "thousand" == word:
            result += result * 999
        elif "million" == word:
            if "thousand" in string.split(" "):
                result += result * 999
            else:
                result += result * 999999
        elif "and" == word:
            pass
        else:
            try:
                result += conversions.get(word)
                last_digits = conversions.get(word)
            except TypeError:
                print (f"Could not convert {word}")
    return result


parse_int("seventy-seven million two hundred forty-six thousand seven hundred and eighty one")
