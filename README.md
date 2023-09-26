#  Pre-employment screening (01JUN23) (MUNI ÚVT)

Files with the implementation of the tasks:
1. extractor.py
2. ml_task.ipynb

All the versions are mentioned in `requirements.txt`. I've used Python3.11.3, but it seems like this version can't be installed using the package manager yet. Delete the first row from the file if there are problems with installation.

## Implementation details

### Extractor
The important thing to mention is that getting information about pipelines and statistics requires personal access token. You will need to add this at the beginning of the file to the variable TOKEN.

Usage:
```bash
$ python3 extractor.py --output [json/yaml]
```
**Details**:
Due to the big number of public repositories (>500) it takes about 6 minutes to parse all of them. I've implemented a counter which prints to stdout current number of parsed repositories so it doesn't seem like nothing is happening.


### Machine learning model


##### Exploring dataset
It is important to know if the dataset has "clean" format, contains NaN values or not, what datatypes contains etc.

##### Data Preprocessing
To prepare the data for modeling, the following preprocessing steps were performed:

1. Cleaned the dataset by removing empty rows and columns.
2. Performed one-hot encoding on categorical variables to convert them into numerical representations.
3. Split the dataset into training and testing sets.

##### Machine Learning Models

For this task, we employed two different machine learning models:

1. **Random Forest Classifier**:
Used for the classification task of predicting whether it will rain tomorrow or not.
Utilized the ensemble of decision trees to make predictions.
2. **Gradient Boosting Regressor**:
Used for the regression task of predicting the amount of rainfall (in mm) on the next day.
Employed the gradient boosting algorithm to create an ensemble of decision trees.
Assessed the model's performance using mean squared error (MSE) and other regression metrics.


##### Analyzing the results and summary

The models achieved the following results:

**Random Forest Classifier**:
Obtained a high accuracy of 1.0, indicating a perfect classification performance.
Generated a classification report and confusion matrix to analyze the model's performance.

**Gradient Boosting Regressor**:
Evaluated the model's performance using mean absolute error (MAE) and R-squared.
Achieved a low mean squared error (MSE) and high R-squared value, indicating good regression performance.

Due to the perfect performance of the models it was necessary to perform some additional steps and analyze the dataset 
and model processing.






## Author:
[Maryia Mazurava](https://github.com/maryia-mazurava)

