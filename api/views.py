# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import json
from rest_framework.permissions import IsAuthenticated 
from .serializers import YourDataSerializer  
from statsmodels.tsa.arima.model import ARIMA
import os


class PredictCategory(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Handle both JSON and form data
            if request.content_type == 'application/json':
                user_input = request.data.get('description', '')
            else:
                user_input = request.data.get('description', '')
            
            if not user_input or not user_input.strip():
                return Response(
                    {'error': 'Description is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Load dataset
            dataset_path = 'dataset.csv'
            if not os.path.exists(dataset_path):
                return Response(
                    {'error': 'Dataset file not found'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            data = pd.read_csv(dataset_path)
            
            # Check if dataset has required columns
            if 'clean_description' not in data.columns or 'category' not in data.columns:
                return Response(
                    {'error': 'Invalid dataset format'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Train model
            tfidf_vectorizer = TfidfVectorizer()
            X = tfidf_vectorizer.fit_transform(data['clean_description'])
            model = RandomForestClassifier(random_state=42, n_estimators=100)
            model.fit(X, data['category'])
            
            # Preprocess user input
            user_input_clean = preprocess_text(user_input)
            user_input_vector = tfidf_vectorizer.transform([user_input_clean])
            
            # Find closest match using cosine similarity
            similarities = cosine_similarity(user_input_vector, X)
            closest_match_index = similarities.argmax()
            
            # Predict category
            predicted_category = model.predict(user_input_vector)
            
            return Response({
                'predicted_category': predicted_category[0],
                'confidence': float(similarities[0][closest_match_index])
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Prediction failed: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class UpdateDataset(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
       new_data = request.data.get('new_data')

       if 'description' in new_data and 'category' in new_data:
            # Load your existing dataset
            data = pd.read_csv('dataset.csv')  # Load the existing dataset
            new_category = new_data['category']
            new_description = new_data['description']

            # Append the new data to the dataset
            new_row = {'description': new_description, 'category': new_category, 'clean_description': preprocess_text(new_description)}
            data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
            # Save the updated dataset
            data.to_csv('dataset.csv', index=False)
            
            tfidf_vectorizer = TfidfVectorizer()

            # Retrain the model with the updated dataset
            X = tfidf_vectorizer.transform(data['clean_description'])
            model.fit(X, data['category'])



def preprocess_text(text):
    try:
        # Ensure NLTK data is available
        try:
            stopwords.words('english')
        except LookupError:
            nltk.download('stopwords', quiet=True)
        
        try:
            word_tokenize("test")
        except LookupError:
            nltk.download('punkt', quiet=True)
            nltk.download('punkt_tab', quiet=True)
        
        stop_words = set(stopwords.words('english'))
        tokens = word_tokenize(text.lower())
        tokens = [t for t in tokens if t.isalnum() and t not in stop_words]
        return ' '.join(tokens) if tokens else text.lower()
    except Exception as e:
        # Fallback to simple preprocessing if NLTK fails
        return ' '.join([word.lower() for word in text.split() if word.isalnum()])
