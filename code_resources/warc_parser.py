
import warc
from bs4 import BeautifulSoup
from urlparse import urlparse


class WarcParser:
    def __init__(self, fname):

        try:
            self.fhandle = warc.open(fname, 'r')
            self.reader = self.fhandle.reader

        except IOError as e:
            print "Could not open warc file", fname
            print type(e), ":", e
            exit(1)

        except Exception as e:
            print "Exception", type(e), ":", e
            raise e

    def get_record(self):
        """
        Read a single warc record (Header and content) and extract the tartget-uri (if any),
        and parse all links associated with the records payload.
        """
        record = self.reader.read_record()
        if record is None:
            raise StopIteration
        try:
            url = self.get_base_url(record.header)
        except KeyError as e:
            raise e

        links = self.get_links(record.payload)
        return url, links

    def get_base_url(self, header):
        """
        Try to extract the base url of the crawled target-uri.
        If none exist, the record may be a Metadata record or a warcinfo record.
        """
        try:
            return urlparse(header['WARC-Target-URI']).netloc
        except KeyError as e:
            raise e

    def get_links(self, payload):
        doc = BeautifulSoup(payload.read(), "lxml")
        links = []
        for link in doc.find_all('a'):
            l = urlparse(link['href']).netloc
            if l == "":
                continue
            else:
                links.append(l)
        return links
