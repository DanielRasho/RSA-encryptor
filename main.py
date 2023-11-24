# 37 characters alphabet
from typing import Any, List


ALPHABET = {"A": 0, "B": 1, "C": 2}

##########################
## EXCEPTION DEFINITION
##########################


class NotPrimeException(Exception):
    pass


class NotPrimeRelatives(Exception):
    pass


class AlphabetToSmallOrBlockLenError(Exception):
    pass

class NotExistingCharacterInAlphabetError(Exception):
    pass

class NotExistingCodeInAlphabetError(Exception):
    pass


##########################
## MODEL CLASSES
##########################


class Alphabet(dict):
    def __init__(self, *args, **kwargs):
        super(Alphabet, self).__init__(*args, **kwargs)

        # This class has another dictionary that store a inverse dictionary
        # where key are values and viceversa.
        self.inverse = {}

        # Filling inverse dict with initial values
        for key, value in self.items():
            self.inverse.setdefault(value, key)

    def __setitem__(self, key: str, value: int):
        if key in self:
            self.inverse.__delitem__(self[key])
            super(Alphabet, self).__delitem__(key)
        if value in self.inverse:
            super(Alphabet, self).__delitem__(self.inverse[value])
            self.inverse.__delitem__(value)
        super(Alphabet, self).__setitem__(key, value)
        self.inverse.setdefault(value, key)

    def __delitem__(self, key: str):
        self.inverse.setdefault(self[key], "")
        if self[key] in self.inverse:
            del self.inverse[self[key]]
        super(Alphabet, self).__delitem__(key)

    def getCharacter(self, value: int):
        if value not in self.inverse:
            raise NotExistingCodeInAlphabetError
        return self.inverse[value]

    def getCode(self, key: str):
        if key not in self:
            raise NotExistingCharacterInAlphabetError
        return self[key]


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
        # Calculating PUBLIC KEY
        (e, n) = self.__getPublicKey(p, q, e)

        # Checking if alphabet is valid
        if not self.__isAlphabetValid(alphabet, n, blockLen):
            raise AlphabetToSmallOrBlockLenError

        # Encoding msg to its numeric equivalent
        codedMsg = self.__textToCode(msg, alphabet)
       
        # Encrypting with public key


        return "ABCFD43K2"

    def __getPublicKey(self, p: int, q: int, e: int) -> tuple[int, int]:
        if not self.mathUtils.isPrime(p) or not self.mathUtils.isPrime(q):
            raise NotPrimeException()

        l = (p - 1) * (q - 1)

        if not self.mathUtils.arePrimeRelatives(e, l):
            raise NotPrimeRelatives()

        modulus = p * q

        return (e, modulus)

    def __isAlphabetValid(self, alphabet: Alphabet, modulus:int, blockLen: int) -> bool:
        alphabetLenDigits = str(len(alphabet))
        digitsPerCharacter = len(alphabetLenDigits)

        if blockLen % digitsPerCharacter:
            return False
        
        maximumCode = int(alphabetLenDigits * (blockLen // digitsPerCharacter)) 

        if maximumCode > modulus: 
            return False
        return True

    def __textToCode(self, message: str, alphabet: Alphabet, blockLen: int) -> List[int] :
        digitsPerCharacter = self.__numDigits(len(alphabet))
        charactersPerBlock = blockLen // digitsPerCharacter

        # Complete message if missing characters
        completedMsg = message
        missingCharacters = len(message) % charactersPerBlock
        if missingCharacters != 0: 
            completedMsg += alphabet.getCharacter(0) * missingCharacters 
        
        # Returning values 
        encodedMsg = []
        for index in range(0, len(completedMsg), charactersPerBlock): 
            textBlock = completedMsg[index:index + charactersPerBlock]
            print(textBlock)
            codedBlock = ""
            for letter in textBlock:
                code = alphabet.getCode(letter)
                if self.__numDigits(code) < digitsPerCharacter:
                    code = ("0" * (self.__numDigits(code) % charactersPerBlock)) + str(code)
                codedBlock += code
            encodedMsg.append(int(codedBlock))

        return encodedMsg

    def __numDigits(self, num : int) -> int:
        return len(str(num))


class Decryptor:
    def decrypt(self, msg: str, e: int, n: int, alphabet: Alphabet, blockLen: int) -> str:
        return "HELLO WORLD"

##################
# ALPHABETS
##################

BASIC_ALPHABET = Alphabet(
    dict(
        [(chr(code), code - ord("A")) for code in range(ord("A"), ord("Z") + 1)]
    )
)

COMPLETE_ALPHABET = Alphabet(
    dict(
        [("*", 0)] + 
        [(chr(code), code - ord("A") + 1) for code in range(ord("A"), ord("Z") + 1)] +
        [(chr(code), code - ord("0") + 27) for code in range(ord("0"), ord("9") + 1)]
    )
)

def main():
    e = Encryptor()


if __name__ == "__main__":
    main()
