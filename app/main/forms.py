from flask_wtf import FlaskForm, Form
from wtforms import StringField, TextAreaField, widgets, SelectMultipleField, SelectField, FieldList, FormField, \
    SubmitField
from wtforms.validators import DataRequired, InputRequired


class MultiCheckBox(SelectMultipleField):
    """
    Widget that allows for multiple checkboxes - allows for input similar to SelectMultipleField, but in checkbox verb_form
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class InfinitiveForm(FlaskForm):
    """
    Flask verb_form used to add infinitives to the database.

    Contains a text-area field that allows for input of arbitrarily long list of verbs, and a Select Field that is used
    to select a verb's type

    """
    infinitive = TextAreaField('Infinitive', validators=[DataRequired()])
    form = SelectField('VerbForm', choices=[], validators=[InputRequired()])
    stem_changer = MultiCheckBox('Stem Change', choices=['o to ue', 'e to i', 'e to ie'])


class CreateSetForm(FlaskForm):
    """
    Flask verb_form used for creation of practice sets

    String field - used for the title of the set
    MultiCheckBox - used for selecting tenses and verb_types to be included in the set
    TextAreaField- used for adding custom infinitives to be used in practice sets
    """
    title = StringField('Title', validators=[DataRequired()])
    subject = MultiCheckBox('Subjects', choices=['singular', 'plural', 'formal'])
    tenses = MultiCheckBox('Tenses', choices=[])
    verb_type = MultiCheckBox('Type', choices=[])
    infinitives = TextAreaField('Infinitives')
    submit1 = SubmitField('submit')


class IrregularForm(FlaskForm):
    """
    Flask verb_form used for adding irregular verb conjugations to the database

    StringFields - text input for the different verb conjugations
    """
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


class TypeForm(Form):
    verb = StringField('verb', validators=[DataRequired()])
    type = SelectField('verb_form', choices=['ar verbs', 'er verbs', 'ir verbs'])
    stem_changer = MultiCheckBox('Stem Change', choices=['o to ue', 'e to i', 'e to ie'])


class UnknownInfForm(FlaskForm):
    # def __init__(self, num_forms):
    #     self.num_forms = num_forms

    unknown_verb = FieldList(FormField(TypeForm))
    submit2 = SubmitField('submit')
