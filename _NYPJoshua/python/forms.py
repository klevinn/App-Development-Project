"""
#Done By Joshua
# only one form since i am reusing the same form for editing product

class CreateProduct(Form):
    img_file_name = StringField("Filename:", [validators.DataRequired()])
    name = StringField("Product Name:", [validators.DataRequired()])
    price = FloatField("Product Price($):", [validators.DataRequired()])
    category = StringField("Product Category:", [validators.DataRequired()])
    short_description = StringField("Short Description:", [validators.DataRequired()])
    long_description = TextAreaField("Long Description:", [validators.DataRequired()])
    stock = IntegerField("Stock:", [validators.DataRequired()])
    picture = FileField('Upload Product Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])

#Done by Joshua end
"""