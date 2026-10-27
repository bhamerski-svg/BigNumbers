# Simone Pastore 35049968 and Bryan Hamerski 35082532


class Link:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

    def __str__(self):
      return str(self.data)
  
class BigNumberLL: ### To complete
    def __init__(self, number=""):
        self.first = None
        self.last = None
        self.size = 0
        self.positive = True
        if number and number[0] == '-':
            self.positive = False
            number = number[1:]    # '-' is number[0], so number[1:] is only the digits
        for digit in number:
            self.insertLast(int(digit))

        self.trimFront()

        if self.size == 1 and self.first.data == 0:  # zero is always positive
            self.positive = True

    def insertLast(self, digit):
        newLink = Link(digit)
        if self.first is None:
            self.first = newLink
            self.last = newLink
        else:
            newLink.prev = self.last
            self.last.next = newLink
            self.last = newLink
        self.size += 1

    def insertFirst(self, digit):
        newLink = Link(digit)
        if self.first is None:
            self.first = newLink
            self.last = newLink
        else:
            newLink.next = self.first
            self.first.prev = newLink
            self.first = newLink
        self.size += 1

    def deleteFirst(self):
        if self.size == 1:
            self.first = None
            self.last = None
        else:
            self.first = self.first.next
            self.first.prev = None
        self.size -= 1

    def trimFront(self):    # removes leading zeros
        while self.size > 1 and self.first.data == 0:  # keeps at least one digit, EX: 0000 --> 0
            self.deleteFirst()

    def __str__(self):
        stringNum = ""
        current = self.last
        count = 0

        while current is not None:    
            stringNum = str(current.data) + stringNum   # adds current digit to front of string
            count += 1

            if count % 3 == 0 and current.prev is not None:   # add comma after 3 digits
                stringNum = "," + stringNum

            current = current.prev

        if self.positive == False:
            stringNum = "-" + stringNum   # adds negative sign to the front if number is negative
        
        return f"[{self.size}] {stringNum}"       

    def __gt__(self, other):
    # If self is positive and other is negative, self is greater
        if self.positive and not other.positive:
            return True

        # If self is negative and other is positive, self is smaller
        if not self.positive and other.positive:
            return False

        # Same sign, but different number of digits
        if self.size != other.size:

            # Both positive: more digits means greater
            if self.positive:
                return self.size > other.size

            # Both negative: fewer digits means greater
            else:
                return self.size < other.size

        # Same sign and same number of digits:
        # compare digit by digit from left to right
        current1 = self.first
        current2 = other.first

        while current1 is not None:
            if current1.data != current2.data:
                # Both positive: larger digit means greater
                if self.positive:
                    return current1.data > current2.data
                # Both negative: smaller digit means greater
                else:
                    return current1.data < current2.data

            current1 = current1.next
            current2 = current2.next

        # If every digit matched, the numbers are equal
        return False

    def __lt__(self, other):
        # self < other is the same as other > self
        return other > self   

    def __eq__(self, other):
        # Equal if neither number is greater than the other
        return not (self > other) and not (other > self)

    def addPos(self, other):
        result = BigNumberLL()
        selfCurrent = self.last
        otherCurrent = other.last
        carry = 0

        while selfCurrent is not None or otherCurrent is not None:

            if selfCurrent is not None:
                digitSelf = selfCurrent.data
            else:
                digitSelf = 0

            if otherCurrent is not None:
                digitOther = otherCurrent.data
            else:
                digitOther = 0
            
            total = digitSelf + digitOther + carry

            newDigit = total % 10
            carry = total // 10

            result.insertFirst(newDigit)

            if selfCurrent is not None:
                selfCurrent = selfCurrent.prev
            if otherCurrent is not None:
                otherCurrent = otherCurrent.prev

        if carry == 1:
            result.insertFirst(carry)

        result.trimFront()
        return result

    def subPos(self, other):
        if self.size != other.size:
            smaller = self.size < other.size
        else:
            selfCurrent = self.first
            otherCurrent = other.first
            smaller = False

            while selfCurrent is not None:
                if selfCurrent.data != otherCurrent.data:
                    smaller = selfCurrent.data < otherCurrent.data
                    break

                selfCurrent = selfCurrent.next
                otherCurrent = otherCurrent.next

        if smaller:
            temp = other.subPos(self)
            temp.positive = False
            return temp

        result = BigNumberLL()
        selfCurrent = self.last
        otherCurrent = other.last
        borrow = 0

        while selfCurrent is not None:
            if otherCurrent is not None:
                digitOther = otherCurrent.data
            else:
                digitOther = 0

            digitSelf = selfCurrent.data
            difference = digitSelf - digitOther - borrow

            if difference < 0:
                borrow = 1
                difference += 10
            else:
                borrow = 0

            result.insertFirst(difference)

            selfCurrent = selfCurrent.prev
            if otherCurrent is not None:
                otherCurrent = otherCurrent.prev

        result.trimFront()
        return result

    def __add__(self,other):
        # +self + +other
        if self.positive and other.positive:
            return self.addPos(other)

        # +self + -other
        elif self.positive and not other.positive:
            return self.subPos(other)

        # -self + +other
        elif not self.positive and other.positive:
            return other.subPos(self)

        # -self + -other
        else:
            result = self.addPos(other)
            if result.size == 1 and result.first.data == 0:
                result.positive = True
            else:                
                result.positive = False
        
            return result

    def __sub__(self, other):
        # +self - +other
        if self.positive and other.positive:
            return self.subPos(other)

        # +self - -other
        elif self.positive and not other.positive:
            return self.addPos(other)

        # -self - +other
        elif not self.positive and other.positive:
            result = self.addPos(other)
            result.positive = False
            return result

        # -self - -other
        else:
            return other.subPos(self)

    def scale(self, factor):
        result = BigNumberLL()
        current = self.last
        carry = 0

        while current is not None:
            total = current.data * factor + carry
            newDigit = total % 10  # gives rightmost value
            carry = total // 10   

            result.insertFirst(newDigit)
            current = current.prev

        if carry > 0:
            result.insertFirst(carry)

        result.trimFront()
        return result

    def __mul__(self, other):
        result = BigNumberLL("0")
        current = other.last
        shift = 0
        while current is not None:
            partial = self.scale(current.data)
            for i in range(shift):
                partial.insertLast(0)
            result += partial
            current = current.prev
            shift += 1
        result.trimFront()
        if self.positive != other.positive and result.first.data != 0:
            result.positive = False
        return result

    # BONUS
    def __floordiv__(self, other):
        # Cannot divide by zero
        if other.size == 1 and other.first.data == 0:
            raise ZeroDivisionError("Cannot divide by zero")

        # Converts the BigNumber digits into integers
        num1 = 0
        current = self.first

        while current is not None:
            num1 = num1 *1 0 + current.data
            current = current.next

        num2 = 0
        current = other.first

        while current is not None:
            num2 = num2 * 10 + current.data
            current = current.next

        if not self.positive:
            num1 = -num1

        if not other.positive:
            num2 = -num2

        # integer floor division
        quotient = num1 // num2

        # converts answer back into a BigNumberLL
        result = BigNumberLL(str(quotient))
        return result
