import pathlib

import test_utils


class Ch13Tests(test_utils.TestCase):

    def setUp(self):
        self.dir = pathlib.Path(__file__).resolve().parent

    def test_food_database(self):
        import os

        # import data
        ret = self.run_script('importdata.py').returncode
        self.assertEqual(0, ret)
        self.assertTrue((self.dir / 'food.db').exists())

        # make queries
        test_cases = [
            "id = '01105'",
            "kcal <= 100 AND fiber >= 10 ORDER BY sugar",
            "desc LIKE 'CHICKEN%' AND fat >= 5 AND fat < 10 ORDER BY protein DESC",
        ]
        for i, cond in enumerate(test_cases, start=1):
            self.assertScriptOutput(
                'food_query.py', args=f'"{cond}"',
                output_file=self.dir / f'testdata/food_database_output{i}.txt')

        os.remove(self.dir / 'food.db')
