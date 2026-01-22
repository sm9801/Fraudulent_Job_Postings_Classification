# Fraudulent Job Postings Classification Pipeline

This project evaluates several different models to effectively identify fraudulent job postings. Using Snowflake as a data streaming platform and warehousing services and Dataiku as an analysis platform, we evaluate multiple models to determine relevant features in fraudulent job posting identification.
Furthermore, we aim to learn more about model parameters that leads to effective classifications.

⚠️ This project is a restored and updated version of an earlier implementation from 2024. During the original development, critical project assets were lost due to platform-level issues involving Dataiku and Snowflake, including trained model artifacts, configuration parameters, and the streaming connection between the two systems.
Rather than abandoning the project, I treated this incident as an opportunity to strengthen my understanding of production data platforms and system reliability.

To recover the environment, I manually disconnected and rebuilt the Snowflake infrastructure, recreating the database, warehouse, role hierarchy, and user permissions from scratch. These configurations were then re-integrated into Dataiku, where I re-established, secured, and validated all connection parameters. 
Throughout this process, I collaborated with technical specialists from both Snowflake and Dataiku to ensure best practices in security, access control, and system stability. 
With the platform fully restored, the project was rebuilt end-to-end, incorporating improved feature engineering, evaluation strategies, and model comparisons.

