import json
import argparse
from collections import Counter
import math


# Helper function to calculate Euclidean distance
def euclidean_distance(point1, point2):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(point1, point2)))


# Helper function to calculate Manhattan distance
def manhattan_distance(point1, point2):
    return sum(abs(x - y) for x, y in zip(point1, point2))


# K-Nearest Neighbors Implementation
def K_Nearest_Neighbors(file: str, k: int, distance_metric: str):
    """ Implements K-Nearest Neighbors Algorithm

    Args:
        file (str): path to the dataset file
        k (int): number of nearest neighbors considered in the analysis
        distance_metric (str): distance metric for K-NN algorithm

    Returns:
        float: accuracy on the test set
    """
    # Load dataset
    with open(file, 'r') as f:
        data = json.load(f)
        X_train, y_train = data['X_train'], data['y_train']
        X_test, y_test = data['X_test'], data['y_test']

    # Choose distance metric
    if distance_metric == "euclidean":
        distance_function = euclidean_distance
    elif distance_metric == "manhattan":
        distance_function = manhattan_distance
    else:
        raise ValueError("Unsupported distance metric. Use 'euclidean' or 'manhattan'.")

    predictions = []

    for test_point in X_test:
        # Calculate distances from test point to all training points
        distances = [(distance_function(test_point, train_point), label)
                     for train_point, label in zip(X_train, y_train)]

        # Sort distances and handle ties by label value
        distances.sort(key=lambda x: (x[0], x[1]))
        k_neighbors = [label for _, label in distances[:k]]

        # Majority voting: Resolve ties by choosing smallest label
        label_count = Counter(k_neighbors)
        most_common_label = min(label for label, count in label_count.items()
                                if count == max(label_count.values()))

        predictions.append(most_common_label)

    # Calculate accuracy
    correct_predictions = sum(1 for pred, actual in zip(predictions, y_test) if pred == actual)
    accuracy_test_set = (correct_predictions / len(y_test)) * 100

    return accuracy_test_set


# Main function
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
