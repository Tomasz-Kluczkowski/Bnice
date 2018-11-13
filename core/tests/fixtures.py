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


@pytest.fixture
def mock_img_save():
    """Use to fake save to the django file storage system."""
    mock_save = mock.Mock()
    mock_save.return_value = 'test.png'
    return mock_save
