import collections, string, datetime, random, math, os, sys

"""general laziness utilities"""

encodings = ['hex', 'base64', 'bz2', 'quopri', 'uu','zlib', 'rot_13','cp037', 'sjis']

dt = os.environ['userprofile']+'\\Desktop\\' #Desktop EV

class Fail(Exception):
    """Generic Failure"""
    pass

class ArgumentError(Exception):
    """Exception raised by invalid arguments"""
    pass

class Encrypt(object):
    import base64
    """Obscurity based encryption
    Usage:
        Print Encrypt("Hello world!").encode("Password")
    returns:
        <whatever the encrypted version of "Hello world!" is>
    """
    def __init__(self, string):
        self.string = string

    def encode(self, password):
        enc = []
        for i in range(len(self.string)):
            key_c = password[i % len(password)]
            enc_c = chr((ord(self.string[i]) + ord(key_c)) % 256)
            enc.append(enc_c)
        return base64.urlsafe_b64encode("".join(enc))

    def decode(self, password):
        dec = []
        self.string = base64.urlsafe_b64decode(self.string)
        for i in range(len(self.string)):
            key_c = password[i % len(password)]
            dec_c = chr((256 + ord(self.string[i]) - ord(key_c)) % 256)
            dec.append(dec_c)
        return "".join(dec)

class Toggleable(object):
    """Toggleable boolean value
    Usage:
        >>>b = Toggleable(True)
        >>>b
        True
        >>>b.toggle()
        >>>b
        False

    It has it's uses."""

    def __init__(self, boolean):
        self.boolean = boolean
        if type(self.boolean) is not bool:
            raise TypeError, 'type {} is not an acceptable type, must be bool'.format(type(self.boolean))

    def __repr__(self):
        return str(self.boolean)

    def toggle(self):
        if self.boolean == True:
            self.boolean = False
        elif self.boolean == False:
            self.boolean = True



def dm(p):
    """make directory if it doesn't exist"""
    if not os.path.exists(p):
        os.makedirs(p)

def nhex(n):
    """int to 2-byte hex"""
    if n == 0:
        return "00"
    else:
        return hex(n).rstrip("L").lstrip("0x") or "0"

def hexn(s):
    """hex to integer"""
    return int(float.fromhex(s))

def stdout(s):
    """updatable print that stays in one spot"""
    sys.stdout.write("{0}\r".format(s))
    sys.stdout.flush()

def center(s):
    """center-justify a string on an 80-wide windows terminal"""
    n = len(s)
    return ' '*(40-(n/2))+s+' '*(40-(n/2))

def crc(s):
    """Basic Redundancy check"""
    k=0
    g=(len(s)/2)*2
    o=0
    while o<g:
        tv=ord(s[o+1])*256+ord(s[o])
        k+=tv
        k&=0xffffffff
        o+=2
    if g<len(s):
        k+=ord(s[len(s)-1])
        k&=0xffffffff
    k=(k>>16)+(k&0xffff)
    k+=(k>>16)
    a=~k
    a&=0xffff
    a=a>>8|(a<<8&0xff00)
    return a

def ntlm(s):
    """ntlm hashing function"""
    import hashlib,binascii
    hash1 = hashlib.new('md4', "s".encode('utf-16le')).digest()
    return binascii.hexlify(hash1)

def squaredImage(list_of_pixel_tuples):
    c = math.ceil
    s = math.sqrt
    """For PIL"""
    return (int(c(s(len(list_of_pixel_tuples)))), int(c(s(len(list_of_pixel_tuples)))))

def tobytes(n):
    """Bytes maker!
    Turns integer into byte! (0 = NUL, 1 = EOF or whatever it is"""
    return '{0:02X}'.format(n).lower().decode('hex')

def dupecheck(object,minimum=1):
    """ Check for duplicates in a list, returns the item if it appears more than the minimum. """
    if type(object) is list:
        return [x for x, y in collections.Counter(object).items() if y > minimum]
    else: raise Fail, "Invalid type - must be list."

def ak():
    """Press any key to continue..."""
    from os import system
    system("pause")

def remrn(object):
    """Strip items in list"""
    if type(object) is list:
        return [i.strip() for i in object]
    else: raise Fail, "Invalid type - must be list."

