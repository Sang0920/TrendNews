import re
import pandas as pd
from GoogleNews import GoogleNews
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from pyvi import ViTokenizer


def remove_string_special_characters(s):
    if s is not None:
        stripped = re.sub('\s+', ' ', s)
        stripped = stripped.strip()
        if stripped != '':
            pattern = r"[^\w\s]"
            return re.sub(pattern, '', stripped).lower()
    return '' 

def news_keyword_extractor(algo="TF-IDF", lang="en", region="US", topic="CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB", period=1, min_ngram=5, max_ngram=5):
  googlenews = GoogleNews(period=f"{period}d", lang=lang, region=region)
  googlenews.set_topic(topic)
  googlenews.get_news()
  results = googlenews.result()
  df = pd.DataFrame(results)

  df['title'].astype('string')
  txt = df['title'].to_numpy()

  if lang == "en":
    stop_words = set(stopwords.words('english'))
    for i, line in enumerate(txt):
        tokens = line.split()
        tokens = [remove_string_special_characters(token) for token in tokens if token.lower() not in stop_words]
        txt[i] = ' '.join(tokens)

  if lang == "vi":
    stop_words = set()
    with open('./vietnamese-stopwords.txt', encoding='utf-8') as stopwords_file:
        stop_words.update(stopwords_file.read().splitlines())
    for i, line in enumerate(txt):
        txt[i] = ' '.join([remove_string_special_characters(token) for token in ViTokenizer.tokenize(line).split() if token not in stop_words])

  if algo == "TF-IDF":
    vectorizer = TfidfVectorizer(ngram_range=(min_ngram, max_ngram))
    X2 = vectorizer.fit_transform(txt)
    scores = X2.toarray()

    sums = X2.sum(axis=0)
    data1 = []
    features = vectorizer.get_feature_names_out()
    for col, term in enumerate(features):
        data1.append((term, sums[0, col]))
    ranking = pd.DataFrame(data1, columns=['term', 'rank'])
    words = ranking.sort_values('rank', ascending=False)
    print("\n\nWords head: \n", words.head(15))
    return words.head(15)

  if algo == "LDA":
    vectorizer = CountVectorizer(ngram_range=(min_ngram, max_ngram))
    X2 = vectorizer.fit_transform(txt)
    lda = LatentDirichletAllocation(n_components=5, random_state=42)
    lda.fit(X2)
    topics = lda.components_
    features = vectorizer.get_feature_names_out()
    def display_topics(model, feature_names, no_top_words):
        topic_dict = {}
        for topic_idx, topic in enumerate(model.components_):
            top_features_ind = topic.argsort()[-no_top_words:][::-1]
            top_features = [feature_names[i] for i in top_features_ind]
            topic_dict[f'Topic {topic_idx}'] = top_features
        return topic_dict
    no_top_words = 15
    topic_words = display_topics(lda, features, no_top_words)
    topics_df = pd.DataFrame(topic_words)
    return topics_df