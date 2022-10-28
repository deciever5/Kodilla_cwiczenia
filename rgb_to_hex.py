def rgb(r, g, b):
    r = round(r)
    g = round(g)
    b = round(b)
    if r < 0: r = 0
    if r > 255: r = 255
    if g < 0: g = 0
    if g > 255: g = 255
    if b < 0: b = 0
    if b > 255: b = 255
    string = f'{hex(r)[2::].zfill(2)}{hex(g)[2::].zfill(2)}{hex(b)[2::].zfill(2)}'
    print(string.upper())
    return string.upper()


rgb(148, -50, 211.1)
