from typing import List
import importlib.util
import sys
import subprocess

module_name = 'PyQt5'

spec = importlib.util.find_spec(module_name)

if spec is None:
    print(f'The {module_name} module is NOT installed')

    # 👇️ optionally install the module if it's not installed
    python = sys.executable
    subprocess.check_call(
        [sys.executable, '-m', 'pip', 'install', module_name],
        stdout=subprocess.DEVNULL
    )

    print(f'The {module_name} module is now installed')

from PyQt5 import QtWidgets, uic

##########################
## EXCEPTION DEFINITION
##########################


class NotPrimeException(Exception):
    pass

class NotPrimeRelatives(Exception):
    pass

class AlphabetToBigOrBlockLenError(Exception):
    pass

class NotExistingCharacterInAlphabetError(Exception):
    pass

class NotExistingCodeInAlphabetError(Exception):
    pass

class IncompleteBlocksOnMsg(Exception):
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
    def isPrime(self, n: int) -> bool:
        # Cheking the simple cases
        if n <= 1:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        
        i = 5 # Starting point
        w = 2 # For skiping even numbers
        
        while i * i <= n:
            if n % i == 0:
                return False
            i += w
            w = 6 - w
        
        return True

    def arePrimeRelatives(self, a: int, b: int) -> bool:
        return self.__EuclidesGCD(a, b) == 1
    
    def getInverseModulus(self, n: int, modulus: int) -> int:
        g, x, _ = self.__EuclidesGCDExtended(n, modulus)
        if g != 1:
            raise ValueError(f"The modular inverse does not exist for {n} mod {modulus}.")
        else:
            return x % modulus

    def getPowerOnModulus(self, base: int, exponent: int, modulus: int) -> int:
            if exponent == 0:
                return 1
            elif exponent % 2 == 0:
                # If exponent is even, use the property a^(2n) = (a^n)^2
                temp = self.getPowerOnModulus(base, exponent // 2, modulus)
                return (temp * temp) % modulus
            else:
                # If exponent is odd, use the property a^(2n+1) = a * a^(2n)
                temp = self.getPowerOnModulus(base, (exponent - 1) // 2, modulus)
                return (base * temp * temp) % modulus

    def primeFactorization(self, n) -> List[int]:
        factors = []
        # Divide by 2 until it's an odd number
        while n % 2 == 0:
            factors.append(2)
            n = n // 2

        # Divide by odd numbers starting from 3
        for i in range(3, int(n**0.5) + 1, 2):
            while n % i == 0:
                factors.append(i)
                n = n // i

        # If n is a prime number greater than 2
        if n > 2:
            factors.append(n)

        return factors

    def __EuclidesGCD(self, a: int, b: int) -> int:
        while b:
            a, b = b, a % b
        return a
    
    def __EuclidesGCDExtended(self, a: int, b: int) -> int:
        if a == 0:
            return (b, 0, 1)
        else:
            g, x, y = self.__EuclidesGCDExtended(b % a, a)
            return (g, y - (b // a) * x, x)


class Encryptor:
    mathUtils = MathUtils()

    def encrypt(
        self, msg: str, p: int, q: int, e: int, alphabet: Alphabet, blockLen: int
    ) -> str:
        # Calculating PUBLIC KEY
        (e, n) = self.__getPublicKey(p, q, e)

        # Checking if alphabet is valid
        if not self.__isAlphabetValid(alphabet, n, blockLen):
            raise AlphabetToBigOrBlockLenError

        # Encoding msg to its numeric equivalent
        encodedMsg = self.__textToCode(msg, alphabet, blockLen)
        print(encodedMsg)

        # Encrypting with public key
        encryptedBlocks = []
        for block in encodedMsg:
            encryptedBlock = self.mathUtils.getPowerOnModulus(block,e,n)
            # Fill block if missing digits
            if len(str(encryptedBlock)) < blockLen:
                encryptedBlocks.append("0" * (blockLen - len(str(encryptedBlock))) + str(encryptedBlock))
            else:
                encryptedBlocks.append(str(encryptedBlock))

        return " ".join(encryptedBlocks)

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
        
        # Returning numeric values 
        encodedMsg = []
        for index in range(0, len(completedMsg), charactersPerBlock): 
            textBlock = completedMsg[index :index + charactersPerBlock]
            print(textBlock)
            codedBlock = ""
            for letter in textBlock:
                code = alphabet.getCode(letter)
                if self.__numDigits(code) < digitsPerCharacter:
                    code = ("0" * (self.__numDigits(code) % charactersPerBlock)) + str(code)
                codedBlock += str(code)
            encodedMsg.append(int(codedBlock))

        return encodedMsg

    def __numDigits(self, num : int) -> int:
        return len(str(num))


class Decryptor:

    mathUtils = MathUtils()

    def decrypt(self, msg: str, e: int, n: int, alphabet: Alphabet, blockLen: int) -> str:
        
        # Check message integrity
        if len(msg) % blockLen != 0:
            raise IncompleteBlocksOnMsg
        if blockLen % self.__numDigits(len(alphabet)) != 0:
            raise AlphabetToBigOrBlockLenError
        
        # Calculating modulus
        modulus = self.__getModulus(n)

        # Calculating private key
        d = self.mathUtils.getInverseModulus(e, modulus)

        # Divide msg in blocks
        blocks = self.__msgToCodeBlocks(msg, blockLen)

        # Decrypt blocks
        for index in range(0, len(blocks)):
            blocks[index] = self.mathUtils.getPowerOnModulus(blocks[index], d, n)
        print(blocks)

        # Filling with 0, for numbers with less digits than blockLen
        for index in range(0, len(blocks)):
            blocks[index] = ("0" * (self.__numDigits(blocks[index]) % blockLen)) + str(blocks[index])
        
        # Translate blocks to text equivalent
        return self.__codeToText(blocks, alphabet, blockLen)
    
    def __getModulus(self, n):
        primeFactors = self.mathUtils.primeFactorization(n)
        if len(primeFactors) != 2:
            raise ValueError("n must be a multiplication of just TWO prime numbers")
        return (primeFactors[0] - 1)*(primeFactors[1] - 1)
    
    def __msgToCodeBlocks(self, msg: str, blockLen: int) -> List[int] :
        blocks = []
        for index in range(0, len(msg), blockLen):
            blocks.append(int(msg[index : index + blockLen]))
        return blocks

    def __codeToText(self, blocks: List[str], alphabet: Alphabet, blockLen:int) -> str:
        digitsPerCharacter = self.__numDigits(len(alphabet))
        charactersPerBlock = blockLen // digitsPerCharacter
        characters = []

        for block in blocks:
            for index in range(0, blockLen, charactersPerBlock):
                code = int(block[index: index + charactersPerBlock])
                characters.append(alphabet.getCharacter(code))
        
        return "".join(characters)

    def __numDigits(self, num : int) -> int:
        return len(str(num))



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

ALPHABET_CHOICES = [BASIC_ALPHABET, COMPLETE_ALPHABET]

##########################
## GUI IMPLEMENTATION
##########################


class RSASystem(QtWidgets.QMainWindow):
    decryptor = Decryptor()
    encryptor = Encryptor()

    def __init__(self):
        super(RSASystem, self).__init__()
        uic.loadUi('UI.ui', self)
        self.setUpEncrypted()
        self.setUpComboBox()

        self.btnOperate.clicked.connect(self.operate)
        self.btnClean.clicked.connect(self.clean)
        self.rbEncrypt.clicked.connect(self.setUpEncrypted)
        self.rbDecrypt.clicked.connect(self.setUpDecrypted)
        self.btnSTM.clicked.connect(self.sendText)

    def operate(self):

        if(self.rbEncrypt.isChecked()):
            try:
                msg = self.txtMessage.text().upper().replace(" ", "")
                p = int(self.txtPrime1.text())
                q = int(self.txtPrime2.text())
                e = int(self.txtPrime3.text())
                alphabet = ALPHABET_CHOICES[self.cmbAlphabet.currentIndex()]
                result = self.encryptor.encrypt(msg, p, q, e, alphabet, 4)
                self.txtResult.setText(result)
            except ValueError:
                self.showAlert("Invalid Input. Please enter valid numbers")
            except:
                self.showAlert("This action cannot be performed")

        elif(self.rbDecrypt.isChecked()):
            try:
                msg = self.txtMessage.text().upper().replace(" ","")
                e = int(self.txtPrime1.text())
                n = int(self.txtPrime2.text())
                alphabet = ALPHABET_CHOICES[self.cmbAlphabet.currentIndex()]
                result = self.decryptor.decrypt(msg, e, n, alphabet, 4)
                self.txtResult.setText(result)
            except ValueError:
                self.showAlert("Invalid Input. Please enter valid numbers")
            except:
                self.showAlert("This action cannot be performed")
        pass
    
    def sendText(self):
        self.txtMessage.setText(self.txtResult.text())
        self.txtResult.clear()
    
    def clean(self):
        widgets_to_clear = [
            self.txtPrime1, self.txtPrime2,
            self.txtPrime3, self.txtResult, self.txtPrivKey
        ]
        for widget in widgets_to_clear:
            widget.clear()

    def setVisibility(self, label, widget, show):
        label.setVisible(show)
        widget.setVisible(show)

    def setUpEncrypted(self):
        self.clean()
        self.lblResult.setText("Encrypted Message (C)")
        self.setVisibility(self.lblPrivKey, self.txtPrivKey, False)
        self.setVisibility(self.lblPrime3, self.txtPrime3, True)
        self.lblPrime1.setText("Prime (p)")
        self.lblPrime2.setText("Prime (q)")
        self.lblPrime3.setText("Prime (e)")

    def setUpDecrypted(self):
        self.clean()
        self.lblResult.setText("Decrypted Message (M)")
        self.setVisibility(self.lblPrivKey, self.txtPrivKey, True)
        self.setVisibility(self.lblPrime3, self.txtPrime3, False)
        self.lblPrime1.setText("Prime (e)")
        self.lblPrime2.setText("Prime (n)")

    def setUpComboBox(self):
        self.cmbAlphabet.addItems(["Basic (26)","Complete (37)"])
        self.cmbAlphabet.setCurrentIndex(0)

    def showAlert(self, description):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(description)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg_box.exec_()


def main():
    e = Decryptor()
    a = Encryptor()
    print(e.decrypt("20062830135311360457", 85, 3551, BASIC_ALPHABET, 4))
    app = QtWidgets.QApplication(sys.argv)
    window = RSASystem()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
