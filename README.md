BACKBLAZE B2 Storage for Django
================================

BackBlaze B2 Storage for django.

###installation
via PIP:

    pip install django-backblazeb2-storage

Manual:

clone this repo locally using `git clone git@github.com:royendgel/django-backblazeb2-storage.git`
and run `python setup.py install`

###Usage

Set this in ypour settings (usualy settings.py)

    BACKBLAZEB2_ACCOUNT_ID = 'your-account-id'
    BACKBLAZEB2_APP_KEY = 'your-app-key'
    BACKBLAZEB2_BUCKET = 'bucketname'

To make it your default django storage : 


    DEFAULT_FILE_STORAGE = 'b2_storage.B2Storage'


if you are making alot of api calls I recommend you to use the b2_storage.authorise,
it stores the seconds in your database and reuses the authorisation_token for other calls.
for this you need to include `'b2_storage.authorise',` in your INSTALLED_APPS

Storage Implimentation : 

- save

    Save the file (overwrite if it already exists)

- open

    Open a file using the filename (the latest version of the file).

- delete

    Deletes the file (all versions of the file)
    

some notes :

Everytime you overwrite a file in backblaze b2 it will create a new file version.
When you download the file the latest version will be downloaded. 
this is the same behavior as s3 but it is enabled be default.
