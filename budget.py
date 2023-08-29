from typing import List
from datetime import datetime, date
from calendar import monthrange


from dateutil.relativedelta import relativedelta


class BudgetService:
    def __init__(self) -> None:
        self.budget_repo = BudgetRepo()

    def get_year_month(self, start: datetime, end: datetime) -> List:

        result = []
        first_date_of_start = date(start.year, start.month, 1)
        first_date_of_end = date(end.year, end.month, 1)

        while first_date_of_start <= first_date_of_end:

            result.append(datetime.strftime(first_date_of_start, '%Y%m'))
            first_date_of_start += relativedelta(months=1)
        return result

    def query(self, start: datetime.date, end: datetime.date) -> float:
        total_amount = 0
        start_year_month = datetime.strftime(start, '%Y%m')
        end_year_month = datetime.strftime(end, '%Y%m')
        start_amount = 0
        end_amount = 0
        start_month_number = monthrange(start.year, start.month)[1]
        end_month_number = monthrange(end.year, end.month)[1]
        range_of_budget_to_query = self.get_year_month(start, end)
        all_budgets_in_repo = self.budget_repo.get_all()
        dict_of_budget = {}

        for budget in all_budgets_in_repo:
            if budget.year_month in range_of_budget_to_query:
                if budget.year_month == start_year_month:
                    start_amount = budget.amount
                elif budget.year_month == end_year_month:
                    end_amount = budget.amount
                else:
                    dict_of_budget[budget.year_month] = budget.amount

        start_month_daily_budget = start_amount / start_month_number
        start_month_end_date = datetime(
            start.year, start.month, start_month_number).date()
        days_in_start_month = (start_month_end_date - start).days + 1
        total_budget_in_start_month = start_month_daily_budget * days_in_start_month

        if end < start_month_end_date:
            days = (end - start).days + 1
            return start_month_daily_budget * days

        end_month_daily_budget = end_amount / end_month_number
        total_budget_in_end_month = end_month_daily_budget * end.day

        if start_year_month == end_month_number:
            total_budget_in_end_month = 0

        total_buget_in_other_months = sum([v for v in dict_of_budget.values()])
        total_amount = total_buget_in_other_months + \
            total_budget_in_end_month + total_budget_in_start_month

        return total_amount


class Budget:

    def __init__(self, year_month: str, amount: int) -> None:
        self.year_month = year_month
        self.amount = amount


class BudgetRepo:

    def __init__(self) -> None:
        self.budget_list = None

    def get_all(self) -> List[Budget]:
        return self.budget_list
