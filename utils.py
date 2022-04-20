import json
import flatten_json
import csv
import pandas as pd


def save_json(json_data, outfile):
    '''
    Saves data to an file
    '''
    o = open(outfile, "w")

    json.dump(json_data, o, indent=4)

    o.close()
    print("JSON data written to {0}".format(outfile))


def writeCSV(data, file, access="w", header=True):
    f = open(file, mode=access, newline='')

    csv_writer = csv.writer(f)

    max_time = 0

    n = 0
    for s in data["data"][list(data["data"].keys())[0]]:

        #entries = data["data"][list(data["data"].keys())[0]]
        #s = [flatten_json.flatten(e, ".") for e in entries]

        if n == 0 and header == True:
            csv_writer.writerow(s)

        csv_writer.writerow(s)

        n += 1

    f.close()

    return max_time


def convert_to_Dataframe(data):
    entries = data["data"][list(data["data"].keys())[0]]
    s = [flatten_json.flatten(e, ".") for e in entries]

    return pd.DataFrame(s)


def convert_to_Dataframe_UNI(data):

    entries = data["data"][list(data["data"].keys())[0]]
    s = [flatten_json.flatten(e, ".") for e in entries]

    return pd.DataFrame(s)


def add_unix_day(unix_time, num_days=1):
    return unix_time + (num_days * 86400)


req = [{'id': '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f',
        'totalVolumeUSD': '400544947751.4855014277204212867206',
        'totalVolumeETH': '276665646.4708543307339665865523307',
        'untrackedVolumeUSD': '273302839978043335604.6127662137628',
        'totalLiquidityUSD': '2950714987.014602158139396464924688',
        'totalLiquidityETH': '936009.5045743332888963183933108106',
        'txCount': '76168596',
        'pairCount': 67712}]
