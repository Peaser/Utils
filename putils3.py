import collections, string, datetime, operator, random, math, os, sys, re, base64, copy, struct
from functools import reduce

dt = os.environ['userprofile']+'\\Desktop\\' #Desktop EV
headers = ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1') #mechanize header

class ArgumentError(Exception):
    """
    Exception raised by invalid arguments
    """
    pass

class fuzz(object):
    import base64
    """
    Obscurity based scrambler
    Usage:
        Print fuzz("Hello world!").encode("Password")
    returns:
        <whatever the fuzzed version of "Hello world!" is>
    """
    def __init__(self, string):
        self.string = string

    def encode(self, password):
        enc = []
        for i in range(len(self.string)):
            key_c = password[i%len(password)]
            enc_c = chr((ord(self.string[i])+ord(key_c))%256)
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
    """
    Toggleable boolean value
    Usage:
        b = Toggleable()
        set to True by default; you can also use Toggleable(False) for example.
    """

    def __init__(self, boolean=True):
        self.boolean = boolean

    def __repr__(self):
        return str(self.boolean)

    def toggle(self):
        self.boolean = not self.boolean

class B128(object):
    """
    Base 128 encoding
    Encoded object is returned as an int or long.
    """
    def __init__(self, inp):
        self.inp = inp

    def encode(self):
        t = 0
        for c in self.inp:
            t <<= 7
            t += ord(c)
        return t

    def decode(self):
        f = []
        while self.inp:
            f.append(chr(self.inp % 128))
            self.inp >>= 7
        return ''.join(reversed(f))

class Miniini(object):
    """
    Miniini config file format
    """
    def __init__(self):
        self.data = {}
    def parse_data(self, data, put_to_data=False):
        final = {}
        """
        Read miniini file into a python dict
        put_to_data stores parsed data into miniini object
        """
        lines = [i for i in data.split("\n") if i.startswith(">")]
        subs = []
        for i in lines:
            subs.append(tuple([a.strip() for a in i.split(":")]))
        del(lines)
        for i in subs:
            i_ = i[1]
            if i_.startswith("$"):
                i_ = eval(i_[1:])
            final[i[0][1:]] = i_
            if put_to_data:
                self.data[i[0][1:]] = i_
        return final
    def parse_file(self, file, mode="rb", _put_to_data=False):
        """
        Open a file, and parse to dict
        """
        fdata = open(file, mode).read()
        return self.parse_data(fdata, put_to_data=_put_to_data)
    def compile_dict(self, dict, comment=None, sort=True):
        """
        Translate a dict into miniini
        """
        prepend = [float, int, int, list, tuple, None]
        stringType = [str, str]
        final = []
        if comment and (type(comment) in stringType):
            final.append(comment)
        for i in dict:
            if type(i) not in stringType:
                raise TypeError("Invalid Identifier")
            K = ">%s:" % str(i)
            if type(dict[i]) in stringType:
                K += dict[i]
            elif type(dict[i]) in prepend:
                K += "$"+str(dict[i])
            else:
                raise TypeError("Invalid Value in key value pair")
            final.append(K)
        if sort:
            final.sort(key=lambda i:i.split(":")[0][1:])
        return '\n'.join(final)
    def write_out(self, data, file, mode="wb"):
        """
        Write data into a file
        if data is dict, it will be translated first, then written out
        if data is string, it will test if it's valid before writing out
        any other type will raise an error.
        """
        __final__ = ""
        if type(data) == dict:
            __final__ = self.compile_dict(data)
        elif type(data) == str:
            try:
                self.parse_data(data)
            except:
                raise TypeError("Invalid data")
            __final__ = data
        else:
            raise TypeError("Invalid data")
        with open(file, mode) as f:
            f.write(__final__)
    methods = ["parse_data", "parse_file", "compile_dict", "write_out"]


