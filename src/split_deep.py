import argparse
import os
import shutil
import logging
import yaml
import pandas as pd 
import numpy as np
from get_data_deep import get_data_deep 

#import boto3
#client = boto3.client('s3')
#root_dir = 's3://mri-corse5i/'

def train_and_test_deep(config_file):
    config = get_data_deep(config_file)
    root_dir = config['data_source']['data_src']
    #client = boto3.client('s3')
    #root_dir = 's3://mri-corse5i/'
    dest = config['load_data_deep']['preprocessed_data']
    p = config['load_data_deep']['full_path']
    cla = config['data_source']['data_src']
    cla = os.listdir(cla)
    
    splitr = config['train_split']['split_ratio']
    for k in range(len(cla)):
        per = len(os.listdir((os.path.join(root_dir,cla[k]))))
        print(k,"->",per)
        cnt = 0
        split_ratio = round((splitr/100)*per)
        for j in os.listdir((os.path.join(root_dir,cla[k]))):
            pat = os.path.join(root_dir+'/'+cla[k],j)
            # print(pat)
            if(cnt!=split_ratio):
                shutil.copy(pat, dest+'/'+'train/class_'+str(k))
                cnt+=1
            else:
                shutil.copy(pat, dest+'/'+'test/class_'+str(k))
        print('Done')


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config",default="deep_params.yaml")
    parsed_args  = args.parse_args()
    train_and_test_deep(config_file=parsed_args.config)
