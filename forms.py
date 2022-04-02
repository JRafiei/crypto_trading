from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired


class OrderForm(FlaskForm):

    order_type = RadioField(
        'Order Type',
        [DataRequired()],
        choices=[
            ("sell", "Sell"),
            ("buy", "Buy")
        ]
    )
    condition = SelectField(
        'Condition',
        [DataRequired()],
        choices=[
            ("up", "Crossing Up"),
            ("down", "Crossing Down")
        ]
    )
    amount = FloatField('Amount', [DataRequired()])
    price = FloatField('price', [DataRequired()])
    src_currency = SelectField('Source Currency', [DataRequired()], choices=[])
    dst_currency = SelectField('Target Currency', [DataRequired()], choices=[])
    submit = SubmitField('Submit')
