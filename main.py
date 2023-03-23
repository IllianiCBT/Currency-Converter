import requests
import json
from os import path


def build_json_entry(currency_from, currency_to, rates):
    return {
        "currency_from": currency_from,
        "currency_to": currency_to,
        "exchange_rate": rates[currency_to]['rate']
    }


def build_cache(currency_from, currency_to, rates):
    # if no cache exists, create cache, add first entry
    if path.isfile('currency_converter_cache.json') is False:
        json_entry = {
            f"{currency_from}_to_{currency_to}":
                {
                    "currency_from": currency_from,
                    "currency_to": currency_to,
                    "exchange_rate": rates[currency_to]['rate']
                }
        }

        with open("currency_converter_cache.json", 'w') as cache:
            json.dump(json_entry, cache, indent=2)

    # if cache already exists read cache, if entry doesn't exist create new entry, otherwise update entry
    else:
        with open('currency_converter_cache.json', 'r') as cache:
            json_contents = json.load(cache)

            json_contents[f"{currency_from}_to_{currency_to}"] = build_json_entry(currency_from, currency_to, rates)

        with open('currency_converter_cache.json', 'w') as cache:
            json.dump(json_contents, cache, indent=2)


def currency_converter():
    currency_from = input("Please enter the original currency (for example, 'USD' for US Dollars): ").lower()

    while True:
        print("Please enter the destination currency (for example, 'GBP' for Pound Sterling): ")
        currency_to = input("Or, press Enter to exit.").lower()

        if currency_to != '':
            currency_held = int(input("Please enter the total currency held: "))

            # cache the most common exchange rates
            rates = requests.get('http://www.floatrates.com/daily/' + currency_from + '.json').json()

            currency_common = ['usd', 'eur']

            for currency in currency_common:
                if currency != currency_from:
                    build_cache(currency_from, currency, rates)

            # check whether conversion exists in the cache
            with open('currency_converter_cache.json', 'r') as cache:
                json_contents = json.load(cache)

            try:
                exchange_rate = json_contents[f"{currency_from}_to_{currency_to}"]['exchange_rate']

            except KeyError:
                exchange_rate = rates[currency_to]['rate']

                # add to cache
                build_cache(currency_from, currency_to, rates)

            # convert currency
            print(f"You received {currency_held * exchange_rate:.2f} {currency_to.upper()}.")
            continue
        else:
            print('Done')
            quit()


if __name__ == '__main__':
    currency_converter()