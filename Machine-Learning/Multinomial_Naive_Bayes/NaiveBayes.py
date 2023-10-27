import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

sentences = [
            "The final scores of the game are out, and it was a high-scoring match.",
            "A very close and competitive game kept the fans on the edge of their seats.",
            "Despite a forgettable start, the team managed to turn the game around.",
            "The candidates are neck and neck in the close election race.",
            "The election is over, and now the counting of votes begins.",
            "The intense match ended with a thrilling victory.",
            "The election polls are closed, and now the wait for results begins.",
            "The players put up a spirited performance in the closely contested game.",
            "The fans cheered loudly as their team scored the winning goal.",
            "A thrilling basketball match had the spectators on the edge of their seats.",
            "In a heated debate, the candidates discussed their views on various issues.",
            "A nail-biting race saw the competitors giving their all until the finish line.",
            "The clean match showcased excellent sportsmanship from both teams.",
            "After weeks of campaigning, the election results are finally in.",
            "The controversial election has led to intense discussions and debates.",
            "The candidates are tirelessly campaigning to win the upcoming election."
        ]

categories = [
            "sports", "sports", "sports", "elections", "elections", "sports", "elections", "sports",
            "sports", "sports", "elections", "sports", "sports", "elections", "elections", "elections"
        ]

class NaiveBayesClassifier:

    @staticmethod
    def fit(X, y):
        classes = np.unique(y)
        class_probs = {}
        word_probs = {}
        total_documents = len(y)
        vocab = set()

        for c in classes:
            class_count = np.count_nonzero(y)
            class_probs[c] = class_count/total_documents

        for c in classes:
            class_docs = [X[i] for i,label in enumerate(y) if label==c]
            total_words_in_class = np.sum(class_docs)
            vocab.update(range(X.shape[1]))
            word_counts = np.sum(class_docs, axis=0)
            word_probs[c] = (word_counts+1)/(total_words_in_class + len(vocab))
            

        return class_probs, word_probs
            
    
    @staticmethod
    def predict(X, class_probs, word_probs, classes):
        predictions = []
        for doc in X:
            best_class = None
            max_prob = -np.inf

            for c in classes:
                class_prob = class_probs[c]
                word_prob = word_probs[c]
                log_prob = np.log(class_prob+np.sum(word_prob * doc))

                if log_prob > max_prob:
                    max_prob = log_prob
                    best_class = c
            predictions.append(best_class)
        return predictions

vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(sentences)
class_probs, word_probs = NaiveBayesClassifier.fit(X_train_vec.toarray(), categories)

test_cases = [
        ("a great match", "sports"),
        ("election is approaching", "elections"),
        ("a very close game", "sports"),
        ("the final election results are in", "elections"),
        ("a heated and competitive match", "sports"),
        ("the candidates are campaigning passionately", "elections"),
        ("a forgettable and uneventful game", "sports"),
        ("fans cheered loudly during the game", "sports"),
        ("a controversial debate between candidates", "elections"),
        ("the thrilling match ended in a tie", "sports")
    ]

num_passed = 0

for test_sentence, correct_category in test_cases:
    test_vector = vectorizer.transform([test_sentence]).toarray()
    prediction = NaiveBayesClassifier.predict(test_vector, class_probs, word_probs, np.unique(categories))[0]
    if prediction == correct_category:
        print(f"Test Passed: '{test_sentence}' - Predicted: {prediction} | Correct: {correct_category}")
        num_passed += 1
    else:
        print(f"Test Failed: '{test_sentence}' - Predicted: {prediction} | Correct: {correct_category}")




