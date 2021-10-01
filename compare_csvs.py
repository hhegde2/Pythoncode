#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:

dev_sheet_name = input('Enter the path of the dev output csv: ')
expected_sheet_name = input('Enter the path of the expected csv: ')

dev_out_df = pd.read_csv(dev_sheet_name)
test_df = pd.read_csv(expected_sheet_name)


# In[3]:


primary_key_column = input("Enter the name of the primary key column: ") # "Name"


# In[4]:


dev_out_cols = list(dev_out_df.columns.values)
test_cols = list(test_df.columns.values)
try:
    dev_out_cols.remove('salesforce_id')
except:
    pass
    
try:
    dev_out_cols.remove('salesforce_created')
except:
    pass
dev_out_df = dev_out_df[dev_out_cols]


# In[5]:


n_dev_cols = len(dev_out_cols)
n_test_cols = len(test_cols)

missing_cols = []

if(n_dev_cols != n_test_cols):
    print("Missing columns count: " + str(n_test_cols - n_dev_cols))
    print("Missing columns: ")
    
    for column in test_cols:
        if column in dev_out_cols:
            continue
        else:
            missing_cols.append(column)
            print(column)
    
else:
    print("No columns missing")


# In[6]:


if(len(missing_cols) != 0):
    for missing_column in missing_cols:
        test_cols.remove(missing_column)
    test_df = test_df[test_cols]


# In[7]:


def generate_base_table_html(cols):
    html_str = "<table><tr>"
    
    for col in cols:
        html_str += "<th>" + col + "</th>"
    
    html_str += "</tr>"
    
    return html_str


# In[8]:


re_indexed_dev_out_df = dev_out_df.set_index(primary_key_column)
re_indexed_test_df = test_df.set_index(primary_key_column)


# In[9]:


missing_rows_df = pd.DataFrame(columns=test_cols)

mismatch_html = generate_base_table_html(cols=dev_out_cols)
mismatch_count = 0

for entry in list(re_indexed_test_df.index.values):
    test_entry = re_indexed_test_df.loc[entry]
    
    # Case 1: Missing Row
    try:
        dev_entry = re_indexed_dev_out_df.loc[entry]
    except:
        missing_rows_df.loc[len(missing_rows_df)] = list(test_df[test_df[primary_key_column] == entry].iloc[0])
        continue
        
    # Case 2: Checking mismatched row
    mismatches = test_entry.compare(dev_entry)
    
    if(len(mismatches) != 0):
        mismatched_columns = list(mismatches.index.values)
        
        mismatch_html += "<tr>"
        mismatch_html += "<td>" + str(entry) + "</td>"
        for col in re_indexed_dev_out_df.columns.values:
            if col in mismatched_columns:
                mismatch_html += '<td style="background-color: indianred;">'+ str(dev_entry[col]) +'</td>'
            else:
                mismatch_html += '<td>'+ str(dev_entry[col]) +'</td>'
        mismatch_html += "</tr>"
        mismatch_count += 1


# In[13]:


print("Number of rows in the dev output: " + str(len(dev_out_df)))
print("Number of missing rows in the dev output: " + str(len(missing_rows_df)))
print("Number of mismatched rows in the dev output: " + str(mismatch_count))


# In[14]:


if(mismatch_count != 0):
    with open("mismatches.html", "w") as out_html:
        out_html.write(mismatch_html)


# In[16]:


missing_rows_df.to_csv('./missing_rows.csv', index=False)


# In[ ]: