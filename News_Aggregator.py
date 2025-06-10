#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item for QUT's teaching unit
#  ITD104, "Building IT Systems", C2, 2024.  By submitting
#  this code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
student_number = 12228591
student_name   = "Chun-Huan Lee"
#
#--------------------------------------------------------------------#

#-----Project Description-----------------------------------------#
#
#  Here and There
#
#  In this project you will combine your knowledge of HTMl/CSS
#  mark-up languages with your skills in Python scripting, pattern
#  matching and Graphical User Interface design to produce
#  a useful application that allows the user to compare news stories
#  from multiple sources.
#
#  See the client's requirements accompanying this file for full details.
#
#--------------------------------------------------------------------#



#-----Initialisation Steps-------------------------------------------#
#

# Import standard Python 3 modules needed to complete this project.
# [No other modules are required for your solution.
# Your solution MUST NOT rely on any other modules.
# You MUST NOT import any other modules.]
#
# A function for exiting the program immediately (renamed
# because "exit" is already a standard Python function).
from sys import exit as abort

# The function for opening a web document given its URL.
# (You WILL need to use this function in your solution,
# either directly or via our "download" function below.)
from urllib.request import urlopen

# Some standard Tkinter functions.  (You WILL need to use
# SOME of these functions in your solution.)  You may also
# import other widgets from the "tkinter" module, provided they
# are standard ones and don't need to be downloaded and installed
# separately.  (NB: DON'T import all of the "tkinter.tkk" functions
# using a "*" wildcard because this module includes alternative
# versions of standard widgets like "Label".)
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

# Functions for finding occurrences of a pattern defined
# via a regular expression.  (You do not necessarily need to
# use these functions in your solution, because the problem
# can be solved with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.)
from re import *

# A function for displaying a web document in the host
# operating system's default web browser (renamed to
# distinguish it from the built-in "open" function for
# opening local files).  (You WILL need to use this function
# in your solution.)
from webbrowser import open as urldisplay

# Import the date and time function.
# This module *may* be useful, depending on the websites you choose.
# Eg convert from a timestamp to a human-readable date:
# >>> datetime.fromtimestamp(1586999803) # number of seconds since 1970
# datetime.datetime(2020, 4, 16, 11, 16, 43)
from datetime import datetime

# Confirm that the student has declared their authorship.
# You must NOT change any of the code below.
if not isinstance(student_number, int):
    print('\nUnable to run: No student number supplied',
          '(must be an integer)\n')
    abort()
if not isinstance(student_name, str):
    print('\nUnable to run: No student name supplied',
          '(must be a character string)\n')
    abort()

#
#--------------------------------------------------------------------#



