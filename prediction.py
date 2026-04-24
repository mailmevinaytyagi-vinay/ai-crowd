def predict_crowd(history):
    """
    Returns:
    - predicted value
    - confidence level
    - trend direction
    """

    if len(history) < 5:
        return (history[-1] if history else 0), "Low", "→"

    recent = history[-5:]
    diff = recent[-1] - recent[0]

    # Prediction
    predicted = int(recent[-1] + diff * 0.5)

    # Confidence
    if abs(diff) < 5:
        confidence = "High"
    elif abs(diff) < 15:
        confidence = "Medium"
    else:
        confidence = "Low"

    # Trend direction
    if diff > 5:
        trend = "↑"
    elif diff < -5:
        trend = "↓"
    else:
        trend = "→"

    return max(predicted, 0), confidence, trend