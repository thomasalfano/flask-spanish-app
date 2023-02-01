from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, BooleanField, widgets, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, InputRequired


class MultiCheckBox(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class InfinitiveForm(FlaskForm):
    infinitive = StringField('Infinitive', validators=[DataRequired()])
    form = SelectField('Form', choices=[], validators=[InputRequired()])


class CreateSetForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    tenses = MultiCheckBox('Tenses', choices=[])
    infinitives = MultiCheckBox('Infinitives', choices=[])

