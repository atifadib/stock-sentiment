from wtforms import Form, FloatField, validators

class InputForm(Form):
    btc = FloatField(
        label='quote', default=1.0,
        validators=[validators.InputRequired()])