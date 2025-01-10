Project Summary:
   * This short project's purpose is to practice end to end analysis and development of ML models using a bike sales dataset from kaggle.
   * This practice focuses on 1) asking relevant business questions to drive analysis direction, 2) exploring visualization techniques and 3) hyper-parameter optimization.
   * Lastly, the steps, outcomes and learnings are documented here to serve as a basis/template for future projects

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

3.  Build classifiers
4.  Outcomes and learnings



|File|Description|
|-|-|
|[Bike_Sales.ipynb](Bike_Sales.ipynb)|Jupyter notebook which contains the steps to achieve the results below|
