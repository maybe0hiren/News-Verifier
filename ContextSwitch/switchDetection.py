import pickle
import numpy as np
import re

class ContextSwitchDetector:
    def __init__(self, model_path='signal_media_context_model.pkl', feature_columns_path='signal_media_features.pkl'):
        try:
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            with open(feature_columns_path, 'rb') as f:
                self.feature_columns = pickle.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("Model files not found. Please train the model first.")

        self.topics = {
            'technology': ['technology', 'digital', 'computer', 'software', 'internet', 'smartphone', 'AI', 'tech'],
            'environment': ['environment', 'pollution', 'climate', 'green', 'sustainable', 'eco', 'carbon', 'nature'],
            'business': ['market', 'stock', 'economy', 'financial', 'business', 'corporate', 'investment', 'money'],
            'health': ['health', 'medical', 'hospital', 'disease', 'treatment', 'doctor', 'patient', 'medicine'],
            'sports': ['sport', 'team', 'game', 'player', 'championship', 'football', 'basketball', 'athletics'],
            'crime': ['crime', 'police', 'robbery', 'suspect', 'investigation', 'arrest', 'criminal', 'law'],
            'politics': ['government', 'political', 'election', 'policy', 'congress', 'senate', 'vote', 'democracy'],
            'entertainment': ['movie', 'music', 'actor', 'film', 'concert', 'show', 'celebrity', 'entertainment']
        }

    def extract_features(self, text):
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) < 2:
            return {
                'num_sentences': len(sentences), 
                'avg_sentence_length': 0,
                'avg_word_overlap': 1.0, 
                'min_word_overlap': 1.0,
                'topic_changes': 0, 
                'topic_change_ratio': 0.0
            }

        features = {}
        features['num_sentences'] = len(sentences)
        features['avg_sentence_length'] = np.mean([len(s.split()) for s in sentences])
        word_overlaps = []
        for i in range(len(sentences) - 1):
            words1 = set(sentences[i].lower().split())
            words2 = set(sentences[i+1].lower().split())
            overlap = len(words1.intersection(words2)) / max(len(words1.union(words2)), 1)
            word_overlaps.append(overlap)

        features['avg_word_overlap'] = np.mean(word_overlaps) if word_overlaps else 0
        features['min_word_overlap'] = np.min(word_overlaps) if word_overlaps else 0
        sentence_topics = []
        for sentence in sentences:
            sentence_lower = sentence.lower()
            sentence_topic_counts = {}

            for topic, keywords in self.topics.items():
                count = sum(1 for keyword in keywords if keyword in sentence_lower)
                sentence_topic_counts[topic] = count
            dominant_topic = max(sentence_topic_counts.items(), key=lambda x: x[1])
            sentence_topics.append(dominant_topic[0] if dominant_topic[1] > 0 else 'other')
        topic_changes = sum(1 for i in range(len(sentence_topics) - 1) 
                           if sentence_topics[i] != sentence_topics[i+1])

        features['topic_changes'] = topic_changes
        features['topic_change_ratio'] = topic_changes / max(len(sentences) - 1, 1)

        return features

    def predict(self, text):
        features = self.extract_features(text)
        feature_vector = np.array([[features[col] for col in self.feature_columns]])
        prediction = self.model.predict(feature_vector)[0]
        probability = self.model.predict_proba(feature_vector)[0]

        return {
            'has_context_switch': bool(prediction),
            'confidence': float(max(probability)),
            'probability_context_switch': float(probability[1]),
            'features': features
        }

    def analyze_text(self, text, verbose=True):
        result = self.predict(text)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if verbose:
            print(f"TEXT ANALYSIS:")
            print("=" * 50)
            print(f"Text: {text}")
            print(f"\nNumber of sentences: {len(sentences)}")
            for i, sentence in enumerate(sentences, 1):
                print(f"  {i}. {sentence}")

            print(f"\nCONTEXT SWITCH DETECTION:")
            print(f"Has Context Switch: {'YES' if result['has_context_switch'] else 'NO'}")
            print(f"Confidence: {result['confidence']:.3f}")
            print(f"Probability of Context Switch: {result['probability_context_switch']:.3f}")

            print(f"\nFEATURES:")
            for feature, value in result['features'].items():
                print(f"  {feature}: {value:.3f}")

        return result

# Example usage
if __name__ == "__main__":
    # Initialize detector
    detector = ContextSwitchDetector()

    # Test examples
    test_texts = [
        "The car explosion in downtown Miami injured three people. Air pollution is a major concern in cities worldwide.",
        "The football team won the championship. Players celebrated with their fans after the victory.",
        "Stock market indices reached new highs today. Technology companies led the market gains.",
        "Scientists discovered a new species in the rainforest. The research team published their findings."
    ]

    print("CONTEXT SWITCHING DETECTION EXAMPLES")
    print("=" * 60)

    for i, text in enumerate(test_texts, 1):
        print(f"\nEXAMPLE {i}:")
        result = detector.predict(text)
        print(f"Text: {text}")
        print(f"Context Switch: {'YES' if result['has_context_switch'] else 'NO'}")
        print(f"Confidence: {result['confidence']:.3f}")
