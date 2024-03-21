import os
from fpdf import FPDF


def extract_nutritional_info_and_images(dataset_path, images_base_path):
    nutritional_info = []
    
    with open(dataset_path, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            dish_id = parts[0]
            dish_info = {
                'dish_id': dish_id,
                'calories': float(parts[1]),
                'total_mass': float(parts[2]),
                'total_fat': float(parts[3]),
                'total_carbohydrates': float(parts[4]),
                'total_protein': float(parts[5]),
            }
            # Assuming the dish images are stored in a predictable path
            dish_image_path = os.path.join(images_base_path, f"realsense_overhead/{dish_id}/rgb.png") # Adjust the file extension as needed
            if os.path.exists(dish_image_path):
                dish_info['image_path'] = dish_image_path
                nutritional_info.append(dish_info)
            else:
                dish_info['image_path'] = 'Image not found'
            
            

    return nutritional_info

def load_the_data(dataset_path, images_base_path):
    # Extract the info
    nutritional_info_with_images = extract_nutritional_info_and_images(dataset_path, images_base_path)
    return nutritional_info_with_images

def get_info(info_data, breakpoint, calories_threshold=50):

    selected_dishes = {}
    for (i, dish) in enumerate(info_data):
        if dish['calories'] > 50:
            print(f"Dish {i+1}: {dish['dish_id']}")
            print(f"Calories: {dish['calories']}")
            print(f"Total Mass: {dish['total_mass']}")
            print(f"Total Fat: {dish['total_fat']}")
            print(f"Total Carbohydrates: {dish['total_carbohydrates']}")
            print(f"Total Protein: {dish['total_protein']}")
            print(f"Image Path: {dish['image_path']}")
            print()
            selected_dishes[i] = dish
        if i == breakpoint:
            break
    return selected_dishes

def save_info_to_pdf(extracted_info, save_path):

    # save the info to pdf, including the image
    pdf = FPDF()
    pdf.set_font("Arial", size = 12)
    for i in extracted_info:
        pdf.add_page()
        pdf.cell(200, 10, txt = f"Dish {i+1}: {extracted_info[i]['dish_id']}", ln = True, align = 'L')
        pdf.cell(200, 10, txt = f"Calories: {extracted_info[i]['calories']}", ln = True, align = 'L')
        pdf.cell(200, 10, txt = f"Total Mass: {extracted_info[i]['total_mass']}", ln = True, align = 'L')
        pdf.cell(200, 10, txt = f"Total Fat: {extracted_info[i]['total_fat']}", ln = True, align = 'L')
        pdf.cell(200, 10, txt = f"Total Carbohydrates: {extracted_info[i]['total_carbohydrates']}", ln = True, align = 'L')
        pdf.cell(200, 10, txt = f"Total Protein: {extracted_info[i]['total_protein']}", ln = True, align = 'L')
        pdf.image(extracted_info[i]['image_path'], x = None, y = None, w = 100, h = 100)
        pdf.cell(200, 10, txt = "", ln = True, align = 'L')
        
    pdf.output(save_path)

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(description='Extract and display the nutritional info of dishes')
    parser.add_argument('--dataset_path', type=str, default='metadata/dish_metadata_cafe1.csv', help='Path to the dataset file')
    parser.add_argument('--images_base_path', type=str, default='imagery/', help='Base path where images are stored')
    parser.add_argument('--breakpoint', type=int, default=5, help='Number of dishes to display')
    parser.add_argument('--save_path', type=str, default='metadata/selected_dishes.pdf', help='Path to save the pdf file')
    args = parser.parse_args()


    dataset_path = args.dataset_path 
    images_base_path = args.images_base_path
    nutritional_info_with_images = load_the_data(dataset_path, images_base_path)

    breakpoint = args.breakpoint
    selected_dishes = get_info(nutritional_info_with_images, breakpoint, calories_threshold=50)
    save_path = args.save_path
    if not os.path.exists(os.path.dirname(save_path)):
        os.makedirs(os.path.dirname(save_path))
    save_info_to_pdf(selected_dishes, save_path)

