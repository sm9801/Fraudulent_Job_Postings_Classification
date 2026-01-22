# Fraudulent Job Postings Classification

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

We use a dataset gathered from multiple sources online streamed into a Snowflake warehouse. For privacy concerns, the data is redacted.
The final dataset contains 17,879 job postings with 19 original columns, including information on the location of the job, hiring company's profile, salaray range, and more.
Through feature engineering, we included additional metrics: 

- median salary, location segmentation
- length of job description/requirements/benefits/company profile
- minimum salary.
  
We also included target column called 'Fraudulent'. In total, we have 27 columns with models trained on 26 features.
The goal is to add binary values to the target column by assigning probabilities to each binary value. Therefore, we can identify fraudulent job postings.

## Approach

To achieve our goal, we first perform feature engineering to enrich the dataset with additional predictive signals. We then evaluate multiple classification algorithms using Dataiku’s built-in modeling framework.

A total of nine models are trained and compared. This model selection strategy is intentional: because fraudulent job postings represent a small minority of the dataset, overall accuracy alone is not a reliable evaluation metric. 
Most models achieve high accuracy simply by predicting the majority class.

Therefore, models are compared across multiple evaluation metrics to better understand their trade-offs, including how they balance false positives and false negatives. This approach enables more informed model selection and supports deployment decisions based on real-world business priorities rather than accuracy alone.

## Evaluation



