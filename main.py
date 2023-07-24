# Steven Rivera
# ID: 69434439

import alpha_vantage
import indicators
import signal_strats
from typing import Union


def _run_user_interface() -> None:
    path, partial_url, symbol, start_date, end_date, indicator, strategy = alpha_vantage.get_input()
    url = alpha_vantage.build_search_url(path, partial_url, symbol)
    try:
        all_data = alpha_vantage.get_result(url)

    except ConnectionError:
        pass
    except ValueError:
        pass

    else:
        dates = alpha_vantage.desired_dates(start_date, end_date)
        try:
            wanted_data = alpha_vantage.narrow_data(all_data, dates)

        except ValueError:
            pass

        else:
            buy_or_sell, indicator_data = _analyze_data(wanted_data, indicator, strategy)
            print(symbol + '\n' + str(len(wanted_data)) + '\n' + indicator + ' ' + strategy)
            _display_result(wanted_data, indicator_data, buy_or_sell)


def _analyze_data(data: list[dict], indicator: str, strategy: str) -> tuple[list[dict], list]:
    if indicator.startswith('TR'):
        buy, sell = strategy.split()
        true_range_indicator = indicators.TrueRange(data)
        true_range_percentages = true_range_indicator.calculate()
        signal = signal_strats.TrueRangeSignal(true_range_percentages, buy[0], float(buy[1:]), sell[0], float(sell[1:]))
        return signal.buy_or_sell(), true_range_percentages

    elif indicator.startswith('M'):
        signal, averages = _sma_indicators(data, indicator, strategy)
        return signal.buy_or_sell(), averages

    else:
        signal, directional_indicator_values = _directional_indicators(data, indicator, strategy)
        return signal.buy_or_sell(), directional_indicator_values


def _sma_indicators(data: list[dict], indicator: str, strategy: str) -> list[float]:
    days = int(strategy)

    if indicator.startswith('MP'):
        sma_closing_indicator = indicators.SMAClosing(data, days)
        averages = sma_closing_indicator.calculate()
        signal = signal_strats.SMASignal(averages, data, days, 'close')

    elif indicator.startswith('MV'):
        sma_volume_indicator = indicators.SMAVolume(data, days)
        averages = sma_volume_indicator.calculate()
        signal = signal_strats.SMASignal(averages, data, days, 'volume')

    return signal, averages


def _directional_indicators(data: list[dict], indicator: str, strategy: str) -> tuple[list[float], int, int]:
    day, buy_threshold, sell_threshold = strategy.split()

    if indicator.startswith('DP'):
        directional_indicator = indicators.DIClosing(data, int(day))
    elif indicator.startswith('DV'):
        directional_indicator = indicators.DIVolume(data, int(day))

    directional_indicator_values = directional_indicator.calculate()
    signal = signal_strats.DISignal(directional_indicator_values, int(buy_threshold), int(sell_threshold))

    return signal, directional_indicator_values


def _display_result(wanted_data: list[dict], indicator_data: Union[float, int], buy_or_sell: list[dict]) -> None:
    print('Date\tOpen\tHigh\tLow\tClose\tVolume\tIndicator\tBuy?\tSell?')

    for index in range(len(wanted_data)):
        print(wanted_data[index]['date'] + '\t', end='')
        print(format(wanted_data[index]['open'], '.4f') + '\t', end='')
        print(format(wanted_data[index]['high'], '.4f') + '\t', end='')
        print(format(wanted_data[index]['low'], '.4f') + '\t', end='')
        print(format(wanted_data[index]['close'], '.4f') + '\t', end='')
        print(str(wanted_data[index]['volume']) + '\t', end='')

        if type(indicator_data[index]) == str:
            print('\t', end='')
        elif type(indicator_data[index]) == int:
            print('{}{}\t'.format('+' if indicator_data[index] > 0 else '', indicator_data[index]), end='')
        else:
            print(format(indicator_data[index], '.4f') + '\t', end='')

        print('{}\t'.format('BUY' if buy_or_sell[index]['BUY'] else ''), end='')
        print('{}'.format('SELL' if buy_or_sell[index]['SELL'] else ''))


if __name__ == '__main__':
    _run_user_interface()
