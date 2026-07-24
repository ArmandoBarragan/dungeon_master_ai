import unittest

from src.game_engine.enemy import Enemy


class EnemyTests(unittest.TestCase):
    def test_enemy_has_armor_class(self):
        enemy = Enemy({"name": "Goblin", "species": "Goblin"})

        self.assertTrue(hasattr(enemy, "armor_class"))
        self.assertIsInstance(enemy.armor_class, int)


if __name__ == "__main__":
    unittest.main()
