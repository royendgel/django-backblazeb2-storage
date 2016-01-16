import base64
import requests
import hashlib


class BackBlazeB2(object):
    def __init__(self, app_key=None, account_id=None, bucket_name=None):
        self.authorize()
        self.bucket_id = None

    def authorize(self):
        headers = {'Authorization': 'Basic: %s' % (base64.b64encode('%s:%s' % (self.account_id, self.app_key)))}
        response = requests.get('https://api.backblaze.com/b2api/v1/b2_authorize_account', headers=headers)
        if response.status_code == 200:
            resp = response.json()
            self.base_url = resp['apiUrl']
            self.download_url = resp['downloadUrl']
            self.authorization_token = resp['authorizationToken']


            return True

        else:
            return False

    def get_upload_url(self):
        url = self._build_url('/b2api/v1/b2_get_upload_url')
        headers = {'Authorization': self.authorization_token}
        return requests.get(url, headers=headers, params={'bucketId': self.bucket_id}).json()

    def _build_url(self, endpoint=None, authorization=True):
        return "%s%s" % (self.base_url, endpoint)

    def upload_file(self, name, content):
        response = self.get_upload_url()
        if 'uploadUrl' not in response:
            return False
        url = response['uploadUrl']
        sha1_of_file_data = hashlib.sha1(content.read()).hexdigest()
        headers = {
            'Authorization': response['authorizationToken'],
            'X-Bz-File-Name': name,
            'Content-Type': "b2/x-auto",
            'X-Bz-Content-Sha1': sha1_of_file_data,
            'X-Bz-Info-src_last_modified_millis': '',
        }

        return requests.post(url, headers=headers, data=content.read()).json()

    def download_file(self, name):
        headers = {'Authorization': self.authorization_token}
        return requests.get("%s/file/%s/%s" % (self.download_url, self.bucket_name, name), headers=headers).headers