## Table of Contents
- [Project Overview](#project-overview)
- [Dataset](#dataset)
- [Approach](#approach)
- [Evaluation](#evaluation)
- [Results](#results)
- [Future Improvements](#future-improvements)

## Project Overview

This data processing flow is designed to analyze job postings and predict the likelihood of them being fraudulent. It begins with a dataset containing various details about job postings, such as job titles, locations, company profiles, and other relevant attributes.
The flow first prepares the data by splitting the location information into separate columns for country, state, and city, which helps in better geographical analysis. It also calculates the length of text fields like company profile, job description, requirements, and benefits, 
which can be useful indicators of job posting quality or authenticity.

Text simplification is applied to these fields to normalize the data, making it easier to process and analyze. This step ensures that the text data is consistent and free from unnecessary variations, which can improve the accuracy of subsequent predictive models.

The core of the flow involves training a predictive model to identify potentially fraudulent job postings. This is achieved by using historical data to train the model, which is then evaluated and scored on test datasets. 
The output datasets, such as "test_scored," "test_scored_2," and "test_scored_3," contain the original job posting information along with additional columns that provide the probability of a job posting being fraudulent and the model's prediction.

These outputs are crucial for businesses and job platforms as they help in identifying and mitigating the risk of fraudulent job postings. By providing a probability score and prediction, the flow enables decision-makers to take proactive measures to ensure the integrity and trustworthiness of job listings on their platforms. 
This not only protects job seekers from scams but also enhances the reputation of the job platform.

## Dataset

We use a sample dataset gathered from multiple sources online streamed into a Snowflake warehouse.

**DISCLAIMER** Due to confidentiality constraints, all data used in this project is synthetic and designed to preserve real-world behavioral patterns. Key attributes such as company names, salary ranges, job descriptions, and other identifying fields have been modified or anonymized. No proprietary, sensitive, or company-specific information is included in this dataset.

The final dataset contains 17,879 job postings with 19 original columns, including information on the location of the job, hiring company's profile, salaray range, and more.
Through feature engineering, we included additional metrics: 

- median salary, location segmentation
- length of job description/requirements/benefits/company profile
- minimum salary.
  
We also included target column called 'Fraudulent'. In total, we have 27 columns with models trained on 26 features.
The goal is to add binary values to the target column by assigning probabilities to each binary value. Therefore, we can identify fraudulent job postings.

## Approach

First, we setup a Snowflake warehouse. We configure the Snowflake environment, ingest job posting and earnings data from S3, join datasets to enrich features, and set up secure Dataiku integration for downstream modeling and analysis. 
Finally, we configure roles, permissions, and stages to securely enable Dataiku access, allowing seamless integration between Snowflake and Dataiku for feature engineering, model training, and evaluation.

<img width="668" height="89" alt="image" src="https://github.com/user-attachments/assets/172ba1dc-be3c-45e8-b451-4fe751a7d0f9" />

To achieve our goal, we perform feature engineering to enrich the dataset with additional predictive signals. We then evaluate multiple classification algorithms using Dataiku’s built-in modeling framework.

A total of 9 models are trained and compared. This model selection strategy is intentional: because fraudulent job postings represent a small minority of the dataset, overall accuracy alone is not a reliable evaluation metric. 
Most models achieve high accuracy simply by predicting the majority class.

Therefore, models are compared across multiple evaluation metrics to better understand their trade-offs, including how they balance false positives and false negatives. This approach enables more informed model selection and supports deployment decisions based on real-world business priorities rather than accuracy alone.

Due to computational constraints, models will initially be trained using an 80:20 train–test split. Based on performance, the best model will be selected for retraining using cross-validation. The results will be used for extracting important features in fraudulent job posting detection.

![](https://github.com/sm9801/Fraudulent_Job_Postings_Classification/blob/master/Model%20Metrics/Data%20Flow.png)

## Evaluation

- Train Evaluation
  
<img title="Train Evaluation" width="2000" height="2000" alt="image" src="https://github.com/sm9801/Fraudulent_Job_Postings_Classification/blob/master/Model%20Metrics/Train%20Summary.png" />

As expected, all models achieve high accuracy scores. Therefore, we focus on recall, precision, and F1-score, as these metrics better capture performance on fraudulent job postings, which are the primary target of this project.
Although the Decision Tree model scored the highest in terms of recall, the trade-offs in precision and F1-score were far too significant to select Decision Tree.
Based on precision, we choose LightGBM, XGBoost, and SVM models for validation.

- Test Validation

<img title="Train Evaluation" width="3000" height="3000" alt="image" src="https://github.com/sm9801/Fraudulent_Job_Postings_Classification/blob/master/Model%20Metrics/Test%20Summary.png" />

| Performance | XGBoost | LightGBM | SVM | 
|---|---|---|---|
| ROC AUC | 0.974 | 0.976 | 0.962 | 
| Accuracy | 0.951 | 0.959 | 0.951 |
| Precision | 0.929 | 0.971 | 0.938 |
| Recall | 0.534 | 0.589 | 0.525 | 
| F1-score | 0.678 | 0.733 | 0.673 |
| Cost Matrix Gain | 0.050 | 0.056 | 0.049 | 
| Lift | 2.478 | 2.456 | 2.427 | 
| Average Precision | 0.859 | 0.891 | 0.847 |
| Log Loss | 0.141 | 0.102 | 0.134 | 
| Calibration Loss | 0.052 | 0.015 | 0.030 |

On all metrics, LightGBM performs considerably better than XGBoost or SVM. This can be attributed to LightGBM's effectiveness in supervised learning, particularly in binary classification performance.
We select LightGBM for further analysis.

## Results

- Feature Importance

![](https://github.com/sm9801/Fraudulent_Job_Postings_Classification/blob/master/Model%20Metrics/Feature%20Importance/CV%20LightGBM%20feature%20importance.png)

Based on our visualization, we identify company profile, presence of company logo, country, and industry to be the 4 most important features in determining fraudulent job postings, that accounts for more than 60% of feature importance.

## Future Improvements

Future work will focus on improving model robustness through systematic stress testing, hyperparameter optimization, and cost-sensitive learning to better address class imbalance. 
Stress tests will help uncover model weaknesses and guide targeted performance improvements, while hyperparameter tuning is expected to improve true positive rates, conducted cautiously due to computational constraints. Cost-sensitive learning will further enhance performance on rare and edge-case fraudulent postings.

In the longer term, integrating real-time data ingestion and model monitoring will enable continuous evaluation and production deployment. Additionally, exploring transformer-based or LLM-driven models may improve generalization by better capturing the complex language patterns inherent in job postings.









