import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from TP3.TransformationWrapper import TransformationWrapper, LabelEncoderP

PATH = "data/"
X_train = pd.read_csv(PATH + "train.csv")
X_test = pd.read_csv(PATH + "test.csv")


def parse_native_country(text):
    if "United-States" not in text:
        return "Other"
    return text


def parse_education(text):
    if "1st" in text \
            or "5th" in text \
            or "7th" in text \
            or "8th" in text \
            or "9th" in text \
            or "10th" in text \
            or "11th" in text \
            or "12th" in text \
            or "HS" in text \
            or "Preschool" in text:
        return "HS or lower"
    return text


def parse_unknown(text):
    if "?" in text:
        return "Unknown"
    return text


def parse_married(text):
    if "Married" in text:
        return "Married"
    return text


def parse_income(text):
    if "." in text:
        return text[:-1]
    return text


def parse_workclass(text):
    words = text.split("-")
    if words[0] == " Self":
        return "Self-employed"
    elif words[0] == " Private":
        return "Private"
    elif len(words) > 1:
        if words[1] == "gov":
            return "Public"
    return "Unknown"


pipeline_workclass = Pipeline([
    ("fill", SimpleImputer(strategy = 'constant', fill_value="Unknown")),
    ('workclass', TransformationWrapper(transformation=parse_workclass)),
    ("encode", LabelEncoderP()),
    ("oneHotEncode", OneHotEncoder(categories='auto', sparse=False))
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
pipeline_hot_encode = Pipeline([
    ("oneHotEncode", OneHotEncoder(categories='auto', sparse=False))
])

pipeline_education = Pipeline([
    ('education', TransformationWrapper(transformation=parse_education)),
    ("encode", LabelEncoderP()),
    ("oneHotEncode", OneHotEncoder(categories='auto', sparse=False))
])

pipeline_country = Pipeline([
    ('native_country', TransformationWrapper(transformation=parse_native_country)),
    ("encode", LabelEncoderP()),
    ("oneHotEncode", OneHotEncoder(categories='auto', sparse=False))
])

pipeline_married = Pipeline([
    ('marital_status', TransformationWrapper(transformation=parse_married)),
    ("encode", LabelEncoderP()),
    ("oneHotEncode", OneHotEncoder(categories='auto', sparse=False))
])

pipeline_occupation = Pipeline([
    ('unknown', TransformationWrapper(transformation=parse_unknown)),
    ("encode", LabelEncoderP()),
    ("oneHotEncode", OneHotEncoder(categories='auto', sparse=False))
])

full_pipeline = ColumnTransformer([
    ("Age", pipeline_numerical, ["Age"]),
    ("Workclass", pipeline_workclass, ["Workclass"]),
    ("Education", pipeline_education, ["Education"]),
    ("Marital-status", pipeline_married, ["Marital-status"]),
    ("Occupation", pipeline_occupation, ["Occupation"]),
    ("Relationship", pipeline_hot_encode, ["Relationship"]),
    ("Sex", pipeline_hot_encode, ["Sex"]),
    ("Capital-gain", pipeline_numerical, ["Capital-gain"]),
    ("Capital-loss", pipeline_numerical, ["Capital-loss"]),
    ("Hours per week", pipeline_numerical, ["Hours per week"]),
    ("Native country", pipeline_country, ["Native country"]),
])

column_names = [
                "Age",
                "Workclass1", "Workclass2", "Workclass3", "Workclass4",
                "Education1", "Education2", "Education3", "Education4",
                "Education5", "Education6", "Education7", "Education8",
                "MaritalStatus1", "MaritalStatus2", "MaritalStatus3", "MaritalStatus4", "MaritalStatus5",
                "Occupation1", "Occupation2",
                "Occupation3", "Occupation4", "Occupation5", "Occupation6", "Occupation7", "Occupation8", "Occupation9",
                "Occupation10", "Occupation11", "Occupation12", "Occupation13", "Occupation14", "Occupation15",
                "Female", "Male",
                "Relationship1", "Relationship2", "Relationship3", "Relationship4", "Relationship5", "Relationship6",
                "Capital-gain", "Capital-loss", "Hours per week",
                "NativeCountry1", "NativeCountry2"
                ]
X_train_preprocess = pd.DataFrame(full_pipeline.fit_transform(X_train), columns=column_names)
X_test_preprocess = pd.DataFrame(full_pipeline.fit_transform(X_test), columns=column_names)
print(X_train_preprocess)