from datetime import datetime
from random import shuffle

from flask import g, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired

from app.actions.salad_bowl import game_action
from app.models import db, Game, PlayerGame, Round
from app.views.subpage import salad_bowl


class CreateGameForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    words_per_player = IntegerField('number of words per person', validators=[DataRequired()])
    number_of_rounds = IntegerField('number of rounds', validators=[DataRequired()])
    seconds_per_turn = IntegerField('seconds per turn', validators=[DataRequired()])


@salad_bowl.route('/create_game/', methods=['GET', 'POST'])
def create_game():
    form = CreateGameForm()

    if form.validate_on_submit():
        new_game = Game(name=form.name.data,
                        words_per_player=form.words_per_player.data,
                        is_open=True,
                        owner_player_id=g.current_user.id,
                        created_at=datetime.utcnow())
        db.session.add(new_game)
        db.session.flush()

        for i in range(min(10, form.number_of_rounds.data)):
            db.session.add(Round(game_id=new_game.id, round_number=i + 1, seconds_per_turn=form.seconds_per_turn.data))
        db.session.commit()

        return redirect(url_for('.games'))

    return render_template('salad_bowl/actions/create_game.html', form=form, action_url=url_for('.create_game'))


class JoinGameForm(FlaskForm):
    pass


@salad_bowl.route('/game/<int:game_id>/join/', methods=['GET', 'POST'])
def join_game(game_id):
    form = JoinGameForm()

    if form.validate_on_submit(
    ):  # make sure game is open, stuff like that, user is logged in, user isnt already in game
        new_player_game = PlayerGame(player_id=g.current_user.id, game_id=game_id)
        db.session.add(new_player_game)
        db.session.commit()

        return redirect(url_for('.view_game', game_id=game_id))

    return render_template('salad_bowl/actions/join_game.html',
                           form=form,
                           action_url=url_for('salad_bowl.join_game', game_id=game_id))


class StartGameForm(FlaskForm):
    pass


@salad_bowl.route('/game/<int:game_id>/start/', methods=['GET', 'POST'])
@game_action
def start_game(game_id):
    form = StartGameForm()

    if form.validate_on_submit(
    ):  # make sure game is open, stuff like that, user is logged in, user isnt already in game
        game = Game.query.options(db.joinedload(Game.teams)).get(game_id)
        game.started_at = datetime.utcnow()
        turn_order = list(range(len(game.teams)))
        shuffle(turn_order)
        for i, team in enumerate(game.teams):
            team.turn_order = turn_order[i]

        db.session.commit()

        return True, redirect(url_for('.view_game', game_id=game_id))

    return False, render_template('salad_bowl/actions/start_game.html',
                                  form=form,
                                  action_url=url_for('salad_bowl.start_game', game_id=game_id))


class DeleteGameForm(FlaskForm):
    pass


@salad_bowl.route('/game/<int:game_id>/delete/', methods=['GET', 'POST'])
@game_action
def delete_game(game_id):
    form = StartGameForm()

    if form.validate_on_submit(
    ):  # make sure game is open, stuff like that, user is logged in, user isnt already in game
        game = Game.query.get(game_id)
        db.session.delete(game)

        db.session.commit()

        return False, redirect(url_for('salad_bowl.games'))

    return False, render_template('salad_bowl/actions/delete_game.html',
                                  form=form,
                                  action_url=url_for('salad_bowl.delete_game', game_id=game_id))
