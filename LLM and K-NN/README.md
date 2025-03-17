# Assignment-4

## Part 1: Can an LLM Play "Tic-Tac-What?"

### 1. Problem Overview

The goal is to test whether a Large Language Model (LLM) can play a variation of Tic-Tac-Toe called **Notakto**. This task evaluates the model's ability to reason, make decisions, and respond effectively based on prompts, while adhering to the specific game rules.

### Rules of Notakto:

1. The game is played on a grid (3x3 or 4x4).
2. Both players use **X's**—there are no O's.
3. Players take turns placing one X in an empty cell.
4. **The player who completes a line** (vertical, horizontal, or diagonal) of the required length (e.g., 3 on a 3x3 board) **loses the game**.
5. Players cannot skip turns or place an X in an already occupied cell.

### Objectives Are :

1. Test if the LLM can make **optimal moves** and pass specific test cases.
2. Analyze how **prompt design** affects its gameplay.
3. Determine if the LLM can successfully complete a game against a random opponent starting from an empty board.

## 2. Experiments Conducted

To tackle the problem, I carried out two experiments:

1. **Experiment 1**:  
   Used the initial code and prompts with minimal adjustments. Tested the model on specific scenarios for both 3x3 and 4x4 grids.

2. **Experiment 2**:  
   Enhanced the prompts for better clarity and reasoning. Focused on guiding the model to think and decide step-by-step.

Both experiments evaluated the LLM's ability to identify valid moves, avoid losing moves, and adhering  rules.

### 3. Experiment 1: Initial Code Implementation

### 3.1 Code Overview

In this experiment, the provided code was used to interact with the **LLama3** model. The prompts were structured but did not include detailed instructions, which occasionally resulted in unclear or ambiguous outputs.

#### System Prompt (Original):  
```
system_template = (
    "You are a Notakto (misere mode) game analyzer. Your goal is to analyze the board "
    "and make a move to avoid forming a sequence of 3 X's vertically, horizontally, or diagonally. "
    "Always follow the rules of the game and provide structured output."
)
```
#### Human Prompt (Original):

```
human_template = """
Analyze the current board state and make a move according to the following rules:
1. Place a single 'X' on an empty cell.
2. Do not form a sequence of 3 'X's in any direction (vertical, horizontal, or diagonal).
3. Return the updated board as a structured 3x3 grid.

Current board:
{board}
"""
```

####  Parser Implementation  - 
The code utilizes **Pydantic schemas** to ensure that the board's output adheres to a structured 3x3 format, maintaining consistency and reliability in board representation.

### 3.2 Results and Observations

**Test Cases on 3x3 Board**:
- The LLM successfully avoided losing moves in straightforward scenarios where only one valid move was available.  
- In situations with multiple valid moves, the model occasionally chose suboptimal moves, leading to immediate losses.  

**Performance on 4x4 Board**:
- On a custom 4x4 board requiring a sequence length of 4, the LLM struggled to generalize, frequently making invalid or losing moves.  

**Key Issue**:
- The model often failed to analyze all possible moves before deciding, highlighting a lack of systematic, step-by-step reasoning.

#### 3.3 Adjustments Made

To address these shortcomings:
1. **Validation**: Input/output validation was enhanced using the Pydantic schema to ensure structured and consistent board formatting.  
2. **Consistency**: Ensured the board formatting remained clear and uniform before being processed by the model.  
3. **Comprehension Improvements**: Made minor tweaks to formatting and whitespace to enhance the model's understanding and output quality.

### 4. Experiment 2: Prompt Refinement

#### 4.1 Changes in the Prompt

In this experiment, the focus was on refining the system and human prompts to enhance clarity and encourage the model to adopt a step-by-step reasoning approach for better decision-making.

#### Modified System Prompt:  
```
system_template = (
    "You are a careful Notakto game-playing assistant. Your goal is to analyze the board carefully "
    "and make a move that avoids forming a sequence of 3 X's. Always prioritize avoiding immediate losses."
)
```
#### Modified Human Prompt:
```
human_template = """
Think step by step and carefully analyze the board state:
1. Identify all empty cells on the board.
2. For each empty cell, simulate placing an 'X'.
3. Check whether placing an 'X' in that cell will form a sequence of 3 X's vertically, horizontally, or diagonally.
4. Choose the cell that avoids creating a sequence of 3 X's.
5. Return the updated board as a structured 3x3 grid.

Current board:
{board}
"""
```
### 4.2 Results and Observations

