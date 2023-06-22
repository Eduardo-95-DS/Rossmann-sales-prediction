# **Rossmann store**
## **Sales prediction**

![220px-Roßmann-Markt_in_Berlin](https://user-images.githubusercontent.com/95311171/221661647-73c0decf-d876-4cd9-9ed6-f7064317aa8d.jpg)

# **1. Business problem**
Rossmann is a european drug store, which have over 3,000 unities in 7 european countries.
Normally the store managers predict their daily sales up to for six weeks in advance, which has two major problems, leading to a unreliable precision: 1 - Important factors like seasonality, locality and holidays across Europe; 2 - thousands individuals managers doing the predictions based on their own empirical knowledge.   

Therefore the goal here is to improve the prediction using a machine learning algorithm while also making possible for the CFO to consult the six weeks prediction via a Telegram bot.        


# **2. Business assumptions**
The assumptions about the business problem are as follows:       
- Days with stores closed and/or zero sales were not taken into account.       
- Stores without close competitors had the distance fixed at 200000, which is a lot higher than other distances, as a way of preserving the rows, instead of deleting them.   



# **3. Solution strategy**
Step 01. Data description: My goal is to use statistics metrics to identify data outside the scope of business.   
Step 02. Feature engineering: Derive new attributes based on the original variables to better describe the phenomenon that will be modeled.    
Step 03. Data filtering: Filter rows and select columns that do not contain information for modeling or that do not match the scope of the business.   
Step 04. Exploratory data analysis: Explore the data to find insights and better understand the impact of variables on model learning.   
Step 05. Data preparation: Prepare the data so that the Machine Learning models can learn the specific behavior.   
Step 06. Feature selection: Selection of the most significant attributes for training the model.   
Step 07. Machine learning modelling: Machine Learning model training.   
Step 08. Hyperparameter fine tunning: Choose the best values for each of the parameters of the model selected from the previous step.   
Step 09. Convert model performance to business values: Convert the performance of the Machine Learning model into a business result.   
Step 10. Deploy model to production: Publish the model in a cloud environment so that other people or services can use the results to improve the business decision.   


# **4. Top 3 data insights**
**Hypothesis 01:** Stores with greater assortments should sell more.   
**True.** As observed, the extra assortment sells more, followed by extended and basic, in that order.       

![Screenshot from 2023-06-19 21-32-36](https://github.com/Soturno95/Rossmann-sales-prediction/assets/95311171/533284b2-9781-4160-afd8-3010c5366834)



**Hypothesis 02:** Stores with closer competitors should sell less.      
**False.** As observed, the distance between stores doesn't affect the sales.
![download (1)](https://github.com/Soturno95/Rossmann-sales-prediction/assets/95311171/5045a85f-e0c2-4b37-b05a-b8097eb5c339)



**Hypothesis 06:** Stores with consecutive promotions should sell more.         
**True.** As observed, consecutive promotions increase sales.    

![download (2)](https://github.com/Soturno95/Rossmann-sales-prediction/assets/95311171/6250b6d8-d612-42f4-9da3-ebe3d7fb5c20)


# **5. Machine learning model applied**   
Tests were made using different algorithms.     

| Model name | MAE | MAPE | RMSE | 
|-----------|---------|-----------|---------|
| CatBoost Regressor   | 987.056237 | 0.143865  | 1412.787567 | 
| Average Model	|1354.800353|	0.455051|	1835.135542 |
| XGBoost Regressor	|1713.183272	|0.261204|	2449.559832
| Random Forest Regressor|	1956.270109	|0.297115|	2837.878419|
| Linear Regression	|2057.384627	|0.301612	|3039.636280|
| Linear Regression - Lasso|	2198.584167|	0.342759	|3110.514747|

# **6. Machine learning model performance**
The chosen algorithm was the CatBoost Regressor. In addition, I made a performance calibration on it.   

These are the metrics obtained from the test set.

| Model name | MAE | MAPE | RMSE | 
|-----------|---------|-----------|---------|
| CatBoost Regressor   | 987.056237 | 0.143865  | 1412.787567 | 

The summary below shows the metrics comparison after running a five fold cross validation without and with tuned hyper parameters.   

| Model name | MAE | MAPE | RMSE | 
|-----------|---------|-----------|---------|
| CatBoost Regressor (CV)  | 1003.69 +/-163.91	 |0.14 +/-0.01  | 1454.77 +/-248.75 | 
| CatBoost Regressor (CV + Tuned HP) | 900.86 +/-84.27| 0.12 +/-0.01  | 1300.25 +/-147.89 | 

# **7. Business results**
In the dataset, there were 1115 different stores; if we take into account the mean absolute error of the predictions from all stores using the average model, which uses a simple mean of all stores to predict sales, it leads to a **€1,509,710** miscalculation, while the algorithm gets to a total of **€978,970** mean absolute error, a difference of **€530,740**.    

Here's an example of a six weeks predictions from the five stores with the more accurate predictions ; predictions are the total sales of a giving store, while worst and best scenarios are the possible under and over estimations based on MAE, the mean absolute error.    


|store|	predictions	|worst_scenario|	best_scenario|	MAE	|MAPE|
|--------|-----------|-----------|------------|--------------|----------|
|1098	|€186,619.22	|€186,337.23	|€186,901.21	|281.990104	|0.055884
|523	|€495,993.58	|€495,219.52	|€496,767.64	|774.063158	|0.056405
|981	|€256,660.41	|€256,274.28	|€257,046.54	|386.131729|	0.056915
|875	|€183,020.81	|€182,758.53	|€183,283.08	|262.276640	|0.058730
|489	|€265,813.56	|€265,286.71	|€266,340.41	|526.850079|	0.059235

This would be the possible scenarios from all the stores in six week's advance:   
|Scenario	|Values|
|---------|-------|
|predictions	|€277,707,021.57|
|worst_scenario	|€276,725,465.55|
|best_scenario	|€278,688,577.58|

# **8. Conclusions**
The project successfully solved the two initial problems; the automatization of the predictions with a good precision and a way for the CFO to consult those in a simple and accesible fashion.

# **9. Lessons learned**   
- Develop solutions in a ciclical way
- Build a telegram bot
- Prioritize tasks   


# **10. Next step to improve**   
**1.** Improving the model performance in stores with a mean absolute percentage error (MAPE) greater than 10%.   
**2.** Improving the model performance by testing different parameters with highter ranges.     
**3.** Improving the model performance by testing new feature encoders.    
**4.** Creating a algorithm capable of predicting the number of customers for a given day, allowing the use of the 'customers' variable. 

