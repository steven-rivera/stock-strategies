# Steven Rivera
# ID: 69434439


class TrueRange:
    def __init__(self, data_wanted: [dict]):
        self._data = data_wanted

    def calculate(self) -> [float]:
        true_range_percentages = ['EMPTY']
        for index in range(1, len(self._data)):
            current_day = self._data[index]
            previous_day_close = self._data[index - 1]['close']
            if current_day['low'] <= previous_day_close <= current_day['high']:
                true_range = current_day['high'] - current_day['low']
            else:
                if previous_day_close > current_day['high']:
                    true_range = previous_day_close - current_day['low']
                else:
                    true_range = current_day['high'] - previous_day_close

            true_range_percentages.append((true_range / previous_day_close * 100))
        return true_range_percentages


class SMAClosing:
    def __init__(self, data_wanted: [dict], num_days: int):
        self._data = data_wanted
        self._num_days = num_days

    def calculate(self) -> [float]:
        average_closing_prices = []

        if len(self._data) < self._num_days:
            for _ in range(len(self._data)):
                average_closing_prices.append('EMPTY')
            return average_closing_prices

        else:
            for _ in range(self._num_days - 1):
                average_closing_prices.append('EMPTY')

            for index in range(self._num_days - 1, len(self._data)):
                closing_sum = 0
                for i in range(self._num_days):
                    closing_sum += self._data[index - i]['close']
                average_closing_prices.append((closing_sum / self._num_days))

            return average_closing_prices


class SMAVolume:
    def __init__(self, data_wanted: [dict], num_days: int):
        self._data = data_wanted
        self._num_days = num_days

    def calculate(self) -> [float]:
        average_volumes = []

        if len(self._data) < self._num_days:
            for _ in range(len(self._data)):
                average_volumes.append('EMPTY')
            return average_volumes

        else:
            for _ in range(self._num_days - 1):
                average_volumes.append('EMPTY')

            for index in range(self._num_days - 1, len(self._data)):
                volume_sum = 0
                for i in range(self._num_days):
                    volume_sum += self._data[index - i]['volume']
                average_volumes.append((volume_sum / self._num_days))

            return average_volumes


class DIClosing:
    def __init__(self, data_wanted: [dict], num_days: int):
        self._data = data_wanted
        self._num_days = num_days

    def calculate(self) -> [int]:
        directional_indicators = [0]

        for index in range(1, len(self._data)):
            indicator = 0
            for i in range(self._num_days):
                if index > i:
                    if self._data[index - i]['close'] > self._data[index - i - 1]['close']:
                        indicator += 1
                    elif self._data[index - i]['close'] < self._data[index - i - 1]['close']:
                        indicator -= 1
            directional_indicators.append(indicator)

        return directional_indicators


class DIVolume:
    def __init__(self, data_wanted: [dict], num_days: int):
        self._data = data_wanted
        self._num_days = num_days

    def calculate(self) -> [int]:
        directional_indicators = [0]

        for index in range(1, len(self._data)):
            indicator = 0
            for i in range(self._num_days):
                if index > i:
                    if self._data[index - i]['volume'] > self._data[index - i - 1]['volume']:
                        indicator += 1
                    elif self._data[index - i]['volume'] < self._data[index - i - 1]['volume']:
                        indicator -= 1
            directional_indicators.append(indicator)

        return directional_indicators
