'''
    Description: All questions.
'''

import os
import argparse
import json
from info_utils import get_data

parser = argparse.ArgumentParser(description='All questions.')
parser.add_argument('--data_path', type=str, default='question/pair', help='Path to the data file')
args = parser.parse_args()


# load the data
data_path = args.data_path
# load all the question_x in the data_path
question_files = os.listdir(data_path)
question_files = [x for x in question_files if 'question' in x]
# only select question_x, x<=30
question_files = [x for x in question_files if int(x.split('_')[-1]) <= 30]

# question_files = question_files[:30]

# sort the questions by question_id
# question_files = sorted(question_files, key=lambda x: int(x.split('_')[-1]))

tasks = ['Strength Training', 'Endurance Training', 'Weight Loss']
save_to_pdf = {}
for question_file in question_files:
    # 1-10: Strength Training, 11-20: Endurance Training, 21-30: Weight Loss
    
    question_path = os.path.join(data_path, question_file)

    # get the question_id
    question_id = int(question_path.split('question_')[-1])

    if question_id <= 10:
        task = tasks[0]
    elif question_id <= 20:
        task = tasks[1]
    else:
        task = tasks[2]

    # get the info
    info_path = os.path.join(question_path, 'info.json')
    with open(info_path, 'r') as f:
        question_set = json.load(f)
    # save task, question A (info, image), question B (info, image) to pdf
    save_path = f'question_setting/questions_display.pdf'
    if not os.path.exists(os.path.dirname(save_path)):
        os.makedirs(os.path.dirname(save_path))

    # preparing the elements for the pdf
    beginning_path = 'question/pair/'
    # question A
    dish_A = question_set[0]
    dish_A['task'] = task
    dish_A['dish'] = 'A'
    dish_A['image_path'] = os.path.join(beginning_path, dish_A['image_path'])
    dish_A['question_id'] = question_id
    # question B
    dish_B = question_set[1]
    dish_B['task'] = task
    dish_B['dish'] = 'B'
    dish_B['image_path'] = os.path.join(beginning_path, dish_B['image_path'])
    dish_B['question_id'] = question_id
    # save to pdf
    save_to_pdf[question_id] = [dish_A, dish_B]


# save to pdf using save_question_to_pdf
beginning_path = 'question/pair/'
get_data.save_question_to_pdf(save_to_pdf, save_path, beginning_path)

    
    
