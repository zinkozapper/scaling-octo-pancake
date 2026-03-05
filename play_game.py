#Author: Daniel Walker
#Play the game receiving both team names.
#Generate random scores without ties.
#Return W or L.

import random

#Determins whether the home team or away team wins the game
def play_game(sTeamOne, sTeamTwo):
    #Takes two teams
    bScoreTied = True
    while bScoreTied:
        iTeamOneScore = random.randrange(0,4,1)
        iTeanTwoScore = random.randrange(0,4,1)

        #Makes sure it only continues if the score isn't tied, otherwise rerolls.
        if iTeamOneScore != iTeanTwoScore:
            bScoreTied = False

    #If you want to print out scores uncomment the next line.
    #print(f"{sTeamOne}'s score: {iTeamOneScore} - {sTeamTwo}'s score: {iTeanTwoScore}")

    #Determines winners and losers
    if iTeamOneScore > iTeanTwoScore:
        #Home team wins!
        return 'W'
    elif iTeamOneScore < iTeanTwoScore:
        #Away team wins
        return 'L'

