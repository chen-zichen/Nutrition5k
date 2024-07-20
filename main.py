from info_utils import get_data
import os
import argparse
import json

'''
Description: building questions set.
    1. collect images and nutritional info
    2. randomly select [2] images, display them and their nutritional info. Send info to LLMs.
    3. LLMs give the advice on which dish to choose.
'''


def question_set_preparing(dataset_path, images_base_path, breakpoint, save_path):
    # load the data
    nutritional_info_with_images = get_data.load_the_data(dataset_path, images_base_path)
    # convert the data to a dictionary
    nutritional_info_with_images = {i['dish_id']: i for i in nutritional_info_with_images}

    # number of questions to ask
    # question_number = breakpoint

    # collect the questions set, total number: question_number * 2
    # candidate_dict = get_data.get_info(nutritional_info_with_images, question_number*2, calories_threshold=50)
    

    # save image to save_path/images
    if not os.path.exists(save_path + 'images/'):
        os.makedirs(save_path + 'images/')

    

    # for i in candidate_dict:
    #     image_path = candidate_dict[i]['image_path']
    #     # image_name = image_path.split('/')[-1]
    #     image_id = candidate_dict[i]['dish_id']
    #     os.system(f'cp {image_path} {save_path}images/{image_id}.png')
    #     # change the image path to the new path
    #     candidate_dict[i]['image_path'] = f'{save_path}images/{image_id}.png'
    # print('Questions set saved successfully!')

    if not os.path.exists(os.path.dirname(save_path)):
        os.makedirs(os.path.dirname(save_path))
    question_path = save_path + 'questions.json'
    with open(question_path, 'w') as f:
        json.dump(nutritional_info_with_images, f, indent=4)

def display_questions(question_path, save_path):
    with open(question_path, 'r') as f:
        question_set = json.load(f)

    question_set = list(question_set.values())
    question_number = len(question_set)//2

    for i in range(question_number):
        single_set = question_set[i*2:i*2+2]
        print(f'Question {i+1}:')
        for j in range(2):
            print(f'Dish {j+1}:')
            print(f"Calories: {single_set[j]['calories']}")
            print(f"Total Mass: {single_set[j]['total_mass']}")
            print(f"Total Fat: {single_set[j]['total_fat']}")
            print(f"Total Carbohydrates: {single_set[j]['total_carbohydrates']}")
            print(f"Total Protein: {single_set[j]['total_protein']}")
            # print(f"Image Path: {single_set[j]['image_path']}")
            print()
        # save to question folder
        if not os.path.exists(save_path + f'pair/question_{i+1}/'):
            os.makedirs(save_path + f'pair/question_{i+1}/')
        if not os.path.exists(save_path + f'pair/question_{i+1}/images/'):
            os.makedirs(save_path + f'pair/question_{i+1}/images/')

        image_path_0 = f'question/all_images/{single_set[0]["dish_id"]}.png'
        image_path_1 = f'question/all_images/{single_set[1]["dish_id"]}.png'
        os.system(f'cp {image_path_0} {save_path}pair/question_{i+1}/images/{single_set[0]["dish_id"]}.png')
        os.system(f'cp {image_path_1} {save_path}pair/question_{i+1}/images/{single_set[1]["dish_id"]}.png')

        # os.system(f'cp {single_set[0]["image_path"]} {save_path}pair/question_{i+1}/images/{single_set[0]["dish_id"]}.png')
        # os.system(f'cp {single_set[1]["image_path"]} {save_path}pair/question_{i+1}/images/{single_set[1]["dish_id"]}.png')
        # save info
        # change the image path to the new path
        # single_set[0]['image_path'] = f'question_{i+1}/images/{single_set[0]["dish_id"]}.png'
        # single_set[1]['image_path'] = f'question_{i+1}/images/{single_set[1]["dish_id"]}.png'
        
        with open(save_path + f'pair/question_{i+1}/info.json', 'w') as f:
            json.dump(single_set, f, indent=4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract and display the nutritional info of dishes')
    parser.add_argument('--dataset_path', type=str, default='metadata/dish_metadata_cafe1.csv', help='Path to the dataset file')
    parser.add_argument('--images_base_path', type=str, default='question/all_images/', help='Base path where images are stored')
    parser.add_argument('--breakpoint', type=int, default=40, help='Number of questions')
    parser.add_argument('--save_path', type=str, default='question/', help='Path to save the questions file')
    args = parser.parse_args()

    dataset_path = args.dataset_path
    images_base_path = args.images_base_path
    breakpoint = args.breakpoint
    save_path = args.save_path

    # step 1: collect images and nutritional info
    questions_path = save_path + 'questions.json'
    # if not os.path.exists(questions_path):
    question_set_preparing(args.dataset_path, args.images_base_path, args.breakpoint, args.save_path)

    # step 2: randomly select [2] images, display them and their nutritional info. Send info to LLMs.
    save_pair_path = save_path + 'pair/'
    if not os.path.exists(save_pair_path):
        os.makedirs(save_pair_path)
    display_questions(questions_path, save_path)

    # TODO: step 3: LLMs give the advice on which dish to choose.


