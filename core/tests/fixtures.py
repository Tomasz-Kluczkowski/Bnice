# import os
import pytest
# from PIL import Image
from io import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
# from django.urls import reverse
# from django.test import TestCase

#
# @pytest.fixture
# def add_smiley_form_set_description():
#     """Returns an instance of AddSmileyForm with a description from one of the choices."""
#     form = AddSmileyForm({'description': 'Folded washing', 'new_description': '', 'points': 3})
#     return form


@pytest.fixture
def mock_text_file():
    """Generates in memory .txt, text/plain file. Size is set to 100kB (fake) for ease of testing of min and max file
    size.
    """
    io = StringIO()
    io.write('test content')
    text_file = InMemoryUploadedFile(io, None, 'foo.txt', 'text', 100*1024, None)
    text_file.seek(0)
    return text_file

# def get_temporary_text_file():
#     io = StringIO()
#     io.write('foo')
#     text_file = InMemoryUploadedFile(io, None, 'foo.txt', 'text', io.len, None)
#     text_file.seek(0)
#     return text_file
#
#
# def get_temporary_image():
#     io = StringIO()
#     size = (200,200)
#     color = (255,0,0,0)
#     image = Image.new("RGBA", size, color)
#     image.save(io, format='JPEG')
#     image_file = InMemoryUploadedFile(io, None, 'foo.jpg', 'jpeg', io.len, None)
#     image_file.seek(0)
#     return image_file
#
#
# class ImageUploadViewTests(TestCase):
#     def test_if_form_submits(self):
#         test_image = get_temporary_image()
#         response = self.client.post(reverse('upload-image'), {'image': test_image})
#         self.assertEqual(302, response.status_code)
#
#     def test_if_form_fails_on_text_file(self):
#         test_file = get_temporary_text_file()
#         response = self.client.post(reverse('upload-image'), {'image': test_file})
#         self.assertEqual(200, response.status_code)
#         error_message = 'Upload a valid image. The file you uploaded was either not an image or a corrupted image.'
#         self.assertFormError(response, 'form', 'image', error_message)
