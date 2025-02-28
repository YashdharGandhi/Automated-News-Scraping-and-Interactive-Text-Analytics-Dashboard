#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install newspaper3k feedparser pandas matplotlib wordcloud dash')


# In[2]:


import newspaper
import feedparser
import pandas as pd
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

def scrape_news_from_feed(feed_url):
    articles = []
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        try:
            article = newspaper.Article(entry.link)
            article.download()
            article.parse()
            articles.append({
                'title': article.title,
                'author': article.authors,
                'publish_date': article.publish_date,
                'content': article.text
            })
        except Exception as e:
            print(f"Error processing article: {entry.link}\n{e}")
    return articles

# Define multiple RSS feeds
feeds = [
    'http://feeds.bbci.co.uk/news/rss.xml',
    'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
    'https://www.theguardian.com/uk/rss'
]

all_articles = []
for feed_url in feeds:
    print(f"Scraping from {feed_url}")
    all_articles.extend(scrape_news_from_feed(feed_url))

# Save to CSV in Downloads folder
if all_articles:
    df = pd.DataFrame(all_articles)
    downloads_path = "C:\\Users\\yashd\\Downloads"
    os.makedirs(downloads_path, exist_ok=True)
    file_path = os.path.join(downloads_path, "articles.csv")
    df.to_csv(file_path, index=False)
    print(f"Scraped data saved to {file_path}")

    # Generate Word Cloud
    text = ' '.join(df['content'].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(os.path.join(downloads_path, "wordcloud.png"))
    print("Word Cloud saved as wordcloud.png")

    # Dashboard with Dash
    app = dash.Dash(__name__)
    app.layout = html.Div([
        html.H1("News Scraper Dashboard"),
        html.Img(src="wordcloud.png", style={"width": "80%"}),
        dcc.Graph(
            id='news-trend',
            figure={
                'data': [
                    {
                        'x': df['publish_date'].dropna(),
                        'y': df.groupby('publish_date').size(),
                        'type': 'bar',
                        'name': 'News Count'
                    }
                ],
                'layout': {
                    'title': 'Number of Articles Published Over Time'
                }
            }
        )
    ])
    
    if __name__ == '__main__':
        app.run_server(debug=True)


# In[ ]:




