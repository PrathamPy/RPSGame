from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
from fontTools import ttLib

FR_PRIVATE  = 0x10
FR_NOT_ENUM = 0x20
fonts = {}

def loadfont(fontpath, private=True, enumerable=False):
    '''
    func loadfont(): Makes fonts located in file `fontpath` available to the font system.

    PARAMETERS
    ----------
    private : Bool.
        if True, other processes cannot see this font, and this 
        font will be unloaded when the process dies.
    enumerable : Bool.
        if True, this font will appear when enumerating fonts

    RETURNS
    -------
    str. fullname variable is returned and can be used as a font.

    '''
    
    if isinstance(fontpath, bytes):
        pathbuf = create_string_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExA
    elif isinstance(fontpath, str):
        pathbuf = create_unicode_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExW
    else:
        raise TypeError('fontpath must be of type str or unicode')

    flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
    numFontsAdded = AddFontResourceEx(byref(pathbuf), flags, 0)
    font = ttLib.TTFont(fontpath)
    fullName= font['name'].getDebugName(4)
    return fullName