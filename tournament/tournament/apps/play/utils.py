# \left(\frac{\left(\frac{\text{num players}}{4}\times\frac{\text{min play time}}{1\text{ hour}}\times\text{complexity}\right)}{\text{num winners}}\right)\times{100}
def score_play(game_min_length, game_complexity, num_winners, num_losers):
    try:
        return (
            (
                (
                    # Number of players, normalised where 4 = 1.0
                    ((num_winners + num_losers) / 4)
                    # Game length, normalised where 1 hour = 1.0
                    * (game_min_length.total_seconds() / 3600)
                    # Complexity multiplyer
                    * float(game_complexity)
                )
                # Share score amongst winners
                / num_winners
            )
            # Make it a bigger number to feel more meaningful
            * 100
        )
    except ZeroDivisionError:
        return 0.0