**Improved Test Case Performance**:  
- On the 3x3 board, the LLM successfully passed all test cases and consistently avoided losing moves.  

**4x4 Board Performance**:  
- The refined prompt significantly improved the model's performance on the 4x4 grid, although occasional errors still occurred when deeper reasoning was required.  

**Impact of Step-by-Step Reasoning**:  
- Adding explicit instructions like "Think step by step" helped the LLM systematically evaluate all possible moves, leading to better decision-making.


### 4.3 Key Comparison

| **Metric**                  | **Experiment 1** | **Experiment 2** |
|-----------------------------|------------------|------------------|
| Test Case Pass Rate (3x3)   | 60%              | 100%             |
| Test Case Pass Rate (4x4)   | 40%              | 80%              |
| Structured Output Accuracy  | Moderate         | High             |
| Step-by-Step Reasoning      | Not Implemented  | Implemented      |

### 5. Key Insights

1. **Importance of Prompt Refinement**:  
   Providing clear, step-by-step instructions greatly enhanced the model's ability to make optimal moves and avoid mistakes.

2. **Limitations of LLMs**:  
   The model performed well on smaller boards (3x3) but struggled with larger boards (4x4), highlighting limitations in its reasoning and problem-solving depth.

3. **Structured Output Validation**:  
   Enforcing a strict format for the output reduced errors and ambiguity, ensuring better consistency and accuracy. 

### 6. Challenges and Assumptions

#### Challenges

1. **Ambiguity in Initial Instructions**:  
   Without explicit step-by-step reasoning, the model struggled to analyze all possible moves effectively.  

2. **Generalization to Larger Boards**:  
   Performance dropped on the 4x4 board due to the added complexity and depth of reasoning required.  

3. **Structured Output Parsing**:  
   Ensuring consistent and valid output for both 3x3 and 4x4 boards required robust schema validation.

#### Assumptions

1. The provided board state is correctly formatted and valid.  
2. The model adheres to the game rules and does not skip moves.  
3. The test cases used accurately represent typical gameplay scenarios.

### 7. Conclusion

The experiments demonstrate that an LLM can effectively play "Notakto" on smaller grids when guided by well-designed prompts. Clear, step-by-step instructions significantly enhance its reasoning and decision-making abilities.

- **3x3 Board**: The model performed flawlessly with refined prompts.  
- **4x4 Board**: Performance improved but still showed limitations in handling complex game states.  

Using structured output schemas ensured valid and consistent responses. However, to improve performance on larger grids, future efforts should focus on enhancing the model's reasoning depth and exposing it to more complex training examples. In summary, the LLM's success relies heavily on the quality of the prompts guiding its decision-making process. 

---
---

## Part 2: K-Nearest Neighbors Algorithm

### 1. Problem Formulation

The goal of this part of the assignment is to implement the K-Nearest Neighbors (K-NN) algorithm from scratch to classify synthetic datasets and analyze its performance. The evaluation involves:

- Calculating the accuracy for different values of \( k \).
- Experimenting with two distance metrics (Euclidean and Manhattan).
- Interpreting the results based on dataset characteristics and parameter changes.

## 2. Implementation Details

### 2.1 What is K-Nearest Neighbors (K-NN)?

K-Nearest Neighbors is a simple machine learning algorithm used for classification tasks. It classifies a test point by looking at the closest \( k \) training points (neighbors) and using majority voting to decide the class label.

### 2.2 Distance Metrics

To find the closest neighbors, we calculate the distance between the test point and each training point using two metrics:

1. **Euclidean Distance (Straight-line distance):**
   - This is the standard distance calculation used in geometry.

2. **Manhattan Distance (Sum of absolute differences):**
   - This distance measures the path between points as if moving along a grid (like a city street).

### 2.3 Python Code for K-NN

Below is the Python code usesd for implementing K-NN:

