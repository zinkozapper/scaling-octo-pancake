#Author: Daniel Walker
#Generates random scores for sports teams and then compares them.
import random

#Variable declaration
aTeamsWonAgainst = []
aTeamsLostAgainst = []
dTeamsComparison = {"Won Against": aTeamsWonAgainst, "Lost Against": aTeamsLostAgainst}
bScoreTied = True
winCount = 0
iHomeTeamScore = 0
iAwayTeamScore = 0

sHomeTeamNames = input("Enter the name of your home team: ")
iHomeTeamGames = int(input("Enter the number of games that BYU will play: "))



for i in range (1, iHomeTeamGames+1):
    sAwayTeamName = input(f"Enter the name of the away team for game {i}: ")
    #Generates random score

    while bScoreTied:
        iHomeTeamScore = random.randrange(0,4,1)
        iAwayTeamScore = random.randrange(0,4,1)

        #Makes sure it only continues if the score isn't tied, otherwise rerolls.
        if iHomeTeamScore != iAwayTeamScore:
            bScoreTied = False
    print(f"{sHomeTeamNames}'s score: {iHomeTeamScore} - {sAwayTeamName}'s score: {iAwayTeamScore}")

    #Determines winners and losers
    if iHomeTeamScore > iAwayTeamScore:
        aTeamsWonAgainst.append(sAwayTeamName)
    elif iHomeTeamScore < iAwayTeamScore:
        aTeamsLostAgainst.append(sAwayTeamName)

    #Reset the score tie check at the end
    bScoreTied = True


#Prints out teams won against and teams lost against along with the season record.


print(f"\nTeams won against: ")
for item in dTeamsComparison["Won Against"]:
    print(item)
    winCount +=1

print(f"\nTeams lost against: ")
for item in dTeamsComparison["Lost Against"]:
    print(item)

print(f"Final season record: {winCount} - {iHomeTeamGames-winCount}")

#Checks if win percent is greater than 75% than 50%
if (winCount/iHomeTeamGames) >= .75:
    print("Qualified for the NCAA Soccer Tournament!")
elif (winCount/iHomeTeamGames) >= .5:
    print("You had a good season.")
else:
    print("Your team needs practice!")





