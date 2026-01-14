# Project Context: n8n Build Club Outreach

## 1. Project Overview
This project is a **local-first automation system** designed to generate, enrich, and manage a high-quality list of 100 "Accessible Entrepreneur-Authors" for outreach. The system has evolved from a simple CLI tool into a full-stack web dashboard (FastAPI + Vue.js) to provide a better user experience.

## 2. Evolution & Requirements History (Prompt Log)
The project has undergone several strategic pivots based on user feedback:

*   **Phase 1: CLI Prototype:** Initially started as a command-line interface to scrape leads.
*   **Phase 2: Web Application:** Pivoted to a local web server (`localhost:8001`) with a dashboard to visualize leads.
*   **Phase 3: Data Quality & Persistence:**
    *   Moved from in-memory/JSON data to **SQLite** (`local_system.db`) for reliability.
    *   Added columns for **LinkedIn** and **Multiple Emails**.
*   **Phase 4: The "Accessible" Pivot:**
    *   **Requirement:** "Stop targeting Bill Gates/Satya Nadella. They won't reply."
    *   **Action:** Wiped the database and curated a new list of **100 "Indie" Founders** (e.g., Arvid Kahl, Daniel Vassallo) who are active on social media and run $10k-$5M ARR businesses.
*   **Phase 5: "Bio-First" Enrichment:**
    *   **Requirement:** "Bios are too short. I need details."
    *   **Action:** Expanded author bios from 1-liners to **10-line detailed briefs** covering revenue figures, exit amounts, and personal "life story" context.
*   **Phase 6: Refinements:**
    *   **Serial Numbers (#):** Added to the dashboard table.
    *   **De-duplication:** Strict logic implemented to ensure exactly 100 unique entries.

## 3. Technology Stack
*   **Backend:** Python 3.11+, FastAPI, Uvicorn (Server).
*   **Database:** SQLite (`local_system.db`).
*   **Frontend:** HTML5, TailwindCSS (for styling), Vue.js (for reactivity) - served statically.
*   **Key Libraries:** `sqlite3`, `pydantic`.

## 4. Architecture & Key Files

### Root Directory (`/`)
*   `run.py`: **Entry Point.** Run this to start the server (`python run.py`).
*   `project_context.md`: This file.

### Backend (`/backend`)
*   `main.py`: The FastAPI application core. Defines API endpoints (`/authors`, `/discover`).
*   `db.py`: Database connection and schema management.
*   `seed_accessible_100.py`: **MASTER DATA SCRIPT.** Contains the curated list of 100+ accessible authors and the logic to inject them into the DB. **(Use this to reset data).**

### Frontend (`/frontend`)
*   `index.html`: The main dashboard UI. Modified to include the `#` column and "Bio & Context" field.
*   `dashboard.js`: Frontend logic (fetching data from API every 2 seconds).

## 5. Current System Status
*   **Lead Count:** ~100 Verified/Unique Leads.
*   **Data Profile:** "Accessible Entrepreneur-Authors" (Indie Hackers, Course Creators).
*   **Richness:** Deep bios with financial metrics.
*   **Server:** Running on port `8001`.
*   **Status:** **Stable & Verified.**

## 6. How to Run
1.  **Start Server:**
    ```bash
    python run.py
    ```
2.  **Access Dashboard:**
    Open [http://localhost:8001](http://localhost:8001) in your browser.
3.  **Reset/Re-seed Data:**
    ```bash
    python -m backend.seed_accessible_100
    ```
