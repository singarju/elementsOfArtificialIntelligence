# Assignment 3
# README
## PART - 1
### Tick-tack-what Formulation
The game is formulated as a grid of size `n x m` represented by a string input. The main problem is to determine the best move for placing an 'X' on the board such that it minimizes the opponent's chances of winning while optimizing for forming a winning line of specified length.

#### Key Elements:
1. **Input:**
    - Board as a string.
    - Grid dimensions `n` (rows) and `m` (columns).
    - Target line length `length` to win.
2. **Output:**
    - Modified board state with the best move applied.
3. **Objective:**
    - Prevent the opponent from forming a winning line.
    - Strategically place 'X' to create opportunities for winning lines.

### Program Workflow
1. **Parsing Board Input:**
    - The board is converted from a string to a 2D grid format for easier manipulation.
2. **Checking Finish State:**
    - The program checks if there is already a winning line on the board before proceeding.
3. **Finding the Best Move:**
        - finding all the empty cells on the board.
        - The program identifies potential moves and evaluates their impact. Replacing one of the '.' with 'x ' and checking if the move makes conginouos  x or not.
        - if it is making a line of specified length we reverse the 'x' to '.' again.
        - Blocks potential opponent winning lines.
        - Avoids creating too many adjacent 'X' positions unnecessarily.
4. **Applying the Move:**
    - if condition of not making continuous lines if fulfilled, the selected move is applied, and the updated board is returned.
5. **Output:**
    - The program prints the board state before and after applying the best move.

### How the Program Works
The program consists of several components:
- **Board Parsing Functions:**
    - `parse_board_string_to_grid`: Converts a string into a grid representation.
    - `parse_board_grid_to_string`: Converts a grid back to a string.
- **State Validation:**
    - `is_finish_state`: Checks if the game is in a winning state.
    - `check_line`: Confirms the existence of a line of specified length.
- **Move Evaluation:**
    - `find_best_move`: Determines the optimal move by evaluating potential lines, blocking opportunities, and adjacency constraints.
- **Utility Functions:**
    - `return_empty_positions`: Identifies empty positions on the board.
    - `print_board`: Displays the board in a human-readable format.

### Problems Encountered
1. **Edge Cases:**
    - Handling boards with no winning lines. If the input board is already a finished game we assert that the game is already finished but I found out that if you call play_game and add the checking of valid board in solver function it will return that game is already finished since solver is called inside play_game untill the game is finished, but it should return we won or we lost. So to fix this we need to make sure that checking of valid board should be done only once so we added a check in the main function to see if the game is already finished. So if we want to test the code against already finished game we can use **python3 solver.py board_string n m length**. But in the test code we are calling play_game which will call solver multiple times and it will never go to main. 
    - Random player moves: Sometimes the random player moves are optimal and we loose. So please make sure that you run the code multiple times to get the correct results. I tested the code with 20 times and it was able to win 18 times. Make sure if the test cases are failing you test it multiple times.
    - Boards with all positions filled. We should make a loosing move
    - Small boards where forming a line is easier.
2. **Simplifications:**
    - Random selection among multiple "safe" moves.
3. **Performance:**
    - Larger boards may require optimization for move evaluation.


## Contributions
1. **Arju Singh:**
    - Designed and implemented core functions for `solver`, `find_best_move`,`count_lines_in_direction`and `check_line` state validation.
    - 
2. **Vimal:**
    - Conducted extensive testing and handled edge cases. Our testing file has few of the test cases that we used to test the code.
    - Documented the program and created the `README.md` file.


## Assumptions and Notes
- The board is always square or rectangular with dimensions matching the input.
- Valid moves are determined purely based on the current board state.
- The program handles moves for the opponent by the function random_solver.


## Output
The program will:
1. Print the initial board.
2. Decide and apply the next move.
3. Print the updated board state.

## Future Improvements
- making random_solver intelligent and make solver and random_solver play aginst each other.
- Optimize the move evaluation algorithm for larger boards.
- solver can have some memory of its last move and use that to make the next move, instead of making every move independent of each other. This will make the solver more intelligent.






## PART - 2
### Part-of-speech Tagging
In order to implement a Part-of-Speech (POS) tagging system, we have to train the model with a labeled dataset of words and corresponding tags, and then using that trained model to predict the tags for new sentences.

#### Key Elements:
1. **Input:**
    - A labeled dataset containing sentences with their corresponding POS tags.
2. **Output:**
    - A sequence of POS tags corresponding to the input sentence.
3. **Objective:**
    - To implement part-of-speech tagging in Python, using Bayes networks.

### Program Workflow
1. **Training the Model:**
The training function processes the input data to learn the necessary probabilities for POS tagging:
    - Emission probabilities: The probability of a word given a particular tag (i.e., how likely it is that a word appears with a specific tag).
    - Transition probabilities: The probability of transitioning from one tag to another (i.e., how likely one POS tag follows another).
    - Initial probabilities: The probability of a sentence starting with a particular tag.
