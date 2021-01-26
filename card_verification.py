from exceptions import MessageBadRequest
import re
from datetime import date
#The card no is varified  using Luhn algorithm.
#Not using for perticular type of card
def vefify_card_no(CreditCardNumber):
    if not CreditCardNumber.isdigit():
        return False

    if(len(CreditCardNumber)<10):
        return False
    if len(CreditCardNumber)>16 or len(CreditCardNumber)<13:
        return False


    sumOfOddPlace = 0
    for i in range(len(CreditCardNumber) - 1, -1, -2):
        digit = (int(CreditCardNumber[i]))
        sumOfOddPlace += digit
    print(sumOfOddPlace)

    sumOfDoubleEvenPlace = 0
    for i in range(len(CreditCardNumber) - 2, -1, -2):
        digit = (int(CreditCardNumber[i])) * 2
        if (len(str(digit)) > 1):
            digit = (digit % 10) + (digit // 10)
        sumOfDoubleEvenPlace += digit

    if (sumOfDoubleEvenPlace+sumOfOddPlace)%10 == 0:
        return True;

def verify_name(CardHolder):
    cardholder_name = re.compile(r'([a-z]+)( [a-z]+)*( [a-z]+)*$', re.IGNORECASE)
    res = cardholder_name.search(CardHolder)
    return res

def verify_expiry_date(ExpirationDate):
    today_date = str(date.today()).replace('-', '')
    today_year = today_date[2:4]
    today_month = today_date[4:6]

    expiration_date =str(ExpirationDate)
    expiry_month = expiration_date[0:2];
    expiry_year = expiration_date[3:5]

    if int(expiry_year) < int(today_year):
        return False
    elif int(expiry_year) == int(today_year) and int(expiry_month) < int(today_month):
        return False

    return True

def verify_security_code(SecurityCode):
    if len(SecurityCode) == 3:
        return True
    return False

def verify_card_details(card_obj):
    CreditCardNumber = card_obj.CreditCardNumber
    CardHolder = card_obj.CardHolder
    ExpirationDate = card_obj.ExpirationDate
    SecurityCode = card_obj.SecurityCode
    if not vefify_card_no(CreditCardNumber):
        raise MessageBadRequest("Card No is Not Valid ",status_code=400)
    if verify_name(CardHolder) is None:
        raise MessageBadRequest("Card Name is Not Valid ",status_code=400)
    if not verify_expiry_date(ExpirationDate):
        raise  MessageBadRequest("This card is expired",status_code=400)
    if SecurityCode:
        if not verify_security_code(SecurityCode):
            raise MessageBadRequest("Enter valid Security Code",status_code=400)
    return True
