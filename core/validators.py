from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
import magic



class ImageFileValidator:
    """
    Use for validation of all image files.
    """

    extension_message = _("Extension '%(extension)s' not allowed. Allowed extensions are: '%(allowed_extensions)s.'")
    mime_message = _("MIME type '%(mimetype)s' is not valid. Allowed types are: %(allowed_mimetypes)s.")
    min_size_message = _('The current file %(size)s, which is too small. The minimum file size is %(allowed_size)s.')
    max_size_message = _('The current file %(size)s, which is too large. The maximum file size is %(allowed_size)s.')

    def __init__(self, allowed_extensions, allowed_mimes, min_size, max_size):
        """
        Parameters
        ----------
        allowed_extensions : list[str],
        allowed_mimes : list[str],
        min_size : int,
        max_size : int,
        """
        self.allowed_extensions = allowed_extensions
        self.allowed_mimes = allowed_mimes
        self.min_size = min_size
        self.max_size = max_size