This function works by iterating over the sentences, counting the occurrences of each word-tag pair, tag transitions, and initial tags, and then calculating the probabilities using maximum likelihood estimation (MLE). It also applies smoothing (Laplace smoothing with alpha = 0.01) to handle unseen words and tag transitions.
2. **Tagging Sentences:**
There are two methods for predicting POS tags for a sentence:
    - Simplified Model (`simplified`):
        - A basic tagging approach where each word is assigned the most probable tag based solely on the emission probabilities. It also considers the previous tag (if any) using transition probabilities.
        - The simplified model is faster but less accurate compared to the more sophisticated HMM approach.
    - HMM Viterbi Algorithm (`hmm_viterbi`):
        - This is a more advanced approach using dynamic programming to find the most likely sequence of tags for a given sentence.
        - The Viterbi algorithm explores all possible tag sequences and selects the one that maximizes the product of both emission and transition probabilities.
        - Beam search is employed with a beam width of 10, which allows the algorithm to explore more possible tag sequences without evaluating all possibilities.
3. **Posterior Probability Calculation**
        - This function calculates the log of the posterior probability for a given sentence and its corresponding tags using either the simplified model or the HMM-based Viterbi algorithm. 
        - The log probabilities of emission and transition are summed to evaluate how well a particular set of tags explains the sentence.
4. **Handling Unknown Words**
    - For words that are not seen during training, a custom function (`hhandle_unknown_word`) handles unknown words based on their characteristics:
        - Proper nouns (words starting with a capital letter) are more likely to be NOUN.
        - Numeric values are more likely to be NUM.
        - Verbs can often be identified by their -ing suffix.
        - For other cases, the function defaults to a low probability for unknown words.
5. **Training and Solving Workflow**
    - Train the Model: We train the model by calling the `train` function with labeled training data. This step calculates the emission, transition, and initial probabilities.
    - Tag a Sentence: Use the `solve` function to tag a new sentence. You can choose either the simplified model or the HMM-based model for tagging. The model predicts the best tags for the words in the sentence using the probabilities learned during training.
6. **Output:**
    - The program prints the predicted POS tags for the input sentence, formatted as a sequence of words and their corresponding tags.

### Code Structure: 
The program consists of several components:
- **`Solver` Class:**
    - Contains the core logic for training the model and solving for POS tags using both the simplified and HMM models.
    - Contains key attributes like `emission_probs`, `transition_probs`, and `initial_probs` that store the learned probabilities
- **Training (`train`):**
    - Processes the input data, calculates probabilities, and stores them in the appropriate dictionaries.
- **Tagging (`simplified`, `hmm_viterbi`):**
    - Implements the two tagging methods. The `simplified` method is a fast but basic approach, while `hmm_viterbi` implements the Viterbi algorithm to find the most likely tag sequence.
- **Utility Functions:**
    - `handle_unknown_word`: Deals with unseen words using heuristics.
    - `posterior`: Computes the log-likelihood of a given sentence and its tags.

### Testing and Evaluation
1. **Training and Evaluation:**
    - To evaluate the performance of the model, you can run the solve function on test sentences. The predicted tags are compared with the true tags to assess the model's accuracy.
2. **Edge Cases Handled:**
    - Unknown Words: Proper nouns, digits, and verb forms are handled with specific heuristics.
    - Tagging Unseen Sentences: The model is capable of tagging sentences that contain words not seen during training.

### Problem Encountered
**Smoothing in Posterior Calculation:** 
    - While testing the model, we encountered cases where a particular probability is zero. i.e., if a word has never been observed with a particular tag during training, the emission probability for that word-tag pair will be zero. Similarly, transition probabilities between some tag pairs were also zero.
    - This made the likelihood of the entire sequence equal to zero. This resulted in an invalid solution, as the model completely disregarded any unseen word-tag pair or tag pair transition.
    - So to solve this, we applied smoothing, where probabilities are adjusted to avoid exact zeros. We set a very small probability value (1e-10) instead of zero, which ensures that the model can still calculate valid probabilities for unseen words or transitions.

## Contributions
1. **Vimal:**
    - Designed and implemented core functions for `solver`, `train`, `handle_unknown_word`, `simplified`, `hmm_viterbi`, `posterior` and `solve`
    - Documented the program and created the `README.md` file.
2. **Arju Singh:**
    - Conducted extensive testing and handled edge cases.


## Assumptions and Notes
- The input data must consist of sentences and their corresponding POS tags.
- The model assumes that all words in the input sentence are already preprocessed (e.g., tokenized).
- The model's performance improves with more training data.


## Output
The program will:
1. Prints the initial sentence and its true POS tags.
2. Tags the sentence using either the simplified model or HMM-based model.
3. Prints the predicted POS tags for the input sentence.
