Functions:
  tennis-sim.cpp:
    int main(int argc, char *argv[7])
        1 2/3: Best of 3 or Best of 5
        2 adv/tie:
        3 spw1: Mean serve win probability (player a)
        4 stddv1: standard deviation from normal from which serves are calculated
        5 spw2: Mean serve win probability (player b)
        6 stddv2: standard deviation from normal from which serves are calculated
        7 [<game target>]: if set, will only care about <game target> amount of games

Variables:

    total_games: sum of all games played. Accessed via match class. Average Match length is calculated from this

Sorting:
    Sorting is done by match length. Unit of length is games.

Metrics:
    Median match length
    Mean match length
