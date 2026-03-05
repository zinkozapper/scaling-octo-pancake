import random

# Daniel Walker, Colby Seeley, Adam Halliday
# This is a group program that is designed to simulate a soccer season with randomly generated values


# Function that introduces rules, prompts for team name, displays welcome message, and returns name value
def introduction():
    print(
        "\nThis program is designed to simulate a soccer season with randomly generated values for game results.\nYou will choose the number of games that will be played and who your team will square off against."
    )
    name = input("\nPlease enter your name for use throughout the program: ")
    print(f"\nWelcome to the program, {name}. Let's get the season started.")
    return name


# Function that displays the initial menu and returns user choice
def initial_menu():
    while True:
        print("\n---Menu Selection---\n")
        print("1 - Add a Team\n2 - Delete a Team\n3 - Select Team\n4 - End Program\n")
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
            print(f"{team}")


# Function to select home team and opponent team
def select_team(teams, team_type = "home"):
    while True:
        print_teams(teams)
        team = input(f"\nPlease enter the {team_type} team from the list of teams: ")
        if team in teams:
            return team
        else:
            print(
                "\nTeam not found in system. Please select a valid team from the system."
            )


# Main function with function calls
teams = []
name = introduction()
while True:
    print_teams(teams)
    menuSelection = initial_menu()
    if menuSelection == 1:
        teams.append(input("\nPlease enter the team name: "))
    elif menuSelection == 2:
        while True:
            team_delete = input(
                "\nPlease enter the name of the team you'd like to delete: "
            )
            if team_delete in teams:
                print(f"The team {team_delete} has been removed from the system.")
                teams.remove(team_delete)
                break
            else:
                print("\nTeam not found. Please try again.")
    elif menuSelection == 3:
        if len(teams) > 1:
            temp_teams = teams.copy()
            home_team = select_team(temp_teams, "home")
            temp_teams.remove(home_team)
            away_team = select_team(temp_teams, "opponent")
            temp_teams.remove(away_team)
        else:
            print(
                "\nThere are currently not enough teams available in the system to have a game.\nPlease ensure at least two teams are stored in the system.\n"
            )
    elif menuSelection == 4:
        break
