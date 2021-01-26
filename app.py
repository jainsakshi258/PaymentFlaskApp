from flask import Flask, request ,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from exceptions import  MessageBadRequest
from card_verification import verify_card_details
from external_service import PaymentService
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
#init app
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

#databse
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'db.sqllite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

#init
ma = Marshmallow(app)

class CardDetails:
    id = db.Column(db.Integer, primary_key=True)
    CreditCardNumber = db.Column(db.String(100))
    CardHolder = db.Column(db.String(100))
    ExpirationDate = db.Column(db.DateTime)
    SecurityCode = db.Column(db.String(200))
    Amount= db.Column(db.Float)

    def __init__(self,CreditCardNumber,CardHolder,ExpirationDate,SecurityCode,Amount):
        self.CreditCardNumber = CreditCardNumber
        self.CardHolder = CardHolder
        self.ExpirationDate = ExpirationDate
        self.SecurityCode = SecurityCode
        self.Amount = Amount

class CardSchema(ma.Schema):
    class Meta:
        fields=("CreditCardNumber", "CardHolder", "ExpirationDate", "SecurityCode", "Amount")


card_schema=CardSchema()

# registering error handling

@app.errorhandler(MessageBadRequest)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


#create a product
@app.route('/pay',methods=['post'])
def ProcessPayment():
    if 'CreditCardNumber' in request.json:
        CreditCardNumber = request.json['CreditCardNumber']
    else:
        raise MessageBadRequest("Please enter card No",status_code=400)

    if 'CardHolder' in request.json:
        CardHolder = request.json['CardHolder']
    else:
        raise MessageBadRequest("Please enter credit your name",status_code=400)

    if 'ExpirationDate' in request.json:
        ExpirationDate = request.json['ExpirationDate']
    else:
        raise MessageBadRequest("Please enter Expiry date",status_code=400)

    if 'SecurityCode' in request.json:
        SecurityCode = request.json['SecurityCode']
    else:
        SecurityCode = ''

    if 'Amount' in request.json and str(request.json['Amount']).isdigit() and  request.json['Amount'] >0 :
        Amount = request.json['Amount']
    else:
        raise MessageBadRequest("Please enter valid positive Amount",status_code=400)

    card_obj = CardDetails(CreditCardNumber,CardHolder,ExpirationDate,SecurityCode,Amount)
    msg= verify_card_details(card_obj)

    if msg is not True:
        return msg

    payment_status = PaymentService.process_payment(card_obj)
    return payment_status


if __name__=='__main__':
    app.run(debug=True)
