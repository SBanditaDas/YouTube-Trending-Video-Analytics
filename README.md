# YouTube Trending Video Analytics & Recommendation

## Objective
_Analyze YouTube trending video datasets across multiple countries to uncover patterns in genre popularity, viewer sentiment, and regional content dynamics. This project combines data cleaning, sentiment analysis, SQL insights, and dashboard storytelling to deliver actionable insights for content creators and marketers._

Furthermore, this repository includes a **Content-Based Recommendation System** that analyzes video titles and tags to suggest similar trending content.

---

## Tools & Technologies
- **Python**: Data preprocessing, NLP sentiment analysis (TextBlob), Machine Learning (Scikit-Learn TF-IDF & Cosine Similarity), Data Handling (Pandas, Numpy)
- **SQL**: Category-level ranking and aggregation
- **Tableau**: Interactive dashboards and region-wise comparisons

---

## Workflow Overview

### 1. Data Cleaning & Standardization (`scripts/preprocess.py`)
- Unifies schema across country-specific Kaggle datasets
- Removes duplicates, handles missing values, normalizes timestamps

### 2. Sentiment Analysis (`scripts/sentiment_analysis.py`)
- NLP-based polarity and subjectivity scoring on video titles and tags using TextBlob
- Prepares data for visualizing sentiment distribution

### 3. Recommendation System (`scripts/recommend.py`)
- Content-based filtering using Term Frequency-Inverse Document Frequency (TF-IDF)
- Calculates Cosine Similarity across video titles, tags, and descriptions to recommend the top 5 most similar videos

### 4. SQL Insights (`notebooks/category_ranking.sql`)
- Ranks video categories by average views, likes, and highest engagement rates

---

## Repository Structure
```
├── data/
│   ├── raw/                 <- Place your raw CSVs here (e.g., USvideos.csv)
│   └── cleaned/             <- Preprocessed and sentiment-analyzed data
├── scripts/
│   ├── preprocess.py        <- Data cleaning script
│   ├── sentiment_analysis.py<- NLP sentiment scoring
│   └── recommend.py         <- TF-IDF recommendation engine
├── notebooks/
│   └── category_ranking.sql <- Category analysis queries
├── requirements.txt         <- Python dependencies
└── README.md
```

---

## How to Run

1. **Clone the repository**  
   `git clone https://github.com/SBanditaDas/YouTube-Trending-Video-Analytics.git`
   `cd YouTube-Trending-Video-Analytics`

2. **Install dependencies**  
   `pip install -r requirements.txt`

3. **Add Data**
   Download the YouTube Trending Dataset from Kaggle and place the `.csv` files into the `data/raw/` directory.

4. **Run preprocessing scripts**  
   `python scripts/preprocess.py` (Cleans and merges datasets into `data/cleaned/cleaned_youtube_data.csv`)

5. **Execute sentiment analysis**  
   `python scripts/sentiment_analysis.py` (Generates sentiment scores into `data/cleaned/sentiment_youtube_data.csv`)

6. **Run the Recommendation Engine**  
   `python scripts/recommend.py --video "Your Video Title Here" --top_n 5`

7. **Run SQL queries**  
   Load the cleaned CSV into your SQL database and run queries from `notebooks/category_ranking.sql`.
