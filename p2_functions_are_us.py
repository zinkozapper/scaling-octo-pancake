import random
import play_game

# Daniel Walker, Colby Seeley, Adam Halliday
# This is a group program that is designed to simulate a soccer season with randomly generated values


# Function that introduces rules, prompts for team name, displays welcome message, and returns name value
def introduction():
    print(
        "\nThis program is designed to simulate a soccer season with randomly generated values for game results.\nYou will choose the number of games that will be played and who your team will square off against."
    )
    name = input("\nPlease enter your name for use throughout the program: ").strip().title()
    print(f"\nWelcome to the program, {name}. Let's get the season started.")
    return name


# Function that displays the initial menu and returns user choice
def initial_menu():
    while True:
        print("\n---Menu Selection---\n")
        print("1 - Add a Team\n2 - Delete a Team\n3 - Play a Game\n4 - Record Lookup\n5 - End Program\n")
        menuSelection = input("Please select a menu option: ")
        if (
            menuSelection == "1"
            or menuSelection == "2"
            or menuSelection == "3"
            or menuSelection == "4"
        ):
            return int(menuSelection)
        else:
            print("\nPlease enter a valid menu option.\n")


# Function to print all current teams stored in the list
def print_teams(teams):
    if len(teams) == 0:
        print("\nNo teams currently stored in system.")
    else:
        print("\nTeams:")
        for team in teams:
            print(team["team"])


# Function to select home team and opponent team
def select_team(teams, team_type="home"):
    while True:
        print_teams(teams)
        team = input(f"\nPlease enter the {team_type} team from the list of teams: ").strip().upper()
        for item in teams:
            if team == item["team"]:
                return team
                break
        print("\nTeam not found in system. Please select a valid team from the system.")

#Function to display final record for a team. It receives selected Team's data and displays it.
#I want to have a list of team name, teams won against, and teams lost against.
#I need to add wins/losses to teams lost against.
def display_team_scores(teams = [], games_played = 0):
    if games_played == 0:
        print("\nNo games have been played. Returning to menu.")
        return
    while True:
        print_teams(teams)
        team = input("\nPlease enter the team you would like to view records for (or type 'exit' to exit): ").strip().upper()
        skip = False
        if team.lower() == "exit":
            break
        for item in teams:
            if team == item["team"]:
                print(
                    f"\n{team} has won against the following teams:"
                    f"\n{item["won against"]}"
                    "\nThey have lost against the following teams:"
                    f"\n{item["lost against"]}"
                )
                skip = True
                break
        if skip == False:
            print("Invalid selection. Enter a valid team.")

# Main function with function calls
teams = []
games_played = 0
name = introduction()
while True:
    print_teams(teams)
    menuSelection = initial_menu()
    if menuSelection == 1:
        teamAdd = input("\nPlease enter the team name: ").strip().upper()
        addIt = True
        for team in teams:
            if teamAdd == team["team"]:
                addIt = False
        if addIt == True:
            teams.append({"team" : teamAdd, "won against" : [], "lost against" : []})
        else:
            print("\nTeam already entered. Returning to menu.")
    elif menuSelection == 2:
        if len(teams) < 1:
            print(
                "\nThere are currently no teams stored in the system for deletion. "
                "Please ensure at least one team is stored in the system."
            )
        else:
            while True:
                skip = False
                team_delete = input("\nPlease enter the name of the team you'd like to delete (or 'exit' to exit function): ").strip().upper()
                if team_delete.lower() == "exit":
                    break
                for team in teams:
                    if team_delete == team["team"]:
                        print(f"\nThe team {team_delete} has been removed from the system.")
                        teams.remove(team)
                        skip = True
                if skip == False:
                    print("\nTeam not found. Please try again.")
    elif menuSelection == 3:
        if len(teams) > 1:
            temp_teams = teams.copy()
            home_team = select_team(temp_teams, "home")
            for team in temp_teams:
                if home_team == team["team"]:
                    temp_teams.remove(team)
                    break
            away_team = select_team(temp_teams, "opponent")
            home_game_result = play_game.play_game(home_team, away_team)
            if home_game_result == "W":
                for team in teams:
                    if home_team == team["team"]:
                        team["won against"].append(away_team)
                    if away_team == team["team"]:
                        team["lost against"].append(home_team)
                print(f"\n{home_team} won against {away_team}.")
            elif home_game_result == "L":
                for team in teams:
                    if home_team == team["team"]:
                        team["lost against"].append(away_team)
                    if away_team == team["team"]:
                        team["won against"].append(home_team)
                print(f"\n{away_team} won against {home_team}.")
            games_played += 1
        else:
            print(
                "\nThere are currently not enough teams available in the system to have a game.\nPlease ensure at least two teams are stored in the system."
            )
    elif menuSelection == 4:
        display_team_scores(teams, games_played)
    elif menuSelection == 5:
        break
