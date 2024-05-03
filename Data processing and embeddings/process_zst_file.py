print('first line')
import sys
version = sys.version_info
if version.major < 3 or (version.major == 3 and version.minor < 10):
    raise RuntimeError("This script requires Python 3.10 or higher")
import os
from typing import Any, Iterable
from sys import argv

sys.path.insert(1, '/Users/benemery/cu/research/code/arctic_shift/scripts')
from fileStreams import getFileJsonStream
import pandas as pd
# import psycopg2
# from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
# import pandas.io.sql as sqlio
# from sqlalchemy import types, create_engine 
from glob import glob
import json
import numpy as np
from time import time

import warnings
warnings.filterwarnings("ignore")

# table_type = str(sys.argv[1])
# start_idx = int(sys.argv[2])
file = str(sys.argv[1])

#Functions for processing .zst files with arctic_shift
def processRow(row: dict[str, Any]):
    # Do something with the row
    return(row)

def getNumRows(path: str):
    jsonStream = getFileJsonStream(path)
    numRows = sum(1 for _ in jsonStream)
    return(numRows)


# Define a function to replace dictionary values with None
def replace_dict_with_none(value):
    if isinstance(value, dict):
        return None
    else:
        return value

def rows_to_df_to_db(rows,cols):
    df = pd.DataFrame(rows)
    if 'created_utc' in df.columns:
        df['timestamp'] = pd.to_datetime(df['created_utc'],unit='s')
    target_cols = cols
    df = df[[c for c in target_cols if c in df.columns]]
    # for col in ['preview','media','media_embed','secure_media','secure_media_embed']:
    #     if col in df.columns:
    #         df[col] = df[col].apply(json.dumps)

    # for col in df.columns:
        # df[col] = df[col].astype(str)
    df = df.replace({"\x00": "\uFFFD"}, regex=True)
    # df = df[[c for c in df.columns if c not in ['preview','media','media_embed','secure_media','secure_media_embed']]]
    # df = df.applymap(replace_dict_with_none) #sledgehammer

    # if i == 0:
    #     cols = df.columns
    # else:
    df = df[[c for c in cols if c in df.columns]] #force column order 


    # if length > 5*(10**6):

    return df


chunkSize = 2*(10**5)

# files = sorted(glob('/data/reddit/'+table_type+'/R*_*.zst'))

# for i,file in enumerate(files[start_idx:]):
file = sys.argv[1]
# i+=start_idx
# print(i,file)
tic = time()
jsonStream = getFileJsonStream(file)

length = getNumRows(file)


# for j in np.arange(0,length+chunkSize,chunkSize):
    # rowsub, le = processFile(file,j,j+chunkSize)
    # rowsub = rows[j:j+chunkSize]
rows = []
cols = ['body', 'author', 'id', 'parent_id', 'retrieved_on', 'timestamp']
redditdf = pd.DataFrame(columns=cols)
for j, (lineLength, row) in enumerate(jsonStream):
    row = processRow(row)
    rows.append(row)
    if ((j>0) and (j % 10_000 == 0) or (j>=length-1)):
        print(f"\rRow {j}", end="")
        redditdf = pd.concat([redditdf,rows_to_df_to_db(rows,cols)],ignore_index=True)
        rows = []
redditdf = pd.concat([redditdf,rows_to_df_to_db(rows,cols)],ignore_index=True)

redditdf.to_csv(file[:-4]+'.csv')
toc = time()
print('done in '+str((toc-tic)/60.0)+' minutes')



# add network location





                  