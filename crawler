#! /usr/bin/python3
import sqlite3
import requests
import sys
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta

connection = sqlite3.connect("/home/z/zubcak2/project/horoscopes.db")
cursor = connection.cursor()


date = datetime.now().strftime("%Y.%m.%d")
signs = ["kozorozec", "vodnar", "ryby", "baran", "byk", "blizenci", "rak", "lev", "panna", "vahy", "skorpion", "strelec"]

for sign in signs:
    # Get daily horoscope from webpage and store it in horoscope_str
    web_url = "https://diva.aktuality.sk/horoskopy/denny-horoskop/" + sign
    r = requests.get(web_url)
    parsed = bs(r.text, 'html.parser')

    horoscope_str = parsed.select("body div.horoscope-text")[0].text


    # Store it in database
    # find max id, so we can keep having unique ids
    cursor.execute("""
            SELECT MAX(h_id)
            FROM horoscopes""")
    first_row = cursor.fetchone()
    if first_row[0] is None:
        id_counter = 0
    else:
        id_counter = 1 + first_row[0]

    # check if horoscope with current date and sign is already present
    cursor.execute("""
                SELECT *
                FROM horoscopes
                WHERE h_sign = ? AND h_date = ?""", (sign, date))
    first_row = cursor.fetchone()
    if first_row == None:
        # if there is no record for todays horoscope of sign "sign", we add it to database
        h_id = id_counter
        id_counter += 1
        cursor.execute("""
            INSERT INTO horoscopes(h_id, h_sign, h_date, h_text)
            VALUES (?, ?, ?, ?)""",(h_id, sign, date, horoscope_str))
        connection.commit()

connection.close()



connection = sqlite3.connect("/home/z/zubcak2/project/horoscopes.db")
cursor = connection.cursor()
cursor.execute("""
            SELECT *
            FROM horoscopes
            """)
f = open("/home/z/zubcak2/project/horoscopes_table.txt", "w")
g = open("/home/z/zubcak2/project/horoscopes_log.txt", "a")
f.write("HOROSCOPES: h_id, h_sign, h_date, h_text\n\n")
g.write("HOROSCOPES: h_id, h_sign, h_date, h_text\n\n")
for row in cursor:
    f.write(row[1] + " at " + row[2] + ":\n" + row[3] + "\n\n")
    g.write(row[1] + " at " + row[2] + ":\n" + row[3] + "\n\n")

g.write("log at: " + str(datetime.now().strftime("%H:%M %d.%m.%Y")) + "\n____________________\n\n")
f.close()
g.close()
connection.close()
