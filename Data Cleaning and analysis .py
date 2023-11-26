#!/usr/bin/env python
# coding: utf-8

# # Import and Read Data

# In[10]:


import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
plt.style.use('ggplot')
pd.options.display.max_rows = 200


# In[11]:


df = pd.read_csv (r'C:\Users\Acer\Desktop\data analyst\Portfolio Projects\Project 4\Dataset\coaster_db.csv')


# # Data understanding

# In[12]:


df.shape


# In[16]:


df.head()


# In[17]:


df.columns


# In[19]:


df.dtypes


# In[20]:


df.describe()


# # Data Preparation

# In[ ]:


# Example of dropping columns
# df.drop(['Opening date'], axis=1)


# In[32]:


df = df[['coaster_name',
    # 'Length', 'Speed',
    'Location', 'Status',
    # 'Opening date',
    #   'Type',
    'Manufacturer',
#     'Height restriction', 'Model', 'Height',
#        'Inversions', 'Lift/launch system', 'Cost', 'Trains', 'Park section',
#        'Duration', 'Capacity', 'G-force', 'Designer', 'Max vertical angle',
#        'Drop', 'Soft opening date', 'Fast Lane available', 'Replaced',
#        'Track layout', 'Fastrack available', 'Soft opening date.1',
#        'Closing date',
#     'Opened', 
    # 'Replaced by', 'Website',
#        'Flash Pass Available', 'Must transfer from wheelchair', 'Theme',
#        'Single rider line available', 'Restraint Style',
#        'Flash Pass available', 'Acceleration', 'Restraints', 'Name',
       'year_introduced',
        'latitude', 'longitude',
    'Type_Main',
       'opening_date_clean',
    #'speed1', 'speed2', 'speed1_value', 'speed1_unit',
       'speed_mph', 
    #'height_value', 'height_unit',
    'height_ft',
       'Inversions_clean', 'Gforce_clean']].copy()


# In[34]:


df.shape


# In[33]:


#change data type of column (object to datetime)
df['opening_date_clean'] = pd.to_datetime(df['opening_date_clean'])


# In[35]:


# Renamecolumns
df = df.rename(columns={'coaster_name':'Coaster_Name',
                   'year_introduced':'Year_Introduced',
                   'opening_date_clean':'Opening_Date',
                   'speed_mph':'Speed_mph',
                   'height_ft':'Height_ft',
                   'Inversions_clean':'Inversions',
                   'Gforce_clean':'Gforce'})


# In[38]:


df.isna().sum()


# In[39]:


df.loc[df.duplicated()]


# In[40]:


# Check for duplicate coaster name
df.loc[df.duplicated(subset=['Coaster_Name'])].head(5)


# In[41]:


# Checking an example duplicate
df.query('Coaster_Name == "Crystal Beach Cyclone"')


# In[42]:


df.columns


# In[43]:


df = df.loc[~df.duplicated(subset=['Coaster_Name','Location','Opening_Date'])] \
    .reset_index(drop=True).copy()


# In[44]:


df.shape


# # Feature Understanding

# In[45]:


#(Unvariate analysis)
#Plotting  Feature distribution
# - Histogram
# - KDE
# - Boxplot


# In[50]:


df['Year_Introduced'].value_counts().head(10)


# In[49]:


ax = df['Year_Introduced'].value_counts() \
    .head(10) \
    .plot(kind='bar', title='Top 10 Years Coasters Introduced')
ax.set_xlabel('Year Introduced')
ax.set_ylabel('Count')


# In[51]:


ax = df['Speed_mph'].plot(kind='hist',
                          bins=20,
                          title='Coaster Speed (mph)')
ax.set_xlabel('Speed (mph)')


# In[52]:


ax = df['Speed_mph'].plot(kind='kde',
                          title='Coaster Speed (mph)')
ax.set_xlabel('Speed (mph)')


# In[53]:


df['Type_Main'].value_counts()


# # Feature Relationships

# In[ ]:


#scatterplot
#Heatmap Corellation
#Pairplot
#GroupBY Comparison


# In[54]:


df.plot(kind='scatter',
        x='Speed_mph',
        y='Height_ft',
        title='Coaster Speed vs. Height')
plt.show()


# In[55]:


ax = sns.scatterplot(x='Speed_mph',
                y='Height_ft',
                hue='Year_Introduced',
                data=df)
ax.set_title('Coaster Speed vs. Height')
plt.show()


# In[58]:


sns.pairplot(df,
             vars=['Year_Introduced','Speed_mph',
                   'Height_ft','Inversions','Gforce'],
            hue='Type_Main')
plt.show()


# In[59]:


df_corr = df[['Year_Introduced','Speed_mph',
    'Height_ft','Inversions','Gforce']].dropna().corr()
df_corr


# In[60]:


sns.heatmap(df_corr, annot=True)


# # Question about the data

# In[ ]:


#Example
#What are the locations with the fastest roller coasters (minimum of 10)?


# In[61]:


ax = df.query('Location != "Other"') \
    .groupby('Location')['Speed_mph'] \
    .agg(['mean','count']) \
    .query('count >= 10') \
    .sort_values('mean')['mean'] \
    .plot(kind='barh', figsize=(12, 5), title='Average Coast Speed by Location')
ax.set_xlabel('Average Coaster Speed')
plt.show()

