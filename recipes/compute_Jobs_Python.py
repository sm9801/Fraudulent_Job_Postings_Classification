

from dataiku.snowpark import DkuSnowpark

# Create the DSS wrapper around Snowpark
dku_snowpark = DkuSnowpark()

# Read inputs
input_dataset = dataiku.Dataset("JOBS_POSTINGS_JOINED_prepared")
input_dataset_df = dku_snowpark.get_dataframe(input_dataset)

# TODO: Replace this part by your actual code that computes the output, as a Snowpark dataframe
# For this sample code, simply copy input to output
output_dataset_df = input_dataset_df

# Write outputs
output_dataset = dataiku.Dataset("Jobs_Python")
dku_snowpark.write_with_schema(output_dataset, output_dataset_df)



