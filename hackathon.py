# importing the required library
import requests
from bs4 import BeautifulSoup
from collections import Counter
import sqlite3
import pandas as pd
import pathlib
import tkinter as tk

# taking the input from user for database name
dbName = input("Enter the name of Database : ")
allWords = None

# check if database is present or not
dbFile = pathlib.Path(f"{dbName}.db")
if dbFile.exists():
    conn = sqlite3.connect(f'{dbName}.db')
else:
    conn = sqlite3.connect(f'{dbName}.db')

# creating the cursor object to fetch data from database
c = conn.cursor()

# creating 2 tables at a time i.e webpages and keywords
c.execute('''CREATE TABLE IF NOT EXISTS  webpages(url TEXT, title TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS  keywords( unique1 INTEGER, total_words INTEGER)''')


# creating function (this is the heart of whole code)
def getSomething(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    text = soup.find_all(text=True)
    output = ''
    # getting elements to extract text from.
    # it will also extract some  extra text but we can manage it by changing the preference provided below
    blacklist = ['[document]', 'header', 'html', 'meta', 'head', 'input', 'script', ]

    # getting the formatted text
    for all_text in text:
        if all_text.parent.name not in blacklist:
            output += '{} '.format(all_text)

    # To know more about output run this 2 code
    # it will print
    print(output)
    # print(Counter(output.split()))

    # to get the title of the page
    for title_name in soup.find_all('title'):
        title = title_name.get_text()
        # print("The title of the page is =>  " + title.get_text())

    title = title
    url = url

    # creating a global variable
    global allWords
    # changing a counter collection to dictionary
    allWords = dict(Counter(output.split()))

    # finding the number of unique words
    # print(Counter(output.split()))
    unique1 = len(Counter(output.split()));
    # finding the number of total words
    total_words = len(output.split());

    # inserting the value inside the table webpages and keywords
    c.execute('''INSERT INTO webpages VALUES(?,?) ''', (url, title))
    c.execute('''INSERT INTO keywords VALUES(?,?) ''', (unique1, total_words))

    # printing everythings  present inside the database
    print("Title of the Page is : "+title)
    print("Text Scraped from URL : "+url)
    print("Number of Unique word in a file ", unique1);
    print("Total Size of the file ", total_words);
    print()
    return


# Using while loop to take infinite number of URL input
while True:
    # asking user to enter a input
    user_input = input("Kindly enter URl to get text or 0 to stop : ")
    # if a user will enter "0" then the code will stop
    if (user_input == '0'):
        # function to count occurrence of word
        def count_keyword():
            global allWords
            keyword = ent.get()
            try:
                counts = allWords[keyword]
            except KeyError:
                counts = 0
            lbl_result["text"] = f"{counts} times"


        # Set-up the window (for GUI) using tkinter
        window = tk.Tk()
        # title on the window
        window.title("THE PYTHON WEEK HACKATHON")
        # window is of fixed size 500*200
        window.resizable(width=False, height=False)
        window.geometry("500x200")

        # Some more stuff using tkinter and positioning the element
        frm_entry = tk.Frame(master=window)
        objective = tk.Label(master=frm_entry, text="Counts occurances of Keyword")
        ent = tk.Entry(master=frm_entry, width=20)
        lbl = tk.Label(master=frm_entry, text="Keyword")

        objective.grid(row=0, column=0)
        lbl.grid(row=1, column=0)
        ent.grid(row=1, column=1)

        # creating a button
        btn = tk.Button(
            master=window,
            text="\N{RIGHTWARDS BLACK ARROW}",
            command=count_keyword
        )
        lbl_result = tk.Label(master=window, text="times")

        # Setting up the layout using the .grid() geometry manager
        frm_entry.grid(row=1, column=1, padx=20)
        btn.grid(row=1, column=2, pady=10)
        lbl_result.grid(row=1, column=3, padx=20)

        # Run the application
        window.mainloop()
        break
    else:
        # if the url donot enter "0" then this function will run
        getSomething(user_input)

url = user_input

# it sends the commit statement to the sql server
conn.commit()

print('completed')

# Now fetching all the database elements from table "webpages" in form of  Dataframe using pandas
c.execute(''' SELECT * FROM webpages ''')
results = pd.DataFrame(c.fetchall())
results.columns = [x[0] for x in c.description]
print(results)

# Now fetching all the database elements from table "keywords" in form of  Dataframe using pandas
c.execute(''' SELECT * FROM keywords ''')
results = pd.DataFrame(c.fetchall())
results.columns = [x[0] for x in c.description]
print(results)

# closing the connection
conn.close();

# In this program all the data are stored in the form of pandas dataframe


