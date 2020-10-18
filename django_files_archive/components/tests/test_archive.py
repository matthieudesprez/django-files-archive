import json
import zipfile
from unittest.mock import call, patch

from django.test import SimpleTestCase
from io import BytesIO

from django_files_archive.tools.download import Downloader


class ArchiveTestCase(SimpleTestCase):
    def test_post_param_ok(self):
        with patch.object(Downloader, 'get_from_url', return_value=b'abc') as mock_urlopen:
            result = self.client.post('/archive/', json.dumps(dict(
                files=[
                    {'url': 'http://fake.net/456.jpg', 'name': 'file1'},
                    {'url': 'http://fake.net/789.jpg', 'name': 'file2'}
                ],
                archiveName="myArchive"
            )), follow=True, content_type="application/json")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result['content-type'], 'application/zip')
        zz = zipfile.ZipFile(BytesIO(result.content))
        files_list = sorted(zz.namelist())
        self.assertEqual(len(files_list), 2)
        self.assertEqual(files_list[0], 'file1')
        self.assertEqual(files_list[1], 'file2')

        mock_urlopen.assert_has_calls([
            call('http://fake.net/456.jpg'),
            call('http://fake.net/789.jpg')
        ])
