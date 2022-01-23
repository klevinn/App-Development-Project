from wtforms import Form, StringField, RadioField, SelectField, TextAreaField
from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, DateField, IntegerField
from wtforms import validators
from wtforms.fields.html5 import EmailField, DateField
from flask import Flask
from flask_bootstrap import Bootstrap
from wtforms.fields.html5 import DateField
from flask_wtf import Form
from wtforms import TextField, BooleanField, PasswordField, TextAreaField, validators
from wtforms.validators import ValidationError
from wtforms.fields import DateField
from wtforms_components import DateRange
from datetime import datetime, date
from wtforms import Form
from wtforms.fields import DateField
from wtforms_components import DateRange
from datetime import datetime


app=Flask(__name__)
bootstrap=Bootstrap(app)


class CreateForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired(), ])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    date_joined = DateField('Date of appointment(YY-MM-DD)', format='%Y-%m-%d',validators=[DateRange(min=date.today())])

    remarks = TextAreaField('Additional request', [validators.Optional()])
    doc=RadioField('Choice of doctor', choices=[('T', 'Dr Tan'), ('M', 'Dr Mok'), ('L', 'Dr Lim')], default='T')


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

class CreateEmailForm(Form):
    email = EmailField("Email:", [validators.Email(), validators.DataRequired()])

class CreateResetPWForm(Form):
    email = EmailField("Email:", [validators.Email(), validators.DataRequired()])
    new_password = PasswordField("Password:", [validators.Length(min=6, max=20), validators.DataRequired()])
    confirm_password = PasswordField("Confirm Password:", [validators.Length(min=6, max=20), validators.DataRequired()])
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




