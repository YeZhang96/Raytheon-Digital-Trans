import numpy as np
import pandas as pd
from typing import TypeVar, List, Any
T = TypeVar('T', str, List[str])

def parse(line: dict, fields: List[T]=['created_at', 'full_text', 'lang', ['user', 'name']]) -> List[Any]:
    """
    Parse one twitter data.
    -------------
    Input:
        line(dict): dictionary of that twitter
        fields(list): a list of fields to extract. If it's a first-level field, 
      input str, if it's a nested field, input list of strs.
      Default fields = ['created_at', 'full_text', 'lang', ['user', 'name']]
    -------------
    Return:
        a list of values of extracted fields.
    """
    ret = []
    for key in fields:
        if type(key) == str:
            ret.append(line[key])
        else:
            value = line
            for subkey in key:
                value = value[subkey]
            ret.append(value)
    return ret

def json2np(json_file: str, fields: List[T]=['created_at', 'full_text', 'lang', ['user', 'name']]) -> np.ndarray:
    """
    Parse json file to np.ndarray.
    --------------
    Input:
        json_file(str): path of input json file
        fields(list): fields(list): a list of fields to extract. 
      If it's a first-level field, input str, if it's a nested field, input list of strs.
      Default fields = ['created_at', 'full_text', 'lang', ['user', 'name']]
    --------------
    Return:
        An NxM matrix, where N = lines of json file, M = number of fields
    """
    data = []
    with open(json_file) as f:
        for line in f:
            data.append(json.loads(line))
    return np.array([parse(line, fields) for line in data])

def json2pd(json_file: str, fields: List[T]=['created_at', 'full_text', 'lang', ['user', 'name']]) -> pd.DataFrame:
    """
    Parse json file to pd.DataFrame.
    --------------
    Input:
        json_file(str): path of input json file
        fields(list): fields(list): a list of fields to extract. 
      If it's a first-level field, input str, if it's a nested field, input list of strs.
      Default fields = ['created_at', 'full_text', 'lang', ['user', 'name']]
    --------------
    Return:
        An NxM matrix, where N = lines of json file, M = number of fields
    """
    data = []
    with open(json_file) as f:
        for line in f:
            data.append(json.loads(line))
    df = pd.DataFrame([parse(line, fields) for line in data])
    col_names = []
    for name in fields:
        if type(name) == str:
            col_names.append(name)
        else:
            col_names.append('_'.join(name))
    df.columns = [col_names]
    return df

def json2csv(json_file: str, fields: List[T]=['created_at', 'full_text', 'lang', ['user', 'name']], csv_file: str=None):
    """
    Parse json file and write parsed data to csv file.
    --------------
    Input:
        json_file(str): path of input json file
        fields(list): fields(list): a list of fields to extract. 
      If it's a first-level field, input str, if it's a nested field, input list of strs.
      Default fields = ['created_at', 'full_text', 'lang', ['user', 'name']].
        csv_file(str): path of output csv fiel. 
      Default would be the path of json file changing '.json' to '.csv'
    """
    if csv_file == None:
        csv_file = json_file[:-5] + '.csv'
    df = json2pd(json_file, fields)
    df.to_csv(csv_file, index=False)
    return
