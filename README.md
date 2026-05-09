# 🏥 eICU Full-Stack Clinical System

## 🚀 [Live Demo: Click Here to Explore](https://icu-system-online.vercel.app)

> **Deployment Note:** This system is hosted on the **Render/Vercel Free Tier**. The backend "spins down" after inactivity. Please allow **40-60 seconds** for the first login to process as the server wakes up.

---

## 📝 Project Overview
This repository contains a comprehensive **ICU Clinical Information System** designed to streamline clinician workflows in high-acuity environments. The platform transforms complex physiological and longitudinal patient data from the **eICU Collaborative Research Database** into actionable insights through an intuitive, multi-page dashboard.

### **Key Highlights**
* **AI-Powered Insights:** Integrated **Anthropic Claude-3.5** Clinical Agent that analyzes patient history to provide "Current Status" summaries and decision support.
* **Comprehensive Workflow:** A 15-page specialized clinician journey, covering everything from ICU census to nursing documentation and severity scoring.
* **Enterprise Architecture:** A decoupled full-stack build utilizing a **FastAPI** REST API and a **Next.js** reactive frontend, containerized with **Docker**.

---

## 🛠️ Technical Stack
* **Frontend:** Next.js (React), Tailwind CSS, Lucide Icons.
* **Backend:** FastAPI (Python 3.11+), Uvicorn.
* **AI/LLM:** Anthropic SDK (Claude API) for clinical summarization.
* **Database:** SQLite (integrated eICU dataset structures).
* **DevOps:** Docker, Docker Compose, Git LFS.
* **Deployment:** Vercel (Frontend), Render (Backend/Docker).

---

## 🧬 Clinical Dashboard Features
The system is architected around a professional 15-page clinician workflow:
1.  **Secure Authentication:** Role-based login.
2.  **ICU Census:** Real-time unit-wide patient tracking.
3.  **Patient List:** Searchable database of active ICU patients.
4.  **Patient Summary:** High-level "At-a-Glance" clinical view.
5.  **Vitals & Hemodynamics:** Longitudinal tracking of physiological data.
6.  **Laboratory Results:** Comprehensive lab panels and trends.
7.  **Medication & Infusion:** Active and historical pharmacological tracking.
8.  **Intake / Output:** Precise fluid balance monitoring.
9.  **Respiratory Support:** Ventilator settings and oxygenation status.
10. **Diagnosis / Problem List:** ICD-coded medical history.
11. **Clinical Notes:** Documentation for MDs/Nurses.
12. **Nursing Documentation:** Bedside flowsheets and assessments.
13. **Care Plan:** Multidisciplinary treatment planning.
14. **Severity & Alerts:** Risk stratification and clinical warning systems.
15. **Unit Dashboard:** Hospital-level capacity and metrics.

---

## 🚀 Local Development (Docker)

To run the system locally for development or testing:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/xiaohanwang1997/eICU-System.git
    cd eICU-System
    ```

2.  **Environment Setup:**
    Create a `.env` file in the `backend/` directory and add your keys:
    ```env
    ANTHROPIC_API_KEY=your_key_here
    ```

3.  **Launch with Docker Compose:**
    ```bash
    docker compose up --build -d
    ```

4.  **Access Points:**
    * **Frontend:** `http://localhost:3000`
    * **Backend API Docs:** `http://localhost:8000/docs`

---

## 🔐 Demo Credentials
Use the following credentials to access the live or local demo:

* **Email:** `doctor@example.com`
* **Password:** `doctor123`

---

### **Author**
**Xiaohan Wang** *Computer Science & Health Informatics*
