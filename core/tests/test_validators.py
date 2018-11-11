import pytest
from django.core.exceptions import ValidationError

from core.validators import FileValidator, ImageValidator # noqa


class TestFileValidator:

    def test_improper_min_max_parametrs(self, mock_text_file):
        with pytest.raises(ValueError) as e:
            FileValidator(min_size=125, max_size=50)
        assert str(e.value) == 'min_size must be lower or equal to max_size. Please check validator parameters.'

    def test_wrong_extension_validation(self, mock_text_file):
        validator = FileValidator(allowed_extensions=['.jpg'])
        with pytest.raises(ValidationError) as e:
            validator(mock_text_file)
        assert str(e.value) == '["Extension \'.txt\' not allowed. Allowed extensions are: \'.jpg\'."]'

    def test_correct_extension_validation(self, mock_text_file):
        validator = FileValidator(allowed_extensions=['.txt'])
        assert validator(mock_text_file) is None

    def test_wrong_mime_type_validation(self, mock_text_file):
        validator = FileValidator(allowed_mimes=['image/jpg'])
        with pytest.raises(ValidationError) as e:
            validator(mock_text_file)
        assert str(e.value) == '["MIME type \'text/plain\' is not valid. Allowed types are: image/jpg."]'

    def test_correct_mime_type_validation(self, mock_text_file):
        validator = FileValidator(allowed_mimes=['text/plain'])
        assert validator(mock_text_file) is None

    def test_min_size_too_small_validation(self, mock_text_file):
        validator = FileValidator(min_size=125)
        with pytest.raises(ValidationError) as e:
            validator(mock_text_file)
        assert str(e.value) == "['File size is too small - 100.0 kB. The minimum file size is 125 kB.']"

    def test_min_size_correct_validation(self, mock_text_file):
        validator = FileValidator(min_size=50)
        assert validator(mock_text_file) is None

    def test_max_size_too_large_validation(self, mock_text_file):
        validator = FileValidator(max_size=90)
        with pytest.raises(ValidationError) as e:
            validator(mock_text_file)
        assert str(e.value) == "['File size is too large - 100.0 kB. The maximum file size is 90 kB.']"

    def test_max_size_correct_validation(self, mock_text_file):
        validator = FileValidator(max_size=125)
        assert validator(mock_text_file) is None
