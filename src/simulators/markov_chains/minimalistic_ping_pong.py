import numpy as np


'''

Match:
    Best of -> 3
    Lead    -> None
    Golden  -> None
        Game:
            Goal   -> 3
            Lead   -> 2
            Golden -> None
'''

transient_states_per_game = 11
num_of_games = 4
total_transient_states = transient_states_per_game * num_of_games
absorbing_states = 2

transition_matrix = np.zeros((total_transient_states,
                                total_transient_states + absorbing_states))

wp = 1.0
lp = 2.0

transition_matrix[0][1] = wp
transition_matrix[0][2] = lp

transition_matrix[1][3] = wp
transition_matrix[1][4] = lp

transition_matrix[2][4] = wp
transition_matrix[2][5] = lp

transition_matrix[3][11] = wp # next-round
transition_matrix[3][6] = lp

transition_matrix[4][6] = wp
transition_matrix[4][7] = lp

transition_matrix[5][7] = wp
transition_matrix[5][22] = lp # next-round

transition_matrix[6][11] = wp # next-round
transition_matrix[6][8] = lp

transition_matrix[7][8] = wp
transition_matrix[7][22] = lp

transition_matrix[8][9] = wp
transition_matrix[8][10] = lp

transition_matrix[9][11] = wp
transition_matrix[9][8] = lp

transition_matrix[10][8] = wp
transition_matrix[10][22] = lp

transition_matrix[11][12] = wp
transition_matrix[11][13] = lp

transition_matrix[12][14] = wp
transition_matrix[12][15] = lp

transition_matrix[13][15] = wp
transition_matrix[13][16] = lp

transition_matrix[14][44] = wp # to absorbing state 
transition_matrix[14][17] = lp

transition_matrix[15][17] = wp
transition_matrix[15][18] = lp

transition_matrix[16][18] = wp
transition_matrix[16][33] = lp

transition_matrix[17][44] = wp # to absorbing state
transition_matrix[17][19] = lp

transition_matrix[18][19] = wp
transition_matrix[18][33] = lp

transition_matrix[19][20] = wp
transition_matrix[19][21] = lp

transition_matrix[20][44] = wp
transition_matrix[20][19] = lp

transition_matrix[21][19] = wp
transition_matrix[21][33] = lp

transition_matrix[22][23] = wp
transition_matrix[22][24] = lp

transition_matrix[23][25] = wp
transition_matrix[23][26] = lp

transition_matrix[24][26] = wp
transition_matrix[24][27] = lp

transition_matrix[25][33] = wp
transition_matrix[25][28] = lp

transition_matrix[26][28] = wp
transition_matrix[26][29] = lp

transition_matrix[27][29] = wp
transition_matrix[27][45] = lp # to absorbing state

transition_matrix[28][33] = wp
transition_matrix[28][30] = lp

transition_matrix[29][30] = wp
transition_matrix[29][45] = lp

transition_matrix[30][31] = wp
transition_matrix[30][32] = lp

transition_matrix[31][33] = wp
transition_matrix[31][30] = lp

transition_matrix[32][30] = wp
transition_matrix[32][45] = lp

transition_matrix[33][34] = wp
transition_matrix[33][35] = lp

transition_matrix[34][36] = wp
transition_matrix[34][37] = lp

transition_matrix[35][37] = wp
transition_matrix[35][38] = lp

transition_matrix[36][44] = wp # to absorbing state
transition_matrix[36][39] = lp

transition_matrix[37][39] = wp
transition_matrix[37][40] = lp

transition_matrix[38][40] = wp
transition_matrix[38][45] = lp # to absorbing state

transition_matrix[39][44] = wp
transition_matrix[39][41] = lp

transition_matrix[40][41] = wp
transition_matrix[40][45] = lp

transition_matrix[41][42] = wp
transition_matrix[41][43] = lp

transition_matrix[42][44] = wp
transition_matrix[42][41] = lp

transition_matrix[43][41] = wp
transition_matrix[43][45] = lp

Q = transition_matrix[:,:total_transient_states]
print(transition_matrix.shape)
R = transition_matrix[:,(total_transient_states):]


np.savetxt('minimalistic_ping_pong.txt', transition_matrix, fmt='%1.1f')
np.savetxt('q.txt', Q, fmt='%1.1f')
np.savetxt('r.txt', R, fmt='%1.1f')

#def propagate_probabilities_point(transition_matrix,
#                                 transient_states_per_game):


