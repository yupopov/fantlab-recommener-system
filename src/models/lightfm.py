import numpy as np

from tqdm.auto import tqdm
# from lightfm.evaluation import precision_at_k

def precision(true: np.array, predicted: np.array):
    return len(np.intersect1d(true, predicted)) / len(predicted)


def recall(true: np.array, predicted: np.array):
    return len(np.intersect1d(true, predicted)) / len(true)


def precision_at_k(model, test_interactions, train_interactions=None,
    k=10, user_features=None, item_features=None, num_threads=2):
    test_interactions_csr = test_interactions.tocsr()
    if train_interactions is not None:
        train_interactions_csr = train_interactions.tocsr()

    num_items = test_interactions.shape[1]
    item_ids = np.arange(num_items)
    user_ids, _ = test_interactions_csr.nonzero()
    user_ids = np.unique(user_ids).tolist()

    precisions = []

    for user in tqdm(user_ids):
        user_predicts = model.predict(
          user, item_ids,
          user_features=user_features, item_features=item_features,
          num_threads=num_threads
        )
        if train_interactions is not None:
            user_train_interactions = train_interactions_csr[user].toarray().\
                flattten().astype(bool)
            user_predicts = np.where(
              ~user_train_interactions, user_predicts, -np.Inf
              )
        top_k_predictions = np.argsort(user_predicts)[-1:-k+1:-1]

        user_test_interactions = test_interactions_csr[user].toarray().\
            flatten().nonzero()[0]
        user_precision = precision(user_test_interactions, top_k_predictions)
        precisions.append(user_precision)
    
    precisions = np.array(precisions)
    return precisions


def precision_at_k(model, test_interactions, train_interactions=None,
    k=10, user_features=None, item_features=None, batch_size=50, num_threads=2):
    test_interactions_csr = test_interactions.tocsr()
    if train_interactions is not None:
        train_interactions_csr = train_interactions.tocsr()

    num_items = test_interactions.shape[1]
    item_ids = np.arange(num_items)
    user_ids, _ = test_interactions_csr.nonzero()
    user_ids = np.unique(user_ids)

    precisions = []

    for batch_start in tqdm(range(0, len(user_ids), batch_size)):
        user_batch = user_ids[batch_start: batch_start + batch_size]
        batch_len = len(user_batch)

        user_ids_batch = np.repeat(user_batch, repeats=num_items)
        item_ids_batch = np.repeat(
            item_ids.reshape(-1, 1),repeats=batch_len, axis=1).T.flatten()
        batch_predicts = model.predict(user_ids_batch, item_ids_batch)
        batch_predicts = batch_predicts.reshape(batch_len, num_items)
        if train_interactions is not None:
            batch_train_interactions = train_interactions_csr[user_batch].\
                toarray().astype(bool)
            batch_predicts = np.where(
              ~batch_train_interactions, batch_predicts, -np.Inf
              )
        batch_top_k_predictions = np.argsort(batch_predicts, axis=1)[-1:-k+1:-1]

        batch_test_interactions = test_interactions_csr[user_batch].toarray()

        for test_interactions, top_k_predictions in \
            zip(batch_test_interactions, batch_top_k_predictions):
            user_test_interactions = test_interactions.nonzero()[0]
            user_precision = precision(user_test_interactions, top_k_predictions)
            precisions.append(user_precision)
    
    precisions = np.array(precisions)
    return precisions

    
def fit_lightfm(model, fm_dataset, fit_params: dict = {}):
    model.fit(interactions=fm_dataset.train_data,
              item_features=fm_dataset.work_features,
              sample_weight=fm_dataset.train_weights,
              **fit_params)
    
    train_precision = precision_at_k(model, fm_dataset.train_data,
                                     item_features=fm_dataset.work_features,
                                     k=10).mean()
    test_precision = precision_at_k(model, fm_dataset.test_data,
                                    train_interactions=fm_dataset.train_data,
                                    item_features=fm_dataset.work_features,
                                    k=10).mean()

    print(f'Train precision: {train_precision:.4f}')
    print(f'Test precision: {test_precision:.4f}')

    return model
    