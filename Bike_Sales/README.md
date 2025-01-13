Project Summary:
   * This short project's purpose is to practice end to end analysis and development of ML models using a bike sales dataset from kaggle.
   * This practice focuses on 1) asking relevant business questions to drive analysis direction, 2) exploring visualization techniques and 3) hyper-parameter optimization.
   * Lastly, the steps, outcomes and learnings are documented here to serve as a basis/template for future projects

|File|Description|
|-|-|
|[Bike_Sales.ipynb](Bike_Sales.ipynb)|Jupyter notebook which contains the steps to achieve the results below|

1.  Business questions:
    * What pattern/trend can you find in the customers who purchased bikes vs those who did not?
      - What relationships can you find between the feature columns and the target column?
      - Which feature(s) is/are highly correlated with the target?
    * Can you build model to predict if a new customer would buy a bike?
      - How can you choose between all available classification models?
      - How can you optimize these models?

2.  EDA Summary:

|Visualization|Description|
|-|-|
|![alt_text](https://github.com/zinogore/Personal_Projects/blob/main/Bike_Sales/assets/imgs/MartialStatus_Gender_PurchaseChoice.png)|<ul><li>The distribution between Married and Single is about even. Being single has an increased probability of purchasing a bike.</li></ul><ul><li>The Gender distribution between Male and Female is about even. Gender does not affect purchasing choice.</li></ul>|
|![alt_text](https://github.com/zinogore/Personal_Projects/blob/main/Bike_Sales/assets/imgs/Income_Children_PurchaseChoice.png)|<ul><li>The 25th, 50th and 75th percentile of income is 30k, 60k and 70k respectively. Income does not affect purchasing choice.</li></ul><ul><li>The 25th, 50th and 75th percentile of having children is 0, 2 and 3 respectively. Having lesser children increases probability of purchasing a bike.</li></ul>|
|![alt_text](https://github.com/zinogore/Personal_Projects/blob/main/Bike_Sales/assets/imgs/Education_Occupation_PurchaseChoice.png)|<ul><li>Majority of the population in this dataset did higher education after high school. Having advanced education increases probability of purchasing a bike.</li></ul><ul><li>Professional, Skilled manual and management are occupations with the highest counts in this dataset. Being in Professional Occupation increases probability of purchasing a bike.</li></ul>|
|![alt_text](https://github.com/zinogore/Personal_Projects/blob/main/Bike_Sales/assets/imgs/HomeOwner_Region_AgeBrackets_PurchaseChoice.png)|<ul><li>The amount of homeowners double that of non-homeowners. Owning a home does not affect purchasing choice.</li></ul><ul><li>50% of the population in this dataset are from North America, followed by Europe at 30%, then Pacific Region at 20%. Being from Pacific region increases probability of purchasing a bike.</li></ul><ul><li>70% of the population in this dataset are middle aged, 20% are old aged, and 10% are adolescent. Being Middle Aged increases probability of purchasing a bike.</li></ul>|
|![alt_text](https://github.com/zinogore/Personal_Projects/blob/main/Bike_Sales/assets/imgs/Cars_CommuteDistance_Age_PurchaseChoice.png)|<ul><li>The 25th, 50th and 75th percentile of having cars is 1, 1 and 2 respectively. Having lesser cars increases probability of purchasing a bike.</li></ul><ul><li>The 25th, 50th and 75th percentile of commute distance is 0-1 Miles, 1-2 Miles and 5-10 Miles respectively. Having samller commute distance increases probability of purchasing a bike.</li></ul><ul><li>The 25th, 50th and 75th percentile of age is 35, 43 and 52 respectively. Being ages 30s - 50s increases probability of purchasing a bike.</li></ul>|

3.  Building classifiers and Hyper-parameter tuning

|Visualization|Description|
|-|-|
|![alt_test](https://github.com/zinogore/Personal_Projects/blob/main/Bike_Sales/assets/imgs/Baseline_Models.png)|<ul><li>Visualization shows the test accuracies for baseline models without hyper-parameter tuning.</li></ul><ul><li>RandomForest Classifier is the best performing model at 70% accuracy.</li></ul>|
|![alt_test](https://github.com/zinogore/Personal_Projects/blob/main/Bike_Sales/assets/imgs/Baseline_SFS_Models.png)|<ul><li>Sequential feature selection was added to increase models' performance.</li></ul><ul><li>RandomForest and KNeighbors Classifiers are the best performing models with accuracies of 70% or more.</li></ul>|
|![alt_test](https://github.com/zinogore/Personal_Projects/blob/main/Bike_Sales/assets/imgs/Simple_HyperParameterTuning.png)|<ul><li>A small hyper-parameter grid was used to simply tune the models to increase models' performance.</li></ul><ul><li>RandomForest Classifier is the best performing model at 72% accuracy.</li></ul><ul><li>The accuracy for KNeighbors Classifier droped marginally and could be due to the small hyper-parameters grid.</li></ul>|


4.  RandomForest Classifier Hyper-paramter optimization
```python
# The hyper-parameter grid used to optimize RandomForest:

param_grid = { 'n_estimators':[100,125,150,175,200],
               'criterion':['gini','entropy','log_loss'],
               'max_depth':[9,10,11,12,13] }

# Best model:  RandomForestClassifier(criterion='log_loss', max_depth=11)
# Best params:  {'criterion': 'log_loss', 'max_depth': 11, 'n_estimators': 100}
# Best score:  0.7262500000000001
# Execution time: 169.22
```

5.  Learning and future works
    * k-fold cv resampling goal is to:
      - Not waste data by splitting it into another validation set (A validation set can have important relationships that your model can learn)
      - Measure model performance on unseen data based on variance of each fold (A complex model will show a higher variance in its cv scores)
    * Handle Null and Duplicate entries
    * Handle outliers (z score)