def average(l):
    return float(sum(l))/len(l)

def copyclipboard(tocopy):
    from pyperclip import copy
    con = True
    while con:
        iscopy = raw_input("Copy to clipboard? [y/n]: ").lower()
        if iscopy == 'n':
            con = False
            break
        if iscopy == 'y':
            copy(tocopy)
            print "%s copied to clipboard." % tocopy
            con = False
            break
        else:
            print "Error, enter y or n."

def listshuf(object):
    """ Shuffles items in a list, returns new list.
    I made a seperate function because I don't think it's ethical
    to use 'list.shuffle()' in the middle of a script."""
    if type(object) is list:
        b = [i for i in object]
        random.shuffle(b)
        return b
    else: raise Fail, "Invalid type - must be list."

def listinlist1(given, in_this):
    """ Returns the 'given' object in list form, if it appears in 'in_this'. """
    if type(given) and type(in_this) is list:
        return [i for i in given if i in in_this]
    else: raise Fail, "Invalid type - must be list."

def listinlist2(given, in_this):
    """ Returns True or False if a 'given' is in 'in_this'. """
    if type(given) and type(in_this) is list:
        return any(x in given for x in in_this)
    else: raise Fail, "Invalid type - must be list."

def anylistinstring(given, in_this):
    """check if any item in a list is in a string"""
    if any(i in given for i in in_this):
        return True

def chop(object,length):
    """ Slice up an item by character amount (length) """
    return [object[i:i+length] for i in range(0, len(object), length)]

def rechop(object, n):
    """Strict version of chop() that uses Regular Expressions.
    By 'strict', I mean it does not leave a remainder."""
    from re import findall
    return findall('.{%d}'%n,object)

def top(object, default=None):
    """ Returns most common items in list (tuple)."""
    if default is None: default = len(object)
    if type(object) is list:
        ob = {}
        for x in object:
            a = ob.get(x, 0)
            ob[x] = a+1
        return reversed(ob.items(), key=lambda x: x[1])[:default]
    else: raise Fail, "Invalid type - must be list."

def multidivide(delimiter1, delimiter2, object):
    """divides lists within lists
    Easier to just remember syntax and do it manually."""
    if type(object) is list:
        final = []
        for i in object:
            if type(i) is tuple:
                final.append(list(i))
            else:
                final.append(i)
        return delimiter1.join([delimiter2.join(i) for i in final])
    else: raise Fail, "Invalid type - must be list."

def halflist(object):
    """slice a list in half down the middle!"""
    if type(object) is list:
        half = len(object)/2
        return object[:half], object[half:]
    else: raise Fail, "Invalid type - must be list."

def replacen(object, char, n):
    """Replace every n'th character in a string with something.
    usage:
        replacen("Hello", "x", 2)
    returns:
        "Hxlxo"

    I have no Idea where this would be useful by the way
        """
    return ''.join(char if i % n == 0 else chara for i, chara in enumerate(object, 1))

def getreplaced(object, char, n):
    """The exact opposite of replacen()
    Find the character that gets replaced.
    This function alone is pretty useless unless you're going to use the replacen function with it."""
    b = []
    full = []
    for (i, chara) in enumerate(object, 1):
        b.append((i, chara))
        full.append(char if i % n == 0 else chara)
    return object[n-1::n]

def npowsqrt(n):
    """number to the power of the square root of itself.

    As source:
        n**sqrt(n)"""
    from math import sqrt
    return n**sqrt(n)

def sanitize(object):
    """ Return a list of lowercase words, all consisting of ascii characters. """
    if type(object) is list:
        main = []
        for i in object:
            parts = []
            for i2 in i:
                if i2 in string.ascii_letters:
                    parts.append(i2)
            main.append(''.join(parts))
        return main
    else: raise Fail, "Invalid type - must be list."


def cycle(str, int):
    """ ROT Style cycler for strings """
    components = [ord(i) for i in str]
    return ''.join([chr(i+int) for i in components if i < 255])

