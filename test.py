import unittest
from budget import BudgetService, Budget
from datetime import datetime


class TestBudget(unittest.TestCase):

    def setUp(self):
        self.budgetservice = BudgetService()

    def test_query_completed_months(self):
        self.budgetservice.budget_repo.budget_list = [
            Budget("202301", 31),
            Budget("202302", 28)
        ]

        result = self.budgetservice.query(
            datetime(2023, 1, 1).date(),  datetime(2023, 2, 28).date())
        expected = 59

        self.assertEqual(result, expected)

    def test_query_not_completed_months(self):
        self.budgetservice.budget_repo.budget_list = [
            Budget("202301", 31),
            Budget("202302", 28)
        ]

        result = self.budgetservice.query(
            datetime(2023, 1, 31).date(),  datetime(2023, 2, 10).date())
        expected = 11

        self.assertEqual(result, expected)

    def test_query_same_day(self):
        self.budgetservice.budget_repo.budget_list = [
            Budget("202301", 31),
            Budget("202302", 28)
        ]

        result = self.budgetservice.query(
            datetime(2023, 1, 1).date(),  datetime(2023, 1, 1).date())
        expected = 1

        self.assertEqual(result, expected)

    def test_query_leap_year(self):
        self.budgetservice.budget_repo.budget_list = [
            Budget("202001", 31),
            Budget("202002", 29)
        ]

        result = self.budgetservice.query(
            datetime(2020, 1, 1).date(),  datetime(2020, 2, 29).date())
        expected = 60

        self.assertEqual(result, expected)

    def test_query_not_in_availale_range(self):
        self.budgetservice.budget_repo.budget_list = [
            Budget("202301", 31),
            Budget("202302", 28)
        ]

        result = self.budgetservice.query(
            datetime(2020, 1, 1).date(),  datetime(2020, 2, 29).date())
        expected = 0

        self.assertEqual(result, expected)

    def test_query_end_earlier_than_start(self):
        self.budgetservice.budget_repo.budget_list = [
            Budget("202301", 31),
            Budget("202302", 28)
        ]

        result = self.budgetservice.query(
            datetime(2020, 2, 29).date(), datetime(2020, 1, 1).date())
        expected = 0

        self.assertEqual(result, expected)

    def test_get_all(self):
        expected_budget_list = [
            Budget("202301", 31),
            Budget("202302", 28)
        ]

        self.budgetservice.budget_repo.budget_list = [
            Budget("202301", 31),
            Budget("202302", 28)
        ]
        self.assertEqual(
            self.budgetservice.budget_repo.get_all()[0].year_month,
            expected_budget_list[0].year_month
        )


if __name__ == '__main__':

    unittest.main()
