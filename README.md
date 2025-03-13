# FCC-RockPaperScissors
FreeCodeCamp.org, Machine Learning with Python - Rock Paper Scissors Project
Rock Paper Scissors AI (FreeCodeCamp Challenge)

Overview

This project is an AI bot that plays Rock, Paper, Scissors against four different AI opponents as part of the FreeCodeCamp Machine Learning with Python Certification. The AI must win at least 60% of matches against all four bots to pass the challenge.

Objective

The AI must identify and adapt to different opponent strategies and maximize its win rate. The key challenge is defeating adaptive opponents like Abbey, who counter the player's patterns using a Markov chain strategy.

Opponents and Their Strategies

The AI faces four pre-programmed bots with the following strategies:

Bot

Strategy

Quincy

Repeats a fixed cycle: ['R', 'R', 'P', 'P', 'S']

Abbey

Uses a Markov chain model to predict and counter likely moves

Kris

Assumes the player will repeat their last move and counters it

Mrugesh

Tracks the last 10 moves, finds the most frequent one, and counters it

Strategy Used in This AI

The AI player employs a multi-strategy approach to counter each opponent effectively:

1. Quincy Detection (Fixed Cycle Counter)

Identifies if the opponent is following Quincy's fixed move cycle.

Predicts Quincy's next move using cycle rotation.

Plays the move that counters the predicted move.

2. Abbey Countering (Adaptive Opponent Detection)

Tracks how often Abbey correctly counters the AI's moves.

If Abbey counters at least 70% of the time in the last 10 moves, we mirror Abbey’s last move to break her pattern.

Otherwise, uses a frequency-based strategy to confuse Abbey.

3. Frequency-Based Prediction (For Kris & Mrugesh)

Counts the last 5 moves to determine the most common move.

If a move dominates, counters it directly.

If moves are evenly distributed, assumes an adaptive opponent and chooses a move using inverse frequency weighting.

4. Randomization for Unpredictability

20% probability to make a completely random move.

Prevents the AI from being too predictable, especially against Abbey and Kris.

Implementation Breakdown

The AI logic is implemented in RPS.py and consists of the following key functions:

even_out(my_history)

Balances move frequency by playing the least used move so far.

 def even_out(my_history):
    if not my_history:
        return random.choice(["R", "P", "S"])
    counts = {"R": my_history.count("R"),
              "P": my_history.count("P"),
              "S": my_history.count("S")}
    return min(counts, key=counts.get)

detect_abbey_pattern(my_history, opponent_history)

Detects if Abbey is countering at least 70% of the time in the last 10 moves.

def detect_abbey_pattern(my_history, opponent_history):
    if len(my_history) < 11:
        return False
    counters = {"R": "P", "P": "S", "S": "R"}
    counter_count = sum(1 for i in range(-11, -1)  
                        if opponent_history[i] == counters.get(my_history[i+1], ""))
    return counter_count / 10 >= 0.7

player(prev_play)

This function decides what move to play based on the opponent's history and detected patterns.

import random

opponent_history = []
my_history = []

def player(prev_play):
    global opponent_history, my_history
    if prev_play:
        opponent_history.append(prev_play)
    
    if not opponent_history or len(opponent_history) < 5:
        move = random.choice(["R", "P", "S"])
        my_history.append(move)
        return move
    
    counter_move = {"R": "P", "P": "S", "S": "R"}
    quincy_cycle = ["R", "R", "P", "P", "S"]
    rotations = [quincy_cycle[i:] + quincy_cycle[:i] for i in range(5)]
    last_five = opponent_history[-5:]
    
    if any(last_five == rotation for rotation in rotations):
        predicted_quincy = quincy_cycle[len(opponent_history) % 5]
        candidate = counter_move[predicted_quincy]
    else:
        counts = {"R": last_five.count("R"),
                  "P": last_five.count("P"),
                  "S": last_five.count("S")}
        max_count = max(counts.values())
        min_count = min(counts.values())
        
        if max_count - min_count <= 1:
            if detect_abbey_pattern(my_history, opponent_history):
                candidate = opponent_history[-1]  # Mirror Abbey
            else:
                candidate = counter_move[even_out(my_history)]
        else:
            predicted = max(counts, key=counts.get)
            candidate = counter_move[predicted]
    
    if my_history and my_history[-1] == candidate:
        candidate = random.choice(["R", "P", "S"])
    
    if random.random() < 0.2:
        candidate = random.choice(["R", "P", "S"])
    
    my_history.append(candidate)
    return candidate

Running the AI

Requirements

Python 3.x

FreeCodeCamp’s Rock-Paper-Scissors boilerplate repository

Steps

Clone the repository

git clone https://github.com/your-github-username/rock-paper-scissors-ai.git
cd rock-paper-scissors-ai

Run the AI against each bot

python main.py

Check the results to ensure a 60% win rate against all bots.

Testing

To verify correctness, use FreeCodeCamp's test suite:

python -m unittest test_module.py

Lessons Learned

Adaptive Opponents Are Hard to Beat: Abbey was particularly challenging since she learns and adapts dynamically.

Randomness Is Essential: Bots that rely on detecting past patterns can be thrown off by occasional randomness.

Multiple Strategies Improve Success: Instead of a single perfect strategy, combining cycle detection, frequency analysis, and randomization was the best approach.

Next Steps

Implement reinforcement learning (Q-learning) to dynamically adjust strategy.

Fine-tune randomness percentages for optimal performance.

Explore more sophisticated AI models to counter Abbey’s predictions better.

Conclusion

This AI successfully adapts to different playstyles using a combination of pattern detection, frequency analysis, and strategic randomization. While it's not perfect, it's a solid attempt at breaking the 60% win rate challenge set by FreeCodeCamp!
