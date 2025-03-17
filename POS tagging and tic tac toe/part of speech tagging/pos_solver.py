###################################
# CS B551 Fall 2024, Assignment #3
#
# Your names and user ids: vvaradh - singarju
#

import math
from collections import defaultdict

class Solver:
    def __init__(self):
        self.emission_probs = defaultdict(lambda: defaultdict(float))
        self.transition_probs = defaultdict(lambda: defaultdict(float))
        self.initial_probs = defaultdict(float)
        self.tag_counts = defaultdict(int)
        self.possible_tags = set()
        self.vocab = set()
        self.alpha = 0.01  # Smoothing factor

    def train(self, data):
        tag_pair_counts = defaultdict(lambda: defaultdict(int))
        word_tag_counts = defaultdict(lambda: defaultdict(int))
        initial_tag_counts = defaultdict(int)

        for sentence, tags in data:
            previous_tag = None
            for i, (word, tag) in enumerate(zip(sentence, tags)):
                self.vocab.add(word)
                self.tag_counts[tag] += 1
                word_tag_counts[word][tag] += 1
                if i == 0:
                    initial_tag_counts[tag] += 1
                if previous_tag is not None:
                    tag_pair_counts[previous_tag][tag] += 1
                previous_tag = tag

        total_tags = sum(self.tag_counts.values())
        total_initial_tags = sum(initial_tag_counts.values())
        vocab_size = len(self.vocab)

        for tag in self.tag_counts:
            self.initial_probs[tag] = (initial_tag_counts[tag] + self.alpha) / (total_initial_tags + len(self.tag_counts))
            for next_tag in self.tag_counts:
                self.transition_probs[tag][next_tag] = (
                    (tag_pair_counts[tag][next_tag] + self.alpha) / (self.tag_counts[tag] + len(self.tag_counts))
                )
            for word in word_tag_counts:
                self.emission_probs[word][tag] = (
                    (word_tag_counts[word][tag] + self.alpha) / (self.tag_counts[tag] + vocab_size)
                )
            self.possible_tags.add(tag)

    def handle_unknown_word(self, word, tag):
        """Handle unknown words with additional features-based logic."""
        if word.istitle():
            return 0.6 if tag == "NOUN" else 0.2  # Proper noun logic
        elif word.isdigit():
            return 0.7 if tag == "NUM" else 0.3  # Numeric value logic
        elif word.endswith("ing") and tag == "VERB":
            return 0.5  # Verb detection logic
        return 0.2  # Default fallback

    def simplified(self, sentence):
        result = []
        for word in sentence:
            max_prob = -1
            best_tag = None

            for tag in self.possible_tags:
                emission_prob = self.emission_probs[word].get(tag, self.handle_unknown_word(word, tag))
                prob = emission_prob
                if result:
                    previous_tag = result[-1]
                    transition_prob = self.transition_probs[previous_tag].get(tag, 1 / (self.tag_counts[previous_tag] + len(self.possible_tags)))
                    prob *= transition_prob * 0.3  # Adjust weight between emission and transition
                if prob > max_prob:
                    max_prob = prob
                    best_tag = tag
            result.append(best_tag)
        return result

    def hmm_viterbi(self, sentence):
        V = [{}]
        path = {}

        beam_width = 10  # Increased beam width for better exploration

        for y in self.possible_tags:
            emission_prob = self.emission_probs[sentence[0]].get(y, self.handle_unknown_word(sentence[0], y))
            V[0][y] = self.initial_probs[y] * emission_prob
            path[y] = [y]

        for t in range(1, len(sentence)):
            V.append({})
            new_path = {}
            sorted_previous = sorted(
                ((V[t-1][y0], y0) for y0 in self.possible_tags), reverse=True
            )[:beam_width]

            for y in self.possible_tags:
                (prob, state) = max(
                    (prev_prob * self.transition_probs[y0].get(y, 1 / (self.tag_counts[y0] + len(self.possible_tags))) *
                     self.emission_probs[sentence[t]].get(y, self.handle_unknown_word(sentence[t], y)), y0)
                    for prev_prob, y0 in sorted_previous
                )
                V[t][y] = prob
                new_path[y] = path[state] + [y]

            path = new_path

        n = len(sentence) - 1
        (prob, state) = max((V[n][y], y) for y in self.possible_tags)
        return path[state]

    def posterior(self, model, sentence, label):
        log_prob = 0

        if model == "Simple":
            for word, tag in zip(sentence, label):
                prob = self.emission_probs[word].get(tag, self.handle_unknown_word(word, tag))
                log_prob += math.log(prob)
            return log_prob

        elif model == "HMM":
            initial_prob = self.initial_probs.get(label[0], 1 / (sum(self.tag_counts.values()) + len(self.possible_tags)))
            log_prob += math.log(initial_prob)
            first_emission_prob = self.emission_probs[sentence[0]].get(label[0], self.handle_unknown_word(sentence[0], label[0]))
            log_prob += math.log(first_emission_prob)

            for i in range(1, len(sentence)):
                transition_prob = self.transition_probs[label[i-1]].get(label[i], 1 / (self.tag_counts[label[i-1]] + len(self.possible_tags)))
                emission_prob = self.emission_probs[sentence[i]].get(label[i], self.handle_unknown_word(sentence[i], label[i]))
                log_prob += math.log(transition_prob) + math.log(emission_prob)

            return log_prob

        return float('-inf')

    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        else:
            print("Unknown algorithm!")