#-----Supplied Function----------------------------------------------#
#
# Below is a function you can use in your solution if you find it
# helpful.  (You are not required to use this function, but it may
# save you some effort.)
#
# A function to download and save a web document.  The function
# returns the downloaded document as a character string and
# optionally saves it as a local file.  If the attempted download
# fails, an error message is written to the shell window and the
# special value None is returned.
#
# Parameters:
# * url - The address of the web page you want to download.
# * target_filename - Name of the file to be saved (if any).
# * filename_extension - Extension for the target file, usually
#      "html" for an HTML document or "xhtml" for an XML
#      document.
# * save_file - A file is saved only if this is True. WARNING:
#      The function will silently overwrite the target file
#      if it already exists!
# * char_set - The character set used by the web page, which is
#      usually Unicode UTF-8, although some web pages use other
#      character sets.
def download(url = 'http://www.wikipedia.org/',
             target_filename = 'downloaded_document',
             filename_extension = 'html',
             save_file = True,
             char_set = 'UTF-8'):

    # Import the function for opening online documents and
    # the class for creating requests
    from urllib.request import urlopen, Request

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        request = url
        web_page = urlopen(request)
    except ValueError:
        print("Download error - Cannot find document at URL '" + url + "'\n")
        return None
    except HTTPError:
        print("Download error - Access denied to document at URL '" + url + "'\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to download " + \
              "the document at URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Read the contents as a character string
    try:
        web_page_contents = web_page.read().decode(char_set)
    except UnicodeDecodeError:
        print("Download error - Unable to decode document from URL '" + \
              url + "' as '" + char_set + "' characters\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to decode " + \
              "the document from URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Optionally write the contents to a local text file
    # (overwriting the file if it already exists!)
    if save_file:
        try:
            text_file = open(target_filename + '.' + filename_extension,
                             'w', encoding = char_set)
            text_file.write(web_page_contents)
            text_file.close()
        except Exception as message:
            print("Download error - Unable to write to file '" + \
                  target_filename + "'")
            print("Error message was:", message, "\n")
            return None

    # Return the downloaded document to the caller
    return web_page_contents

#
#--------------------------------------------------------------------#

## NewsAggregator class
    
# This class represents a news aggregator application that fetches and displays
# technology news from BBC and ABC RSS feeds.
class NewsAggregator:

    def __init__(self, master):
        
        # Attributes:
        #     master (Tk): The root window of the Tkinter application.
        #     bbc_url (str): The URL for the BBC technology news RSS feed.
        #     abc_url (str): The URL for the ABC technology news RSS feed.
        #     bbc_logo (str): The file path for the BBC logo image.
        #     abc_logo (str): The file path for the ABC logo image.
        #     selected_feed (StringVar): Tkinter variable to store the selected feed.
        #     current_feed (str): The currently selected feed.
        #     summary_displayed (dict): Tracks whether summaries have been displayed for each feed.
        
        self.master = master
        master.title("Technology in the News")
        master.geometry("800x700")

        # URLs for RSS feeds
        self.bbc_url = "https://feeds.bbci.co.uk/news/technology/rss.xml"
        self.abc_url = "https://abcnews.go.com/abcnews/technologyheadlines"
        
        # Paths to logo images
        self.bbc_logo = "BBC_Logo.png"
        self.abc_logo = "ABC_Logo.png"
        
        self.selected_feed = StringVar(value="")
        self.current_feed = None
        self.summary_displayed = {'bbc': False, 'abc': False}

        self.setup_gui()

    def setup_gui(self):
        # Create a canvas that fills the entire window
        self.canvas = Canvas(self.master, width=800, height=700)
        self.canvas.grid(row=0, column=0, sticky='nsew')

        # Configure the grid
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Load the background image
        self.bg_image = PhotoImage(file='background.png')
        
        # Display the image on the canvas
        self.canvas.create_image(0, 0, image=self.bg_image, anchor='nw')

        # Main frame
        self.main_frame = Frame(self.canvas, bg='#34495e')
        
        # Create a window for the main frame in the canvas
        self.window = self.canvas.create_window(400, 350, window=self.main_frame, 
                                                anchor='center')

        # Bind the configure event of the canvas to update the window's position(center)
        self.canvas.bind('<Configure>', self.center_main_frame)

        # Define the number of rows in the main frame
        MAIN_FRAME_ROWS = 3
        # Configure the grid for main_frame
        for row_index in range(MAIN_FRAME_ROWS):
            self.main_frame.grid_rowconfigure(row_index, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.setup_feeds_section()
        self.setup_summaries_section()
        self.setup_options_section()

    def setup_feeds_section(self):
        # Feeds section
        feeds_frame = Frame(self.main_frame, bg='#34495e')
        feeds_frame.grid(row=0, column=0, pady=15, padx=30, sticky='nsew')

        # Configure the column in feeds_frame to expand
        feeds_frame.grid_columnconfigure(0, weight=1)

        Label(feeds_frame, text="Feeds", bg='#34495e', fg='white', 
              font=('Arial', 14, 'bold')).grid(row=0, column=0, pady=10, sticky='ew')

        Radiobutton(feeds_frame, text="United Kingdom (BBC Technology News)", 
                    variable=self.selected_feed, 
                    value="bbc", command=self.select_feed, 
                    bg='#c0d0fc', fg='black', pady=4,
                    selectcolor='#011859', indicatoron=0, 
                    relief=RAISED).grid(row=1, column=0, sticky='ew', padx=5, pady=2)
        
        Radiobutton(feeds_frame, text="United States (ABC Technology News)", 
                    variable=self.selected_feed, 
                    value="abc", command=self.select_feed, bg='#c0d0fc', 
                    fg='black', pady=4,
                    selectcolor='#2980b9', indicatoron=0, 
                    relief=RAISED).grid(row=2, column=0, sticky='ew', padx=5, pady=2)

    def setup_summaries_section(self):
        # Quick summaries section
        summaries_frame = Frame(self.main_frame, bg='#34495e')
        summaries_frame.grid(row=1, column=0, padx=30, sticky='nsew')

        Label(summaries_frame, text="Quick summaries...", bg='#34495e', 
              fg='white', font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2)

        # BBC summary text
        self.setup_summary_text(summaries_frame, "BBC", 0)
        
        # ABC summary text
        self.setup_summary_text(summaries_frame, "ABC", 1)

        # Configure the grid for summaries_frame
        summaries_frame.grid_rowconfigure(1, weight=1)
        summaries_frame.grid_columnconfigure(0, weight=1)
        summaries_frame.grid_columnconfigure(1, weight=1)

    def setup_summary_text(self, parent, feed_name, column):
        frame = Frame(parent, bg='#34495e')
        frame.grid(row=1, column=column, sticky='nsew', padx=5)
        
        Label(frame, text=feed_name, bg='#34495e', fg='white').grid(row=0, column=0)
        
        summary_text = Text(frame, height=15, width=35, wrap='word', bg='#ecf0f1', 
                            fg='#2c3e50', padx=15, pady=10)
        summary_text.grid(row=1, column=0, sticky='nsew')
        summary_text.insert(
            'end', 
            f"\n\n\n\n\n\nSummary will appear here when {feed_name} "
            "Technology feed selected\n")

        setattr(self, f"{feed_name.lower()}_summary_text", summary_text)

    def setup_options_section(self):
        # Display Options section
        options_frame = Frame(self.main_frame, bg='#34495e')
        options_frame.grid(row=2, column=0, pady=20, padx=20, sticky='nsew')

        Label(options_frame, text="Display Options", bg='#34495e', fg='white', 
              font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        self.quick_summary_btn = Button(options_frame, text="Quick Summary", 
                                        command=self.display_quick_summary, 
                                        state='disabled', bg='#2ecc71', fg='white')
        
        self.quick_summary_btn.grid(row=1, column=0, pady=5, padx=5, sticky='ew')

        self.export_html_btn = Button(options_frame, text="Export to HTML", 
                                      command=self.export_to_html, 
                                      state='disabled', bg='#e74c3c', fg='white')
        
        self.export_html_btn.grid(row=1, column=1, pady=5, padx=5, sticky='ew')

        self.open_website_btn = Button(options_frame, text="Open Live Website", 
                                       command=self.open_live_website, 
                                       state='disabled', bg='#f39c12', fg='white', 
                                       font=('Arial', 8, 'bold'), pady=10)
        
        self.open_website_btn.grid(row=2, column=0, columnspan=2, padx=5, sticky='ew')

        # Configure the grid for options_frame
        options_frame.grid_columnconfigure(0, weight=1)
        options_frame.grid_columnconfigure(1, weight=1)

    # Not necessary
    # but I got a huge sense of accomplishment after completing this part :)
    # event=None allows this method to be called both as an event handler and directly
    def center_main_frame(self, event=None):
    
        # Get the current canvas width and height
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Update the background image to fill the new canvas size
        self.canvas.delete("bg_image")
        self.canvas.create_image(0, 0, image=self.bg_image, anchor='nw', tags="bg_image")
        
        # Calculate the center of the canvas
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        
        # Move the window to the center of the canvas
        self.canvas.coords(self.window, center_x, center_y)

        ## Update the size of the main_frame
        
        # 90% of canvas width or 800, whichever is smaller
        frame_width = min(canvas_width * 0.9, 800)  
        # 90% of canvas height or 700, whichever is smaller
        frame_height = min(canvas_height * 0.9, 700) 
        self.main_frame.configure(width=frame_width, height=frame_height)
        
    def select_feed(self):
        new_feed = self.selected_feed.get()
        
        # Update the appearance of the radio buttons
        for widget in self.main_frame.winfo_children()[0].winfo_children():
            if isinstance(widget, Radiobutton):
                if widget['value'] == new_feed:
                    widget.config(relief=SUNKEN, selectcolor='#3498db', fg='white')
                else:
                    widget.config(relief=RAISED, fg='black')
        
        # Enable Quick Summary button and Open Live Website button
        self.quick_summary_btn['state'] = 'normal'
        self.open_website_btn['state'] = 'normal'
        
        # Maintain Export to HTML button state
        if not hasattr(self, 'summary_displayed'):
            self.summary_displayed = {'bbc': False, 'abc': False}
        
        
        if self.summary_displayed[new_feed]:
            self.export_html_btn['state'] = 'normal' 
        else:
            self.export_html_btn['state'] = 'disable' 

        # Clear and update the summary text
        self.update_summary_text(new_feed)

        # Update the current feed
        self.current_feed = new_feed
    
    # Let the users know something is happened
    def update_summary_text(self, selected_feed):
        feed = self.selected_feed.get()
        summary_text = getattr(self, f"{feed}_summary_text")
        
        if feed == selected_feed:
            summary_text.delete('1.0', 'end')
            summary_text.insert(
                'end', 
                f"You can get a quick summary from this source now...\n")
                
    def display_quick_summary(self):
        # Get the selected feed and corresponding text widget
        feed = self.selected_feed.get()
        summary_text = getattr(self, f"{feed}_summary_text")
        
        # Clear the existing content in the summary text widget
        summary_text.delete('1.0', 'end')
        
        # Determine the URL based on the selected feed
        url = self.bbc_url if feed == "bbc" else self.abc_url

        try:
            # Fetch and parse the RSS content
            content = self.fetch_rss_content(url)
            items = self.parse_rss_content(content)

            # Display the first 5 items in the summary
            for numbered_list, item in enumerate(items[:5], 1):
                summary = (
                    f"{numbered_list}. {item['pubDate']}\n\n"
                    f"{item['title']}\n\n"
                    "===================================\n\n"
                )
                summary_text.insert('end', summary)

        except Exception as message:
            # Handle any errors that occur during fetching or parsing :/
            error_message = f"Error fetching or parsing the RSS feed: {str(message)}"
            summary_text.insert('end', error_message)
        
        # Update the button state
        self.summary_displayed[feed] = True
        self.export_html_btn['state'] = 'normal'
        
        # Disable the summary_text when you got the first 5 items in the summary
        # This way the user doesn't need to go through the entire process again 
        # when they select another feed :)
        summary_text['state'] = 'disabled'

    def fetch_rss_content(self, url):
        # Fetch the RSS content from the given URL
        with urlopen(url) as response:
            return response.read().decode('utf-8')

    def parse_rss_content(self, content):
        items = []
        # Define regex patterns for extracting information from RSS content
        item_pattern = compile(r'<item>(.*?)</item>', DOTALL)
        title_pattern = compile(r'<title>(.*?)</title>')
        pubDate_pattern = compile(r'<pubDate>(.*?)</pubDate>')
        description_pattern = compile(r'<description>(.*?)</description>')
        image_pattern = compile(r'<media:thumbnail.*?url="(.*?)"')

        # Iterate through each item in the RSS feed
        for item_match in item_pattern.finditer(content):
            item_content = item_match.group(1)
            
            # Extract title, publication date, description, and image URL
            title = title_pattern.search(item_content)
            pubDate = pubDate_pattern.search(item_content)
            description = description_pattern.search(item_content)
            image = image_pattern.search(item_content)

            # If title and publication date are present, add the item to the list
            if title and pubDate:
                items.append({
                    'title': self.clean_html(title.group(1)),
                    'pubDate': self.clean_html(pubDate.group(1)),
                    'description': self.clean_html(description.group(1)) 
                        if description else '',
                    'image': image.group(1) if image else ''
                })

        return items

    def clean_html(self, text):
        # Define a list of HTML entities and their replacements
        replacements = [
            ('&quot;', '"'), ('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'),
            ('<![CDATA[', ''), (']]>', ''), ('&apos;', "'"), (' -0400', " EDT")
        ]
        
        # Apply all replacements to the text
        for old, new in replacements:
            text = text.replace(old, new)
        
        # Remove leading and trailing whitespace
        return text.strip()

    def export_to_html(self):
        # Get the selected feed and corresponding information
        feed = self.selected_feed.get()
        url = self.bbc_url if feed == "bbc" else self.abc_url
        feed_name = "BBC" if feed == "bbc" else "ABC"
        logo = self.bbc_logo if feed == "bbc" else self.abc_logo

        try:
            # Fetch and parse the RSS content
            content = self.fetch_rss_content(url)
            items = self.parse_rss_content(content)
            
            # Generate the HTML content
            html_content = self.generate_html_content(feed_name, logo, url, items)

            # Write the HTML content to a file
            filename = f"{feed_name.lower()}_news.html"
            with open(filename, 'w', encoding='utf-8') as html_file:
                html_file.write(html_content)

            # Open the generated HTML file in the default web browser
            urldisplay(filename)

        except Exception as message:
            # Handle any errors that occur during the export process :/
            error_message = f"Error exporting to HTML: {str(message)}"
            summary_text = getattr(self, f"{feed}_summary_text")
            summary_text.insert('end', error_message)

    def generate_html_content(self, feed_name, logo, url, items):
        # Define the CSS styles for the HTML page
        html_style = """
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; 
            background-color: #f0f0f0; }
            
            .container { max-width: 800px; margin: 0 auto; background-color: white; 
            padding: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            
            h1 { color: #333; text-align: center; }
            
            .logo { display: block; margin: 20px auto; max-width: 200px; }
            
            .news-item { margin-bottom: 30px; border-bottom: 1px solid #ddd; 
            padding-bottom: 20px; }
            
            .news-item:last-child { border-bottom: none; }
            
            h2 { color: #444; }
            
            .date { color: #666; font-style: italic; }
            
            .news-image { max-width: 100%; height: auto; margin-bottom: 10px; 
            width: 35%; }
        """

        # Generate the HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{feed_name.upper()} NEWS SUMMARY</title>
            <style>{html_style}</style>
        </head>
        <body>
            <div class="container">
                <h1>{feed_name.upper()} TECHNOLOGY NEWS</h1>
                <img class="logo" src="{logo}" alt="{feed_name} Logo">
                <p>News source: <a href="{url}">{url}</a></p>
                <p>Created by: {student_name}</p>
        """

        # Add each news item to the HTML content
        for numbered_list, item in enumerate(items[:10], 1):
            html_content += f"""
                <div class="news-item">
                    <h2>{numbered_list}: {item['title']}</h2>
                    <p class="date">Date/time: {item['pubDate']}</p>
                    {'<img class="news-image" src="' + item['image'] + 
                    '" alt="News Image">' if item['image'] else ''}
                    <p>{item['description']}</p>
                </div>
            """

        html_content += """
            </div>
        </body>
        </html>
        """

        return html_content

    def open_live_website(self):
        # Get the URL for the selected feed
        feed = self.selected_feed.get()
        url = self.bbc_url if feed == "bbc" else self.abc_url
        
        try:
            # Open the URL in the default web browser
            urldisplay(url)
            
        except Exception as message:
            # Handle any errors that occur when trying to open the website :/
            error_message = f"Error opening live website: {str(message)}"
            summary_text = getattr(self, f"{feed}_summary_text")
            summary_text.insert('end', error_message)

# Main execution block for the NewsAggregator application.
if __name__ == "__main__":
    # Create the root Tkinter window
    root = Tk()
    # Instantiate the NewsAggregator application
    app = NewsAggregator(root)  
    # Start the Tkinter event loop
    root.mainloop()  

#----------------------------------------------------------------
