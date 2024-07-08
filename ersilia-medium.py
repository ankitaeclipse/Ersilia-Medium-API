# Import libraries
import os
import pandas as pd
from medium_api import Medium # pip install medium-api
from datetime import datetime

# Get RAPIDAPI_KEY from the environment
api_key = os.getenv('RAPIDAPI_KEY', 'your_default_api_key')  # Replace 'your_default_api_key' with your actual API key if needed

# Create a `Medium` Object
medium = Medium(api_key)

# Get the `Publication` Object using "publication_slug"
publication_slug = "ersiliaio"
publication = medium.publication(publication_slug=publication_slug)
num_followers = publication.followers

# Get editor IDs and count
editors = [editor._id for editor in publication.editors]
num_editors = len(editors)

# Editor details
editor_names = []
editor_follower_count = []
editor_article_count = []
editor_ids = []

for editor in publication.editors:
    editor_names.append(editor.info['fullname'])
    editor_follower_count.append(editor.info['followers_count'])
    editor_article_count.append(len(editor.article_ids))
    editor_ids.append(editor.info['id'])

# Create author ID to name mapping
author_id_to_name = dict(zip(editor_ids, editor_names))

# Calculate the total publication article count
publication_article_count = sum(editor_article_count)

# Fetch publication articles published since the start
all_time_articles = publication.get_articles_between(
    _to=datetime(2021, 6, 1),
    _from=datetime.now()
)

# Initialize lists to store article details
article_title = []
article_claps = []
article_voters = []
article_tags = []
article_topics = []
article_published_at = []
author_ids = []
author_names = []
popularity = []

for article in all_time_articles:
    # Save article properties
    article_title.append(article.title or "NA")
    article_claps.append(article.claps if article.claps is not None else "NA")
    article_voters.append(article.voters if article.voters is not None else "NA")
    article_tags.append(article.tags or "NA")
    article_topics.append(article.topics or "NA")
    
    # Extract and save only the date part of the published time
    published_date = article.info['published_at'].split(' ')[0] if 'published_at' in article.info else "NA"
    article_published_at.append(published_date)
    
    # Save the author ID and corresponding author name
    author_id = article.info.get('author', "NA")
    author_ids.append(author_id)
    author_names.append(author_id_to_name.get(author_id, "Unknown"))

    # Calculate popularity
    popularity_num = 50 * article.voters + article.claps if article.voters is not None and article.claps is not None else "NA"
    popularity.append(popularity_num)

# Create dataframes
publication_data = {
    'publication_slug': [publication_slug],
    'num_followers': [num_followers],
    'num_editors': [num_editors],
    'publication_article_count': [publication_article_count]
}

editors_data = {
    'editor_id': editor_ids,
    'editor_name': editor_names,
    'editor_follower_count': editor_follower_count,
    'editor_article_count': editor_article_count
}

articles_data = {
    'article_title': article_title,
    'article_claps': article_claps,
    'article_voters': article_voters,
    'article_tags': article_tags,
    'article_topics': article_topics,
    'article_published_at': article_published_at,
    'author_id': author_ids,
    'author_name': author_names,
    'popularity': popularity
}

# Replace empty strings with 'NA' and create DataFrames
publication_df = pd.DataFrame(publication_data).replace('', 'NA')
editors_df = pd.DataFrame(editors_data).replace('', 'NA')
articles_df = pd.DataFrame(articles_data).replace('', 'NA')

# Display the DataFrames (optional)
print(publication_df)
print(editors_df)
print(articles_df)

publication_df.to_csv('Ersilia Datatables Medium Publication.csv', index=False)
editors_df.to_csv('Ersilia Datatables Medium Editors.csv', index=False)
articles_df.to_csv('Ersilia Datatables Medium Articles.csv', index=False)