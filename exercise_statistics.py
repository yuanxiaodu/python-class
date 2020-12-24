import os
import glob
import json
import pandas as pd
import numpy as np


def duplicates(cells):
    tmp = []
    for i, cell in enumerate(cells):
        if cell['source'] in tmp:
            del cells[i]
        else:
            tmp.append(cell['source'])


def main():
    exercise = pd.DataFrame(columns=('id',))
    exercise = exercise.set_index('id')
    for f in os.listdir('.'):
        if f.isnumeric():
            file_list = glob.glob(f'{f}/作业/*.ipynb')
            for file_path in file_list:
                try:
                    with open(file_path) as file:
                        section, stu_id = os.path.splitext(os.path.split(file_path)[1])[0].split('_')
                        if f'cell_{section}' not in exercise.columns:
                            exercise[f'cell_{section}'] = np.nan
                            exercise[f'code_cell_{section}'] = np.nan
                            exercise[f'valid_cell_{section}'] = np.nan
                            exercise[f'line_{section}'] = np.nan
                        ipynb = json.loads(file.read())
                        cells = ipynb['cells']
                        if stu_id not in exercise.index.to_numpy():
                            exercise.loc[stu_id] = np.nan
                        exercise.at[stu_id, f'cell_{section}'] = len(cells)
                        code_cell = list(filter(lambda x: x['cell_type'] == 'code', cells))
                        exercise.at[stu_id, f'code_cell_{section}'] = len(code_cell)
                        valid_cell = list(filter(lambda x: x['execution_count'] is not None, code_cell))
                        duplicates(valid_cell)
                        exercise.at[stu_id, f'valid_cell_{section}'] = len(valid_cell)
                        line = sum(map(lambda x: len(x['source']), valid_cell))
                        exercise.at[stu_id, f'line_{section}'] = line
                except:
                    print(f'error at {file_path}')
    exercise = exercise.sort_index(key=lambda x: list(map(lambda y: y[-1], x.str.split('_'))), axis=1)
    exercise.to_excel('作业.xlsx')


if __name__ == '__main__':
    # # 显示所有列
    # pd.set_option('display.max_columns', None)
    # # 显示所有行
    # pd.set_option('display.max_rows', None)
    # # 设置value的显示长度为100，默认为50
    # pd.set_option('max_colwidth', 100)
    main()
