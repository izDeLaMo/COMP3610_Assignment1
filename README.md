# 🚕 NYC Taxi Trip Dashboard

An interactive Streamlit dashboard that explores NYC Yellow Taxi trip data. The dashboard provides key metrics, interactive visualizations, and insights into trip patterns, fares, payment types, and demand trends.

---

## 🌐 Live Dashboard

Deployed App URL:  
👉 https://your-streamlit-app-url-here.streamlit.app  

*(Replace this with your actual Streamlit Community Cloud URL before submission.)*

---

## 📊 Features

- Key performance metrics (Total Trips, Average Fare, Revenue, Distance, Duration)
- Top 10 Pickup Zones
- Average Fare by Hour
- Trip Distance Distribution (Histogram)
- Payment Type Breakdown
- Trips by Day of Week and Hour (Grouped Bar Chart)
- Interactive sidebar filters:
  - Date range
  - Hour range
  - Payment type

---

## 🗂 Dataset

Data Sources:
- NYC Yellow Taxi Trip Data (January 2024)
- Taxi Zone Lookup Table

Data is loaded directly from official NYC TLC public datasets via public URLs.  
No data files are stored in this repository.

---

## 📁 Repository Structure

assignment1.ipynb      # Parts 1, 2, and visualization prototypes  
app.py                 # Streamlit dashboard application  
requirements.txt       # Project dependencies  
README.md              # Project documentation  
.gitignore             # Ignored files  

---

## ⚙️ Installation & Setup Instructions

### 1️⃣ Clone the Repository

git clone https://github.com/your-username/your-repository-name.git  
cd your-repository-name  

### 2️⃣ Create a Virtual Environment (Recommended)

Mac/Linux:
python -m venv venv  
source venv/bin/activate  

Windows:
python -m venv venv  
venv\Scripts\activate  

### 3️⃣ Install Dependencies

pip install -r requirements.txt  

If needed, install manually:
pip install streamlit pandas numpy plotly pyarrow  

### 4️⃣ Run the Streamlit App

streamlit run app.py  

The dashboard will open in your browser at:  
http://localhost:8501  

