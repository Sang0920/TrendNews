import re
from GoogleNews import GoogleNews
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Simplified English stopwords list
ENGLISH_STOPWORDS = set([
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your",
    "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", 
    "her", "hers", "herself", "it", "its", "itself", "they", "them", "their",
    "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
    "these", "those", "am", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an",
    "the", "and", "but", "if", "or", "because", "as", "until", "while", "of",
    "at", "by", "for", "with", "about", "against", "between", "into", "through",
    "during", "before", "after", "above", "below", "to", "from", "up", "down",
    "in", "out", "on", "off", "over", "under", "again", "further", "then", 
    "once", "here", "there", "when", "where", "why", "how", "all", "any", 
    "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor",
    "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can",
    "will", "just", "don", "should", "now"
])

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
    
    titles = [remove_string_special_characters(article['title']) for article in results]

    if lang == "en":
        titles = [
            ' '.join([word for word in title.split() if word not in ENGLISH_STOPWORDS])
            for title in titles
        ]
    elif lang == "vi":
        with open('./vietnamese-stopwords.txt', encoding='utf-8') as stopwords_file:
            vietnamese_stopwords = set(stopwords_file.read().splitlines())
        titles = [
            ' '.join([remove_string_special_characters(word) for word in re.findall(r'\w+', title) if word not in vietnamese_stopwords])
            for title in titles
        ]

    if algo == "TF-IDF":
        vectorizer = TfidfVectorizer(ngram_range=(min_ngram, max_ngram))
        X2 = vectorizer.fit_transform(titles)
        sums = X2.sum(axis=0)
        features = vectorizer.get_feature_names_out()

        ranking = [(term, sums[0, col]) for col, term in enumerate(features)]
        words = sorted(ranking, key=lambda x: x[1], reverse=True)[:15]

        print("\n\nWords head: \n", words)
        return words

    if algo == "LDA":
        vectorizer = CountVectorizer(ngram_range=(min_ngram, max_ngram))
        X2 = vectorizer.fit_transform(titles)
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
        print("\n\nLDA Topics: \n", topic_words)
        return topic_words