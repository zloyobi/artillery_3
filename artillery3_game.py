import math
import random

def print_welcome():
    print("\t\tARTILLERY 3")
    print("\t     CREATIVE COMPUTING")
    print("           MORRISTOWN, NEW JERSEY")
    print("\nWELCOME TO 'WAR3'. TWO OR THREE HUMANS MAY PLAY!")
    assistance = input("DO YOU WISH SOME ASSISTANCE? ").strip().upper()
    if assistance == "YES":
        print_instructions()

def print_instructions():
    print("\nTHIS IS A WAR GAME. TWO OR THREE PLAYERS ARE GIVEN")
    print("(THEORETICAL) CANNONS WITH WHICH THEY ATTEMPT TO SHOOT EACH")
    print("OTHER. THE PARAMETERS FOR DISTANCES AND MUZZLE VELOCITIES ARE")
    print("SET AT THE BEGINNING OF THE GAME. THE SHOTS ARE FIRED BY")
    print("GIVING A FIRING ANGLE, EXPRESSED IN DEGREES FROM HORIZONTAL")
    print("\nTHE COMPUTER WILL KEEP TRACK OF THE GAME AND REPORT ALL")
    print("MOVES. A 'HIT' IS SCORED BY FIRING A SHOT WITHIN 5% OF THE")
    print("TOTAL DISTANCE FIRED OVER. GOOD LUCK\n")

def get_players():
    while True:
        try:
            n = int(input("NO. OF PLAYERS? "))
            if n in [2, 3]:
                return n
            else:
                print("ERROR--TWO OR THREE PLAYERS!")
        except ValueError:
            print("Please enter a valid number.")

def initialize_game(n):
    r = {}
    v = {}
    p = {player: 0 for player in range(1, n + 1)}

    print("\nDISTANCES BETWEEN PLAYERS:")
    for i in range(1, n):
        for j in range(i + 1, n + 1):
            while True:
                try:
                    distance = float(input(f"DISTANCE (FT.) {i} TO {j}? "))
                    r[(i, j)] = distance
                    r[(j, i)] = distance
                    break
                except ValueError:
                    print("Enter a valid distance.")
    
    print("\nMUZZLE VELOCITIES:")
    for player in range(1, n + 1):
        while True:
            try:
                velocity = float(input(f"MUZZLE VELOCITY (FT./SEC.) OF {player}? "))
                v[player] = velocity
                break
            except ValueError:
                print("Enter a valid number.")

    return r, v, p

def is_defunct(player, p):
    return p[player] == 12

def shoot(player, target, angle, r, v, p):
    if angle < 0 or angle > 180:
        print(f"ERROR--FIRED INTO GROUND. Player {player} is now defunct.")
        p[player] = 12
        return

    if angle > 90:
        print("ERROR--FIRED WRONG WAY, LOSE SHOT.")
        return

    z = (math.sin(math.radians(angle)) * v[player]**2) / 32
    x = (r[(player, target)] / 1000) * (random.random() - random.random())
    d = x + z
    d1 = r[(player, target)] * 0.05

    if abs(d - r[(player, target)]) < d1:
        print(f"A HIT - Player {target} is now defunct.")
        p[target] = 12
    elif d < r[(player, target)]:
        print(f"YOU UNDERSHOT BY {abs(d - r[(player, target)]):.2f} FEET.")
    else:
        print(f"YOU OVERSHOT BY {abs(d - r[(player, target)]):.2f} FEET.")

def main():
    print_welcome()
    n = get_players()
    r, v, p = initialize_game(n)

    round_count = 1
    active_players = n

    while active_players > 1:
        print(f"\nROUND {round_count}")
        for player in range(1, n + 1):
            if is_defunct(player, p):
                continue

            while True:
                try:
                    target = int(input(f"Player {player}, choose your target: "))
                    if target == player or is_defunct(target, p):
                        print("ERROR--Invalid target.")
                    elif target in range(1, n + 1):
                        break
                    else:
                        print("ERROR--Invalid target.")
                except ValueError:
                    print("Enter a valid player number.")

            while True:
                try:
                    angle = float(input(f"Player {player}, enter firing angle: "))
                    shoot(player, target, angle, r, v, p)
                    break
                except ValueError:
                    print("Enter a valid angle.")

        active_players = sum(1 for player in p if not is_defunct(player, p))
        round_count += 1

    winner = [player for player in p if not is_defunct(player, p)][0]
    print(f"GAME OVER. Player {winner} wins!")
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
