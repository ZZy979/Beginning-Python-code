def checkIndex(key):
    """
    Is the given key an acceptable index?

    To be acceptable, the key should be a non-negative integer.
    If it is not an integer, a TypeError is raised;
    if it is negative, an IndexError is raised (since the sequence is of infinite length).
    """
    if not isinstance(key, int): raise TypeError
    if key < 0: raise IndexError


class ArithmeticSequence:
    """
    An "infinite" sequence of numbers in which each is greater than the previous one by a constant amount.
    The user is allowed to change some of the elements.
    """

    def __init__(self, start=0, step=1):
        """
        Initialize the arithmetic sequence.

        start - the first value in the sequence
        step - the difference between two adjacent values
        changed - a dictionary of values that have been modified by
        the user
        """
        self.start = start  # Store the start value
        self.step = step    # Store the step value
        self.changed = {}   # No items have been modified

    def __getitem__(self, key):
        """
        Get an item from the arithmetic sequence.
        """
        checkIndex(key)
        try:
            return self.changed[key]             # Modified?
        except KeyError:                         # otherwise...
            return self.start + key * self.step  # ...calculate the value

    def __setitem__(self, key, value):
        """
        Change an item in the arithmetic sequence.
        """
        checkIndex(key)
        self.changed[key] = value  # Store the changed value