import copy, struct, sys
class sha512(object):
    """
    sha512 raw python implementation.
    """
    _k = (0x428a2f98d728ae22, 0x7137449123ef65cd, 0xb5c0fbcfec4d3b2f, 0xe9b5dba58189dbbc,
          0x3956c25bf348b538, 0x59f111f1b605d019, 0x923f82a4af194f9b, 0xab1c5ed5da6d8118,
          0xd807aa98a3030242, 0x12835b0145706fbe, 0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2,
          0x72be5d74f27b896f, 0x80deb1fe3b1696b1, 0x9bdc06a725c71235, 0xc19bf174cf692694,
          0xe49b69c19ef14ad2, 0xefbe4786384f25e3, 0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65,
          0x2de92c6f592b0275, 0x4a7484aa6ea6e483, 0x5cb0a9dcbd41fbd4, 0x76f988da831153b5,
          0x983e5152ee66dfab, 0xa831c66d2db43210, 0xb00327c898fb213f, 0xbf597fc7beef0ee4,
          0xc6e00bf33da88fc2, 0xd5a79147930aa725, 0x06ca6351e003826f, 0x142929670a0e6e70,
          0x27b70a8546d22ffc, 0x2e1b21385c26c926, 0x4d2c6dfc5ac42aed, 0x53380d139d95b3df,
          0x650a73548baf63de, 0x766a0abb3c77b2a8, 0x81c2c92e47edaee6, 0x92722c851482353b,
          0xa2bfe8a14cf10364, 0xa81a664bbc423001, 0xc24b8b70d0f89791, 0xc76c51a30654be30,
          0xd192e819d6ef5218, 0xd69906245565a910, 0xf40e35855771202a, 0x106aa07032bbd1b8,
          0x19a4c116b8d2d0c8, 0x1e376c085141ab53, 0x2748774cdf8eeb99, 0x34b0bcb5e19b48a8,
          0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb, 0x5b9cca4f7763e373, 0x682e6ff3d6b2b8a3,
          0x748f82ee5defb2fc, 0x78a5636f43172f60, 0x84c87814a1f0ab72, 0x8cc702081a6439ec,
          0x90befffa23631e28, 0xa4506cebde82bde9, 0xbef9a3f7b2c67915, 0xc67178f2e372532b,
          0xca273eceea26619c, 0xd186b8c721c0c207, 0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178,
          0x06f067aa72176fba, 0x0a637dc5a2c898a6, 0x113f9804bef90dae, 0x1b710b35131c471b,
          0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc, 0x431d67c49c100d4c,
          0x4cc5d4becb3e42b6, 0x597f299cfc657e2a, 0x5fcb6fab3ad6faec, 0x6c44198c4a475817)
    _h = (0x6a09e667f3bcc908, 0xbb67ae8584caa73b, 0x3c6ef372fe94f82b, 0xa54ff53a5f1d36f1,
          0x510e527fade682d1, 0x9b05688c2b3e6c1f, 0x1f83d9abfb41bd6b, 0x5be0cd19137e2179)
    _output_size = 8

    blocksize = 1
    block_size = 128
    digest_size = 64

    def __init__(self, m=None):
        self._buffer = ''
        self._counter = 0

        if m is not None:
            if type(m) is not str:
                raise TypeError('%s() argument 1 must be string, not %s' % (self.__class__.__name__, type(m).__name__))
            self.update(m)

    def _rotr(self, x, y):
        return ((x >> y) | (x << (64-y))) & 0xFFFFFFFFFFFFFFFF

    def _sha512_process(self, chunk):
        w = [0]*80
        w[0:15] = struct.unpack('!16Q', chunk)

        for i in range(16, 80):
            s0 = self._rotr(w[i-15], 1) ^ self._rotr(w[i-15], 8) ^ (w[i-15] >> 7)
            s1 = self._rotr(w[i-2], 19) ^ self._rotr(w[i-2], 61) ^ (w[i-2] >> 6)
            w[i] = (w[i-16] + s0 + w[i-7] + s1) & 0xFFFFFFFFFFFFFFFF

        a,b,c,d,e,f,g,h = self._h

        for i in range(80):
            s0 = self._rotr(a, 28) ^ self._rotr(a, 34) ^ self._rotr(a, 39)
            maj = (a & b) ^ (a & c) ^ (b & c)
            t2 = s0 + maj
            s1 = self._rotr(e, 14) ^ self._rotr(e, 18) ^ self._rotr(e, 41)
            ch = (e & f) ^ ((~e) & g)
            t1 = h + s1 + ch + self._k[i] + w[i]

            h = g
            g = f
            f = e
            e = (d + t1) & 0xFFFFFFFFFFFFFFFF
            d = c
            c = b
            b = a
            a = (t1 + t2) & 0xFFFFFFFFFFFFFFFF

        self._h = [(x+y) & 0xFFFFFFFFFFFFFFFF for x,y in zip(self._h, [a,b,c,d,e,f,g,h])]

    def update(self, m):
        if not m:
            return
        if type(m) is not str:
            raise TypeError('%s() argument 1 must be string, not %s' % (sys._getframe().f_code.co_name, type(m).__name__))

        self._buffer += m
        self._counter += len(m)

        while len(self._buffer) >= 128:
            self._sha512_process(self._buffer[:128])
            self._buffer = self._buffer[128:]

    def digest(self):
        mdi = self._counter & 0x7F
        length = struct.pack('!Q', self._counter<<3)

        if mdi < 112:
            padlen = 111-mdi
        else:
            padlen = 239-mdi

        r = self.copy()
        r.update('\x80'+('\x00'*(padlen+8))+length)
        return ''.join([struct.pack('!Q', i) for i in r._h[:self._output_size]])

    def hexdigest(self):
        return self.digest().encode('hex')

    def copy(self):
        return copy.deepcopy(self)
 
