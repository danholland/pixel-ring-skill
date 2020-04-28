Colours = {
    'black': 0x0,
    'red': 0xff0000,
    'green': 0x00ff00,
    'yellow': 0xffff00,
    'light_blue': 0x5db3ce,
    'blue': 0x0000ff,
    'aquamarine': 0x5fbebe,
    'purple': 0x985fbe
}


def interpolate(start, end, steps=6):
    s = []
    f = []
    s.append((start & 0xFF0000) >> 16)
    s.append((start & 0x00FF00) >> 8)
    s.append((start & 0x0000FF))
    f.append((end & 0xFF0000) >> 16)
    f.append((end & 0x00FF00) >> 8)
    f.append((end & 0x0000FF))
    arr_result = []
    for i in range(steps):
        curr_vector = [
            int(s[j] + (float(i)/(steps-1))*(f[j]-s[j]))
            for j in range(3)
        ]
        res = "0x"+"".join(["0{0:x}".format(v) if v < 16 else
                            "{0:x}".format(v) for v in curr_vector])
        arr_result.append(int(res, 16))
    return arr_result
