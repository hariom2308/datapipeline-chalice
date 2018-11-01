# datapipeline-chalice
Chalice project for an ETL process used for preparing reports.

It is often required that data engineering team has to handle small scope ETL processes, tailored with respect to the stakeholder requests. We have found it practical to use Python libraries to process the data and upload the data chunks to an S3 bucket. 

In this exercise, a similar reporting process will be reenacted. The revenue reports from Android platform sales require some pre-processing before being handed over to Accounting. 

Tasks

1. Remove all the transactions that were not handled in Euros. (Use Buyer Currency)
2. Use only the columns "Description", "Transaction Type", "Merchant Currency", "Buyer Currency", "Buyer Country", "Amount (Buyer Currency)", "Amount (Merchant Currency)"
3. Rename the columns as following : 
  Amount (Buyer Currency) = Buyer Amount
  Amount (Merchant Currency) = Merchant Amount
4. Establish an SQL connection to Analyst and retrieve the Registration dates of the customers.
5. For each customer calculate a "Google Fee" and add it as a new column. The calculation will be held as follows:
  For customers who registered before 01.01.2018, the fee would be 20% of Merchant Amount.
  For customers who registered after 01.01.2018, Google will charge a fee of 10% of Merchant Amount.
6. Upload results to S3 as a csv file. 
7. Deploy the project using chalice.
