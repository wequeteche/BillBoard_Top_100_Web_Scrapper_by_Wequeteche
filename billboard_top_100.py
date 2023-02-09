# ! pip install pandas
# ! pip install datetime
# ! pip install requests_html
# ! pip install openpyxl


from requests_html import HTMLSession
import datetime
import pandas as pd

print("Welcome to the BilBoard Top 100")

while True:
    
    date = input("Enter date to search in the format(YYYY-MM-DD)(Enter OFF to exit the program):\n")

    if date.lower() == "off":
        print("Bye")
        break

    try:
        datetime.date.fromisoformat(date)
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
    else:
        URL = f"https://www.billboard.com/charts/hot-100/{date}/"

        session = HTMLSession()

        response = session.get(URL)

        song_titles = response.html.find("h3.c-title")
        artists = response.html.find("span.c-label")
        artists_list = [artist.text for artist in artists if not artist.text.isdigit()]
        dirt = ['Songwriter(s):','-','NEW','RE- ENTRY', 'Producer(s):', 'Imprint/Promotion Label:', 'Symba: September R&B/Hip-Hop Rookie of the Month', 'Gains in Weekly Performance', 'Additional Awards',]
        artists_list = [artist for artist in artists_list if artist not in dirt]
        song_titles = {"song title":list(dict.fromkeys([song.text for song in song_titles if song.text not in dirt and len(song.text.split()) < 10]))}
        song_titles = [song for index, song in enumerate(song_titles['song title']) if index < 100]

        print(len(song_titles))
        print(len(artists_list))
        # print(song_titles)
        # print(artists_list)

        data_frame = pd.DataFrame({
            "Song Title": song_titles,
            "Artist(s)": artists_list
        }, index=pd.RangeIndex(start=1, stop=101, name="Possition"), )
        
        excel = input(f"Do you want data to be exported to an excel file(Billboard_top_100_{date}.xlsx)?(Y, N)\n")
        
        if excel.lower() == "y":
            data_frame.to_excel(f"Billboard_top_100_{date}.xlsx")
        elif excel.lower() == "n":
            continue
        else:
            print(f"Invalid input, expected(Y, N) got {excel}")
        
        print(data_frame) 
        
        print(f"\n \n")
