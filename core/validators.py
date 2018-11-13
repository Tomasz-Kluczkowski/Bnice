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
            raise ValueError(_('min_size must be lower than or equal to max_size. Please check validator parameters.'))

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

    min_width_message = _('The width of the image is too small - %(width)spx. '
                          'The minimum width allowed is %(min_width)spx.')
    max_width_message = _('The width of the image is too large - %(width)spx. '
                          'The maximum width allowed is %(max_width)spx.')
    min_height_message = _('The height of the image is too small - %(height)spx. '
                           'The minimum height allowed is %(min_height)spx.')
    max_height_message = _('The height of the image is too large - %(height)spx. '
                           'The maximum height allowed is %(max_height)spx.')

    wrong_config_message = _('%(min_attribute)s must be lower than or equal to %(max_attribute)s. '
                             'Please check validator parameters.')
    fields = ['width', 'height']

    def __init__(self, *args, **kwargs):
        """
        Validation of image files. Extends file validator.

        Additional checks possible: min width, max width, min height, max height.
        Please note that we will NOT check file type here to prevent trying to read dimensions of a .txt file
        - the onus is on the programmer to set allowed extensions and mime types to prevent this.
        This is to avoid duplication in solving the same validation problem.

        Parameters
        ----------
        min_width : int, minimum width of the image in px
        max_width : int, maximum width of the image in px
        min_height : int, minimum height of the image in px
        max_height : int, maximum height of the image in px
        """
        super().__init__(*args, **kwargs)
        self.min_width = kwargs.get('min_width', None)
        self.max_width = kwargs.get('max_width', None)
        self.min_height = kwargs.get('min_height', None)
        self.max_height = kwargs.get('max_height', None)
        for field in self.fields:
            min_attribute, max_attribute = (f'min_{field}', f'max_{field}')
            if (
                    getattr(self, min_attribute) and
                    getattr(self, max_attribute) and
                    getattr(self, min_attribute) > getattr(self, max_attribute)
            ):
                raise ValueError(self.wrong_config_message % {'min_attribute': min_attribute,
                                                              'max_attribute': max_attribute})

    def __call__(self, value):
        width, height = get_image_dimensions(value)

        # check minimum width
        if self.min_width and width < self.min_width:
            raise ValidationError(
                self.min_width_message,
                code='image_width_too_small',
                params={'width': width, 'min_width': self.min_width}
            )

        # check maximum width
        if self.max_width and width > self.max_width:
            raise ValidationError(
                self.max_width_message,
                code='image_width_too_large',
                params={'width': width, 'max_width': self.max_width}
            )

        # check minimum height
        if self.min_height and height < self.min_height:
            raise ValidationError(
                self.min_height_message,
                code='image_height_too_small',
                params={'height': height, 'min_height': self.min_height}
            )

        # check maximum height
        if self.max_height and height > self.max_height:
            raise ValidationError(
                self.max_height_message,
                code='image_height_too_large',
                params={'height': height, 'max_height': self.max_height}
            )
