from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, MonthField, EmailField, DateField, IntegerField
from wtforms.fields.simple import PasswordField

class CreateLoginForm(Form):
    email = EmailField("Email:", [validators.Email(), validators.DataRequired()])
    password = PasswordField("Password:", [validators.DataRequired()])

class CreateSignUpForm(Form):
    username = StringField("Username:", [validators.DataRequired()])
    email = EmailField("Email:", [validators.Email(), validators.DataRequired()])
    password = PasswordField("Password:", [validators.Length(min=10, max=20), validators.DataRequired()])
    password_confirm = PasswordField("Confirm Password:", [validators.Length(min=10, max=20), validators.DataRequired()])

class CreateAddPaymentForm(Form):
    card_name = StringField("Card Name:", [validators.Length(min=1, max=150), validators.DataRequired()])
    card_no = IntegerField("Card Number:", [validators.Length(min=0, max=16), validators.DataRequired()])
    card_expiry = MonthField("Expiry Date:", [validators.DataRequired()])
    card_CVV = IntegerField("CVV:", [validators.NumberRange(min=0, max=3), validators.DataRequired()])

class CreateAddShippingAddressForm(Form):
    shipping_address = StringField("Shipping Address: ", [validators.DataRequired()])
    postal_code = IntegerField("Postal Code: ",[validators.NumberRange(min=0, max=6)] , [validators.DataRequired()])
    unit_number = StringField("Unit Number: ",[validators.NumberRange(min=5, max=6)], [validators.DataRequired()])
    phone_no = IntegerField("Phone Number: ",[validators.NumberRange(min=0, max=8)], [validators.DataRequired()])

class CreateStaffMemberForm(Form):
    staff_name = StringField("Staff Name:", [validators.DataRequired()])
    staff_email = EmailField("Email:", [validators.Email(), validators.DataRequired()])