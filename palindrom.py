def palindrome_check(x):
    return True if x[::] == x[::-1] else False


word = input("Podaj słowo do sprawdzenia: ")
print(f'Słowo {word} to{[" nie ", " "][palindrome_check(word)]}palindrom')
