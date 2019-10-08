BACKBLAZE B2 Storage for Django
================================

BackBlaze B2 Storage for django.

### Installation

via PIP:

    pip install django-backblazeb2-storage

Manual:

    pip install git+git://github.com/royendgel/django-backblazeb2-storage.git

### Usage

Add these to your Django app's settings

    BACKBLAZEB2_ACCOUNT_ID = 'your-account-id'
    BACKBLAZEB2_APP_KEY = 'your-app-key'
    BACKBLAZEB2_BUCKET_NAME = 'bucketname'
    BACKBLAZEB2_BUCKET_ID = 'bucketid'

To make it your default django storage:

    DEFAULT_FILE_STORAGE = 'b2_storage.storage.B2Storage'
