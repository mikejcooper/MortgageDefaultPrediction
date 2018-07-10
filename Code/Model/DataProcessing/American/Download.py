import requests
import os
import zipfile
import sys

from DataParser import DataParser


class Download:
    """ A class that parses input data from file. """

    INSPECT_LOANS_WITHOUT_FINAL_STATE = True
    PRINT_LOAN_BREAKDOWN = True
    TESTING = True

    def __init__(self):
        """ Example of docstring on the __init__ method.  """
        site_url = "https://freddiemac.embs.com/FLoan/secure/auth.php"
        s = requests.Session()
        payload = {'username': 'mike@mjcooper.co.uk', 'password': 'GrA;lk_>', 'pagename' : 'download3'}
        p = s.post(site_url, data=payload)
        url = "https://freddiemac.embs.com/FLoan/Data/download3.php"
        payload = {'accept':'Yes', 'action':'acceptTandC', 'acceptSubmit':'Continue'}
        p = s.post(url, data=payload)



        download_urls = [
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=historical_data1_1999&s=570199258",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=historical_data1_2000&s=213575455",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=historical_data1_2001&s=659112190",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=historical_data1_2002&s=798136534",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=historical_data1_2003&s=1513081471",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=historical_data1_2004&s=869488207",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=historical_data1_2005&s=1314064506",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=historical_data1_2006&s=797722009",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=historical_data1_2007&s=716910619",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=historical_data1_2008&s=578892979",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=historical_data1_2009&s=1093383576",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=historical_data1_2010&s=677707412",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=historical_data1_2011&s=467929546",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=historical_data1_2012&s=690372870",
            "https://freddiemac.embs.com/FLoan/Data/download.php?f=historical_data1_2013&s=568015319",
            "https://freddiemac.embs.com/FLoan/Data/download.php?f=historical_data1_2014&s=297454876",
            "https://freddiemac.embs.com/FLoan/Data/download.php?f=historical_data1_2015&s=295402771",
            "https://freddiemac.embs.com/FLoan/Data/download.php?f=historical_data1_2016&s=165076479",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=sample_1999&s=24669805",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=sample_2000&s=14064597",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=sample_2001&s=18939513",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=sample_2002&s=23271421",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=sample_2003&s=38804904",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=sample_2004&s=38584003",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=sample_2005&s=39176393",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=sample_2006&s=31691049",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=sample_2007&s=29384745",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=sample_2008&s=23881252",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=sample_2009&s=27627626",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=sample_2010&s=26764196",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=sample_2011&s=24624393",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=sample_2012&s=26246421",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=sample_2013&s=21571753",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=sample_2014&s=15778079",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=sample_2015&s=11671785",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=sample_2016&s=5861527",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=harp_historical_data1&s=571296941",
            # "https://freddiemac.embs.com/FLoan/Data/download.php?f=READ_ME&s=973713"
        ]

        # for download_url in download_urls:
        #     self.DownloadFile(download_url, s)

        for download_url in download_urls:
            self.unzip_files(download_url)

    def DownloadFile(self, url, s):
        local_filename = url.split('/')[-1].split("f=",1)[1].split("&s",1)[0]
        with open(local_filename + '.zip', "wb") as f:
            print "Downloading %s" % local_filename
            response = s.get(url, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None:  # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                    sys.stdout.flush()


    def unzip_files(self, url):
        local_filename = url.split('/')[-1].split("f=",1)[1].split("&s",1)[0]
        zip_ref = zipfile.ZipFile(local_filename + '.zip', 'r')
        zip_ref.extractall(local_filename)
        zip_ref.close()
        for filename in os.listdir(os.getcwd() + '/' + local_filename + '/'):
            filename_out = filename.split(".zip", 1)[0]
            zip_ref = zipfile.ZipFile(os.getcwd() + '/' + local_filename + '/' + filename, 'r')
            zip_ref.extractall(os.getcwd() + '/' + local_filename + '/' + filename_out)
            zip_ref.close()



if __name__ == "__main__":
    Download()

