from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import URL, DataRequired, Length, Optional


class FeedForm(FlaskForm):
    url = StringField(
        'フィードURL',
        validators=[DataRequired(message='フィードURLを入力してください'), URL(message='URLの形式が正しくありません')],
    )
    title = StringField(
        '表示名（省略可）',
        validators=[Optional(), Length(max=120)],
    )
    submit = SubmitField('追加する')
