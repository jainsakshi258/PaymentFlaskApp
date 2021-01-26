from card_verification import verify_card_details
class external_services:
    def __init__(self, repeat=0):
        self.repeat=repeat

    def __repr__(self):
        return f'{{}}'.format("BasePaymentGateway")

    def send(self,card_obg):
        print("gateway: ",repr(self))
        if verify_card_details(card_obg):
            return True;

    def pay_via_exernal_services(self,card_oj):
        while self.repeat>=0:
            if self.send(card_oj):
                return "Payment Successful"
            self.repeat-=1;
        return "Payment Failed"


class PremiumBasePaymentGateway(external_services):
    def __init__(self, repeat=3):
        super().__init__(repeat)

    def __repr__(self):
        return f'{{}}'.format("PremiumBasePaymentGateway Called")


class ExpensiveBasePaymentGateway(external_services):
    def __init__(self, repeat=1):
        super().__init__(repeat)

    def __repr__(self):
        return f'{{}}'.format("PremiumBasePaymentGateway Called")


class CheapBasePaymentGateway(external_services):
    def __init__(self, repeat=0):
        super().__init__(repeat)

    def __repr__(self):
        return f'{{}}'.format("CheapBasePaymentGateway Called")


class PaymentService:
    def process_payment(card_obj):
        try:
            if card_obj.Amount <= 20:
                service = CheapBasePaymentGateway()
            elif 20 < card_obj.Amount < 500:
                service = ExpensiveBasePaymentGateway()
            elif card_obj.Amount >= 500:
                service = PremiumBasePaymentGateway()
            else:
                return False

            status = service.pay_via_exernal_services(card_obj)
            print(status,"sakshi jain")
            return status
        except:
            return False