```
import json
import argparse
from collections import Counter
import math

def euclidean_distance(point1, point2):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(point1, point2)))

def manhattan_distance(point1, point2):
    return sum(abs(x - y) for x, y in zip(point1, point2))

def K_Nearest_Neighbors(file: str, k: int, distance_metric: str):
    with open(file, 'r') as f:
        data = json.load(f)
        X_train, y_train = data['X_train'], data['y_train']
        X_test, y_test = data['X_test'], data['y_test']

    if distance_metric == "euclidean":
        distance_function = euclidean_distance
    elif distance_metric == "manhattan":
        distance_function = manhattan_distance
    else:
        raise ValueError("Unsupported distance metric. Use 'euclidean' or 'manhattan'.")

    predictions = []

    for test_point in X_test:
        distances = [(distance_function(test_point, train_point), label)
                     for train_point, label in zip(X_train, y_train)]
        distances.sort(key=lambda x: (x[0], x[1]))
        k_neighbors = [label for _, label in distances[:k]]
        label_count = Counter(k_neighbors)
        most_common_label = min(label for label, count in label_count.items()
                                if count == max(label_count.values()))
        predictions.append(most_common_label)

    correct_predictions = sum(1 for pred, actual in zip(predictions, y_test) if pred == actual)
    accuracy_test_set = (correct_predictions / len(y_test)) * 100

    return accuracy_test_set

def main():
    parser = argparse.ArgumentParser(description='KNN Classification with Synthetic Data')
    parser.add_argument('--dataset_path', type=str, help="path to the json file containing data")
    parser.add_argument('--k', type=int, help="k for k-NN algorithm")
    parser.add_argument('--distance_metric', type=str, help="distance metric for K-NN")
    args = parser.parse_args()

    accuracy = K_Nearest_Neighbors(args.dataset_path, args.k, args.distance_metric)
    print(f"Test set accuracy for {args.dataset_path} - {accuracy}.")

if __name__ == '__main__':
    main()



```


### 2.4 How It Works

1. The program reads the dataset, which includes training and test points.
2. It calculates distances (using **Euclidean** or **Manhattan**) between each test point and all training points.
3. It selects the \( k \)-nearest training points based on the smallest distances.
4. Using majority voting, the most frequent class label among the neighbors is assigned to the test point.
5. Accuracy is calculated as the percentage of correctly predicted labels.

### 2.5 Execution Example

To run the program:

1. Euclidean Distance we use -
 ```
python3 main.py --dataset_path dataset_1.json --k 3 --distance_metric "euclidean"
```  
   
2. Manhattan Distance we use -
```
python3 main.py --dataset_path dataset_1.json --k 3 --distance_metric "manhattan"
```

## 3. Results

The following tables summarize the accuracy for all datasets with both Euclidean and Manhattan distances:

### Euclidean Distance Results

| Dataset   |  k = 3  |  k = 6 |  k =  9 |
|-----------|-------------|-------------|-------------|
| Dataset 1 | 100.0%      | 100.0%      | 100.0%      |
| Dataset 2 | 72.0%       | 72.0%       | 74.0%       |
| Dataset 3 | 42.0%       | 48.0%       | 44.0%       |

### Manhattan Distance Results

| Dataset   |  k =  3 | k = 6|  k = 9 |
|-----------|-------------|-------------|-------------|
| Dataset 1 | 100.0%      | 100.0%      | 100.0%      |
| Dataset 2 | 72.0%       | 72.0%       | 74.0%       |
| Dataset 3 | 38.0%       | 36.0%       | 44.0%       |

## 4. Observations and Insights

### 4.1 Accuracy Trends Across Datasets

- **Dataset 1**: Accuracy is perfect (100%) because the data points are well-separated and easy to classify.
- **Dataset 2**: Accuracy stabilizes around 72-74%, indicating some overlap between classes.
- **Dataset 3**: Lower accuracy reflects the complexity and noise in the data.

### 4.2 Impact of  k  Values

- **Smaller \( k \)** (e.g., 3): Sensitive to noise and local patterns, leading to potentially unstable predictions.
- **Larger \( k \)** (e.g., 9): Provides smoother classification but may miss smaller or isolated clusters in the data.

### 4.3 Comparison of Distance Metrics

- **Euclidean Distance**: Generally performs better on datasets where class separation involves large distances.
- **Manhattan Distance**: Performs similarly to Euclidean in most cases but struggles with noisy or complex datasets like Dataset 3.

## 5. Challenges and Assumptions

### Challenges

1. **Ties**: Handling ties among \( k \)-nearest neighbors added complexity.  
2. **Dataset Issues**: Dataset 3 was noisy and had overlapping classes, making it harder to classify.  
3. **Choosing \( k \)**: Finding the right \( k \) required trial and error.  
4. **Distance Metrics**: Results varied depending on whether Euclidean or Manhattan distances were used, especially for noisy data.  
5. **Performance**: Calculating distances for large datasets was time-consuming.

### Assumptions

1. Datasets are preprocessed and scaled.  
2. Input JSON files are correctly formatted and split into training and test data.  
3. \( k \) is chosen based on experimentation.  
4. Labels are consistent and accurate.  
5. Input files have no missing or corrupted data.











