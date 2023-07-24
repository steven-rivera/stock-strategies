# Steven Rivera
# ID: 69434439

import json
import datetime
import urllib.parse
import urllib.request
from pathlib import Path


def get_input():
    path = Path(input())
    partial_url = input()
    symbol = input()
    start_date = input()
    end_date = input()
    indicator_and_strategy = input()
    indicator = indicator_and_strategy[0:2]
    strategy = indicator_and_strategy[3:]

    return path, partial_url, symbol, start_date, end_date, indicator, strategy


def build_search_url(path: Path, partial_url: str, symbol: str) -> str:
    """Builds the url given the company symbol."""

    with path.open() as file:
        apikey = file.readline()

    query_parameters = [
        ('function', 'TIME_SERIES_DAILY'), ('symbol', symbol),
        ('outputsize', 'full'), ('apikey', apikey),
    ]
    return partial_url + '/query?' + urllib.parse.urlencode(query_parameters)


def get_result(url: str) -> dict:
    """
    This function takes a URL and returns a Python dictionary representing the
    parsed JSON response. A ConnectionError is raised if there is no network
    connectivity or if the status code returned by the request is not 200. A
    ValueError is raised if the response is not proper JSON.
    """
    response = None

    try:
        response = urllib.request.urlopen(url)

    except urllib.error.HTTPError as e:
        e = str(e)
        code = e.split()[2][:-1]
        print(f'FAILED\n{code}\nNOT 200')
        raise ConnectionError

    except urllib.error.URLError:
        print('FAILED\n0\nNetwork')
        raise ConnectionError

    else:
        json_text = response.read().decode(encoding='utf-8')

        try:
            data = json.loads(json_text)
            return data

        except json.decoder.JSONDecodeError:
            print(f'FAILED\n200\nFORMAT')
            raise ValueError

    finally:
        if response is not None:
            response.close()


def narrow_data(data: dict, considered_dates: list) -> list[dict]:
    """
    Returns a list of dictionaries in which each dictionary
    contians the keys open, high, low, close, and volume whos
    values correspond to their values on that date. The first
    index of the list contains the values for the start day
    specified and continues to the end date specified. A ValueError
    is raised if not all field were present.
    """
    try:
        dict_of_dates = data['Time Series (Daily)']
    except KeyError:
        print('FAILED\n200\nFORMAT')
        raise ValueError

    else:
        data_wanted = []

        for date in considered_dates:
            temporary_dict = {}
            try:
                temporary_dict['date'] = date
                temporary_dict['open'] = float(dict_of_dates[date]['1. open'])
                temporary_dict['high'] = float(dict_of_dates[date]['2. high'])
                temporary_dict['low'] = float(dict_of_dates[date]['3. low'])
                temporary_dict['close'] = float(dict_of_dates[date]['4. close'])
                temporary_dict['volume'] = int(dict_of_dates[date]['5. volume'])

            except KeyError:
                pass
            else:
                data_wanted.append(temporary_dict)

        if len(data_wanted) == 0:
            print('FAILED\n200\nFORMAT')
            raise ValueError
        else:
            return data_wanted


def desired_dates(start_date: str, end_date: str) -> list[str]:
    """
    Returns a list of all the dates in-between the start date
    and the end date in form YYYY-MM-DD. List is inclucsive.
    """
    start_date = datetime.date.fromisoformat(start_date)
    end_date = datetime.date.fromisoformat(end_date)
    considered_dates = []

    for i in range(int((end_date - start_date).days) + 1):
        date = start_date + datetime.timedelta(i)
        considered_dates.append(date.isoformat())

    return considered_dates
