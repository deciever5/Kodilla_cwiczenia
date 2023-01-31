def convert_to_roman(number):
    roman_numerals = {
        1000: 'M',
        900: 'CM',
        500: 'D',
        400: 'CD',
        100: 'C',
        90: 'XC',
        50: 'L',
        40: 'XL',
        10: 'X',
        9: 'IX',
        5: 'V',
        4: 'IV',
        1: 'I'
    }
    if not isinstance(number, int):
        raise ValueError("Input must be an integer.")
    if number < 1:
        raise ValueError("Number must be a positive integer")
    result = ""
    for value, roman in roman_numerals.items():
        while number >= value:
            result += roman
            number -= value
    return result