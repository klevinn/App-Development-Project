# using Luhn's Algorithms 
"""
Outline of Luhn's Algo:
Start from Last Digit:
x2 Odd Digits:
If resulting number of the x2 is a double digit, add both digits together
Then add all the final digits together
If divisible by 10, it is valid
"""


def IntegerList(credit_card_number):
    try:
        x = [int(a) for a in str(credit_card_number)]
        return x
    except:
        x = ""
        return x


def validate_card_number(credit_card_number):
    card_num_digits = IntegerList(credit_card_number)
    if card_num_digits=="":
        print("Blank Card")
        return True
    else:
        #Start from the most right and move in 2s
        odd_digits = card_num_digits[-1::-2]
        print(odd_digits)

        #Start from second most right digit and move in 2s
        even_digits = card_num_digits[-2::-2]
        print(even_digits)

        odd_digits_sum = 0
        odd_digits_sum = sum(odd_digits)
        print(odd_digits_sum)
        even_digits_sum = 0

        for digit in even_digits:
            digit = digit * 2
            if digit >= 10:
                digitList = IntegerList(digit)
                digitSum = sum(digitList)
                even_digits_sum += digitSum
            else:
                even_digits_sum += digit
        
        print(even_digits_sum)
        total_sum = even_digits_sum + odd_digits_sum
        valid_card = total_sum % 10
        if valid_card == 0:
            return True
        else:
            return False

"""
Testing Codes
print(IntegerList(12334))
validate_card_number(12395)
print(validate_card_number(12395))
"""

def Sanitise(stringInput):
    stringInput = stringInput.strip()
    return stringInput