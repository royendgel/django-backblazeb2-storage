from django.conf import settings
from django.core.files.storage import Storage
from backblaze_b2 import BackBlazeB2


class B2Storage(Storage):
    def __init__(self, account_id=None, app_key=None, bucket_name=None):
        self.account_id = settings.BACKBLAZEB2_ACCOUNT_ID# if account_id == None
        self.app_key = settings.BACKBLAZEB2_APP_KEY # if app_key == None
        self.bucket_name = settings.BACKBLAZEB2_BUCKET_NAME# if bucket_name == None
        self.b2 = BackBlazeB2(account_id=self.account_id, app_key=self.app_key)

    def _save(self, name, content, max_length=None):
        """
        Save and retrieve the filename
        """
        return self.b2.upload_file('Procfile', bucket_name=self.bucket_name)

    def save(self, name, content, max_length=None):
        """
        Save and retrieve the filename
        """
        return self.b2.upload_file('Proc', bucket_name=self.bucket_name)

    # def _open(self, name, mode='rb'):
    #     return self.b2.download_file_by_name('/path/to/myfile.txt', 'savedfile.txt')
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
