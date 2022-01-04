from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, MonthField, EmailField, DateField, IntegerField
from wtforms.fields.simple import PasswordField

#Form Validation for all Forms in the website


# Done By Calvin
class CreateLoginForm(Form):
    email = EmailField("Email:", [validators.Email(), validators.DataRequired()])
    password = PasswordField("Password:", [validators.DataRequired()])

class CreateSignUpForm(Form):
    username = StringField("", [validators.DataRequired()])
    email = EmailField("Email:", [validators.Email(), validators.DataRequired()])
    password = PasswordField("Password:", [validators.Length(min=6, max=20), validators.DataRequired()])
    password_confirm = PasswordField("Confirm Password:", [validators.Length(min=6, max=20), validators.DataRequired()])

class CreateAddPaymentForm(Form):
    card_name = StringField("Card Name:", [validators.Length(min=1, max=150)])
    card_no = IntegerField("Card Number:", [validators.NumberRange(min=0, max=9999999999999999)])
    #some browsers dont support monthfields
    #card_expiry = MonthField("Expiry Date:")
    card_expiry_month = IntegerField("", [validators.NumberRange(min=0, max=12)])
    card_expiry_year = IntegerField("", [validators.NumberRange(min=0, max=9999)])
    card_CVV = IntegerField("CVV:", [validators.NumberRange(min=0, max=999)])

#Labels are empty, because of form related css, they intefere with design
class CreateAddShippingAddressForm(Form):
    shipping_address = StringField("")
    postal_code = IntegerField("",[validators.NumberRange(min=0, max=999999)])
    unit_number1 = IntegerField("",[validators.NumberRange(min=0, max=99)])
    unit_number2 = IntegerField("",[validators.NumberRange(min=0, max=99)])
    phone_no = IntegerField("",[validators.NumberRange(min=0, max=99999999)])

class CreateStaffMemberForm(Form):
    staff_name = StringField("Staff Name:", [validators.DataRequired()])
    staff_email = EmailField("Email:", [validators.Email(), validators.DataRequired()])

class CreateUserInfoForm(Form):
    new_username = StringField("", [validators.DataRequired()])
    new_email = EmailField("Email:", [validators.Email(), validators.DataRequired()])

"""
class CreateUserCardInfoForm(Form):
    new_card_name = StringField("Card Name:", [validators.Length(min=1, max=150)],  [validators.DataRequired()])
    new_card_no = IntegerField("Card Number:", [validators.NumberRange(min=0, max=9999999999999999)] , [validators.DataRequired()])
    new_card_expiry = MonthField("Expiry Date:" , [validators.DataRequired()])
    new_card_CVV = IntegerField("CVV:", [validators.NumberRange(min=0, max=999)] , [validators.DataRequired()])
"""
"""
class CreateUserAddressInfoForm(Form):
    shipping_address = StringField("Shipping Address: ",  [validators.DataRequired()])
    postal_code = IntegerField("Postal Code: ",[validators.NumberRange(min=0, max=999999)],  [validators.DataRequired()])
    unit_number = StringField("Unit Number: ",[validators.NumberRange(min=5, max=6)],  [validators.DataRequired()])
    phone_no = IntegerField("Phone Number: ",[validators.NumberRange(min=0, max=99999999)],  [validators.DataRequired()])
"""

class CreateNewPasswordForm(Form):
    old_password = PasswordField("Password:", [validators.Length(min=6, max=20)])
    password = PasswordField("Password:", [validators.Length(min=6, max=20)])
    password_confirm = PasswordField("Confirm Password:", [validators.Length(min=6, max=20)])


#Done By