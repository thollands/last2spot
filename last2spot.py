"""

"""

from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus
import json
import time
import oauth2 as oauth
# import pandas as pd

def create_last_url(method, user, api, format="", fromtime="", totime=""):

    params = {
        "method": method,
        "user": user,
        "api_key": api
    }
    if format:
        params['format'] = format
    if fromtime:
        params['from'] = fromtime
    if totime:
        params['to'] = totime

    all_params = urlencode(params)

    return r"http://ws.audioscrobbler.com/2.0/?" + all_params

def spot_search_url(artist, track, album, year, stype='track'):

    params = {}

    params["q"] = "artist:" + str(artist) + " track:" + str(track)# + " album:" + str(album) + " year:" + str(year)

    params['type'] = stype

    all_params = urlencode(params)

    return r"https://api.spotify.com/v1/search?" + all_params

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

def last_get():
    """
    main script

    :return:
    """
    user_url = create_last_url("user.getInfo", "supertang", "14de72a7b1c95b126eefed71dfe27c45", format="json")

    # user_response = open_decode_json(user_url)

    chartlist_url = create_last_url("user.getWeeklyChartList", "supertang", "14de72a7b1c95b126eefed71dfe27c45", format="json")

    chartlist_response = open_decode_json(chartlist_url)

    total_charts = len(chartlist_response['weeklychartlist']['chart'])

    outdir = "c:\\Temp\\lasttemp\\"

    alltracks = []

    with open(outdir + 'alltracks.json', 'w') as outfileall, open(outdir + 'uniquetracks.json', 'w') as outfileunique:

        for i in range(40, 41):

            start = time.time()

            chart_from = chartlist_response['weeklychartlist']['chart'][i]['from']
            chart_to = chartlist_response['weeklychartlist']['chart'][i]['to']

            chart_url = create_last_url("user.getWeeklyTrackChart", "supertang", "14de72a7b1c95b126eefed71dfe27c45", format="json", fromtime=chart_from, totime=chart_to)

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
                        'lastid': track['artist']["mbid"]
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

        return uniquetracks

def spot_search(tracks):
    spot_tracks = []
    for i in tracks:
        search_url = spot_search_url(i['artist'], i['track'], None, None)

        response = open_decode_json(search_url)

        results = response['tracks']['items']

        if not results:
            print("search for '" + i['track'] + "' by " + i['artist'] + " returned no results :(")
        else:
            print("search for '" + i['track'] + "' by " + i['artist'] + " returned " + str(
                response['tracks']["total"]) + " results :D")
            spot_tracks.append({
                'artist': response['tracks']['items'][0]['artists'][0]['name'],
                'track': response['tracks']['items'][0]['name'],
                'spotid': response['tracks']['items'][0]['uri']
            })

    return spot_tracks

def spot_post(tracks, user, playlist):

    base_url = r"https://api.spotify.com/v1/users/"

    def oauth_req(url, key, secret, http_method="POST", post_body=None, http_headers="Content-type: application/json"):

        CONSUMER_KEY = "BQBQeK0EGFXN_W2YJdfq7e6j_1QsirDAEJV-G74-aJ1raf529NEcM6cb7eV2wbpUVL8WaCuHXD0M-gy6fLuHWRxTbawlrCR9zwpmHgcLnamIA291j400JXbqgx6VdzUwQqiTNHGLykYkGqq_ei62VEk6KwFMfAXHUBuHZHLRBoCGf7bNrl_zCZY"
        CONSUMER_SECRET = "db8ce5bc60404116a30bc9fa8aa2e1d2"
        consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
        token = oauth.Token(key=key, secret=secret)
        client = oauth.Client(consumer, token)
        resp, content = client.request(
            url,
            method=http_method,
            body=urlencode({'status': post_body}),
            headers=http_headers,
            force_auth_header=True
        )
        return content

    oauth_req('http://api.twitter.com/1/statuses/update.json', KEY, SECRET, post_body=MESSAGE)

    spotid_str = ",".join([i['spotid'] for i in tracks])

    print(spotid_str)
    uri_str = r"https://api.spotify.com/v1/users/" + user + r"/playlists/" + playlist + r"/" + spotid_str


if __name__ == '__main__':
    tracks = last_get()
    search_results = spot_search(tracks)
    spot_post(search_results, "1233944934", "4GI3euyla7Ga1SyYd9K0oF")
