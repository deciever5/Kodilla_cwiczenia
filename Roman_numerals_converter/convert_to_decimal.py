def convert_to_decimal(number):
    roman_numerals = {'X': 10}
    if isinstance(number,str):
        print(isinstance(number,str))
        return roman_numerals[number]
    else:
        raise ValueError

