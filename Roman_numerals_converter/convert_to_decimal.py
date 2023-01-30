def convert_to_decimal(number):
    roman_numerals = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000}
    if isinstance(number, str):
        decimal_value = 0
        for i in range(len(number)):
            if i > 0 and roman_numerals[number[i]] > roman_numerals[number[i - 1]]:
                decimal_value += roman_numerals[number[i]] - 2 * roman_numerals[number[i - 1]]
            else:
                decimal_value += roman_numerals[number[i]]
        return decimal_value
    else:
        raise ValueError
