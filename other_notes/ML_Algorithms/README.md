# ML Algorithms

## Table of Content

- [ML Algorithms](#ml-algorithms)
  - [Table of Content](#table-of-content)
  - [Hard Vs Soft Voting In ML](#hard-vs-soft-voting-in-ml)
    - [Hard Voting](#hard-voting)
    - [Advantages of Hard Voting](#advantages-of-hard-voting)
    - [Disadvantages of Hard Voting](#disadvantages-of-hard-voting)
    - [Hard Voting Code](#hard-voting-code)
    - [Soft Voting](#soft-voting)
    - [Advantages of Soft Voting](#advantages-of-soft-voting)
    - [Disadvantages of Soft Voting](#disadvantages-of-soft-voting)
    - [Soft Voting Code](#soft-voting-code)

## Hard Vs Soft Voting In ML

### Hard Voting

[![image.png](https://i.postimg.cc/FsZXFwnH/image.png)](https://postimg.cc/rKKPQZkB)

- Hard voting, also known as `majority voting`, is a simple technique used in ensemble learning to combine the predictions of multiple machine learning models for classification tasks.

- Here's how it works:
  - Individual predictions: Each base model in the ensemble makes a prediction for a given data point. These predictions are typically class labels, such as "cat" or "dog" for an image classification task.
  - Vote counting: For each class, the number of votes received from individual models is counted.
  - Majority wins: The class with the highest vote count is chosen as the final prediction of the ensemble.

- [More info (blog)](https://ilyasbinsalih.medium.com/what-is-hard-and-soft-voting-in-machine-learning-2652676b6a32#:~:text=Hard%20voting%20is%20the%20simplest,image%20is%20of%20a%20cat.)

### Advantages of Hard Voting

- **Simple and easy to implement**: It requires minimal computational resources and is straightforward to understand.
- **Interpretable**: The final prediction can be directly linked to the majority vote, offering some level of interpretability.

### Disadvantages of Hard Voting

- **May not consider model confidence**: All models are treated equally regardless of their individual performance or confidence in their predictions.
- **Potentially suboptimal**: It might not always lead to the best possible performance compared to other ensemble methods like soft voting.

### Hard Voting Code

```py
import numpy as np
from sklearn.ensemble import VotingClassifier

# Create a list of classifiers.
classifiers = [
    KNeighborsClassifier(n_neighbors=5),
    RandomForestClassifier(n_estimators=100),
    DecisionTreeClassifier()
]

# Create a voting classifier.
voting_clf = VotingClassifier(estimators=classifiers, voting='hard')

# Train the voting classifier.
voting_clf.fit(X_train, y_train)

# Make predictions.
y_pred = voting_clf.predict(X_test)

# Evaluate the accuracy.
print(accuracy_score(y_test, y_pred))
```

### Soft Voting

- Soft voting, also known as `weighted voting`, is another technique used in ensemble learning to combine predictions from multiple models for classification tasks.

- Unlike hard voting, which relies solely on the majority vote, soft voting takes into account the `confidence scores` associated with each model's prediction.

- Here's how it works:

  - **Individual predictions**: Similar to hard voting, each base model makes a prediction for a given data point. However, instead of simply providing a class label, the models also output a confidence score (often a probability) indicating how certain they are about their prediction.
  - **Weighted voting**: Each model's prediction is weighted by its respective confidence score. This means that models with higher confidence scores have a greater influence on the final prediction.
  - **Sum and choose**: The weighted predictions for each class are summed. The class with the highest sum of weighted scores is chosen as the final prediction of the ensemble.

### Advantages of Soft Voting

- everages confidence scores: It utilizes the confidence information from individual models, potentially leading to a more accurate final prediction.
- Can be more robust: By considering confidence, it may be less susceptible to noisy predictions from individual models.

### Disadvantages of Soft Voting

- Requires confidence scores: Not all models naturally output confidence scores. Additional processing might be needed to obtain them.
- Potentially complex: Depending on the weighting scheme used, soft voting can be more intricate to implement compared to hard voting.

### Soft Voting Code

```py
import numpy as np
from sklearn.ensemble import VotingClassifier

# Create a list of classifiers.
classifiers = [
    KNeighborsClassifier(n_neighbors=5),
    RandomForestClassifier(n_estimators=100),
    DecisionTreeClassifier()
]

# Create a voting classifier.
voting_clf = VotingClassifier(estimators=classifiers, voting='soft')

# Train the voting classifier.
voting_clf.fit(X_train, y_train)

# Make predictions.
y_pred = voting_clf.predict_proba(X_test)

# Evaluate the accuracy.
print(accuracy_score(y_test, y_pred.argmax(axis=1)))
```
