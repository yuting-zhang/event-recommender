from bs4 import BeautifulSoup
import urllib.request
import csv
import re
import datetime

class Scraper:

    def get_las_set(self):
        years = [2017]#[i for i in range(2005, 2019)]
        months = [i for i in range(1, 13)]
        last_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        dataset = []
        for year in years:
            print("Crawling Year " + str(year))
            for month in months:
                print("Crawling Month " + str(month))
                url = "https://calendars.illinois.edu/search/1249?go=" + \
                      "go&listType=summary&startDate=" + \
                      str(month) + \
                      "%2F" +  \
                      "1" + \
                      "%2F" + \
                      str(year) + \
                      "&endDate=" + \
                      str(month) + \
                      "%2F" + \
                      str(last_days[month - 1]) + \
                      "%2F" + \
                      str(year) + \
                      "&searchEventType=&KEYWORDS="

                with urllib.request.urlopen(url) as response:
                    html = response.read()
                soup = BeautifulSoup(html, "html.parser")

                dataset_year = self.crawl_events_search(soup)
                if len(dataset_year) > 0:
                    dataset += dataset_year

        self.write_csv(dataset, "las-train.csv")

    def get_cs_set(self):
        years = [i for i in range(2005, 2019)]
        months = [i for i in range(1, 13)]
        last_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        dataset = []
        for year in years:
            print("Crawling Year " + str(year))
            for month in months:
                url = "https://calendars.illinois.edu/search/2654?go=" + \
                      "go&listType=summary&startDate=" + \
                      str(month) + \
                      "%2F" +  \
                      "1" + \
                      "%2F" + \
                      str(year) + \
                      "&endDate=" + \
                      str(month) + \
                      "%2F" + \
                      str(last_days[month - 1]) + \
                      "%2F" + \
                      str(year) + \
                      "&searchEventType=&KEYWORDS="

                with urllib.request.urlopen(url) as response:
                    html = response.read()
                soup = BeautifulSoup(html, "html.parser")

                dataset_year = self.crawl_events_search(soup)
                if len(dataset_year) > 0:
                    dataset += dataset_year

        self.write_csv(dataset, "cs-train.csv")


    def get_cs_latest(self):
        # Get the calendar page html.
        calendar_url = "https://cs.illinois.edu/calendar"
        with urllib.request.urlopen(calendar_url) as response:
            html = response.read()
        soup = BeautifulSoup(html, "html.parser")

        # Find the link with full calendar.
        for link in soup.findAll("a"):
            if link.string == "See the Full Calendar":
                full_calendar_url = link.get("href")

        # Get html of the full calendar
        with urllib.request.urlopen(full_calendar_url) as response:
            html = response.read()
        soup = BeautifulSoup(html, "html.parser")

        dataset = self.crawl_events_latest(soup)
        self.write_csv(dataset, "cs-latest.csv")

    def write_csv(self, dataset, filename):
        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile)
            for row in dataset:
                writer.writerow(row)

    def parse_common(self, time_tag, loc_tag):
        loc_text = loc_tag.get_text()
        loc_text = loc_text.replace(u"\xa0", u" ")

        title_tag = time_tag.parent.parent.next_sibling
        title_string = title_tag.string

        event_url = title_tag.find("a").get("href")
        event_url = "https://calendars.illinois.edu" + event_url

        with urllib.request.urlopen(event_url) as response:
            detailed_page = response.read()
        soup = BeautifulSoup(detailed_page, "html.parser")
        content = soup.find("dd", attrs={"class":"ws-description"})
        if content == None:
            content = ""
        else:
            content = content.get_text().replace(u"\xa0", u" ")
            content = content.replace("  ", " ")
            content = content.replace("\n", " ")

        return loc_text, title_string, content

    def crawl_events_search(self, soup):
        # Get element containing all events
        elem = soup.find(id="list-type-1")

        # This is the number of results
        h2_tag = elem.find("h2")

        retval = []
        while True:
            ul_tag = h2_tag.next_sibling
            li_tags = ul_tag.findAll("li", attrs={"class":"date"})

            for time_tag in li_tags:
                time_text = str(time_tag)
                time_text = time_text.replace(u"\xa0", u" ")
                time_text = time_text.replace("  ", " ")

                loc_tag = time_tag.next_sibling
                # There is no location for this event. Unlikely a CS event.
                if loc_tag == None:
                    continue

                try:
                    pattern = re.compile(
                        "<li class=\"date\">(.*?)<br/>" +
                        "([0-9]+?)/([0-9]+?)/([0-9][0-9][0-9][0-9]).*?</li>")

                    time, m, d, y = pattern.findall(time_text)[0]

                    date = datetime.date(int(y), int(m), int(d))
                    date = date.strftime("%A, %B %d, %Y")
                except:
                    date = ""

                loc_text, title_string, content = self.parse_common(
                    time_tag, loc_tag)

                retval.append([date, time, loc_text, 
                        title_string, content])

            h2_tag = ul_tag.next_sibling
            if h2_tag == None:
                break
        return retval

    def crawl_events_latest(self, soup):
        # Get element containing all events
        elem = soup.find(id="list-type-2")
        
        h2_tag = elem.find("h2")

        retval = []
        while True:
            date_string = h2_tag.string.replace(u"\xa0", u" ")
            ul_tag = h2_tag.next_sibling
            li_tags = ul_tag.findAll("li", attrs={"class":"date"})

            for time_tag in li_tags:
                time_text = time_tag.get_text()
                time_text = time_text.replace(u"\xa0", u" ")
                time_text = time_text.replace("  ", " ")

                loc_tag = time_tag.next_sibling
                # There is no location for this event. Unlikely a CS event.
                if loc_tag == None:
                    continue

                loc_text, title_string, content = self.parse_common(
                    time_tag, loc_tag)

                retval.append([date_string, time_text, loc_text, 
                        title_string, content])

            h2_tag = ul_tag.next_sibling
            if h2_tag == None:
                break
        return retval

