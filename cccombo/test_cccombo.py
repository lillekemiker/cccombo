import unittest
from cccombo import CCCombo

combo_dict = {
    ('right', 'a'): 'Bounce',
    ('b', 'b', 'right'): 'Dashrun',
    ('up', 'up', 'right', 'a'): 'Super Fileball',
    ('left', 'right', 'left', 'right', 'b', 'b', 'b'): 'Mega Shake',
    ('up', 'up', 'down', 'down', 'left', 'right', 'left', 'right', 'select', 'start'): 'Konami'
}

class TestCCCombo(unittest.TestCase):
    def test_buffer_initiates(self):
        detector = CCCombo(combo_dict)
        self.assertEquals(detector._buffer_size, 10)
        self.assertEquals(detector._combo_lengths, {2, 3, 4, 7, 10})
        self.assertEquals(detector._buffer, [])

    def test_buffer_filling(self):
        detector = CCCombo(combo_dict)
        # Assert it fills until full
        for x in xrange(detector._buffer_size):
            detector(x)
            self.assertEquals(detector._buffer, range(x+1))

    def test_buffer_shifts_when_full(self):
        detector = CCCombo(combo_dict)
        # Fill buffer
        _ = [detector('a') for x in xrange(detector._buffer_size)]
        # Test push/pop
        for x in xrange(detector._buffer_size):
            detector(x)
            expected_buffer = ['a'] * (detector._buffer_size - x - 1) + range(x+1)
            self.assertEquals(detector._buffer, expected_buffer)

    def test_no_detect_when_no_combos(self):
        detector = CCCombo(combo_dict)
        # Since the buffer is tested, no need to test further than the buffer size
        for x in xrange(detector._buffer_size):
            detected_combos = detector('a')
            self.assertEquals(detected_combos, set())

    def test_detect_combos(self):
        detector = CCCombo(combo_dict)
        for key_stroke in ('up', 'up', 'right'): # No Combos yet
            detected_combos = detector(key_stroke)
            self.assertEquals(detected_combos, set())
        detected_combos = detector('a')
        expected_combos = {(('up', 'up', 'right', 'a'), 'Super Fileball'), (('right', 'a'), 'Bounce')}
        self.assertEquals(detected_combos, expected_combos)