class Pad(object):
    """One time pad cryptography class"""
    def __init__(self):
        super(Pad, self).__init__()

    def getRandomCypher(self, data):
        """Generates random key and returns dict with key and cyphered data."""
        key = os.urandom(len(data))
        pairs = [[ord(a) for a in i] for i in zip(data, key)]
        retval = [chr(i[0]^i[1]) for i in pairs]
        return {"KEY":key, "CRYPT":str().join(retval)}
 
    def decypher(self, dict):
        """Decyphers with a dict. Takes dict with keys 'KEY' and 'CRYPT'."""
        if list(sorted(dict.keys())) != ["CRYPT","KEY"]:
            raise SyntaxError("Invalid argument dict")
        pairs = [[ord(a) for a in i] for i in zip(dict["KEY"], dict["CRYPT"])]
        retval = [chr(i[0]^i[1]) for i in pairs]
        return str().join(retval)
 
    def cypherFile(self, path):
        kp = self.getRandomCypher(open(path, "rb").read())
        with open("outfile.bin", "wb") as of:
            of.write(kp["CRYPT"])
        with open("cryptkey.KEY", "wb") as ck:
            ckdat = """START?{d}?END\nFILE_NAME:'{fn}'"""\
            .format(d=kp["KEY"].encode("base64"), fn=os.path.split(path)[1])
            ck.write(ckdat)
 
    def decypherFile(self, keyFile, cypherFile):
        keyDat = open(keyFile, "rb").read()
        cypherDat = open(cypherFile, "rb").read()
        keyRead = re.findall("START\?(.+)\?END", keyDat, re.DOTALL)[0]
        FName   = re.findall("FILE_NAME:'(.+)'", keyDat, re.DOTALL)[0]
        Decyphered = self.decypher({"KEY":keyRead.decode("base64"), "CRYPT":cypherDat})
        with open(FName, "wb") as file:
            file.write(Decyphered)

def dm(p):
    """
    make directory if it doesn't exist
    """
    if not os.path.exists(p):
        os.makedirs(p)

def stdout(s):
    """
    updatable write
    """
    sys.stdout.write("{0}\r".format(s))
    sys.stdout.flush()

def crc(s):
    """
    Basic Redundancy check
    """
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
crcHexLiteral = lambda s: hex(crc(s)).rstrip("L")
crcHexLiteral.__doc__ = "Literal hex identifier of an object applied with crc function"
crcHexLiteral.__lambda__ = "lambda s: hex(crc(s)).rstrip(\"L\")"

