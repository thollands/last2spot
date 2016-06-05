"""

"""

from urllib.request import urlopen
import json
import time
import pandas as pd

def create_url(method, user, api, format="", fromtime="", totime=""):

    method = r"method=" + method
    user = r"&user=" + user
    api = r"&api_key=" + api
    if format:
        format = r"&format=" + format
    if fromtime:
        fromtime = r"&from=" + fromtime
    if totime:
        totime = r"&to=" + totime
    return r"http://ws.audioscrobbler.com/2.0/?" + method + user + api + format + fromtime + totime

def open_decode_json(url):

    response = urlopen(url).read().decode('utf-8')
    return json.loads(response)

def remove_dupes(alllist):

    seen = set()
    unique = []
    for d in alllist:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            unique.append(d)
    return unique

def main():
    """
    main script

    :return:
    """
    user_url = create_url("user.getInfo", "supertang", "14de72a7b1c95b126eefed71dfe27c45", format="json")

    # user_response = open_decode_json(user_url)

    chartlist_url = create_url("user.getWeeklyChartList", "supertang", "14de72a7b1c95b126eefed71dfe27c45", format="json")

    chartlist_response = open_decode_json(chartlist_url)

    total_charts = len(chartlist_response['weeklychartlist']['chart'])

    outdir = "c:\\Temp\\lasttemp\\"

    alltracks = []

    with open(outdir + 'alltracks.json', 'w') as outfileall, open(outdir + 'uniquetracks.json', 'w') as outfileunique:

        for i in range(total_charts):

            start = time.time()

            chart_from = chartlist_response['weeklychartlist']['chart'][i]['from']
            chart_to = chartlist_response['weeklychartlist']['chart'][i]['to']

            chart_url = create_url("user.getWeeklyTrackChart", "supertang", "14de72a7b1c95b126eefed71dfe27c45", format="json", fromtime=chart_from, totime=chart_to)

            chart_response = open_decode_json(chart_url)

            tracks = chart_response['weeklytrackchart']['track']

            if not tracks:
                print("No tracks played in week " + str(i+1))
            else:
                print(str(len(tracks)) + " tracks played in week "+ str(i+1))
                for track in tracks:
                    alltracks.append({
                        'artist': track['artist']["#text"],
                        'track': track['name'],
                        'mbid': track['artist']["mbid"]
                    })

            end = time.time()
            remain = (start + 1) - end
            if remain > 0:
                time.sleep(remain)

        uniquetracks = remove_dupes(alltracks)

        json.dump(alltracks, outfileall)
        json.dump(uniquetracks, outfileunique)

        print("Total tracks: " + str(len(alltracks)))
        print("Unique tracks: " + str(len(uniquetracks)))

if __name__ == '__main__':
    main()
