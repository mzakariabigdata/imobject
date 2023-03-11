# fonction to compare two dicts
def compare_document(d1, d2):
    """
    Compare two documents (collection or structures contain different types of data)
      and their attributes recursively.

    Parameters:
        d1 (list, dict or object): First document or object to compare.
        d2 (list, dict or object): Second document or object to compare.

    Returns:
        bool: True if the two documents or objects are equal, False otherwise.
    """
    if isinstance(d1, dict) and isinstance(d2, dict):
        if len(d1) != len(d2):
            return False
        for key, value in d1.items():
            if key not in d2 or not compare_document(value, d2[key]):
                return False
        return True
    elif not any(isinstance(d1, t) for t in (int, float, str, bool, list)) and type(
        d1
    ) == type(d2):
        return d1.__dict__() == d2.__dict__()
    elif isinstance(d1, list) and isinstance(d2, list):
        if len(d1) != len(d2):
            return False
        for i in range(len(d1)):
            if not compare_document(d1[i], d2[i]):
                return False
        return True
    else:
        return d1 == d2
