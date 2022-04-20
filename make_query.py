import requests
import queries
import utils
import pandas as pd


def make_request(url, query):
    '''
    Function to query TheGraph using requests, checks for failure
    before returning
    '''

    head = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    r = requests.post(url,
                      headers=head,
                      json={'query': query, 'variables': {}})

    if r.status_code != 200:
        raise Exception("Query Request failed with code " + r.status_code)

    return r.json()


if __name__ == "__main__":
    timestamp = queries.UNISWAP_START

    query = queries.compoundUsers(0)
    req = make_request(queries.UNISWAP_URL, query)
    print(req)
