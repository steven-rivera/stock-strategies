# Steven Rivera
# ID: 69434439


class TrueRangeSignal:
    def __init__(self, true_ranges: list[float], lt_gt_buy: str, buy_percentage: float, lt_gt_sell: str,
                 sell_percentage: float):
        self._true_ranges = true_ranges
        self._lt_gt_buy = lt_gt_buy
        self._buy_percentage = buy_percentage
        self._lt_gt_sell = lt_gt_sell
        self._sell_percentage = sell_percentage

    def buy_or_sell(self) -> list[dict]:
        buy_or_sell = [{'BUY': False, 'SELL': False}]

        for percentage in self._true_ranges[1:]:
            dic = {}
            if type(percentage) == str:
                pass
            else:
                if self._lt_gt_buy == '<':
                    if percentage < self._buy_percentage:
                        dic['BUY'] = True
                    else:
                        dic['BUY'] = False
                elif self._lt_gt_buy == '>':
                    if percentage > self._buy_percentage:
                        dic['BUY'] = True
                    else:
                        dic['BUY'] = False
                if self._lt_gt_sell == '<':
                    if percentage < self._sell_percentage:
                        dic['SELL'] = True
                    else:
                        dic['SELL'] = False
                elif self._lt_gt_sell == '>':
                    if percentage > self._sell_percentage:
                        dic['SELL'] = True
                    else:
                        dic['SELL'] = False
                buy_or_sell.append(dic)

        return buy_or_sell


class SMASignal:
    def __init__(self, average_closing_prices: list[float], data_wanted: list[dict], num_days: int, field: str):
        self._averages = average_closing_prices
        self._data = data_wanted
        self._num_days = num_days
        self._field = field

    def buy_or_sell(self) -> list[dict]:
        buy_or_sell = []

        if len(self._data) < self._num_days:
            for _ in range(len(self._data)):
                buy_or_sell.append({'BUY': False, 'SELL': False})
            return buy_or_sell
        else:
            for _ in range(self._num_days):
                buy_or_sell.append({'BUY': False, 'SELL': False})

            for index in range(self._num_days - 1, len(self._data)):
                dic = {}
                if type(self._averages[index - 1]) == str:
                    pass
                else:
                    if (self._data[index][self._field] > self._averages[index] and
                            self._data[index - 1][self._field] < self._averages[index - 1]):
                        dic['BUY'] = True
                    else:
                        dic['BUY'] = False

                    if (self._data[index][self._field] < self._averages[index] and
                            self._data[index - 1][self._field] > self._averages[index - 1]):
                        dic['SELL'] = True
                    else:
                        dic['SELL'] = False

                    buy_or_sell.append(dic)

            return buy_or_sell


class DISignal:
    def __init__(self, directional_indicators: list[int], buy_threshold: int, sell_threshold: int):
        self._indicators = directional_indicators
        self._buy = buy_threshold
        self._sell = sell_threshold

    def buy_or_sell(self) -> list[dict]:
        buy_or_sell = [{'BUY': False, 'SELL': False}]

        for index in range(1, len(self._indicators)):
            dic = {}
            if self._indicators[index] > self._buy >= self._indicators[index - 1]:
                dic['BUY'] = True
            else:
                dic['BUY'] = False

            if self._indicators[index] < self._sell <= self._indicators[index - 1]:
                dic['SELL'] = True
            else:
                dic['SELL'] = False

            buy_or_sell.append(dic)

        return buy_or_sell
