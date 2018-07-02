from Crypto.Cipher import AES
import base64
import zlib
from tools import Pkcs7Encoder
import time
from hashlib import md5, sha1

BS = 16
# pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)


def pad(s):
    try:
        return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    except TypeError:
        return s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()


class Crypter(object):
    def __init__(self):
        self.ks = b'\xd8\x80\xb6v\x8dI\xb2\x9e\xd0Z\xd3u\xe3?\x1b\x8fb\xa1\xbam\xbd$\x96\xc9\xa7OkJU6\x87\xde\x8e\xb2' \
                  b'\xce6\xeb\xc4+\xd1s\xbb?\x80\x06\x1c+\xab\xb2\x8dz\x85~;\x11\xce\x06\x97~*\x0b\\%\xbb\x97x\t' \
                  b'\x87EX]5k \r\xf0\xbd\xa1\xe4\xdfu\xd5q\xfaB\xd3}\xe8";\x9f\xbd\xb2\x82!\xc7!^4\xf2\t\xb8\xe2\x16' \
                  b'\xdbh\xca5\x97j\x99\xe2H\x82\xd4\xfb|\xb5-Q\x7fc\xbc\xa48\x10\xec(' \
                  b'xS\xabK\xd6\xc1.\xf1\x98\xa5\xf1\x0c3=;\xfd\x1f\xcb\x98\xf7oz\xc9\x0e\xfd\xe3\xd8P\'tL\xc4\xe3' \
                  b'\xbd\xc5>z\xee\xb6\xc9uN\x99c\xaeD\xd3W\xa3\xec\xde\r\x031\xf5\\\x0cT\x03n\xfc\x9d&P\x0b\xcd\x94' \
                  b'>\x8a\xa5~\xbe\x18K\xa5dzM\xb0\x0b#\x96\xe4\x8d\x017\x8d\x96\r\x0flNc{' \
                  b'\x8b\xc56\x00\xce\x05\xe9\xaa]C\xden\x97\x90\x927\xcdH\xe5\x00M\xa5~\r\xcfZ\xa7\x9f\x82\xc5\x14OJ' \
                  b'\xdf\xb2\x9d\xf0u\x97\x85\x9d3|\xdf^\xe7n\xbd\x9fR;-\xd6\xb5+\\\xc2PuQ\x12}n\x87\x8d=\xc7]\xb9' \
                  b'<\'\xd9{\xbd@\x02R\x05\xd6\xb5M\xf6P\xfd\x85\xa4\x19\xdf\xaed\'\xbf\x15\xdc\xe7f\xf7\x97%\xc1{' \
                  b'o\x1c\xc8=\xebN*\xef\rh\x12`h\xc3\x9e8\xef\xc3\xf9\x8e\xba:g%\xf8:\xc3\x1f&\xfb\xf9\xa6\x9d\xfc' \
                  b'\xec\x11\xae\xec\xd6:\xf2\xd7\x0f=\xb8\x8c*GS\xa8L\xa6%\xcd\xdf!\xc0\x81\x8av\xba\xe2M.\xed\xbax' \
                  b'\xe5\xad\xb0\x83\xcfu\x17]A\xe7\xde\'\xa0\xbfLoe\x0c\xd0\xa7\xb5\x93z\xfam-G\xab\xbbZG\x04a\xd7' \
                  b'\x0fX\'\x85\x02\xe6y(\xf2\xfe!\xde}!3\xac\x1d\xd9/};R\xeb\xbf\xac9\x81$\xdb\xd2\xdb\xb8S\x978\x8e' \
                  b'&x\xeeoo/i\xa0H\x1a=G\x8eh\xa0\x0e,' \
                  b'\xa2\xe1]9\xa0\n\xdb\x0eW\xd0\xc1t\xe6\x8e\xea\xe6\xba2\xf7}\x02\xf5~-\xf5\xde\xa8\xeb\xdd\xfd' \
                  b'\xe0-8\x0c\x8b\x15\x107\xfc\x07Pc-\xce0\xbb\xb7\\/i\x95 ' \
                  b'\x8c\xaf\x93\xde\x81_\xc0\x8e\xb4\xe1\xfb\xe3\xa6\x83\xe2\xd6\xf8\xefM\x19Oo;*\xdb\xd9O\x9c\xa0' \
                  b'\xebn\xf7K\xb5\x1c-Y6\xaf|\xbb\x0fuf\x85\xab\x9d\xe0\xf89\x8b\x9e\xc5\xeb\x19\xb5_1\xb1\xab\x9en' \
                  b'\xd1\xdf\x18\xb6@46\xdf6\xc19}b\xa9\x1bo\xdd\xf5\x9a\x1d8\x17\xb13\x1d\xafhS\x8dm\xd9\xfd;\x1b' \
                  b'\x84=\x1aC\xaa\xa5q\x90\x8cY}K\xa6\x99\x10\xc9\xf7-\x9e;\x08\x90\x14z\xf1\xc6\xf4\xb3\x00\xbfmm,' \
                  b'\x89HZM{O\xbf\x03\x13Nj\x147\x08}\x1a:\xd3\x99s\x02\xe6\xcez\xdd\xb9pt\xeb\x96\xd3u!Oi\xb3K\xb5' \
                  b'\xefm\xf8\x932zZ\xc9\xf8\xd1\xafP\xb7\nKyN\xf7GM\xbb4\xc1\x94T\xeec\xb3\xac^\xed\x0f7\xd6\x1e*l' \
                  b'\x9a\xde\xa7\x8d \xf0\x84\xfd"\xbd\x1a\x8bfg\xce\'\xb3\x96]oz\xf0)\xec\x91\xbc\xe7c`m\xa7}\xd6GA '
        self.ks_c2 = '\x11\xc4?\xc4V\xeb&V\x90\xb4\x10\x89\xb4E\xfc\xe2Kv\xbcu\x91s\xe5=$\xab\x8aC|xv\x8a\x8c\xb8\xd3' \
                     '\r\x84\xbb*\x90V\xc5Y\xc4\x1d\x81,\xd9Q=4ke[' \
                     '.N\r\x16/\xa1\xb3PY\xfb\x92$o\xbcs\x04\xf5;\xfd\x03\xc8\xe1\xb2\xa34<\xfe_\xd2\xda!\x9fQn+t' \
                     '<\x9bCl\x8f\xd5\xd3\x9b\xc7\x19qc\x14\xc7\x0b\xc5(' \
                     '\t^M\x12h\xdd\x1c\xb6\x1c\xaf1u\xfb\x90\x10\xf4T<*\x7f\x99\xce\x8e\xfd\x0b\xabC\\\x9d\x1b\xf1' \
                     '\x848\xa0\xbc"k\xed\xaeCH??\xff\xffGR)z\x91N\xf67&\'\xbcG(' \
                     ']\xb6\x13\xc2\xb6Q\x0f\x9b?^\xff\x13w\x15l!V-f\xcc\x14H\xc0\x9c\x8a\xd7w\xbd.\xd7\xbc\xddg\xfb' \
                     '\xe1\x19i\xadqa~\xdeO\x8e\xd4]\xa0\xed\xd8\xb2\x90\xec\xa3\x95\xa1<f\xdc\xae\x1c\x98I\x06a\x84' \
                     '\xad\x1e\nn\xca\x14E\xfd\xfa\xba\xcc&\x1e\xd0\xafp\x81\xb5\x80\x173\xba_\x991h\xbd\xfc\x83\x97' \
                     '^\x176>\xaf\x00@\x06\x85\xbe\xa3]Y\xff\\\x833\x11@\x96G\xdaA\xd852b<&=\xa0B\xfd\xcb\xd0\xa6H' \
                     '\xb5\x92%s\xa0@\x19\xab\xbd\xdc\xe9\xf4\x0c\x95Kn\xd7o\xb2\x98\xee\xeb\xf91\xd6QGkp2\xca3\xb6' \
                     '\x14\xcf\xa5\x95\x11U\x0e\xceh\xc6=\xbcK9S\x91\x0e\x1a%?\x8d\x01U\x01\xfc~\x16\x9cP\x84U\x99' \
                     '\x06\xed\x13\xbe\xe7\xbc\xf8\xec\xf9\xb4Hq\xb4\xd9\xdeZ\xe1\xf0\x94z")\x85\x1c\xed\x85R\xf3I' \
                     '\xa7(\r\xf0\xa47W\xb0\x01\x99\xd6\xa5|RTvb\x9fo\xb8x+\x9ch\xee\x8c\x88@\xb5\x1a\xf1\xe2\x8e\xb9' \
                     '\x12++e\xa6)\x19\xf7\xb4l\xa4<\xa7\x85\xf5\xdb\x08\x17%\x11S\x8c\xe1\r\xfb\xc7\xa9\xc23\xa2\xff' \
                     '\xc6\xbd\xf6]p\xdbV\xb8\xc0j\xaa\x87Ef@\xa3x\x81O\x1d\x82\xff\xccykJ\x1f>\xcb\x11V\x0fw\xbb7' \
                     '-\xadp\xdf\xf2\x07\x1fj\xf3\xaavmU\x11\xfb:\x8a\xcby\xc0\xb90\t\xd8 ' \
                     '\x0e\x1e\xae\xda\xe0\x9dB\xff+\xb0f=\xb5P*\x97w\x13\x13+.\xd1\xa5\xf3U\x0b>t\x91t@\xaf\xe6\x8d' \
                     '\x8cp\x8bE\x02(\x16\x19\x86\x88\xa1\xe7\x18\xd0b<\x8ch\xa0\xecU\xcc\xf1\xf6\n\x0f\x10w3\x86\x9e' \
                     '=\x16\xdb\x8b\xcd\xf9/`\x86\x9b}\xc1\x91\xd2~\xe7\x9b\x80\xc0\xc5\x0f\xd7\xffp`\xb7\xdc\xb3\xa1' \
                     '\xe3\x0e\xfe\x97\x85\xfd\xbe\x18\x0b|\xb5\x0fI9\xea\x8b9_y\xfb\xfb\xc1\x06A)h\x9bCAi\xdey\x07N8' \
                     '\x0c\xea\xc7O\xf5hS\xa0\xa3\xba\xe9J\xbb6\x00\x98%`\x03\x9ak-\x06t\x9c\xb3\xde\xa8\x96\xb2]\xd0' \
                     '\xff\xb1\xb1\xf3\x11M/\xe3Z^\xd6T[' \
                     '\x19\xc2l\xa5\x0e\xb3\xe8m0\xa0k$\xb7\xf6"\xf7\xdf\xa0\x92\xab\xca4\xf9\xc0\xe9\x9ce\x85\xa8' \
                     '\x80\xf9\xb5\xf7\xc5\xc1\xfc\x16v\xefW\xc8>D\xe5C^/\xf3\x0b+\xc1\xc7\x17\xff\xac\x9e\'\xe6\x10F' \
                     '\x0e\'7\xc5X\xfc?$t\x9d\x8e;I\x80\xf2\x93\xee\xff\x8e\xd8GLz\xab\x97GDQ8\xb0\xfeL\xef\x93\xcb' \
                     '\x82\xcf>g\xf6"Y\\\x89\x97A\xe7\xde\xeew\xc9Z\x8bI\x05\x91&\xf4\x085!\xa1\xa7J0P\x16\x98\xafL' \
                     '^IAb\x07\x1f\xdc\x9fJ\x0bP\xe7\xf6t\xa1\x1cbpVb\x86Fg\x18\xb8\xa4#+H\x91\xb8\xb6\r,' \
                     '\xde\xcf\tx_\xf0\x95\xeaA\xc1(\x82g\x83p\x1cg\x95V\xa7\xfa{' \
                     '2c\x86\xc6\x13\x12\xe6\x18\xf9y\x9c&4\xe2\x9a\x89\xd1\xab\x9e\xaf\x95\xaan\xd7Pu6\xd2\x1c\xa7' \
                     '\x1a\x95\xc8\x88\x95\x03KJ\x99\xcf\xc1\xd3\xaa$r\x8b\x88k\xde\x17l\xfe"\x9e\x901\x87\xa5\xab' \
                     '\xbb^N\xa9\xb1\x030\xe84\xbd\xad\x1b\xe1\x82\x10Sj\xcf[' \
                     'm9\x9dV\x16=\xec\x8d\xc8>\xc7\xa3\xbav\\\x0fN\xd8\x07\x17\x99\xa3?\xdc[' \
                     '\rt4\x15\xa2#\xdb\x0b^\x83\x83\xcb\x96\x0eH4\x99\xe9\xb0\xf9U-s\xe87~\xfd\x92V\x16KB\x9an,' \
                     '\xfa\x01\xf7\xce\xc4\'\x17t\xfd\xe3 '
        self.encoder = Pkcs7Encoder()
        self.mode = AES.MODE_CBC
        self.key = '60e2e90bb43b37fb'

    def md5(self, s):
        return md5(s.encode('utf-8')).hexdigest()

    def sha1(self, s):
        return str(sha1(s.encode('utf-8')).hexdigest()).upper()

    def get_smon_checker(self, s, ts):
        ss = '%s%s%s' % (self.key, s, ts)
        return self.sha1(ss)

    def EG_knlCurrentUpTime(self, ts):
        v5 = 0x5A8EF52B
        v1 = ts - v5
        tsu = 22222
        return 1000 * v1 + ((274877907 * tsu >> 38) + ((274877907 * tsu) >> 63))

    def get_player_server_connect_elapsed_time(self, ts=None):
        if not ts:
            ts = int(time.time())
        return ((0x5A92AD2B + (
                    (((self.EG_knlCurrentUpTime(ts) - 0xE86C29C) >> 3) * 0x20C49BA5E353F7CF >> 64) >> 4)) ^ 0x1C2F0688)

    def decrypt_aes128(self, s, key):
        e = AES.new(key, self.mode, b'\x00'*16)
        return self.encoder.decode(e.decrypt(base64.b64decode(s)))

    def encrypt_aes128(self, s, key):
        e = AES.new(key, self.mode, b'\x00' * 16)
        return self.encoder.decode(e.encrypt(s))

    def _decrypt(self, msg, version=1):
        if version == 1:
            i = [337, 21, 428, 323, 104, 684, 636, 232, 154, 266, 770, 83, 908, 424, 644, 739]
            key = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            k = str(base64.b64encode(self.ks))
            for j in range(0, 16):
                key = key[0:j] + k[i[j]] + key[j + 1:]
        elif version == 2:
            i_c2 = [281, 679, 919, 500, 179, 489, 379, 98, 321, 920, 885, 343, 285, 50, 639, 969]
            i2_c2 = [3, 3, 1, 3, 0, 1, 2, 2, 2, 0, 3, 1, 0, 2, 0, 1]
            tkey = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            for j in range(0, 16):
                tkey = tkey[0:j] + self.ks_c2[i_c2[j] + i2_c2[j]] + tkey[j + 1:]
            key = tkey[8:16] + tkey[4:8] + tkey[0:4]
        else:
            raise ValueError('Unknown key version')
        obj = AES.new(bytes(key, 'utf-8'), AES.MODE_CBC,
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        r = obj.decrypt(msg)
        # padding = r[-1]
        return r[:-r[-1]]

    def _encrypt(self, msg, version=1):
        if version == 1:
            i = [337, 21, 428, 323, 104, 684, 636, 232, 154, 266, 770, 83, 908, 424, 644, 739]
            key = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            k = str(base64.b64encode(self.ks))
            for j in range(0, 16):
                key = key[0:j] + k[i[j]] + key[j + 1:]
        elif version == 2:
            i_c2 = [281, 679, 919, 500, 179, 489, 379, 98, 321, 920, 885, 343, 285, 50, 639, 969]
            i2_c2 = [3, 3, 1, 3, 0, 1, 2, 2, 2, 0, 3, 1, 0, 2, 0, 1]
            tkey = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            for j in range(0, 16):
                tkey = tkey[0:j] + self.ks_c2[i_c2[j] + i2_c2[j]] + tkey[j + 1:]
            key = tkey[8:16] + tkey[4:8] + tkey[0:4]
        else:
            raise ValueError('Unknown key version')
        obj = AES.new(bytes(key, 'utf-8'), AES.MODE_CBC,
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        try:
            return obj.encrypt(pad(msg).encode())
        except AttributeError:
            return obj.encrypt(pad(msg))

    def decrypt_request(self, msg, version=1):
        return self._decrypt(base64.b64decode(msg), version)

    def decrypt_response(self, msg, version=1):
        try:
            return zlib.decompress(self._decrypt(base64.b64decode(msg), version))
        except zlib.error:
            return zlib.decompress(bytes(str(self._decrypt(base64.b64decode(msg), version)), 'latin-1'))

    def encrypt_request(self, msg, version=1):
        return base64.b64encode(self._encrypt(msg, version))

    def encrypt_response(self, msg, version=1):
        zlib_compress = zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS)
        return base64.b64encode(self._encrypt(zlib_compress.compress(msg) + zlib_compress.flush(), version)).decode()

    def decrypt_dat_file(self, file):
        with open(file) as f:
            return self.decrypt_response(f.read().strip('\0'), 2)
