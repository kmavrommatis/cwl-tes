import urllib
import os
import sys
import cwltool.argparser
import json
import logging
from typing import (
    AnyStr,
    cast
)
from schema_salad.fetcher import  DefaultFetcher
from schema_salad.ref_resolver import file_uri

logger=logging.getLogger('Fetcher_s3')

class BucketFetcher(DefaultFetcher):
    def __init__(
            self, 
            cache, 
            session, 
            fs_access=None):
        super().__init__(cache, session)
        self.fsaccess = fs_access
        

    def fetch_text(self, url, content_types=None):

        split = urllib.parse.urlsplit(url)
        scheme, path = split.scheme, split.path
        logger.critical("Kostas: url {} , Scheme {}, path {}".format(url ,scheme, path))
        #sys.exit(11)
        if scheme == "s3" :
            with self.fsaccess.open(url, "r", encoding="utf-8") as f:
                return f.read()
        else:
            return super().fetch_text(url,content_types)

    def check_exists(self, url):


        split = urllib.parse.urlsplit(url)
        scheme, path = split.scheme, split.path
        try:
            if scheme == "s3" :
                return self.fsaccess.exists(url)
            
        except Exception as e:
            logger.exception("Got unexpected exception checking if file exists")
            return False
        return super().check_exists(url)

    def urljoin(self, base_url, url):
        if not url:
            return base_url

        urlsp = urllib.parse.urlsplit(url)
        if urlsp.scheme or not base_url:
            return url

        basesp = urllib.parse.urlsplit(base_url)
        if basesp.scheme == "s3":
            if not basesp.path:
                raise IOError(errno.EINVAL, "Invalid s3 path", base_url)

            baseparts = basesp.path.split("/")
            urlparts = urlsp.path.split("/") if urlsp.path else []

            locator = baseparts.pop(0)


# TODO check if we have a well formatted s3 object (with scheme, bucket and path)


            if urlsp.path.startswith("/"):
                baseparts = []
                urlparts.pop(0)

            if baseparts and urlsp.path:
                baseparts.pop()

            path = "/".join([locator] + baseparts + urlparts)
            return urllib.parse.urlunsplit((basesp.scheme, "", path, "", urlsp.fragment))

        return super().urljoin(base_url, url)

    schemes = [u"file", u"s3" ]

    def supported_schemes(self):  # type: () -> List[Text]
        return self.schemes