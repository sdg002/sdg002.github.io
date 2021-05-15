import unittest
import Util
import numpy as np
import os
import skimage
import skimage.io



class Test_Util(unittest.TestCase):

    def test_create_noisy_image_and_verify_that_width_height_match_expected(self):
        expected_width=100
        expected_height=200
        actual_image:np.ndarray=Util.generate_noisy_image(width=expected_width, height=expected_height, salt_pepper=0.5)

        actual_width=actual_image.shape[1]
        actual_height=actual_image.shape[0]

        #Asserts
        self.assertEquals(len(actual_image.shape),3)
        self.assertEquals(actual_width, expected_width)
        self.assertEquals(actual_height, expected_height)

    def test_create_noisy_image_verify_that_count_of_black_pixels_matches_expected_saltpepper_ration(self):
        expected_width=500
        expected_height=500
        expected_saltpepper=0.5
        actual_image:np.ndarray=Util.generate_noisy_image(width=expected_width, height=expected_height, salt_pepper=expected_saltpepper)
        all_white_indices=np.where(actual_image == Util.WHITE_COLOR)
        count_of_white=len(all_white_indices[0])

        all_black_indices=np.where(actual_image == Util.BLACK_COLOR)
        count_of_black=len(all_black_indices[0])
        actual_saltpepper=count_of_white/(count_of_black+count_of_white)
        self.assertEqual(expected_height*expected_width, (count_of_white+count_of_black),msg="The total count of white+black should be total pixels in the picture")
        self.assertAlmostEquals(actual_saltpepper, expected_saltpepper,delta=0.1,msg="The salt peper ratios should match approximately")

    def test_superimpose_dotted_line_vertical_along_the_middle(self):
        expected_width=200
        expected_height=400
        image = np.full([expected_height,expected_width,1],dtype=np.uint8,fill_value=Util.WHITE_COLOR)
        
        start_x=expected_width/2
        start_y=0
        end_x=expected_width/2
        start_y=expected_height
        max_distance=7

        actual_image=Util.superimpose_straight_line_between_2_points(input_image=image,start_x=start_x, start_y=start_y, end_x=end_x, end_y=0, max_distance=max_distance)

        actual_width=actual_image.shape[1]
        actual_height=actual_image.shape[0]
        self.assertEquals(actual_width, expected_width)
        self.assertEquals(actual_height, expected_height)

        all_black_indices=np.where(actual_image == Util.BLACK_COLOR)
        count_of_black=len(all_black_indices[0])
        self.assertGreater(count_of_black,0,"Count of black pixels should be non zero")
        self.assertGreaterEqual(count_of_black, round(expected_height/max_distance)-1)
        self.assertLessEqual(count_of_black, round(expected_height/max_distance)+6)

        self.__save_numpy_image("Util_unittest_vertical_dotted_line.png", actual_image)
        pass

    '''
    Saves the numpy image to a file under the local script folder
    Use for manual inspection
    '''
    def __save_numpy_image(self,filename:str,image:np.ndarray):
        folder_script=os.path.dirname(__file__)
        file_result=os.path.join(folder_script,"out",filename)
        skimage.io.imsave(file_result,image)


if __name__ == '__main__':
    unittest.main()
