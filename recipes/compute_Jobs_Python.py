# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
import dataiku
from snowflake.snowpark.functions import *
from dataiku.snowpark import DkuSnowpark

# Create the DSS wrapper around Snowpark
dku_snowpark = DkuSnowpark()

# Read inputs
input_dataset = dataiku.Dataset("JOBS_POSTINGS_JOINED_prepared")
input_dataset_df = dku_snowpark.get_dataframe(input_dataset)

#strip minimum salary from the given range
output_dataset_df = input_dataset_df.withColumn('"MIN_SALARY"', split(col('"SALARY_RANGE"'), lit('-'))[0])

# Write outputs
output_dataset = dataiku.Dataset("Jobs_Python")
dku_snowpark.write_with_schema(output_dataset, output_dataset_df)
