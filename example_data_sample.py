from info_utils import get_data
import os
import argparse

parser = argparse.ArgumentParser(description='Extract and display the nutritional info of dishes')
parser.add_argument('--dataset_path', type=str, default='metadata/dish_metadata_cafe1.csv', help='Path to the dataset file')
parser.add_argument('--images_base_path', type=str, default='imagery/', help='Base path where images are stored')
parser.add_argument('--breakpoint', type=int, default=30, help='Number of dishes to display')
parser.add_argument('--save_path', type=str, default='metadata/selected_dishes.pdf', help='Path to save the pdf file')
args = parser.parse_args()

# load the data
dataset_path = args.dataset_path 
images_base_path = args.images_base_path
nutritional_info_with_images = get_data.load_the_data(dataset_path, images_base_path)

# set the demo number of dishes to display
breakpoint = args.breakpoint

# NOTE: the threshold is set to 50 in this case
selected_dishes = get_data.get_info(nutritional_info_with_images, breakpoint, calories_threshold=50)

# save the info to pdf
save_path = args.save_path
if not os.path.exists(os.path.dirname(save_path)):
    os.makedirs(os.path.dirname(save_path))
get_data.save_info_to_pdf(selected_dishes, save_path)
