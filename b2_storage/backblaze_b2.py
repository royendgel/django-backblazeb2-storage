import base64
from contextlib import closing

import requests
import hashlib


B2_BASE = 'https://api.backblazeb2.com/b2api/v2'
AUTHORIZE_URL = f'{B2_BASE}/b2_authorize_account'
B2_API_PREFIX = '/b2api/v2/'

class BackBlazeB2(object):

    def __init__(self, key_id=None, app_key=None, bucket_id=None, bucket_name=None):
        self.bucket_id = bucket_id
        self.key_id = key_id
        self.app_key = app_key
        self.bucket_name = bucket_name
        self.authorize()

    def authorize(self):
        key = base64.b64encode(f'{self.key_id}:{self.app_key}'.encode('utf-8')).decode('utf-8')
        response = requests.get(
            AUTHORIZE_URL,
            headers={'Authorization': f'Basic {key}'}
        )

        response.raise_for_status()

        resp = response.json()
        self.base_url = resp['apiUrl']
        self.download_url = resp['downloadUrl']
        self.authorization_token = resp['authorizationToken']

    def get_upload_url(self):
        r = requests.get(
            self._build_url('b2_get_upload_url'),
            headers={'Authorization': self.authorization_token},
            params={'bucketId': self.bucket_id}
        )
        r.raise_for_status()
        return r.json()

    def upload_file(self, name, content):
        response = self.get_upload_url()

        sha1 = hashlib.sha1(content.read()).hexdigest()
        content.seek(0)

        upload_response = requests.post(
            response['uploadUrl'],
            headers={
                'Authorization': response['authorizationToken'],
                'X-Bz-File-Name': name,
                'Content-Type': "b2/x-auto",
                'X-Bz-Content-Sha1': sha1,
            },
            data=content.read()
        )
        upload_response.raise_for_status()
        return upload_response.json()

    def get_file_info(self, file_id):
        r = requests.get(
            self._build_url('b2_get_file_info'),
            headers={'Authorization': self.authorization_token},
            params={'fileId': file_id},
        )
        r.raise_for_status()
        return r

    def download_file(self, name):
        r = requests.get(
            get_file_url(name),
            headers={'Authorization': self.authorization_token},
        )
        r.raise_for_status()
        return r.content

    def delete_file_version(self, filename, file_id):
        r = requests.get(
            self._build_url('b2_delete_file_version'),
            headers={'Authorization': self.authorization_token},
            params={
                'fileId': file_id,
                'fileName': filename,
            },
        )
        r.raise_for_status()
        return r

    def get_file_url(self, name):
        return f'{self.download_url}/file/{self.bucket_name}/{name}'

    def _build_url(self, endpoint):
        return  f'{self.base_url}{B2_API_PREFIX}{endpoint}'

