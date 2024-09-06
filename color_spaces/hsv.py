# HSV color space


def HSV_COLOR(h, s, v):
    # Given values are in range [0, 360], [0, 100], [0, 100], return HEX color in RGB
    # Convert HSV to RGB
    h /= 360
    s /= 100
    v /= 100

    if s == 0:
        r = g = b = v
    else:
        h *= 6
        if h == 6:
            h = 0

        i = int(h)
        p = v * (1 - s)
        q = v * (1 - s * (h - i))
        t = v * (1 - s * (1 - (h - i)))

        if i == 0:
            r, g, b = v, t, p
        elif i == 1:
            r, g, b = q, v, p
        elif i == 2:
            r, g, b = p, v, t
        elif i == 3:
            r, g, b = p, q, v
        elif i == 4:
            r, g, b = t, p, v
        else:
            r, g, b = v, p, q

    return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"
