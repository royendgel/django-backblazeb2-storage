from tempfile import TemporaryFile

from io import BytesIO
from django.conf import settings
from django.core.files.storage import Storage
from django.core.files.base import File
from .backblaze_b2 import BackBlazeB2


class B2Storage(Storage):
    def __init__(self, account_id=None, app_key=None, bucket_name=None):
        self.account_id = settings.BACKBLAZEB2_ACCOUNT_ID  # if account_id == None
        self.app_key = settings.BACKBLAZEB2_APP_KEY  # if app_key == None
        self.bucket_name = settings.BACKBLAZEB2_BUCKET_NAME  # if bucket_name == None
        self.b2 = BackBlazeB2(app_key=self.app_key, account_id=self.account_id, bucket_name=self.bucket_name)

    def save(self, name, content, max_length=None):
        """
        Save and retrieve the filename.
        If the file exists it will make another version of that file.
        """

        resp = self.b2.upload_file(name, content)
        if 'fileName' in resp:
            return resp['fileName']

        else:
            # Raise exception
            pass

    def exists(self, name):
        '''
        BackBlaze B2 does not have a method to retrieve a filename info.
        To get the info you need to make a download request, it will request the whole body.
        imagine a file of 1 GB to only get the file info.
        you can also list all files in that directory in chunks of 1000 imagine a directory of 10000.
        For now it will only request return False.
        '''

        return False

    def _temporary_storage(self, contents):
        '''
        Use this to return file objects
        '''

        conent_file = TemporaryFile(contents, 'r+')
        return conent_file

    def open(self, name, mode='rb'):
        resp = self.b2.download_file(name)

        output = BytesIO()
        output.write(resp)
        output.seek(0)
        return File(output, name)


        #
        # def get_available_name(self, name, max_length=None):
        #     pass
        #
        # def delete(self, name):
        #     pass
        #
        # def exists(self, name):
        #     pass
        #
        # def listdir(self, path):
        #     pass
        #
        # def size(self, name):
        #     pass
        #
        # def url(self, name):
        #     pass
