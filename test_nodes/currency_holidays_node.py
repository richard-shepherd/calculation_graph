from graph import *
from .holiday_database import HolidayDatabase


class CurrencyHolidaysNode(GraphNode):
    """
    Manages the collection of holidays for one currency.
    """
    def __init__(self, currency, *args, **kwargs):
        """
        The constructor.
        """
        super().__init__(*args, **kwargs)

        # The currency...
        self.currency = currency

        # The collection of holidays for the currency...
        self.holidays = set()

        # We observe changes to the holidays...
        self.holiday_db = self.environment.holiday_db
        self.holiday_db.add_observer(self)

    def dispose(self):
        """
        Called when the node is removed fro the graph.
        """
        self.holiday_db.remove_observer(self)

    def updated(self, observable):
        """
        Called when the holidays DB has been updated.
        """
        self.needs_calculation()

    def calculate(self):
        """
        Called when the node needs calculation.
        """
        # We find the collection of holidays for the currency we are managing...
        currency_holidays = self.holiday_db.get_currency_holidays(self.currency)

        # We check if the data has changed...
        if (self.holidays != currency_holidays.holidays) or (self.quality != currency_holidays.quality):
            # The data has changed, so we store it and calculate our children...
            self.holidays = currency_holidays.holidays.copy()
            self.quality.set_from(currency_holidays.quality)
            return GraphNode.CalculateChildrenType.CALCULATE_CHILDREN
        else:
            # Nothing has changed...
            return GraphNode.CalculateChildrenType.DO_NOT_CALCULATE_CHILDREN




