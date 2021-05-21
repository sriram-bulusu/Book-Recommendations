#!/usr/bin/env python
# coding: utf-8

# ### Imports

# In[1]:


import numpy as np
import pandas as pd


# ### Load dataset

# In[2]:


df = pd.read_csv('book data.csv')
df.head()


# In[3]:


df.tail()


# In[4]:


df.drop(['Unnamed: 12'], axis=1, inplace=True)


# In[5]:


df.head()


# In[6]:


def combine(data):
    features = []
    for i in range(0, df.shape[0]):
        features.append( data['title'][i] + ' ' + data['authors'][i] + ' ' + data['publisher'][i] )
    return features


# In[7]:


df['Imp_Features'] = combine(df)


# In[8]:


df.drop(['isbn', 'isbn13', 'ratings_count', 'text_reviews_count', 'publication_date'], axis=1, inplace=True)


# In[9]:


index_names = df[ (df['language_code'] != 'eng') & (df['language_code'] != 'en-US')].index

df.drop(index_names, inplace=True)


# In[10]:


df.language_code.unique()


# In[11]:


df.drop_duplicates(subset='title', keep='first', inplace=True)


# In[12]:


df.reset_index(drop=True, inplace=True)


# In[13]:


df['bookID_idx'] = np.arange(len(df))


# In[14]:


df.head()


# In[15]:


df.tail()


# In[20]:


df.to_csv(r'./book_rec_data.csv', index=False)


# In[21]:


def get_data():
    book_data = pd.read_csv('book_rec_data.csv')
    book_data['title'] = book_data['title'].str.lower()
    
    return book_data


# In[17]:


from sklearn.feature_extraction.text import CountVectorizer as cv
from sklearn.metrics.pairwise import cosine_similarity as cs


# In[18]:


def transform_data(data):
    count_mat = cv().fit_transform(data['Imp_Features'])
    
    cos_sim_mat = cs(count_mat)

    return cos_sim_mat


# In[30]:


def recommender(btitle, data, transform):
    bID = data[data.title == btitle]['bookID_idx'].values[0]
    scores = list(enumerate(transform[bID]))
    
    sorted_scores = sorted(scores, key = lambda x:x[1], reverse=True)
    sorted_scores = sorted_scores[1:6]
    
    book_indices = [i[0] for i in sorted_scores]
    book_id = data['bookID'].iloc[book_indices]
    book_title = data['title'].iloc[book_indices]
    
    recommendation_data = pd.DataFrame(columns=['Book_ID', 'Title'])
    
    recommendation_data['Book_ID'] = book_id
    recommendation_data['Title'] = book_title
    
    return recommendation_data

            


# In[31]:


def results(title):
  
    find_title = get_data()
    transf_res = transform_data(find_title)
    
    if title not in find_title['title'].unique():
        return 'Book not in Database'
    else:
        recommendation = recommender(title, find_title, transf_res)
        return recommendation

        