def dummylist(length, contains):
    """ Generate a dummy list
    For content customization, put different types in contains=[].
    Example: To generate a dummy list with strings and integers, make contains equal [str, int]
    ie..
        dummylist(5, [int, float, str])
        returns something like [15, 72, 1.62, "FrjwW", 14.555]

    Accepted Types: Float, Int, String, NoneType

    Todo: add tuples, lists,"""
    def create(Type):
        if Type is None:
            return None
        if Type is str:
            return ''.join(random.choice(string.ascii_lowercase) for i in range(random.randint(3,8))).capitalize()
        if Type is int:
            return random.randint(1,10000)
        if Type is float:
            return random.random()*random.randint(1,256)
    final = []
    picker = []
    if len(contains)==0: return []
    else:
        for i in range(length):
            picker.append(choice(contains))
        for i2 in picker:
            final.append(create(i2))
        return final

def vectorAverage(object):
    """ Average out all values in a 3-point tuple """
    if type(object) is tuple:
        ret = []
        for i in range(len(object)):
            ret.append(reduce(lambda x,y:x+y,object)/len(object))
        return tuple(ret)

def recur(object, amt):
    """ Recur a string for amt times, returns string """
    total = []
    while len(total) < amt:
        for i in object:
            total.append(i)
    return ''.join(total[:amt])

def clean(object, delimiter=''):
    """For strings, basically removes crap that isn't string-y."""
    b = []
    for i in object:
        if i in string.ascii_letters:
            b.append(i.lower())
    return delimiter.join(b)

def combinelist(object):
    """ Join a list of tuples or lists into a single list"""
    if type(object) is list:
        return [i for i2 in object for i in i2]
    else: raise Fail, "Invalid type - must be list."

def SysInfo(Info):
    """Information Available:
        OS
        User
        Processor
        UName      <--This is basically __all__ but formatted as a list but with a wierd order.
        All        <--This is __all__ but formatted as a string, delimited with pipes.
        __all__    <--This returns this tuple: (OS, User, Processor)

        Usage:
            Sysinfo('OS')
        Returns:
            Information on whatever Operating System you have."""
    import platform
    UName = platform.uname()
    OS = ' '.join([UName[0], UName[2], UName[3]])
    User = UName[1]
    Processor = ' '.join([UName[4], UName[5]])
    All ="%s|%s|%s" % (OS, User, Processor)
    __all__ = (OS, User, Processor)
    return eval(Info)

def infos(object, infotype):
    from datetime import datetime as dt
    """EXAMPLE:

            try:
                print "Hello" + 2   #String + int = Bad
            except Exception, e:
                print utils.infostream(str(e), "Fail")

            [Fail] - 2014-08-19 23:03:47.258000 - cannot concatenate 'str' and 'int' objects

        """
    return "[%s] - %s - %s" % (infotype, str(dt.now()), object)

def swap(thelist, what, replacer):
    """Swap an item in a list with something else"""
    for n,i in enumerate(thelist):
        if i==what:
            thelist[n]=replacer
    return thelist

def getUt(formatted=True):
    """Get your system's uptime"""
    import uptime
    return str(datetime.timedelta(seconds=uptime.uptime())) if formatted else uptime.uptime()

def secsFormat(n, asTimeDelta=False, ):
    """format seconds as h:m:s"""
    if asTimeDelta == True:
        return datetime.timedelta(seconds=n)
    else:
        h=n//3600
        m=(n%3600)//60
        s=n%60
        return(h,m,s)

def isin(iterable, object):
    """isin(['yes','no'], 'asdiasno')  ->  True"""
    for i in iterable:
        if i in object:
            return True
            break
    return False

def intertwine(*args):
    """ Turns multiple strings into a single by intertwining it.
    "hey", "bro", "yes" -> hbyereyos"""
    return combinelist(zip(*args))

def unintertwine(object, n):
    """object being a string, n being amount to unpack.
    hefsopuhliciyckt -> ['holy', 'epic', 'fuck', 'shit']"""
    return [object[i::n] for i in range(n)]

def r(*args):
    """a range()-like function based on 1 because i'd rather write
    a whole new function instead of type range(1, n+1)

    range(4) = [0,1,2,3]

    r(4) = [1,2,3,4]
"""
    if len(args) == 0:
        raise ArgumentError, "No arguments provided."
    elif len(args) == 1:
        mode = "Single"
        i2 = args[0]
    elif len(args) == 2:
        mode = "Double"
        i1 = args[0]
        i2 = args[1]
    else:
        raise ArgumentError, "Too many arguments."
    if mode == "Single":
        return range(1, i2+1)
    if mode == "Double":
        if i1 > i2:
            raise ArgumentError,"arg1 should not be greater than arg2."
        return range(i1, i2+1)

