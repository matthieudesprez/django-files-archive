import logging
import urllib.request
from urllib.error import HTTPError

from django.conf import settings


class DownloadError(Exception):
    """ Exter file download exception
    """


class Downloader:
    """ External file download
    """

    def __init__(self):
        self.options = settings.DJANGO_FILES_ARCHIVE_OPTIONS
        self.logger = logging.getLogger("django_files_archive.download")

    def get_from_url(self, url):
        if not self.options["DOWNLOAD_ENABLED"]:
            raise DownloadError("Download explicitly disabled")

        self.logger.info("Downloading {}".format(url))

        try:
            with urllib.request.urlopen(url, timeout=self.options['DOWNLOAD_TIMEOUT']) as f:
                return f.read()
        except HTTPError as exc:
            raise DownloadError("HTTP error {}".format(exc.code))
