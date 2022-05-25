# Fantlab recommender system
This is a project aimed at creating recommendation system for rusiian e-library fantlab.ru. At the moment there are some datasets, python modules to create them and [LightFM](making.lyst.com/lightfm/docs/home.html) collaborative filtration model, showing decent results. Also a content-based model will be available soon.

# Repository content

Here is a little repository content guide.

### [Data/raw](github.com/yupopov/fantlab-recommender-system/tree/main/data/raw)

Data/raw folder contains: 
- html source code files which were used to parse work ids (there is obviously smarter way to do this operation)
- parsed work ids
- works information file
- work features file

### [Data/interim](github.com/yupopov/fantlab-recommender-system/tree/main/data/interim )

This is a folder which contains all the information used during the model fitting, inference etc.:
- embeddings obtained by different ways
- work descriptions, raw and prepared to consume by all the models, assembled to a dictionary
- key to index dictionary in case of using work descriptions as a list, not dictionary

### [src/data_retrieval](github.com/yupopov/fantlab-recommender-system/tree/main/src/data_retrieval)

Folder which is needed to obtain data from Fantlab public API, contains:
- html parser to extract work ids 
- asynchronous downloaders of work infos and users marks

### [src/models](github.com/yupopov/fantlab-recommender-system/tree/main/src/models)

Folder containing models modules:
- linear recommender which eats user interaction matrix and work embeddings and builds personal content recommendation for every user ([LinearRecommender.py](github.com/yupopov/fantlab-recommender-system/blob/main/src/models/LinearRecommender.py))
- LightFM custom recommend function ([lightfm.py](github.com/yupopov/fantlab-recommender-system/blob/main/src/models/lightfm.py))
- auxiliary module to get predictions from the model ([get_top_k_predictions_with_label.py](github.com/yupopov/fantlab-recommender-system/blob/main/src/models/get_top_k_predictions_with_label.py))

### [src/preprocessing](github.com/yupopov/fantlab-recommender-system/tree/main/src/preprocessing)

Folder containing data preprocessing modules:
- [datasets.py](https://github.com/yupopov/fantlab-recommender-system/blob/main/src/preprocessing/datasets.py) has functions to create datasets for both collaborative and content models
- [item_features_buildup.py](https://github.com/yupopov/fantlab-recommender-system/blob/main/src/preprocessing/item_features_buildup.py) module is needed to build additional categorical features of works put in consumable by LightFM format
- [mark_weights.py](https://github.com/yupopov/fantlab-recommender-system/blob/main/src/preprocessing/mark_weights.py) module is needed to filter interaction matrix by marks
- [time_weights.py](https://github.com/yupopov/fantlab-recommender-system/blob/main/src/preprocessing/time_weights.py) module is needed to filter interaction matrix by time
- [title_parser.py](https://github.com/yupopov/fantlab-recommender-system/blob/main/src/preprocessing/title_parser.py) contains methods to parse work infos in .json format to pd.DataFrame