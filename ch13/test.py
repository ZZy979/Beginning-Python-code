import test_utils


class Ch13Tests(test_utils.TestCase):
    dirname = 'ch13'

    def test_food_database(self):
        import os

        # import data
        ret = self.run_script('importdata.py').returncode
        self.assertEqual(0, ret)
        self.assertTrue((self.src_dir / 'food.db').exists())

        # make queries
        test_cases = [
            "id = '01105'",
            "kcal <= 100 AND fiber >= 10 ORDER BY sugar",
            "desc LIKE 'CHICKEN%' AND fat >= 5 AND fat < 10 ORDER BY protein DESC",
        ]
        for i, cond in enumerate(test_cases, start=1):
            self.assertScriptOutput(
                'food_query.py', args=f'"{cond}"',
                output_file=self.testdata_dir / f'food_database_output{i}.txt')

        os.remove(self.src_dir / 'food.db')
