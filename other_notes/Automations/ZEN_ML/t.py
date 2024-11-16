def probability_to_credit_score(probability: float) -> int:
    """Convert a probability value to a credit score.

    This function takes a probability value and converts it to a credit score
    in the range of 300-800. A small alpha value is added to the probability
    to ensure proper scaling.

    Parameters
    ----------
    probability : float
        Input probability value, typically between 0 and 1

    Returns
    -------
    int
        Calculated credit score between 300 and 800
    """
    alpha: float = 0.005  # This adds a small increment to the probability
    probability = probability + alpha
    min_score: int = 300
    max_score: int = 800
    score_range: int = max_score - min_score

    # Calculate the credit score based on the probability
    credit_score: int = round(max_score - (probability * score_range))

    return credit_score


# Example usage
pd = 0.45

credit_score = probability_to_credit_score(pd)
# print(credit_score)
