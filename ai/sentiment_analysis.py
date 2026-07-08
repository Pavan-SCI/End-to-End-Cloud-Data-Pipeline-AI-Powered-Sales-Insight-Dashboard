import pandas as pd
from textblob import TextBlob
from etl.logger import setup_logger
from etl.config import config
import os

logger = setup_logger(__name__)

# Try importing OpenAI, but handle if it's not configured
try:
    from openai import OpenAI
    has_openai = True
except ImportError:
    has_openai = False

def analyze_sentiment_textblob(text: str) -> tuple:
    """Mode 1: Uses TextBlob for local, free sentiment analysis."""
    if pd.isna(text) or not text.strip():
        return 'Neutral', 0.0
    
    analysis = TextBlob(str(text))
    polarity = analysis.sentiment.polarity
    
    if polarity > 0.1:
        label = 'Positive'
    elif polarity < -0.1:
        label = 'Negative'
    else:
        label = 'Neutral'
        
    return label, polarity

def apply_sentiment_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies AI sentiment analysis to the ReviewText column.
    Defaults to TextBlob (Mode 1).
    """
    logger.info("Starting AI Sentiment Analysis Enrichment...")
    
    if 'ReviewText' not in df.columns:
        logger.warning("No 'ReviewText' column found. Skipping sentiment analysis.")
        return df

    # We will use TextBlob (Mode 1) for the pipeline to ensure it runs without paid API keys
    # To use OpenAI (Mode 2), one would check if config.OPENAI_API_KEY exists
    
    sentiments = df['ReviewText'].apply(analyze_sentiment_textblob)
    df['SentimentLabel'] = [s[0] for s in sentiments]
    df['SentimentPolarity'] = [s[1] for s in sentiments]
    
    logger.info("AI Sentiment Analysis completed.")
    
    return df

def generate_ai_executive_summary(df: pd.DataFrame) -> str:
    """
    Mode 2: Uses OpenAI API to generate a qualitative executive summary.
    This is an optional function for advanced AI integration.
    """
    if not has_openai or not config.OPENAI_API_KEY:
        logger.warning("OpenAI API key missing or package not installed. Skipping Mode 2.")
        return "OpenAI summary unavailable."
        
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    
    # Sample top positive and negative reviews to send as context
    positives = df[df['SentimentLabel'] == 'Positive']['ReviewText'].head(5).tolist()
    negatives = df[df['SentimentLabel'] == 'Negative']['ReviewText'].head(5).tolist()
    
    prompt = f"""
    You are a Data Analyst for a retail company. Based on recent customer reviews, provide a brief executive summary (max 3 sentences) of customer satisfaction, highlighting the main complaints and what they love.
    
    Positive Feedback Examples: {positives}
    Negative Feedback Examples: {negatives}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return "Error generating AI summary."
