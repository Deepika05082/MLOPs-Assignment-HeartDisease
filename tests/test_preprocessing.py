from src.preprocessing import preprocess_data

def test_preprocess_shape():
    result = preprocess_data()
    # Take only the first 4 values
    X_train, X_test, y_train, y_test = result[:4]

    assert X_train.shape[0] > 0
    assert X_test.shape[0] > 0
    assert len(y_train) > 0
    assert len(y_test) > 0