def median(l):
    """
    Median object of list (NOT the number median, but the index median)
    If the list is even in length, it returns both median items.

    Usage:
        median(["a", "b", "c"])
            Returns:
                "b"

        median(["a", "b", "c", "d"])
            Returns:
                ("b", "c")
                """
    return l[(len(l)/2)] if len(l)%2==1 else (l[(len(l)/2)-1], l[(len(l)/2)])

def ntlm(s):
    """
    ntlm hashing function
    """
    import hashlib,binascii
    hash1 = hashlib.new('md4', "s".encode('utf-16le')).digest()
    return binascii.hexlify(hash1)

def squaredImage(list_of_pixel_tuples):
    """
    For PIL; Turns len of a list of RGB pixels into a perfect square (x,y)
    """
    c = math.ceil
    s = math.sqrt
    return (int(c(s(len(list_of_pixel_tuples)))), int(c(s(len(list_of_pixel_tuples)))))

def dupecheck(object,minimum=1):
    """
    Check for duplicates in a list, returns the item if it appears more than the minimum.
    """
    return [x for x, y in list(collections.Counter(object).items()) if y > minimum]

def pause():
    """
    Press any key to continue...
    """
    os.system("pause")

def inlist(given, in_this, return_bool=False):
    """
    Returns the 'given' object in list form, if it appears in 'in_this'.
    Note: If boolean is true, returns True or False respectively
    """
    return any(x in given for x in in_this) if return_bool else [i for i in given if i in in_this]

def anyinstr(given, in_this):
    """
    check if any item in a list is in a string
    """
    return any(i in given for i in in_this)


def chop(object,length):
    """
    Slice up an item by character amount (length)
    uses __lambda__ for source
    """
    return [object[i:i+length] for i in range(0, len(object), length)]
chop.__lambda__ = "lambda o, l: [o[i:i+l] for i in range(0, len(o), l)]"

def rechop(object, n):
    """
    Strict version of chop() that uses Regular Expressions.
    By 'strict', I mean it does not leave a remainder.
    """

    return re.findall('.{%d}'%n,object)

def multidivide(delimiter1, delimiter2, object):
    """
    divides lists within lists
    Easier to just remember syntax and do it manually.
    """
    final = []
    for i in object:
        final.append(list(i) if type(i) == tuple else i)
    return delimiter1.join([delimiter2.join(i) for i in final])

def halflist(object):
    """
    slice a list in half
    uses __lambda__ for source
    """
    half = len(object)/2
    return object[:half], object[half:]
halflist.__lambda__ = "lambda o: o[:len(o)/2],o[len(o)/2:]"

def replacen(object, char, n):
    """
    Replace every n'th character in a string with something.
    usage:
        replacen("Hello", "x", 2)
    returns:
        'Hxlxo'
    """
    return ''.join(char if i % n == 0 else chara for i, chara in enumerate(object, 1))

def getreplaced(object, char, n):
    """
    The exact opposite of replacen()
    Find the character that gets replaced.
    """
    b = []
    full = []
    for (i, chara) in enumerate(object, 1):
        b.append((i, chara))
        full.append(char if i % n == 0 else chara)
    return object[n-1::n]

def dummylist(length, contains):
    """
    Generate a dummy list

    For content, put different types in contains.
    Example: To generate a dummy list with strings and integers, make contains equal [str, int]
    ie..
        dummylist(5, [int, float, str])
        returns something like [15, 72, 1.62, "FrjwW", 14.555]

    Accepted Types: Float, Int, String, NoneType

    Todo: add tuples, lists,
    """

    creatorDict = {
        None: None,
        str: ''.join(random.choice(string.ascii_lowercase) for i in range(random.randint(3,8))).capitalize(),
        int: random.randint(1,10000),
        float: random.random()*random.randint(1,256)
    }

    final = []
    picker = []
    if len(contains)==0: return []
    else:
        for i in range(length):
            picker.append(random.choice(contains))
        for i2 in picker:
            final.append(creatorDict[i2])
        return final

