import unittest
from unittest.mock import patch
import artillery3_game

class TestArtillery3Game(unittest.TestCase):

    def test_is_defunct(self):
        p = {1: 12, 2: 0, 3: 12}
        self.assertTrue(artillery3_game.is_defunct(1, p))
        self.assertFalse(artillery3_game.is_defunct(2, p))
        self.assertTrue(artillery3_game.is_defunct(3, p))

    @patch('builtins.input', side_effect=['2'])
    def test_get_players_valid(self, mock_input):
        self.assertEqual(artillery3_game.get_players(), 2)

    @patch('builtins.input', side_effect=['4', '1', '2'])
    def test_get_players_invalid(self, mock_input):
        self.assertEqual(artillery3_game.get_players(), 2)

    @patch('random.random', return_value=0.5)
    def test_shoot_hit(self, mock_random):
        r = {(1, 2): 1000, (2, 1): 1000}
        v = {1: 100}
        p = {1: 0, 2: 0}
        artillery3_game.shoot(1, 2, 45, r, v, p)
        self.assertEqual(p[2], 12)  # Target becomes defunct on hit

    def test_shoot_invalid_angle(self):
        r = {(1, 2): 1000}
        v = {1: 100}
        p = {1: 0, 2: 0}
        artillery3_game.shoot(1, 2, 181, r, v, p)
        self.assertEqual(p[1], 12)  # Shooter becomes defunct

    @patch('builtins.input', side_effect=['2',
    '45', '10', '3', '45', '100', '1', '45'])
    def test_game_dialogue_sequence(self, mock_input):
        artillery3_game.play_game()
        # Check the game log against expected sequence
        log_file = 'game_log.txt'
        with open(log_file, 'r') as f:
            actual_log = f.read()
        with open('reference_log.txt', 'r') as f:
            expected_log = f.read()
        self.assertEqual(actual_log, expected_log)