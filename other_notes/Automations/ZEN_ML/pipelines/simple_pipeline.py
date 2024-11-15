from steps.simple_steps import (
    load_train_test_data,
    prepare_model_features,
    train_model,
)
from typeguard import typechecked
from zenml import pipeline


@pipeline
@typechecked
def simple_pipeline() -> None:
    """This is used to run the pipeline."""
    train_data, test_data = load_train_test_data()
    X_train, _, y_train, _ = prepare_model_features(train_data, test_data)
    train_model(X_train, y_train)
