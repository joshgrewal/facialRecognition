import unittest
import os
import shutil
from face_taker import create_directory, get_face_id

class TestFaceRecognitionFunctions(unittest.TestCase):

    def setUp(self):
        self.test_dir = 'test_images'
        create_directory(self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_create_directory(self):
        new_dir = os.path.join(self.test_dir, 'new_folder')
        create_directory(new_dir)
        self.assertTrue(os.path.exists(new_dir))

    def test_get_face_id(self):
        for i in range(1, 4):
            with open(os.path.join(self.test_dir, f'Users-{i}-1.jpg'), 'w') as f:
                f.write('')  

        self.assertEqual(get_face_id(self.test_dir), 4)

if __name__ == '__main__':
    unittest.main()
