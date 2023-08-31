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
import os
class CustomFileBasedCache(FileBasedCache):
    def _write(self, key, value):
        # Call the parent class method to write the cache file
        super()._write(key, value)
        
        # Get the cache file path
        cache_file_path = self._key_to_file(key)

        # Set the permissions to 666
        try:
            os.chmod(cache_file_path, 0o666)
        except OSError as e:
            # Handle the exception if needed
            pass

                
