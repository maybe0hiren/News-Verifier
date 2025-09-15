import json
import gzip
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import pickle
import re
from collections import Counter

class ContextSwitchTrainer:
    def __init__(self):
        self.topics = {
            'technology': ['technology', 'digital', 'computer', 'software', 'internet', 'smartphone', 'AI', 'tech'],
            'environment': ['environment', 'pollution', 'climate', 'green', 'sustainable', 'eco', 'carbon'],
            'business': ['market', 'stock', 'economy', 'financial', 'business', 'corporate', 'investment'],
            'health': ['health', 'medical', 'hospital', 'disease', 'treatment', 'doctor', 'patient'],
            'sports': ['sport', 'team', 'game', 'player', 'championship', 'football', 'basketball'],
            'crime': ['crime', 'police', 'robbery', 'suspect', 'investigation', 'arrest', 'criminal'],
            'politics': ['government', 'political', 'election', 'policy', 'congress', 'senate', 'vote'],
            'entertainment': ['movie', 'music', 'actor', 'film', 'concert', 'show', 'celebrity']
        }

    def load_signal_media_data(self, file_path, max_articles=10000):
        """Load and process Signal Media dataset"""
        articles = []

        with gzip.open(file_path, 'rt', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i >= max_articles:
                    break

                try:
                    data = json.loads(line)
                    content = data.get('content', '')

                    # Split content into paragraphs
                    paragraphs = [p.strip() for p in content.split('\n') if p.strip()]

                    # Process paragraphs that are long enough
                    for paragraph in paragraphs:
                        sentences = re.split(r'[.!?]+', paragraph)
                        sentences = [s.strip() for s in sentences if s.strip()]

                        if len(sentences) >= 2 and len(paragraph.split()) >= 15:
                            articles.append(paragraph)

                except Exception as e:
                    continue

                if i % 1000 == 0:
                    print(f"Processed {i} articles, collected {len(articles)} paragraphs")

        return articles

    def create_labels(self, articles):
        """Create labels for context switching based on heuristics"""
        labels = []

        for article in articles:
            features = self.extract_features(article)

            # Heuristic for context switching:
            # High topic change ratio + low word overlap = likely context switch
            has_context_switch = (
                features['topic_change_ratio'] > 0.3 and 
                features['avg_word_overlap'] < 0.1 and
                features['topic_changes'] > 0
            )

            labels.append(1 if has_context_switch else 0)

        return labels

    def extract_features(self, text):
        """Extract features for context switching detection"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) < 2:
            return {'num_sentences': len(sentences), 'avg_sentence_length': 0,
                   'avg_word_overlap': 1.0, 'min_word_overlap': 1.0,
                   'topic_changes': 0, 'topic_change_ratio': 0.0}

        # Basic features
        features = {}
        features['num_sentences'] = len(sentences)
        features['avg_sentence_length'] = np.mean([len(s.split()) for s in sentences])

        # Word overlap
        word_overlaps = []
        for i in range(len(sentences) - 1):
            words1 = set(sentences[i].lower().split())
            words2 = set(sentences[i+1].lower().split())
            overlap = len(words1.intersection(words2)) / max(len(words1.union(words2)), 1)
            word_overlaps.append(overlap)

        features['avg_word_overlap'] = np.mean(word_overlaps)
        features['min_word_overlap'] = np.min(word_overlaps)

        # Topic analysis
        sentence_topics = []
        for sentence in sentences:
            sentence_lower = sentence.lower()
            sentence_topic_counts = {}
            for topic, keywords in self.topics.items():
                count = sum(1 for keyword in keywords if keyword in sentence_lower)
                sentence_topic_counts[topic] = count

            dominant_topic = max(sentence_topic_counts.items(), key=lambda x: x[1])
            sentence_topics.append(dominant_topic[0] if dominant_topic[1] > 0 else 'other')

        # Topic changes
        topic_changes = sum(1 for i in range(len(sentence_topics) - 1)
                           if sentence_topics[i] != sentence_topics[i+1])
        features['topic_changes'] = topic_changes
        features['topic_change_ratio'] = topic_changes / max(len(sentences) - 1, 1)

        return features

    def train_model(self, dataset_path='ContextSwitch/signalmedia-1m.jsonl.gz'):
        """Train the context switching detection model"""
        print("Loading Signal Media dataset...")
        articles = self.load_signal_media_data(dataset_path)
        print(f"Loaded {len(articles)} articles")

        print("Creating labels...")
        labels = self.create_labels(articles)
        context_switch_count = sum(labels)
        print(f"Articles with context switches: {context_switch_count}")
        print(f"Articles without context switches: {len(labels) - context_switch_count}")

        print("Extracting features...")
        feature_dicts = [self.extract_features(article) for article in articles]
        feature_df = pd.DataFrame(feature_dicts)

        # Train model
        X = feature_df.values
        y = np.array(labels)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        print("Training Random Forest model...")
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Evaluate
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model accuracy: {accuracy:.3f}")
        print(classification_report(y_test, y_pred))

        # Save model
        with open('signal_media_context_model.pkl', 'wb') as f:
            pickle.dump(model, f)
        with open('signal_media_features.pkl', 'wb') as f:
            pickle.dump(list(feature_df.columns), f)

        print("Model saved successfully!")
        return model, feature_df.columns

if __name__ == "__main__":
    trainer = ContextSwitchTrainer()
    trainer.train_model()
