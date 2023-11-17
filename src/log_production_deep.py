import numpy as np
from keras_preprocessing.image import ImageDataGenerator
from keras.layers import Dense, Input, Flatten
from keras.models import Model
from glob import glob
import os
import argparse
from get_data_deep import get_data_deep
import matplotlib.pyplot as plt
from keras.applications.vgg19 import VGG19
import tensorflow
import mlflow
from urllib.parse import urlparse
from mlflow.keras import log_model
from mlflow.tracking import MlflowClient
import joblib
from pprint import pprint

def log_production_deep(config_file):
    config = get_data_deep(config_file)
    mlflow_config_deep = config["mlflow_config_deep"]
    model_name = mlflow_config_deep["registered_deep_model_name"]
    remote_server_uri_deep = mlflow_config_deep["remote_server_uri_deep"]
    mlflow.set_tracking_uri(remote_server_uri_deep)
    mlflow.set_experiment(mlflow_config_deep["experiment_name_deep"])
    
    runs = mlflow.search_runs(experiment_ids='2')
    lowest = runs["params.train_accuracy"].sort_values(ascending=True)[0]
    lowest_run_id = runs[runs["params.train_accuracy"] == lowest]["run_id"][0]

    client = MlflowClient()
    logged_model = None
    

    for mv in client.search_model_versions(f"name='{model_name}'"):
        
        mv = dict(mv)
        if mv["run_id"] == lowest_run_id:
            current_version = mv["version"]
            logged_model = mv["source"]
            pprint(mv, indent=4)
            client.transition_model_version_stage(name=model_name, version=current_version, stage="Production")
        else:
            current_version = mv["version"]
            client.transition_model_version_stage(name=model_name, version=current_version, stage="Staging")
    
    if logged_model is not None:
        loaded_model = mlflow.pyfunc.load_model(logged_model)
        model = config["model"]
        model_path = model["save_dir"]
        joblib.dump(loaded_model, model_path)
    else:
        print("No logged model found.")

if __name__ == '__main__':
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--config', default='deep_params.yaml')
    passed_args = args_parser.parse_args()
    log_production_deep(config_file=passed_args.config)
