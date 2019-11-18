import pandas as pd
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from TransformationWrapper import TransformationWrapper

PATH = "data/"
X_train = pd.read_csv(PATH + "train.csv")
X_test = pd.read_csv(PATH + "test.csv")


pipeline_feature1 = Pipeline([
    ("name", TransformationWrapper()),
])


full_pipeline = ColumnTransformer([
        ("workclass", pipeline_feature1, ["Workclass"])
        # ("feature2", pipeline_feature2, ["Feature2"]),
    ])

column_names = [] # TODO ajouter les noms des colonnes selon le nouvel ordre du pipeline
X_train_preprocess = pd.DataFrame(full_pipeline.fit_transform(X_train), columns=column_names)
X_test_preprocess = pd.DataFrame(full_pipeline.fit_transform(X_test), columns=column_names)