from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, widgets, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, InputRequired


class MultiCheckBox(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class InfinitiveForm(FlaskForm):
    infinitive = TextAreaField('Infinitive', validators=[DataRequired()])
    form = SelectField('Form', choices=[], validators=[InputRequired()])


class ConfirmForm(FlaskForm):
    form = SelectField('Form', choices=[], validators=[InputRequired()])


class CreateSetForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    tenses = MultiCheckBox('Tenses', choices=[])
    verb_type = MultiCheckBox('Type', choices=[])
    infinitives = TextAreaField('Infinitives')


class IrregularForm(FlaskForm):
    ir_infin = StringField('Infin', validators=[DataRequired()])
    yo_form = StringField('yo conjugation', validators=[DataRequired()])
    tu_form = StringField('tu conjugation', validators=[DataRequired()])
    el_form = StringField('el conjugation', validators=[DataRequired()])
    ella_form = StringField('ella conjugation', validators=[DataRequired()])
    usted_form = StringField('usted conjugation', validators=[DataRequired()])
    nosotros_form = StringField('nosotros conjugation', validators=[DataRequired()])
    nosotras_form = StringField('nosotras conjugation', validators=[DataRequired()])
    ellos_form = StringField('ellos conjugation', validators=[DataRequired()])
    ellas_form = StringField('ellas conjugation', validators=[DataRequired()])
    ustedes_form = StringField('ustedes conjugation', validators=[DataRequired()])


