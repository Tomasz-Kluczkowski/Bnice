import magic
from os.path import splitext

from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions


@deconstructible
class FileValidator:
    """
    Validation of files.
    Possible checks: extension, mime type, min size, max size.
    """

    extension_message = _("Extension '%(extension)s' not allowed. Allowed extensions are: '%(allowed_extensions)s'.")
    mime_message = _("MIME type '%(mime_type)s' is not valid. Allowed types are: %(allowed_mimes)s.")
    min_size_message = _('File size is too small - %(size)s kB. The minimum file size is %(allowed_size)s kB.')
    max_size_message = _('File size is too large - %(size)s kB. The maximum file size is %(allowed_size)s kB.')

    def __init__(self, *args, **kwargs):
        """
        Parameters
        ----------
        allowed_extensions : list[str], list of allowed file extensions (['.jpg', '.png'])
        allowed_mimes : list[str], list of allowed file mime types (['image/jpg', 'image/png'])
        min_size : int, minimum file size in kB (1 = 1kiB = 1024B)
        max_size : int, maximum file size in kB ((10 = 10kiB = 10*1024B)
        """
        self.allowed_extensions = kwargs.get('allowed_extensions', None)
        self.allowed_mimes = kwargs.get('allowed_mimes', None)
        self.min_size = kwargs.get('min_size', None)
        self.max_size = kwargs.get('max_size', None)
        if self.min_size and self.max_size and self.min_size > self.max_size:
            raise ValueError('min_size must be lower or equal to max_size. Please check validator parameters.')

    def __call__(self, value):
        # check extension
        file_name, extension = splitext(value.name)
        if self.allowed_extensions and extension not in self.allowed_extensions:
            raise ValidationError(
                self.extension_message,
                code='invalid_extension',
                params={'extension': extension,
                        'allowed_extensions': ', '.join(self.allowed_extensions)}
            )

        # check mime type
        mime_type = magic.from_buffer(value.read(), mime=True)
        if self.allowed_mimes and mime_type not in self.allowed_mimes:
            raise ValidationError(
                self.mime_message,
                code='invalid_mime_type',
                params={'mime_type': mime_type, 'allowed_mimes': ', '.join(self.allowed_mimes)}
            )

        file_size = value.size
        print(file_size)

        # check min size
        if self.min_size and file_size < self.min_size * 1024:
            raise ValidationError(
                self.min_size_message,
                code='file_size_too_small',
                params={'size': round(file_size / 1024, 1), 'allowed_size': self.min_size}
            )

        # check max size
        if self.max_size and file_size > self.max_size * 1024:
            raise ValidationError(
                self.max_size_message,
                code='file_size_too_large',
                params={'size': round(file_size / 1024, 1), 'allowed_size': self.max_size}
            )


@deconstructible
class ImageValidator(FileValidator):

    def __init__(self, *args, **kwargs):
        """
        Validation of image files. Extends file validator.

        Additional checks possible: min x dimension, max x dimension, min y dimension, max y dimension.

        Parameters
        ----------
        min_x : int, minimum x dimension of the image
        max_x : int, maximum x dimension of the image
        min_y : int, minimum y dimension of the image
        max_y : int, maximum y dimension of the image
        """
        super().__init__(*args, **kwargs)
        self.min_x = kwargs.get('min_x', None)
        self.max_x = kwargs.get('max_x', None)
        self.min_y = kwargs.get('min_y', None)
        self.max_y = kwargs.get('max_y', None)

    def __call__(self, value):
        x, y = get_image_dimensions(value)

        # check dimensions
        # print(get_image_dimensions(value))
