"""

"""

from urllib.request import urlopen
import json
import time

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

def main():
    """
    main script

    :return:
    """
    user_url = create_url("user.getInfo", "supertang", "14de72a7b1c95b126eefed71dfe27c45", format="json")

    # user_response = open_decode_json(user_url)

    chartlist_url = create_url("user.getWeeklyChartList", "supertang", "14de72a7b1c95b126eefed71dfe27c45", format="json")

    chartlist_response = open_decode_json(chartlist_url)

    i = 0

    while i<50:

        start = time.time()

        chart_from = chartlist_response['weeklychartlist']['chart'][i]['from']
        chart_to = chartlist_response['weeklychartlist']['chart'][i]['to']

        chart_url = create_url("user.getWeeklyTrackChart", "supertang", "14de72a7b1c95b126eefed71dfe27c45", format="json", fromtime=chart_from, totime=chart_to)

        chart_response = open_decode_json(chart_url)

        print(chart_response)

        end = time.time()
        remain = (start + 1) - end
        if remain > 0:
            time.sleep(remain)

        i += 1

    # for trackname in decoded['weeklytrackchart']['track']:
    #     print(trackname['artist']["#text"], " - ", trackname['name'], "(", trackname['artist']["mbid"], ")")

if __name__ == '__main__':

    main()