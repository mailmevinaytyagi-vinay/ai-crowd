import random

def get_telecom_estimate(location, base_count):
    """
    Simulate telecom-based crowd estimation
    """

    variation = random.randint(-10, 20)
    telecom_count = max(0, int(base_count * 1.2 + variation))

    # Confidence logic
    if telecom_count < 30:
        confidence = 0.6
    elif telecom_count < 80:
        confidence = 0.75
    else:
        confidence = 0.9

    return telecom_count, confidence


def fuse_counts(ai_count, telecom_count):
    """
    Combine AI + telecom signals
    """
    return int((ai_count * 0.6) + (telecom_count * 0.4))