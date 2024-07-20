import os

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

def extract_nutritional_info_from_images(dataset_path, images_base_path):
    nutritional_info = []
    dish_ids = []
    # for all images in the images_base_path
    for root, dirs, files in os.walk(images_base_path):
        for file in files:
            if file.endswith('.png'):
                dish_id = file.split('.')[0]
                # remove the 'dish_' prefix
                # dish_id = dish_id[5:]
                # record the dish_id
                dish_ids.append(dish_id)

    with open(dataset_path, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            dish_id = parts[0]
            if dish_id in dish_ids:
                dish_info = {
                    'dish_id': dish_id,
                    'calories': float(parts[1]),
                    'total_mass': float(parts[2]),
                    'total_fat': float(parts[3]),
                    'total_carbohydrates': float(parts[4]),
                    'total_protein': float(parts[5]),
                }
                nutritional_info.append(dish_info)
    return nutritional_info


    
    

def load_the_data(dataset_path, images_base_path):
    # Extract the info
    # nutritional_info_with_images = extract_nutritional_info_and_images(dataset_path, images_base_path)
    nutritional_info_with_images = extract_nutritional_info_from_images(dataset_path, images_base_path)

    return nutritional_info_with_images
def save_image_to_pdf(image_path, save_path):
    from fpdf import FPDF

    # NOTE: temp
    # save the image to a pdf
    pdf = FPDF()
    
    pdf.add_page()
        # if the image is broken, this will raise an error
    try:
        pdf.image(image_path, x=10, y=8, w=100)
        pdf.output(save_path)
        return True  # Successfully saved to PDF
    except:
        return False

def get_info(info_data, breakpoint, calories_threshold=50):

    selected_dishes = {}
    for (i, dish) in enumerate(info_data):
        if dish['calories'] > calories_threshold:
            # save image to a temp pdf to check whether the image is broken
            # if save_image_to_pdf does not have any error, then the image is not broken
            
            # save the image to a temp pdf
            continue_or_not = save_image_to_pdf(dish['image_path'], 'temp.pdf')
            if continue_or_not:
                print(f"Dish {i+1}: {dish['dish_id']}")
                print(f"Calories: {dish['calories']}")
                print(f"Total Mass: {dish['total_mass']}")
                print(f"Total Fat: {dish['total_fat']}")
                print(f"Total Carbohydrates: {dish['total_carbohydrates']}")
                print(f"Total Protein: {dish['total_protein']}")
                print(f"Image Path: {dish['image_path']}")
                print()
                selected_dishes[i] = dish
            
        if len(selected_dishes) >= breakpoint:
            break
    return selected_dishes

def save_info_to_pdf(extracted_info, save_path):
    from fpdf import FPDF

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

# def save_question_to_pdf(question_set, save_path, task, question_id, beginning_path):
def save_question_to_pdf(question_sets, save_path, beginning_path):
    from fpdf import FPDF

    pdf = FPDF()


    for item in question_sets:
        task = question_sets[item][0]['task']
        question_id = question_sets[item][0]['question_id']
        question_set = question_sets[item]

        # save the questions: A, B to pdf, including their images
    
        pdf.set_font("Arial", size = 12)
        pdf.add_page()
        pdf.cell(200, 10, txt = f"Task: {task}", ln = True, align = 'L')
        pdf.cell(200, 10, txt = f"Question ID: {question_id}", ln = True, align = 'L')
        # Question A and B are in 2 columns layout
        pdf.set_fill_color(200, 220, 255)
        pdf.set_draw_color(0)
        pdf.set_line_width(0.3)
        col_width = pdf.w / 2.2
        row_height = pdf.font_size
        pdf.set_font('Arial', 'B', 12)
        pdf.ln(row_height)
        # Headers
        pdf.set_font('Arial', '', 12)
        # Data
        for i in range(len(question_set)):
            pdf.cell(col_width, row_height, f"Dish {i+1}", border=1)
        pdf.ln(row_height)
        # Images 
        # align with dish 1 and dish 2
        pdf.image(question_set[0]['image_path'], x = 10, y = 70, w = 50, h = 50)
        pdf.image(question_set[1]['image_path'], x = 120, y = 70, w = 50, h = 50)

        # info aligns with dish 1 and dish 2 after the images
        pdf.ln(row_height)
        for i in range(len(question_set)):
            pdf.cell(col_width, row_height, f"Calories: {question_set[i]['calories']}", border=1)
        pdf.ln(row_height)
        for i in range(len(question_set)):
            pdf.cell(col_width, row_height, f"Total Mass: {question_set[i]['total_mass']}", border=1)
        pdf.ln(row_height)
        for i in range(len(question_set)):
            pdf.cell(col_width, row_height, f"Total Fat: {question_set[i]['total_fat']}", border=1)
        pdf.ln(row_height)
        for i in range(len(question_set)):
            pdf.cell(col_width, row_height, f"Total Carbohydrates: {question_set[i]['total_carbohydrates']}", border=1)
        pdf.ln(row_height)
        for i in range(len(question_set)):
            pdf.cell(col_width, row_height, f"Total Protein: {question_set[i]['total_protein']}", border=1)
        pdf.ln(row_height)
        
    # save to pdf
    pdf.output(save_path)
    



