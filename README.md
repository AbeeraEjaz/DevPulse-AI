<div align="center">

# 🌐 DevPulse AI
### Socio-Economic Policy Simulator & HDI Forecasting Engine

[![Live Web Application](https://img.shields.io/badge/Streamlit%20App-Live%20Demo-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://devpulse-ai.streamlit.app/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/AbeeraEjaz/DevPulse-AI)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/abeera-ejaz-0b287a316)

<p align="center">
  <b>An AI-driven decision-support intelligence platform built on World Bank Open Datasets and UNDP Human Development Index (HDI) methodology.</b>
</p>

---

[🌐 Explore Live App](https://devpulse-ai.streamlit.app/) • [📊 Architecture](#-architecture--methodology) • [🚀 Key Features](#-key-features) • [🛠️ Tech Stack](#️-tech-stack) • [👩‍💻 Author](#-author)

</div>

---

## 📌 Executive Overview

**DevPulse AI** addresses a fundamental challenge in international development policy: *identifying and prioritizing interventions that yield the highest socio-economic returns.*

By ingesting verified indicators across **265+ countries and territories** over nearly two decades of historical data, the platform trains Explainable Machine Learning models (Random Forest & Gradient Boosting) to:
1. **Decode non-linear drivers** of national development (Education, Digital Access, Health, Energy).
2. **Simulate real-time policy interventions** through interactive "What-If" parametric forecasting.
3. **Generate downloadable, executive-grade Policy Briefs (PDF)** for multilateral organizations and stakeholders.

---

## 🚀 Key Features

* **🌍 Global Indicator ETL Pipeline:** Automated extraction and cleaning of World Bank development metrics covering 5,000+ verified country-year records.
* **📈 Standardized HDI Formulation:** Re-computes UNDP-aligned composite Human Development Index scores using geometric means across Health, Education, and Standard of Living proxies.
* **🎯 Explainable AI (XAI) Priority Ranking:** Mathematically reveals which sector investments (e.g., adult literacy vs. digital infrastructure) exert the highest leverage on human well-being.
* **🎛️ Parametric "What-If" Simulator:** Real-time sliders allowing researchers to tweak national targets and immediately forecast projected HDI tiers and GDP per capita growth ($).
* **📄 Automated Policy Brief Generator:** 1-click export of structured 1-page PDF diagnostic memos ready for stakeholder presentation.

---

## 🏗️ Architecture & Methodology
[ World Bank Open Data API ]
                            │
                            ▼
     [ Automated Data Pipeline (ETL & Imputation) ]
                            │
                            ▼
     [ Composite HDI Calculation (UNDP Methodology) ]
                            │
      ┌─────────────────────┴─────────────────────┐
      ▼                                           ▼
[ Random Forest Regressor ]              [ Gradient Boosting Regressor ]
(HDI Target: R² > 95%)                  (GDP Target: R² > 90%)
│                                           │
└─────────────────────┬─────────────────────┘
▼
[ Feature Importance Engine ]
│
▼
[ Streamlit Interactive UI + Real-time Intervention Engine ]
│
▼
[ Executive PDF Brief Generator (FPDF) ]

---

## 🛠️ Tech Stack

| Domain | Technologies & Libraries |
|---|---|
| **Frontend & UI** | Streamlit, HTML5/CSS3 (Custom UN Blue Theme) |
| **Data Visualizations** | Plotly Express, Plotly Graph Objects |
| **Data Engineering** | World Bank API (`wbgapi`), Pandas, NumPy |
| **Machine Learning** | Scikit-Learn (Random Forest, Gradient Boosting), Joblib |
| **Reporting & Export** | FPDF2 |
| **Cloud Deployment** | Streamlit Community Cloud, GitHub CI/CD |

---

## 💻 Local Installation & Setup

```bash
# 1. Clone the repository
git clone [https://github.com/AbeeraEjaz/DevPulse-AI.git](https://github.com/AbeeraEjaz/DevPulse-AI.git)
cd DevPulse-AI

# 2. Create and activate a virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 3. Install required dependencies
pip install -r requirements.txt

# 4. Launch the dashboard locally
streamlit run app.py
👩‍💻 Author
Abeera Ejaz
BS Computer Science | Full-Stack & Applied AI Developer (MERN / React / Python)