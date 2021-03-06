from flask import g, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, StringField
from wtforms.validators import DataRequired

from app.actions.salad_bowl import game_action
from app.models import db, Game, SaladBowlWord
from app.views.subpage import salad_bowl


@salad_bowl.route('/<int:game_id>/add_words/', methods=['GET', 'POST'])
@game_action
def add_words(game_id):

    game = Game.query.get(game_id)

    entries = game.words_per_player

    class AddWordsForm(FlaskForm):
        words = FieldList(StringField('name', validators=[DataRequired()]), min_entries=entries, max_entries=entries)

    form = AddWordsForm()

    if form.validate_on_submit():
        for word in form.words.data:
            db.session.add(SaladBowlWord(word=word, writer_id=g.current_user.id, game_id=game_id))
        db.session.commit()
        return True, redirect(url_for('salad_bowl.view_game', game_id=game_id))

    return False, render_template('salad_bowl/actions/add_words.html',
                                  form=form,
                                  action_url=url_for('salad_bowl.add_words', game_id=game_id),
                                  prevent_refresh=True)
