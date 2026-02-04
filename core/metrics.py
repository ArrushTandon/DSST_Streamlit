import Levenshtein

def cer(predicted, reference):
    if not reference or len(reference) < 5:
        return None
    return Levenshtein.distance(
        predicted.lower(),
        reference.lower()
    ) / len(reference)
