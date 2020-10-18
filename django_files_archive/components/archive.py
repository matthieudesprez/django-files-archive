import json
import logging
import zipfile
from multiprocessing.pool import ThreadPool

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from functools import partial
from io import BytesIO

from django_files_archive.tools.download import DownloadError, Downloader

LOGGER = logging.getLogger("django_files_archive.archive")


def build_response(*args, headers=None, **kwargs):
    result = HttpResponse(*args, **kwargs)
    if headers:
        for key, value in headers.items():
            result[key] = value
    return result


def download_file_and_write_zip(file_informations, zf, downloader):
    try:
        file = downloader.get_from_url(file_informations['url'])
        print(file_informations)
        data = zipfile.ZipInfo(file_informations['name'].split('?')[0])
        data.compress_type = zipfile.ZIP_DEFLATED
        zf.writestr(data, file)
    except DownloadError:
        LOGGER.exception("File not found")


def generate_zip(files):
    memory_file = BytesIO()
    downloader = Downloader()
    pool = ThreadPool(10)
    with zipfile.ZipFile(memory_file, 'w') as zf:
        pool.map(partial(download_file_and_write_zip, zf=zf, downloader=downloader), files)

    memory_file.seek(0)
    return memory_file


def format_files_array(files):
    """Return a formatted json array
    files can be a str array ['url1', 'url2', 'url3']
    or already a json array [{url:'url1', name:'name1'}, {url:'url2', name:'name2'}]
    """
    result = []
    for f in files:
        url = ''
        if isinstance(f, str):
            url = f
        elif type(f) is dict and f['url']:
            url = f['url']

        try:
            name = f['name']
        except (TypeError, KeyError):
            name = url.split('/')[-1]

        result.append({'url': url, 'name': name})
    return result


def test_archive(request):
    return render(request, "test_archive.html")


@csrf_exempt
def post_zip_and_serve(request):
    data = json.loads(request.body.decode('utf8'))
    try:
        archive = generate_zip(format_files_array(data['files']))
        try:
            name = data['archiveName']
        except KeyError:
            name = 'archive'

        return build_response(archive, status=200, content_type="application/zip",
                              headers={'Content-Disposition': 'attachment; filename=' + name + '.zip'})
    except:
        LOGGER.exception("Archive creation error")
        return build_response(status=400)
