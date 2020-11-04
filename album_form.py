from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, IntegerField, HiddenField
from wtforms.validators import DataRequired

class AlbumForm(FlaskForm):
    id = HiddenField("ID", validators=[])
    title = StringField("Title", validators=[DataRequired()])
    artist = StringField("Artist", validators=[DataRequired()])
    genre = StringField("Genre", validators=[])
    year = IntegerField("Year", validators=[])

class SearchForm(FlaskForm):
    search = StringField("Search", validators=[DataRequired()])
