import pytest
from unittest import mock
from PIL import Image
from io import StringIO, BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile


@pytest.fixture
def mock_text_file():
    """
    Generates in memory .txt, text/plain file. Size is set to 100kB (fake) for ease of testing of min and max file
    size.
    """
    io = StringIO()
    io.write('test content')
    text_file = InMemoryUploadedFile(io, None, 'foo.txt', 'text', 100*1024, None)
    text_file.seek(0)
    return text_file


@pytest.fixture
def mock_image_file():
    """
    Generates in memory .png, image/png file. Size is set to 100kB (fake).
    Dimensions are 500 x 500px.
    """
    io = BytesIO()
    size = (500, 500)
    color = (255, 255, 255, 0)
    image = Image.new("RGBA", size, color)
    image.save(io, format='PNG')
    image_file = InMemoryUploadedFile(io, None, 'test.png', 'png', 100*1024, None)
    image_file.seek(0)
    return image_file


"""
DO NOT SAVE TO HDD IN TESTS!
To avoid reading the file system we generate in memory file - use fixtures mock_txt_file and mock_image_file.
If needed - parametrize them to make them flexible.
To prevent saving to the file system we use mock_img_save as a fixture together with monkeypatch fixture.
Then we patch django storage save method as per line below:
monkeypatch.setattr('django.core.files.storage.FileSystemStorage.save', mock_img_save)
Example usage: dashboard/tests/test_views.py::TestChildUpdate::test_updating_child_data
"""


@pytest.fixture
def mock_img_save():
    """Use to fake save to the django file storage system."""
    mock_save = mock.Mock()
    mock_save.return_value = 'test.png'
    return mock_save
