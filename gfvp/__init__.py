def null_session(request):
    '''
    It is necessary in the view where login required
    `interested_in` parameter to control registering user type
    if user autheticated then it can make trouble.
    '''
    if 'interested_in' in request.session:
        request.session['interested_in'] = None   
        
    if request.user.is_authenticated:
            try:
                del request.session['interested_in']
            except Exception as e:
                pass
            
from django.core.cache.backends.filebased import FileBasedCache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
import os

class CustomFileBasedCache(FileBasedCache):
    def set(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        super().set(key, value, timeout, version)

        # Set the permissions to 666
        cache_path = self._key_to_file(key, version)
        try:
            os.chmod(cache_path, 0o666)
            os.chown(cache_path, 'gfvpcom', 'gfvpcom')
        except OSError as e:
            # Handle the exception if needed
            pass

                
