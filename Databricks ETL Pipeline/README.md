# End-to-End Azure/AWS Databricks ETL Pipeline

A production-grade, orchestrated data engineering pipeline built entirely within Databricks Community Edition. This project showcases the ingestion, transformation, and automated orchestration of **e-commerce retail sales & customer transaction data**.

---

## 🏗️ Architecture Overview

The pipeline implements a classic **Medallion Architecture** (Bronze ➡️ Silver ➡️ Gold) managed via Databricks Delta Live Tables (DLT) and orchestrated using Databricks Jobs.

```text
[ Ingestion Sources ]
        │
        ▼  (Autoloader / Raw Ingestion Notebook)
┌─────────────────────────────────┐
│     Bronze: Raw Data Landing    │
└─────────────────────────────────┘
        │
        ▼  (Data Cleansing & Schema Enforcement)
┌─────────────────────────────────┐
│   Silver: Enriched / Cleaned    │
└─────────────────────────────────┘
        │
        ▼  (Aggregation & Business Logic)
┌─────────────────────────────────┐
│    Gold: Analytics-Ready        │
└─────────────────────────────────┘
```

**High-level execution sequence:**

```text
Ingestion Notebook  ➡️  DLT ETL Pipeline  ➡️  Orchestration Job
     (raw load)          (Bronze→Silver→Gold)     (schedule + alerts)
```

---

## 🛠️ Tech Stack & Features

* **Platform:** Databricks (Free Tier / Community Edition)
* **Storage & Format:** Delta Lake (ACID transactions, time travel, schema evolution)
* **Languages:** PySpark, Spark SQL
* **Orchestration:** Databricks Jobs (multi-task orchestration)
* **Data Pipeline:** Delta Live Tables (DLT) for declarative, reliable end-to-end processing
* **Ingestion:** Auto Loader for incremental file-based landing

---

## 📂 Repository Structure

```text
├── notebooks/
│   ├── 01_bronze_ingestion.py    # Raw data streaming/loading via Auto Loader
│   ├── 02_silver_transform.py    # Deduplication, null handling, data typing
│   └── 03_gold_aggregations.py   # Business logic and BI-ready aggregates
├── workflows/
│   ├── pipeline_definition.json  # Delta Live Tables (DLT) configuration
│   └── job_definition.json       # Databricks Job Orchestration template
└── README.md
```

---

## ⚙️ Workflow & Orchestration Setup

The infrastructure configurations are fully version-controlled in the `/workflows` directory to allow seamless deployment across environments.

### 1. Data Pipeline (DLT)
The **End-to-End ETL Pipeline** handles continuous processing across the Medallion layers. It enforces data quality constraints (expectations) and automatically promotes records from raw files through to analytical aggregates.

* Config file: `workflows/pipeline_definition.json`

### 2. Job Orchestration
The **Job to run end-to-end pipeline** automates system execution. It is configured to run on a **daily schedule** (with optional file-arrival / table-update triggers for incremental loads). The job sequences dependent tasks (ingestion → DLT pipeline → post-processing) and fires email/Slack alerts on failure.

* Config file: `workflows/job_definition.json`

**Trigger details:**
- Primary: Scheduled (daily at 02:00 UTC)
- Secondary: Can be switched to continuous / table-update mode when using Auto Loader with cloud storage notifications
- Failure handling: Retry policy + notification webhooks

---

## 🚀 How to Replicate This Project

To import and run this pipeline configuration inside your own Databricks environment:

1. **Import Notebooks**  
   Clone this repository directly into your Databricks workspace using **Workspace → Repos → Add Repo**.

2. **Deploy the DLT Pipeline**  
   - Go to **Delta Live Tables → Create Pipeline**.  
   - Switch to the **JSON** tab in the top-right corner.  
   - Copy and paste the contents of `workflows/pipeline_definition.json`.

3. **Deploy the Orchestration Job**  
   - Go to **Workflows (Jobs) → Create Job**.  
   - Open the Advanced options to view/edit JSON configuration.  
   - Paste the contents of `workflows/job_definition.json` to instantly link your notebooks and pipeline tasks.

**Live Job Link (example workspace):**  
https://dbc-9b4ea1c4-6779.cloud.databricks.com/jobs?o=7474660702177872

---

## 📌 Key Highlights for Recruiters

- Full Medallion (Bronze / Silver / Gold) implementation using Delta Lake
- Declarative pipeline with DLT + production-style job orchestration
- Incremental ingestion pattern ready for production cloud storage
- Version-controlled infrastructure-as-code (JSON configs)
- Designed to be easily portable from Community Edition to Azure / AWS / GCP Databricks workspaces
