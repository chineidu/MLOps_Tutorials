from typing import Annotated

from typeguard import typechecked


@typechecked
def prepare_model_features() -> (
    tuple[
        Annotated[int, "X_train"],
        Annotated[int, "X_test"],
        Annotated[float, "y_train"],
        Annotated[float, "y_test"],
    ]
):
    X_train_tr, X_test_tr, y_train, y_test = 10, 5, 3.14, 1.618
    return X_train_tr, X_test_tr, y_train, y_test


prepare_model_features()
