# 37 characters alphabet
ALPHABET = {"A": 0, "B": 1, "C": 2}

##########################
## EXCEPTION DEFINITION
##########################


class NotPrimeException(Exception):
    pass

class NotPrimeRelatives(Exception):
    pass

class AlphabetToSmallError(Exception):
    pass

class NotExistingCharacterInAlphabetError(Exception):
    pass


##########################
## MODEL CLASSES
##########################


class Alphabet(dict):
    def __init__(self, *args, **kwargs):
        super(Alphabet, self).__init__(*args, **kwargs)
        self.inverse = {}
        for key, value in self.items():
            self.inverse.setdefault(value, []).append(key)

    def __setitem__(self, key, value):
        if key in self:
            self.inverse[self[key]].remove(key)
        super(Alphabet, self).__setitem__(key, value)
        self.inverse.setdefault(value, []).append(key)

    def __delitem__(self, key):
        self.inverse.setdefault(self[key], []).remove(key)
        if self[key] in self.inverse and not self.inverse[self[key]]:
            del self.inverse[self[key]]
        super(Alphabet, self).__delitem__(key)


##########################
## LOGIC CLASSES
##########################


class MathUtils:
    def isPrime(self, a: int) -> bool:
        return True

    def arePrimeRelatives(self, a: int, b: int) -> bool:
        return True

    def getInverseModulus(self, n: int, modulus: int) -> int:
        return 0

    def getExponentModulus(self, n: int, exponent: int, modulus: int) -> int:
        return 0

    def __EuclidesDecomposition(self, a: int, b: int) -> int:
        return 0

    def __BezautComposition(self, a: int, b: int) -> tuple[int, int]:
        return (0, 0)


class Encryptor:
    mathUtils = MathUtils()

    def encrypt(
        self, msg: str, p: int, q: int, e: int, alphabet: Alphabet, blockLen: int
    ) -> str:
        publicKey = self.__getPublicKey(p, q, e)

        return ""

    def __getPublicKey(self, p: int, q: int, e: int) -> tuple[int, int]:
        if not self.mathUtils.isPrime(p) or not self.mathUtils.isPrime(q):
            raise NotPrimeException()

        l = (p - 1) * (q - 1)

        if not self.mathUtils.arePrimeRelatives(l, e):
            raise NotPrimeRelatives()

        modulus = p * q

        return (e, modulus)

    def __isAlphabetValid(self, alphabet : Alphabet, blockLen: int)-> bool:
        return True


class Decryptor:
    def decrypt(self, msg: str, e: int, n: int) -> str:
        return ""


def main():
    pass


if __name__ == "__main__":
    main()