def vectorAverage(object):
    """
    Average out all values in a vector3
    """
    return tuple([reduce(lambda x,y:x+y,object)/len(object) for i in range(len(object))])

def recur(object, amt):
    """
    Recur a string for amt times, returns string
    """
    total = []
    while len(total) < amt:
        for i in object:
            total.append(i)
    return ''.join(total[:amt])

def combinelist(object):
    """
    Join a list of tuples or lists into a single list
    """
    return [i for i2 in object for i in i2]

def SysInfo(Info):
    """
    Information Available:
        OS
        User
        Processor
        UName      <--This is basically __all__ but formatted as a list but with a wierd order.
        All        <--This is __all__ but formatted as a string.
        __all__    <--This returns this tuple: (OS, User, Processor)

        Usage:
            Sysinfo('OS')
        Returns:
            Information on whatever Operating System you have.
    """
    import platform
    UName = platform.uname()
    OS = ' '.join([UName[0], UName[2], UName[3]])
    User = UName[1]
    Processor = ' '.join([UName[4], UName[5]])
    All ="%s, %s, %s" % (OS, User, Processor)
    __all__ = (OS, User, Processor)
    return eval(Info)

def infos(object, infotype):
    from datetime import datetime as dt
    """
    EXAMPLE:

            try:
                print "Hello" + 2   #String + int = Bad
            except Exception, e:
                print utils.infostream(str(e), "Fail")

            [Fail] - 2014-08-19 23:03:47.258000 - cannot concatenate 'str' and 'int' objects

    """
    return "[%s] - %s - %s" % (infotype, str(dt.now()), object)

def swap(thelist, what, replacer):
    """
    Swap an item in a list with something else
    """
    for n,i in enumerate(thelist):
        if i == what:
            thelist[n] = replacer
    return thelist

def getUt(formatted=True):
    """
    Get your system's uptime
    """
    import uptime
    return str(datetime.timedelta(seconds=uptime.uptime())) if formatted else uptime.uptime()

def secsFormat(n, asTimeDelta=False, ):
    """
    format seconds as h:m:s
    """
    if asTimeDelta == True:
        return datetime.timedelta(seconds=n)
    else:
        h=n//3600
        m=(n%3600)//60
        s=n%60
        return(h,m,s)

def intertwine(*args):
    """
    Turns multiple strings into a single by intertwining it.
    "hey", "bro", "yes" -> hbyereyos
    """
    return combinelist(list(zip(*args)))

def unintertwine(object, n):
    """
    object being a string, n being amount to unpack.
    opposite of intertwine
    """
    return [object[i::n] for i in range(n)]

def r(*args):
    """
    a range()-like function based on 1 because i'd rather write
    a whole new function instead of type range(1, n+1)

    range(4) = [0,1,2,3]

    r(4) = [1,2,3,4]
    """
    if len(args) == 0:
        raise ArgumentError("No arguments provided.")
    elif len(args) == 1:
        mode = "Single"
        i2 = args[0]
    elif len(args) == 2:
        mode = "Double"
        i1 = args[0]
        i2 = args[1]
    else:
        raise ArgumentError("Too many arguments.")
    if mode == "Single":
        return list(range(1, i2+1))
    if mode == "Double":
        if i1 > i2:
            raise ArgumentError("arg1 should not be greater than arg2.")
        return list(range(i1, i2+1))

def percent(part, whole, factor=100):
    """
    part as percent of whole
    returns number%

    Usage:
        percent(25,75)
    Returns:
        33.33333333
    """
    return factor * float(part)/float(whole)

pythag = lambda a, b: (a**2+b**2)**.5

def formatter(t, delimiter='-', l=50):
    """
    makes a tuple look pretty
    """
    aa = len(''.join(str(i) for i in t))
    dashes = delimiter*(l-aa)
    return dashes.join(str(i) for i in t)

