# Databricks notebook source
# MAGIC %sql
# MAGIC select *
# MAGIC from read_files('/Volumes//idp/default/final_project')

# COMMAND ----------

# MAGIC %sql
# MAGIC create or replace table parsed_data as 
# MAGIC select path,
# MAGIC ai_parse_document(content) as parsed_content
# MAGIC from read_files('/Volumes//idp/default/final_project')

# COMMAND ----------

# MAGIC %sql
# MAGIC create or replace table pretty_table as 
# MAGIC select path,
# MAGIC   concat_ws('\n', 
# MAGIC     transform(
# MAGIC       try_cast(parsed_content:document:elements as array<variant>), 
# MAGIC       e -> coalesce(try_cast(e:content as string), '')
# MAGIC     )
# MAGIC   ) as doc_text
# MAGIC from parsed_data

# COMMAND ----------

# MAGIC %sql
# MAGIC create or replace table classified_data as 
# MAGIC select *, 
# MAGIC ai_classify(doc_text, array('Invoice', 'Purchase Order', 'Receipt', 'Other')) as doc_classification
# MAGIC from pretty_table 
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC create or replace table invoice_data as 
# MAGIC select *, 
# MAGIC   ai_extract(
# MAGIC     doc_text, 
# MAGIC     array('Vender_Name', 'Invoice_Number', 'Invoice_Date', 'Due_Date', 'Payment_Method', 'Total')
# MAGIC   ) as extracted
# MAGIC from classified_data
# MAGIC where doc_classification = 'Invoice'

# COMMAND ----------

# MAGIC %sql
# MAGIC create schema if not exists idp.finance

# COMMAND ----------

# MAGIC %sql
# MAGIC create or replace table idp.finance.invoices as
# MAGIC select path,
# MAGIC extracted.Vender_Name as Vender,
# MAGIC extracted.Invoice_Number as Invoice_Number,
# MAGIC extracted.Invoice_Date as Invoice_Date,
# MAGIC extracted.Due_Date as Due_Date,
# MAGIC extracted.Payment_Method as Payment_Method,
# MAGIC extracted.Total as Total
# MAGIC from invoice_data

# COMMAND ----------

# MAGIC %sql
# MAGIC select * 
# MAGIC from idp.finance.invoices

# COMMAND ----------

# MAGIC %sql
# MAGIC create or replace table purchase_order_data as 
# MAGIC select *, 
# MAGIC   ai_extract(
# MAGIC     doc_text, 
# MAGIC     array('Merchant_Name', 
# MAGIC           'PO_Number',
# MAGIC           'Purchase_Order_Date',
# MAGIC           'Total')
# MAGIC   ) as extracted
# MAGIC from classified_data
# MAGIC where doc_classification = 'Purchase Order'

# COMMAND ----------

# MAGIC %sql
# MAGIC create or replace table idp.finance.purchase_order as 
# MAGIC select path,
# MAGIC extracted.Merchant_Name as Merchant_Name,
# MAGIC extracted.PO_Number as PO_Number,
# MAGIC extracted.Purchase_Order_Date as Purchase_Order_Date,   
# MAGIC extracted.Total as Total
# MAGIC from purchase_order_data
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC create or replace table receipts as 
# MAGIC select *, 
# MAGIC   ai_extract(
# MAGIC     doc_text, 
# MAGIC     array('Merchant_Name', 
# MAGIC           'Receipt_Number',
# MAGIC           'Transaction_Date',
# MAGIC           'Total')
# MAGIC   ) as extracted
# MAGIC from classified_data
# MAGIC where doc_classification = 'Receipt'

# COMMAND ----------

# MAGIC %sql
# MAGIC create or replace table idp.finance.receipts as 
# MAGIC select path,
# MAGIC extracted.Merchant_Name as Merchant_Name,
# MAGIC extracted.Receipt_Number as Receipt_Number,
# MAGIC extracted.Transaction_Date as Transaction_Date,   
# MAGIC extracted.Total as Total
# MAGIC from receipts