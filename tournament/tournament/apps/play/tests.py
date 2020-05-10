import pytest

from tournament.apps.play.utils import score_play

from datetime import timedelta


class TestScore:
    def test_base_game(self):
        assert (
            score_play(
                game_min_length=timedelta(minutes=60),
                game_complexity=1.0,
                num_winners=1,
                num_losers=3,
            )
            == 100
        )

    def test_carcasonne(self):
        """
        One person winning a four player game of Carcassonne. 
        """
        assert (
            score_play(
                game_min_length=timedelta(minutes=30),
                game_complexity=1.92,
                num_winners=1,
                num_losers=3,
            )
            == 96
        )

    def test_dobble(self):
        assert score_play(
            game_min_length=timedelta(minutes=5),
            game_complexity=1.03,
            num_winners=1,
            num_losers=3,
        ) == pytest.approx(8.5833, rel=1e-3)

    def test_sushi_go(self):
        assert score_play(
            game_min_length=timedelta(minutes=15),
            game_complexity=1.16,
            num_winners=1,
            num_losers=3,
        ) == pytest.approx(29)

    def test_sushi_go_two_winners(self):
        assert score_play(
            game_min_length=timedelta(minutes=15),
            game_complexity=1.16,
            num_winners=2,
            num_losers=2,
        ) == pytest.approx(14.5)
