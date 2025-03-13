import random

# Keeping track of both player's move history.
opponent_history = []
my_history = []

def even_out(my_history):
    """
    Tries to balance our move frequency by returning the move we have played the least.
    This is useful against opponents who track our patterns.
    
    * The struggle: At first, I tried just countering the opponent's most frequent move,
      but that was too predictable. So now, I try to even out my own plays to confuse adaptive bots.
    """
    if not my_history:
        return random.choice(["R", "P", "S"])
    
    counts = {
        "R": my_history.count("R"),
        "P": my_history.count("P"),
        "S": my_history.count("S")
    }
    
    # Returns the move with the lowest count, making our play distribution more uniform.
    return min(counts, key=counts.get)

def detect_abbey_pattern(my_history, opponent_history):
    """
    Detects if the opponent (Abbey) is adapting too well (i.e., countering our moves at least 70% of the time).
    This is done by checking if Abbey correctly predicted and countered our moves in the last 10 rounds.
    
    * The struggle: Abbey was a nightmare! Simple frequency tracking was useless against her.
      She used a Markov model, meaning she wasn't just counting moves—she was predicting transitions.
      I had to create a way to detect when she was adapting too well and switch things up.
    """
    if len(my_history) < 11:
        return False  # Not enough rounds to analyze patterns
    
    counters = {"R": "P", "P": "S", "S": "R"}
    counter_count = sum(1 for i in range(-11, -1)  # Checking last 10 rounds
                        if opponent_history[i] == counters.get(my_history[i+1], ""))
    
    return counter_count / 10 >= 0.7  # If Abbey countered us 70%+ of the time, she's detected!

def player(prev_play):
    """
    The main function that decides our move based on opponent history.
    
    Strategy breakdown:
    - If it's the start of the game, play randomly.
    - If the opponent follows a known cycle (like Quincy), counter it.
    - If the opponent is adapting well (like Abbey), try to disrupt patterns.
    - If no clear pattern, default to countering the most frequent move in the last 5 rounds.
    - Add occasional randomization to avoid being predictable.
    
    * The struggle: I started with simple frequency counting—failed.
      Then I tried Markov predictions—failed.
      Then reinforcement learning—failed.
      Finally, I landed on this hybrid strategy that combines all the previous failures
      into something that actually works (sometimes).
    """
    
    global opponent_history, my_history

    # Keep track of the opponent's plays.
    if prev_play:
        opponent_history.append(prev_play)

    # First 5 moves: Play randomly since we have no data.
    if not opponent_history or len(opponent_history) < 5:
        move = random.choice(["R", "P", "S"])
        my_history.append(move)
        return move

    counter_move = {"R": "P", "P": "S", "S": "R"}  # Basic counter-move map

    # --- Quincy Detection ---
    quincy_cycle = ["R", "R", "P", "P", "S"]
    rotations = [quincy_cycle[i:] + quincy_cycle[:i] for i in range(5)]
    last_five = opponent_history[-5:]

    if any(last_five == rotation for rotation in rotations):
        # Predict Quincy's next move based on the cycle.
        predicted_quincy = quincy_cycle[len(opponent_history) % 5]
        candidate = counter_move[predicted_quincy]  # Counter it!
    
    else:
        # --- Frequency-Based Prediction ---
        counts = {
            "R": last_five.count("R"),
            "P": last_five.count("P"),
            "S": last_five.count("S")
        }
        
        max_count = max(counts.values())
        min_count = min(counts.values())

        if max_count - min_count <= 1:
            # If move distribution is balanced, suspect Abbey's predictive adaptation.
            if detect_abbey_pattern(my_history, opponent_history):
                candidate = opponent_history[-1]  # Mirror Abbey to throw her off.
            else:
                candidate = counter_move[even_out(my_history)]  # Use our least-used move as a base.
        else:
            # Predict the opponent's most common move and counter it.
            predicted = max(counts, key=counts.get)
            candidate = counter_move[predicted]

    # Avoid playing the same move twice in a row unless necessary.
    if my_history and my_history[-1] == candidate:
        candidate = random.choice(["R", "P", "S"])

    # 20% chance to play randomly to introduce unpredictability.
    if random.random() < 0.2:
        candidate = random.choice(["R", "P", "S"])

    # Record and return our final choice.
    my_history.append(candidate)
    return candidate