def percent(part, whole, factor=100):
    """part as percent of whole
    returns number%

    Usage:
        percent(25,75)
    Returns:
        33.33333333"""
    return factor * float(part)/float(whole)

def pdo(function, object):
    """print something as well as do it too"""
    print(object)
    function(object)

def pythagorean(a, b, squared=True):
    """Just a Pythagorean theorem"""
    from math import sqrt
    return sqrt(a**2+b**2) if squared else a**2+b**2

def formatter(t, delimiter='-', l=50):
    """makes a tuple look pretty
    ('b', 491) would become b---------491"""
    aa = len(''.join(str(i) for i in t))
    dashes = delimiter*(l-aa)
    return dashes.join(str(i) for i in t)

def incrup(n, function):
    """List of lists of numbers
    Usage:
        incrup([2,5,7])
    Returns:
        [[1,2],[3,4,5,6,7],[8,9,10,11,12,13,14]]

    What does this mean?
    2 = first 2 numbers
    5 = next 5 numbers
    7 = last 7 numbers

    functions:
        r       <--- defined earlier in utils.py
        range

    This function was designed mainly for randprob()

    """
    result = []
    last = []
    st = 0
    for i in n:
        la = len(last)
        new = function(i)
        result.append([i+la+st for i in new])
        st += la
        last = new
    return result

def randweight(dict):
    """Pick key from dictionary based on weight (values)
    Usage:
        diction = {
        'a': 10,         #10 instances
        'b': 1,          #1 instance
        'c': 3           #3 instances
        }

        print randweight(diction)

    Returns:
        'a' #Most likely
        #There is a ~76% chance of the answer being 'a'.

    """
    return random.choice([k for k in dict for i in range(dict[k])])

def randprob(dict):
    """Pick key from dictionary based on it's probability percentage (value)
    **The sum of all the keys' values must equal 100!**
    Usage:
        randprob({'a':5, 'b':95})
    Returns:
        'b' #Most likely
        #literally 95% chance of it being 'b'

    By the way, You have no idea how hard my poor brain had to work to figure this shit out.
    Seriously, I feel like a genius.
    """
    parts = [dict[i] for i in dict]
    keys = [i for i in dict]

    if sum(parts) != 100:
        raise ValueError, "The sum of all the keys' values must equal 100. Yours equal {0}".format(sum(parts))

    ranges = incrup(parts, r)
    thevalue = random.randint(1,100)
    enumeration = [i for i, v in enumerate(ranges) if thevalue in v][0]
    return keys[enumeration]

def between(string, start, stop):
    """find a string between two substrings in a main string

    Usage Example:

        thestring = "This is the string. Find THIS HERE and end."
        print between(thestring, "Find ", " and end")

    Returns:
        "THIS HERE"

    #Probably most useful for web scraping if the soup is...
    ...less than beautiful."""

    begindex = string.find(start)+len(start)
    endex = string.find(stop)
    return string[begindex:endex]

def shorten(string, n):
    """If a string is longer than n character long, cut it off and append an ellipsis.
    Note: The 3 dots in the ellipses *DO NOT* count towards n.
    n is the length of the string itself, without '...'

    Usage:
        shorten("Hello, world!", 6)
    Returns:
        "Hello,..."
        """
    if len(string) > n:
        return string[:n]+'...'
    else:
        return string

def newDynamicType(name, d):
    """Create a dynamic, fully variable type.
    Usage:
        type11 = newDynamicType("This_is_type", {"x": "hello"})
        print type11().x
    Prints:
        "hello"""
    return type(name, (object,), d)

def spam_find(spam, strictness=15):
    """the higher the strictness, the more strict it is (100 = max).

    0   = nothing is spam
    15  = pretty fair
    25  = kinda strict
    50  = super strict
    100 = EVERYTHING is spam."""

    part = ''.join(list(set(spam)))
    pcent = percent(len(part), len(spam))
    if pcent <= strictness:
        return True
    else:
        return False