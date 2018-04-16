from bs4 import BeautifulSoup
import urllib.request


class CSScraper:

    def parse(self):
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

                retval.append((date_string, time_text, loc_text, 
                        title_string, content))

            h2_tag = ul_tag.next_sibling
            if h2_tag == None:
                break
        return retval

if __name__ == "__main__":
    cs_scrapper = CSScraper()
    print("\n".join([str(elem) for elem in cs_scrapper.parse()]))
