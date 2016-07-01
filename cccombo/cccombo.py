


VALID_KEY_STROKES = ('a', 'b', 'up', 'down', 'left', 'right', 'select', 'start')


class CCCombo(object):
    '''
    Combo keys should be in the form of tuples
    '''
    def __init__(self, combo_dict):
        self._combo_dict = combo_dict
        self._combo_lengths = set([len(combo) for combo in combo_dict])
        self._buffer_size = max(self._combo_lengths)
        self._buffer = []

    def _add_keystroke(self, key_stroke):
        '''
        It is assumed that key_stroke has already been verified to be a legit input.
        '''
        self._buffer.append(key_stroke)
        while len(self._buffer) > self._buffer_size:
            self._buffer.pop(0)

    def _detect_combos(self):
        combos = set()
        for key_len in self._combo_lengths:
            test_key = tuple(self._buffer[-key_len:])
            try:
                combos.add((test_key, self._combo_dict[test_key]))
            except KeyError:
                pass
        return combos

    def __call__(self, key_stroke):
        self._add_keystroke(key_stroke)
        return self._detect_combos()
