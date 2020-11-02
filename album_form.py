from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired

class AlbumForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    artist = StringField("Artist", validators=[DataRequired()])
    genre = StringField("Genre", validators=[])
    year = IntegerField("Year", validators=[])

class SearchForm(FlaskForm):
    search = StringField("Search", validators=[])
    output = TextAreaField("Albums found:", validators=[])