def incrup(n, function=r):
    """
    List of lists of numbers
    Usage:
        incrup([2,5,7])
    Returns:
        [[1,2],[3,4,5,6,7],[8,9,10,11,12,13,14]]

    > What does this mean?
    2 = first 2 numbers
    5 = next 5 numbers
    7 = last 7 numbers

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
    """
    Pick key from dictionary based on weight (values)
    Usage:
        diction = {
        'a': 10,         #10 instances
        'b': 1,          #1 instance
        'c': 3           #3 instances
        }

        print randweight(diction)
    """
    return random.choice([k for k in dict for i in range(dict[k])])

def randprob(dict):
    """
    Pick key from dictionary based on it's probability percentage (value)
    **The sum of all the keys' values must equal 100!**
    """
    parts = [dict[i] for i in dict]
    keys = [i for i in dict]

    if sum(parts) != 100:
        raise ValueError("The sum of all the keys' values must equal 100.")

    ranges = incrup(parts, r)
    thevalue = random.randint(1,100)
    enumeration = [i for i, v in enumerate(ranges) if thevalue in v][0]
    return keys[enumeration]

def between(string, start, stop):
    """
    Between function
    Uses Regex to search through <string>, to find
    everything BETWEEN <start> and <stop>.

    Example:

        >>> k = "I want to find this right here, but not this."
        >>> between(k, "I want to find ", ", but not this.")
        "this right here"
    """
    pattern = "{0}(.+?){1}".format(start, stop)
    regex = re.compile(pattern)
    data = regex.findall(string)
    return data

def shorten(string, n):
    """
    If a string is longer than n character long, cut it off and append an ellipsis.
    Note: The 3 dots in the ellipses do not count towards n.
    Usage:
        shorten("Hello, world!", 6)

    """
    return string[:n]+'...' if len(string) > n else string

def newDynamicType(name, d):
    """
    Create a dynamic, fully variable class type.
    Usage:
        type11 = newDynamicType("This_is_type", {"x": "hello"})
        print type11().x
    """
    return type(name, (object,), d)

def spam_find(spam, strictness=15):
    """
    the higher the strictness, the more strict it is (100 = max).
    0   = NOTHING is spam
    15  = pretty fair
    25  = kinda strict
    50  = super strict
    75  = very strict
    100 = EVERYTHING is spam.
    """
    part = ''.join(list(set(spam)))
    pcent = percent(len(part), len(spam))
    return True if pcent <= strictness else False

def i(string):
    """string interpolation.
        given that the respective variables are declared...

            >>> string_ex = "Hello, world!"
            >>> i("I'd like to say #{string_ex}")
            "I'd like to say Hello, world!"

            >>> age = 20
            >>> i("I am #{age} years old.")
            "I am 20 years old."
    """
    if "#{}" in string:
        raise KeyError("Empty variable identifier")
    results = re.findall("(#{(.+?)})", string)
    for match in results:
        try:
            eval(match[1])
        except:
            raise KeyError("The variable: '%s' is not defined." % match[1])
        variable = str(eval(match[1]))
        string = string.replace(match[0], variable)
    return string

def i_(string):
    """alternate string interpolation that uses the following syntax:
some text some text $variable some text
this matches to "variable"
    """
    results = re.findall(r"(\$(.+?))\b", string)
    for match in results:
        try:
            eval(match[1])
        except:
            raise KeyError("The variable: '%s' is not defined." % match[1])
        variable = str(eval(match[1]))
        string = string.replace(match[0], variable)
    return string

def dicttrans(string, dict):
    """Translate using a dict. simpler than replace()"""
    for i in dict:
        string = string.replace(i, dict[i])
    return string

def unixmatch(query, l):
    """This function is experimental.
Unix-style terminal matching.

>>> unixmatch("*.html", pages)
["index.html", "test.html"]

>>> unixmatch("pic_?.jpg", files)
["pic_1.jpg", "pic_2.jpg", "pic_3.jpg"]

>>> unixmatch("b?g", wordlist)
["bag", "beg", "big", "bog", "bug"]"""

    query   = dictTrans(query, {"?":".", "*":".*"})
    matches = [re.findall(query, i) for i in l]
    return    [i[0] for i in matches if i]

def highestKey(stats, index=1):
    """Returns dict item with highest value (key)"""
    return max(iter(stats.items()), key=operator.itemgetter(index))[0]