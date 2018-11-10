import magic
from os.path import splitext

from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


@deconstructible
class FileValidator:
    """
    Use for validation of all image files.
    """

    extension_message = _("Extension '%(extension)s' not allowed. Allowed extensions are: '.%(allowed_extensions)s'.")
    mime_message = _("MIME type '%(mimetype)s' is not valid. Allowed types are: %(allowed_mimetypes)s.")
    min_size_message = _('The current file %(size)s, which is too small. The minimum file size is %(allowed_size)s.')
    max_size_message = _('The current file %(size)s, which is too large. The maximum file size is %(allowed_size)s.')

    def __init__(self, allowed_extensions=None, allowed_mimes=None, min_size=None, max_size=None):
        """
        Parameters
        ----------
        allowed_extensions : list[str], list of allowed file extensions ('jpg', 'png')
        allowed_mimes : list[str], list of allowed file mime types ('image/jpg')
        min_size : int, minimum file size in bytes (500 will be 500B)
        max_size : int, maximum file size in bytes ((10 * 1024 * 1024 will be 10MiB)
        """
        print('INIT IN VALIDATOR')
        self.allowed_extensions = allowed_extensions
        self.allowed_mimes = allowed_mimes
        self.min_size = min_size
        self.max_size = max_size

    def __call__(self, value):
    # check extension
        file_name, extension = splitext(value.name)
        print(file_name, extension)
        if self.allowed_extensions and extension not in self.allowed_extensions:
            raise ValidationError(self.extension_message,
                                  code='invalid_extension',
                                  params={'extension': extension,
                                          'allowed_extensions': ', .'.join(self.allowed_extensions)})

    #     raise ValidationError(
    #         _('%(value)s is not an even number'),
    #         params={'value': value},
    #     )
    #
    # if invalid_input:
    #     raise ValidationError(self.message, code=self.code)

    # check mime type
    # check min size
    # check max size

