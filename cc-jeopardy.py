import numpy as np
import pandas as pd
import re
pd.set_option('display.max_colwidth', None)
jeopardy = pd.read_csv('jeopardy.csv')
# print(jeopardy)

jeopardy.rename(columns={'Show Number': 'show_number', ' Air Date': 'air_date', ' Round': 'round', ' Category': 'category', ' Value': 'value', ' Question': 'question', ' Answer': 'answer'}, inplace=True)
# print(jeopardy.columns)
# print(jeopardy.question)

# filtruj kolumne question gdzie wystepuja wszystkie slowa z listy. 1

def filter_dataset(lst, column, dataset):
    str1 = r""
    for i in lst:
        str1 += f"(?=.*{i})"
    filtered = dataset[column.str.contains(str1, flags=re.IGNORECASE)]
    return filtered

my_list = ['King', 'England']
filtered = filter_dataset(my_list,jeopardy.question,jeopardy)
# print(filtered.value)

# def filter_dataset_2(dataset, lst):
#     filter = lambda x: all(word in x for word in lst)
#     return dataset.loc[dataset['question'].apply(filter)]
# filtered_2 = filter_dataset_2(jeopardy, my_list)
# print(filtered_2['question'])

jeopardy['value'] = jeopardy['value'].replace(np.nan, 0)
jeopardy['value'] = jeopardy['value'].replace("[\$,]","", regex=True)

jeopardy['value'] = jeopardy['value'].astype(float)

# jeopardy['value'] = jeopardy['value'].apply(lambda x: x.replace("[\$,]","",inplace=True, regex=True) if x != 'None' else 0)

filtered_3 = filter_dataset(['King'],jeopardy.question,jeopardy)

# print(filtered_3.value.mean())

def count_unique(column):
    n_unique = column.value_counts()
    return n_unique

# print(count_unique(filtered_3['answer']))

jeopardy['air_date'] =pd.to_datetime(jeopardy['air_date'])
# print(jeopardy['air_date'].dtype)
# print('In the 90s:', jeopardy[(jeopardy['question'].str.contains('computer', flags=re.IGNORECASE)) & (jeopardy['air_date']>'1990-01-01') & (jeopardy['air_date']<'2000-01-01')].count())
# print('In the 00s:', jeopardy[(jeopardy['question'].str.contains('computer', flags=re.IGNORECASE)) & (jeopardy['air_date']>'2000-01-01') & (jeopardy['air_date']<'2010-01-01')].count())

def quiz():
    i = 0
    correct_answers = 0
    while i < 5:
        question = jeopardy[['question', 'answer']].sample()
        print(question['question'].item())
        # print(question['answer'].item())
        my_answer = input('Write your answer:')
        if my_answer.lower() == question['answer'].item().lower():
            correct_answers += 1
            print('Correct answer. You get a point!')
        else:
            print(f'Wrong answer. The correct answer was "{question.answer.item()}".')
        i += 1
    return f'Your score is {correct_answers} out of {i}'

print(quiz())
