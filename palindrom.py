def palindrome_check(x):
    if x[::] == x[::-1]:
        return True


word = input()
print(f'Słowo {word} to {not palindrome_check(word) * "nie"} palindrom')
"""if palindrome_check(word) is True:
    print(f'słowo {word} to palindrom')
else:
    print(f'słowo {word} to nie palindrom')"""
