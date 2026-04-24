🖥️ Crowd Intelligence Command Center
📌 Overview

This project is a real-time crowd monitoring and analytics system that estimates the number of people present at public locations and provides live insights, forecasts, and alerts.

It combines computer vision + simulated telecom data + predictive analytics to deliver a smart crowd intelligence dashboard.

🎯 Use Case

Designed for monitoring crowd density at:

🚉 Railway Stations
✈️ Airports
🛍️ Shopping Malls
🏟️ Stadiums
🛣️ Streets & Public Areas
🚀 Key Features
👁️ Real-Time Crowd Detection
Uses AI-based video processing (YOLO model)
Detects and counts people from live/video feeds
📶 Telecom Data Simulation
Simulates mobile network-based crowd estimation
Combines with AI data for better accuracy
🔀 Data Fusion
Merges AI + telecom estimates for reliable crowd count
🔮 Prediction Engine
Forecasts crowd levels for upcoming time intervals
Displays trend indicators (↑ ↓ →)
🚨 Smart Alerts
Predicts overcrowding before it happens
Blinking NOC-style alerts for attention
🗺️ Heatmap Visualization
Displays crowd intensity geographically
Interactive map with location labels
🖥️ Command Center Dashboard
Dark-themed NOC-style UI
Multi-location monitoring in real time
🧠 Architecture (Simplified)
Video Feed → AI Detection → Crowd Count
                        ↓
                Telecom Simulation
                        ↓
                  Data Fusion
                        ↓
             Prediction + Alerts
                        ↓
                  Dashboard UI
📁 Project Structure
ai-crowd/
│
├── app.py               # Main dashboard
├── counter.py           # AI-based people detection
├── telecom.py           # Telecom estimation logic
├── prediction.py        # Forecasting engine
├── yolov8n.pt           # YOLO model
├── requirements.txt     # Dependencies
└── videos/
    ├── station.mp4
    ├── park.mp4
    └── mall.mp4
⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/your-username/ai-crowd-dashboard.git
cd ai-crowd-dashboard
2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Run the app
streamlit run app.py
🌐 Deployment

You can deploy this app using:

Streamlit Community Cloud (recommended for quick demo)
Amazon Web Services (for production)
⚠️ Notes
This project uses simulation for telecom data (not real operator data)
Video feeds are sample/demo videos
Performance may vary based on system resources
🔮 Future Enhancements
Live CCTV integration
Real telecom data APIs
Mobile app integration
Alert notification system (SMS / Email)
Historical analytics dashboard
💡 Demo Statement

This system provides real-time and predictive crowd intelligence using AI, network-based estimation, and geospatial visualization for proactive decision-making.

👨‍💻 Author

Vinay Tyagi
General Manager – Reliance Jio

⭐ If you like this project

Give it a ⭐ on GitHub and share your feedback!