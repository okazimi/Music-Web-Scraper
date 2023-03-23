# WEB DEVELOPMENT IMPORTS
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
# WEB SCRAPING IMPORTS
from bs4 import BeautifulSoup
import requests
# YOUTUBE REDIRECT IMPORTS
import urllib
import webbrowser

# INITIALIZE FLASK APPLICATION
app = Flask(__name__)
# INITIALIZE BOOTSTRAP
Bootstrap(app)


# SCRAPE SONG DATA
def scrape_song_data():
    # INITIALIZE TARGET URL
    URL = "https://www.top-charts.com/"
    # SEND GET REQUEST TO TARGET URL
    response = requests.get(URL)
    # RETURN TEXT OF THE RESPONSE
    website_html = response.text
    # INITIALIZE BEAUTIFUL-SOUP HTML PARSER AND PASS RESPONSE TEXT
    sp = BeautifulSoup(website_html, "html.parser")
    # SCRAPE SONG NAME
    song_name = sp.findAll("span", {"id": "song_name"})
    # SCRAPE ARTIST NAME
    song_artist = sp.findAll("div", {"id": "Artist"})
    # SCRAP SONG IMAGE
    song_image = sp.findAll("img", {"class": "image-on-bar"})
    # GET TEXT OF SONG NAMES
    songs = [song.getText() for song in song_name]
    # GET TEXT OF ARTIST NAMES
    artists = [artist.getText() for artist in song_artist]
    # GET SONG IMAGES
    images = [image["data-src"] for image in song_image]
    # INITIALIZE NESTED SONG DATA DICTIONARY
    song_dict = {"entry0": {"name": "", "artist": "", "image": ""},
                 "entry1": {"name": "", "artist": "", "image": ""},
                 "entry2": {"name": "", "artist": "", "image": ""},
                 "entry3": {"name": "", "artist": "", "image": ""},
                 "entry4": {"name": "", "artist": "", "image": ""}}
    # UPDATE NESTED SONG DATA DICTIONARY
    for i in range(0, 5):
        # INSERT SONG NAME
        song_dict[f"entry{i}"]["name"] = songs[i]
        # INSERT ARTIST NAME
        song_dict[f"entry{i}"]["artist"] = artists[i]
        # INSERT IMAGE NAME
        song_dict[f"entry{i}"]["image"] = images[i]
    # RETURN NESTED SONG DATA DICTIONARY
    return song_dict


# REDIRECT TO YOUTUBE
def youtube_redirect(song):
    # ENCODE IMPORT
    encode = urllib.parse.urlencode
    # INITIALIZE QUERY STRING
    query_string = encode({"search_query": song})
    # INITIALIZE TARGET URL
    URL = f"https://www.youtube.com/results?{query_string}"
    # RETURN FINALIZED YOUTUBE URL
    return URL


# HOME PAGE (REQUESTS: GET, POST)
@app.route("/home", methods=["GET", "POST"])
def home():
    # IF USER SUBMITS GET REQUEST
    if request.method == "GET":
        # OBTAIN SONG DATA VIA WEB SCRAPING
        song_data = scrape_song_data()
        # RENDER INDEX.HTML TEMPLATE AND PASS SONG DATA
        return render_template("index.html", song_data=song_data)
    # IF USER SUBMITS POST REQUEST
    elif request.method == "POST":
        # OBTAIN INDEX OF TARGET SONG
        target_song = int(request.args.get("index"))
        # OBTAIN SONG DATA VIA WEB SCRAPING
        song_data = scrape_song_data()
        # OBTAIN TARGET SONG NAME FROM NEST SONG DATA DICTIONARY
        target_song_name = song_data[f"entry{target_song}"]["name"]
        # OBTAIN TARGET YOUTUBE URL
        target_youtube_url = youtube_redirect(target_song_name)
        # OPEN YOUTUBE URL ON A NEW TAB
        webbrowser.open(target_youtube_url)
        # RENDER INDEX.HTML TEMPLATE AND PASS SONG DATA, TARGET SONG, TARGET YOUTUBE URL
        return render_template("index.html", song_data=song_data, target_song=target_song, target_youtube_url=target_youtube_url)


# RUN APPLICATION IF NAME OF FILE IS "__MAIN__"
if __name__ == "__main__":
    # RUN APPLICATION IN DEBUG MODE
    app.run(debug=True)
