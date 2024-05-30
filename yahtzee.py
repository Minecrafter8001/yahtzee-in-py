import random

class Yahtzee:
    def __init__(self, players):
        if players < 1 or players > 8:
            raise ValueError("Number of players must be between 1 and 8.")
        self.players = players
        self.scores = {player: {'ones': 0, 'twos': 0, 'threes': 0, 'fours': 0, 'fives': 0, 'sixes': 0, 'three_of_a_kind': 0, 'four_of_a_kind': 0, 'full_house': 0, 'small_straight': 0, 'large_straight': 0, 'yahtzee': 0, 'chance': 0} for player in range(1, players + 1)}
        self.dice = [0] * 5
        self.held_dice = [False] * 5
        self.dice_labels = ['A', 'B', 'C', 'D', 'E']

    def roll_dice(self):
        for i in range(5):
            if not self.held_dice[i]:
                self.dice[i] = random.randint(1, 6)

    def hold_dice(self, labels):
        for label in labels:
            index = self.dice_labels.index(label)
            self.held_dice[index] = True

    def release_dice(self, labels):
        for label in labels:
            index = self.dice_labels.index(label)
            self.held_dice[index] = False

    def show_dice(self):
        return ', '.join(f"{label}: {value}{'(held)' if held else ''}" for label, value, held in zip(self.dice_labels, self.dice, self.held_dice))

    def get_possible_scores(self):
        possible_scores = {}
        dice_count = {i: self.dice.count(i) for i in range(1, 7)}
        
        # Calculate possible scores for each category based on current dice
        possible_scores['ones'] = dice_count[1] * 1
        possible_scores['twos'] = dice_count[2] * 2
        possible_scores['threes'] = dice_count[3] * 3
        possible_scores['fours'] = dice_count[4] * 4
        possible_scores['fives'] = dice_count[5] * 5
        possible_scores['sixes'] = dice_count[6] * 6
        possible_scores['three_of_a_kind'] = sum(self.dice) if max(dice_count.values()) >= 3 else 0
        possible_scores['four_of_a_kind'] = sum(self.dice) if max(dice_count.values()) >= 4 else 0
        possible_scores['full_house'] = 25 if sorted(dice_count.values()) == [2, 3] else 0
        possible_scores['small_straight'] = 30 if len(set(self.dice)) >= 4 and any(all(num + i in self.dice for i in range(4)) for num in range(1, 4)) else 0
        possible_scores['large_straight'] = 40 if sorted(set(self.dice)) in [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6]] else 0
        possible_scores['yahtzee'] = 50 if len(set(self.dice)) == 1 else 0
        possible_scores['chance'] = sum(self.dice)

        return possible_scores

    def score_roll(self, category):
        return self.get_possible_scores()[category]

    def play_round(self, player):
        input(f"Player {player}, press 'Enter' to roll the dice...")
        self.roll_dice()
        print("Dice: ", self.show_dice())
        
        for roll in range(2):  # Two more rolls allowed
            holds = input("Enter the letters of dice to hold separated by space or type 'score' to score now (e.g., A C E): ").upper().strip()
            if holds.lower() == 'score':
                break
            holds = holds.split() if holds else []
            self.hold_dice(holds)
            self.roll_dice()
            print("Dice: ", self.show_dice())
            self.release_dice(holds)  # Release all dice for the next player

        possible_scores = self.get_possible_scores()
        print("Possible scoring categories:")
        for category, score in possible_scores.items():
            if score > 0:
                print(f"{category.capitalize()} ({score})")
        
        category = input("Choose the scoring category: ").lower()
        while category not in possible_scores or possible_scores[category] == 0:
            print("Invalid category or no score possible. Please choose a valid scoring category.")
            category = input("Choose the scoring category: ").lower()

        score = self.score_roll(category)
        self.scores[player][category] += score
        print(f"You scored {score} points for {category}.")

    def play_game(self):
        for _ in range(13):  # Each player gets 13 turns
            for player in range(1, self.players + 1):
                self.play_round(player)
                print("Player {}'s scorecard:".format(player))
                for category, score in self.scores[player].items():
                    print("{:<15}: {}".format(category.capitalize(), score))
                print("")

while True:
    try:
        players = int(input("Enter the number of players (up to 8): "))
        if 2 <= players <= 8:
            break
        else:
            print("Player count must be between 2-8")
            continue
    except ValueError:
        continue
players = int(players)
game = Yahtzee(players)
game.play_game()
