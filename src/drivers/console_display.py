import framebuf


# index is binary representation of upper pixel + lower pixel
UTFBLKS = (
    " ",          # 0b00 or 0: space
    chr(0x2584),  # 0b01 or 1: lower-half
    chr(0x2580),  # 0b10 or 2: upper-half
    chr(0x2588)	  # 0b11 or 3: full block
)
UTFBORDER = chr(0x2593) # shade


def hpixels_1x2(top, bottom, lsb=True):
    """
    receives top and bottom byte for 8 1x2 pixel couples,
    returns joined string of block elements to represent 8x2 pixel tile

    top and bottom are both bitwise-anded with 2**i to select bit[i].
    those powers of 2 are fed to int(bool()) resulting in 0 or 1 for each.
    top is left shifted 1 bit then bitwise-ored with bottom for an intval (0-3)
    to be used indexing UTFBLKS.
    """
    bits = range(8)
    if lsb:
        bits = reversed(bits)

    return ''.join(
        (UTFBLKS[int(bool(top & 2**i)) << 1 | int(bool(bottom & 2**i))]
            for i in bits
        )
    )


def vpixels_1x2(vpix_bytes):
    """
    receives bytes of 8 vertical pixels side-by-side,
    returns 4tuple of UTFBLKS indices of 1x2 pixels from left to right

    each byte is bitwise-anded with 2**i to select bit[i] for all 8 bits.
    those powers of 2 are fed to int(bool()) resulting in 0 or 1 for each.
    the odd bits are left shifted 1 then ored with the adjacent even bit
    for an intval (0-3) to be used by caller for indexing UTFBLKS.
    """
    bits = range(0,8,2)

    return tuple([
        [row[j] for row in [
            [int(bool(x & 2**i)) << 1 | int(bool(x & 2**(i+1))) for i in bits]
                for x in vpix_bytes
        ]] for j in range(4)
    ])


def mono_vlsb(buf, w, h, invert=False, footnote=""):
    '''
    interprets buf as a MONO_VLSB frame buffer, 
    uses unicode block-element characters to display 4 possible 1x2 pixel couples,
    8 pixel rows at a time -- 2 per line, from left to right and down.
    '''

    buf = bytearray(buf)
    assert len(buf) == w // 8 * h
    assert h % 8 == 0

    if invert:
        buf = bytearray([x ^ 255 for x in buf])

    print(UTFBORDER * (w + 4))
    for i in range(0, len(buf), w):
        for line in vpixels_1x2(buf[i:i+w]):
            print('{}{}{}'.format(
                UTFBORDER * 2,
                ''.join([UTFBLKS[x] for x in line]),
                UTFBORDER * 2
            ))
    print(UTFBORDER * (2 + w - len(footnote)) + footnote + UTFBORDER * 2)


def mono_hlsb(buf, w, h, invert=False, footnote=""):
    '''
    interprets buf as a MONO_HLSB frame buffer, 
    uses unicode block-element characters to display 4 possible 1x2 pixel couples,
    two pixel rows per line, from left to right and down.
    '''
    buf = bytearray(buf)
    assert len(buf) == w // 8 * h
    assert h % 2 == 0

    if invert:
        buf = bytearray([x ^ 255 for x in buf])

    print(UTFBORDER * (w + 4))
    for i in range(0, len(buf), w//8*2):
        print("{}{}{}".format(
            UTFBORDER * 2,
            ''.join((hpixels_1x2(buf[x], buf[x+w//8]) for x in range(i, i+w//8))),
            UTFBORDER * 2
        ))
    print(UTFBORDER * (2 + w - len(footnote)) + footnote + UTFBORDER * 2)


def mono_hmsb(buf, w, h, invert=False, footnote=""):
    '''
    interprets buf as a MONO_HMSB frame buffer, 
    uses unicode block-element characters to display 4 possible 1x2 pixel couples,
    two pixel rows per line, from left to right and down.
    '''
    buf = bytearray(buf)
    assert len(buf) == w // 8 * h
    assert h % 2 == 0

    if invert:
        buf = bytearray([x ^ 255 for x in buf])

    print(UTFBORDER * (w + 4))
    for i in range(0, len(buf), w//8*2):
        print("{}{}{}".format(
            UTFBORDER * 2,
            ''.join((hpixels_1x2(buf[x], buf[x+w//8], lsb=False) for x in range(i, i+w//8))),
            UTFBORDER * 2
        ))
    print(UTFBORDER * (2 + w - len(footnote)) + footnote + UTFBORDER * 2)


class MonoConsoleDisplay(framebuf.FrameBuffer):
    def __init__(self, width, height, mode="MONO_HLSB", invert=False):
        self.width = int(width)
        self.height = int(height)
        if mode == "MONO_VLSB":
            self.mode = framebuf.MONO_VLSB
            self.renderer = mono_vlsb
        elif mode == "MONO_HMSB":
            self.mode = framebuf.MONO_HMSB
            self.renderer = mono_hmsb
        elif mode == "MONO_HLSB":
            self.mode = framebuf.MONO_HLSB
            self.renderer = mono_hlsb
        else:
            raise ValueError("mode not supported: %s" % mode)
        self.invert = bool(invert)
        self.buffer = bytearray(width // 8 * height)
        self.show_calls = 0
        super().__init__(self.buffer, width, height, self.mode)

    @staticmethod
    def rgb(r, g, b):
        return int((r|g|b) > 0x7f)
        
    def show(self):
        self.show_calls += 1
        self.renderer(self, self.width, self.height, invert=self.invert,
            footnote=" {} {}, {} ".format(
                "{}x{}".format(self.width, self.height),
                self.renderer.__name__,
                "show() calls: {}".format(self.show_calls)
            )
        )

    def init(self): pass
    def init_partial(self): pass
    def wait_until_ready(self): pass
    def sleep(self): pass
