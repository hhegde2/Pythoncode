#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os


# In[7]:


source_df_name = input("Enter the name of the source csv: ")


# In[8]:


lookup_df_name = input("Enter the name of the lookup csv: ")


# In[10]:


source_df = pd.read_csv(source_df_name, error_bad_lines=False)
lookup_df = pd.read_csv(lookup_df_name, error_bad_lines=False)


# In[14]:


source_df_column = input("Enter the name of the column with the ID values in the source CSV: ")
lookup_df_column = input("Enter the name of the column with the ID values in the lookup CSV: ")


# In[15]:


lookup_ids = list(source_df[source_df_column].values)


# In[23]:


missing_ids = ""
missing_id_count = 0
out_count = 0

for lookup_id in lookup_ids:
    filtered_df = lookup_df[lookup_df[lookup_df_column] == lookup_id]
    
    # Case 1: Missing ID
    if(len(filtered_df) == 0):
        missing_ids += str(lookup_id) + "\n"
        missing_id_count += 1
    
    # Case 2: Filtering
    else:
        out_count += 1
        filtered_df.fillna("").to_csv("./out_csvs/output_" + str(out_count) + "_lookup.csv", index=False)
        (source_df[source_df[source_df_column] == lookup_id]).fillna("").to_csv("./out_csvs/output_" + str(out_count) + "_source.csv", index=False)


# In[24]:


with open('missing_ids.txt', 'w') as out_missing_ids:
    out_missing_ids.write(missing_ids)


# In[25]:


print('number of missing IDs in lookup: ' + str(missing_id_count))


# In[ ]:




