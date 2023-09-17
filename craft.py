S = [0xc, 0xa, 0xd, 0x3, 0xe, 0xb, 0xf, 0x7, 0x8, 0x9, 0x1, 0x5, 0x0, 0x2, 0x4, 0x6]
P = [0xf, 0xc, 0xd, 0xe, 0xa, 0x9, 0x8, 0xb, 0x6, 0x5, 0x4, 0x7, 0x1, 0x2, 0x3, 0x0]
Q = [0xc, 0xa, 0xf, 0x5, 0xe, 0x8, 0x9, 0x2, 0xb, 0x3, 0x7, 0x4, 0x6, 0x0, 0x1, 0xd]
RC3 = [0x1, 0x4, 0x2, 0x5, 0x6, 0x7, 0x3, 0x1, 0x4, 0x2, 0x5, 0x6, 0x7, 0x3, 0x1, 0x4,
       0x2, 0x5, 0x6, 0x7, 0x3, 0x1, 0x4, 0x2, 0x5, 0x6, 0x7, 0x3, 0x1, 0x4, 0x2, 0x5]
RC4 = [0x1, 0x8, 0x4, 0x2, 0x9, 0xc, 0x6, 0xb, 0x5, 0xa, 0xd, 0xe, 0xf, 0x7, 0x3, 0x1,
       0x8, 0x4, 0x2, 0x9, 0xc, 0x6, 0xb, 0x5, 0xa, 0xd, 0xe, 0xf, 0x7, 0x3, 0x1, 0x8]


def bin_to_nibbles(data):
    result = []
    for byte in data:
        result.append(byte >> 4)
        result.append(byte & 0xF)
    return result


def nibbles_to_bin(nibbles):
    result = []
    for i in range(0, len(nibbles), 2):
        result.append(nibbles[i] << 4 | nibbles[i + 1])
    return bytes(result)


class CraftBase:
    def MixColumn(self):
        for i in range(4):
            self.Stt[i] ^= self.Stt[i + 8] ^ self.Stt[i + 12]
            self.Stt[i + 4] ^= self.Stt[i + 12]

    def AddConstants(self, r):
        self.Stt[4] ^= RC4[r]
        self.Stt[5] ^= RC3[r]

    def AddTweakey(self, r):
        for i in range(16):
            self.Stt[i] ^= self.TK[r % 4][i]

    def Permutation(self):
        Temp = [0] * 16
        for i in range(16):
            Temp[P[i]] = self.Stt[i]

        for i in range(16):
            self.Stt[i] = S[Temp[i]]


class Encryptor(CraftBase):
    def __init__(self, key, tweak):
        self.key = [bin_to_nibbles(key[0:8]), bin_to_nibbles(key[8:16])]
        self.tweak = bin_to_nibbles(tweak)
        self.Stt = [0] * 16
        self.TK = [[0] * 16 for _ in range(4)]

        self.Initialize_key()

    def Initialize_key(self):
        for i in range(16):
            self.TK[0][i] = self.key[0][i] ^ self.tweak[i]
            self.TK[1][i] = self.key[1][i] ^ self.tweak[i]
            self.TK[2][i] = self.key[0][i] ^ self.tweak[Q[i]]
            self.TK[3][i] = self.key[1][i] ^ self.tweak[Q[i]]

    def encrypt(self, plaintext):
        self.Stt = bin_to_nibbles(plaintext)
        for r in range(32):
            self.MixColumn()
            self.AddConstants(r)
            self.AddTweakey(r)
            if r != 31:
                self.Permutation()
        return nibbles_to_bin(self.Stt)


class Decryptor(CraftBase):
    def __init__(self, key, tweak):
        self.key = [bin_to_nibbles(key[0:8]), bin_to_nibbles(key[8:16])]
        self.tweak = bin_to_nibbles(tweak)
        self.Stt = [0] * 16
        self.TK = [[0] * 16 for _ in range(4)]

        self.Initialize_key()

    def Initialize_key(self):
        for i in range(16):
            self.TK[0][i] = self.key[0][i] ^ self.tweak[i]
            self.TK[1][i] = self.key[1][i] ^ self.tweak[i]
            self.TK[2][i] = self.key[0][i] ^ self.tweak[Q[i]]
            self.TK[3][i] = self.key[1][i] ^ self.tweak[Q[i]]

        for j in range(4):
            for i in range(4):
                self.TK[j][i] ^= self.TK[j][i + 8] ^ self.TK[j][i + 12]
                self.TK[j][i + 4] ^= self.TK[j][i + 12]

    def decrypt(self, ciphertext):
        self.Stt = bin_to_nibbles(ciphertext)
        for r in range(32):
            ind = 31 - r
            self.MixColumn()
            self.AddConstants(ind)
            self.AddTweakey(ind)
            if r != 31:
                self.Permutation()
        return nibbles_to_bin(self.Stt)


def encrypt(plaintext, key, tweak):
    return Encryptor(key, tweak).encrypt(plaintext)


def decrypt(ciphertext, key, tweak):
    return Decryptor(key, tweak).decrypt(ciphertext)


def main():
    from binascii import unhexlify, hexlify

    key = unhexlify("27A6781A43F364BC916708D5FBB5AEFE")
    tweak = unhexlify("54CD94FFD0670A58")
    plaintext = unhexlify("5734F006D8D88A3E")

    ciphertext = encrypt(plaintext, key, tweak)
    assert ciphertext == unhexlify("A17D6BD4BEEB996F")

    decrypted = decrypt(ciphertext, key, tweak)
    assert decrypted == plaintext


if __name__ == "__main__":
    main()
