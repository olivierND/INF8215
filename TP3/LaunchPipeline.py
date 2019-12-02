import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder

from TP3.TransformationWrapper import TransformationWrapper, LabelEncoderP

PATH = "data/"
X_train = pd.read_csv(PATH + "train.csv")
X_test = pd.read_csv(PATH + "test.csv")


def parse_unknown(text):
    if "?" in text:
        return "Unknown"
    return text


def parse_income(text):
    if "." in text:
        return text[:-1]
    return text


pipeline_workclass = Pipeline([
    ('unknown', TransformationWrapper(transformation=parse_unknown))
])

pipeline_income = Pipeline([
    ('income', TransformationWrapper(transformation=parse_income))
])

# pour normaliser
pipeline_numerical = Pipeline([
    ("fillna", SimpleImputer(strategy='mean')),
    ("scaler", StandardScaler())
])

# pour binariser
pipeline_binary = Pipeline([
    ("encode", OneHotEncoder(categories='auto', sparse=False))
])

full_pipeline = ColumnTransformer([
    ("Age", pipeline_numerical, ["Age"]),
    ("Workclass", pipeline_workclass, ["Workclass"]),
    ("Sex", pipeline_binary, ["Sex"]),
    ("Capital-gain", pipeline_numerical, ["Capital-gain"]),
    ("Capital-loss", pipeline_numerical, ["Capital-loss"]),
    ("Hours per week", pipeline_numerical, ["Hours per week"]),
])

column_names = ["Age", "Workclass", "Female", "Male", "Capital-gain", "Capital-loss", "Hours per week"] # TODO ajouter les noms des colonnes selon le nouvel ordre du pipeline
X_train_preprocess = pd.DataFrame(full_pipeline.fit_transform(X_train), columns=column_names)
X_test_preprocess = pd.DataFrame(full_pipeline.fit_transform(X_test), columns=column_names)
print(X_train_preprocess.head())