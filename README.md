# Data Analytics & BI Pipeline Project

โปรเจกต์สำหรับสร้าง Data Pipeline ในการประมวลผลข้อมูลคำสั่งซื้อ การชำระเงิน และการจัดส่ง เพื่อนำไปทำเป็นแดชบอร์ดสรุปผลเชิงธุรกิจ (BI)
data source : https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce?select=olist_order_payments_dataset.csv

---

# 1. Project Structure

```text
├── bi/
│   ├── dashboard.pbix                      # ไฟล์ Power BI Dashboard
│   ├── dax_measure.md                      # รวมสูตร DAX Measures ที่ใช้งาน
│   └── screen_shot_dash_board.png          # ภาพตัวอย่างหน้าจอแดชบอร์ด
│
├── pipelines/
│   ├── tasks/                              # Sub-tasks สำหรับการประมวลผลย่อย
│   ├── flow.py                             # ไฟล์หลักในการรันและควบคุม Pipeline
│   └── living-os-project-ac24a0a8cacb.json # Google Cloud Service Account Key
│
├── sql/
│   ├── staging/                            # Layer 1: เคลียร์ข้อมูลดิบและจัดประเภทเบื้องต้น
│   │   ├── stg_order_items.sql
│   │   ├── stg_orders.sql
│   │   └── stg_payments.sql
│   │
│   ├── intermediate/                       # Layer 2: เชื่อมโยงข้อมูล (Join/Transform)
│   │   └── int_orders_enriched.sql
│   │
│   └── mart/                               # Layer 3: ตารางพร้อมใช้สำหรับ BI
│       ├── aov.sql
│       ├── mart_daily_revenue.sql
│       ├── monthly_gmv.sql
│       └── on_time_delivery_rate.sql
│
├── Dockerfile                              # Docker setup สำหรับจำลอง Environment
└── requirements.txt                        # Python dependencies
```

---

# 2. Setup & How to Run Pipeline

## Prerequisites

* ติดตั้ง Docker บนเครื่องคอมพิวเตอร์
* ตรวจสอบให้แน่ใจว่าไฟล์ Service Account Key (`living-os-project-ac24a0a8cacb.json`) มีสิทธิ์เข้าถึง BigQuery
* ตรวจสอบ ไฟล์ Service Account Key (`living-os-project-ac24a0a8cacb.json`) เเละ ไฟล์ .env ว่าอยู่ใน folder "pipeline" ไหม 

## Build Docker Image

สร้าง Environment จาก "dockerfile"

```bash
docker build -t data-pipeline-app .
```

## Run Pipeline

รัน Docker Container เพื่อดึงข้อมูล ประมวลผล และโหลดข้อมูลเข้าสู่ BigQuery

```bash
docker run --rm data-pipeline-app
```

---

# 3. BigQuery Datasets

โครงสร้าง Data Warehouse บน BigQuery แบ่งออกเป็น 3 Datasets ตามระดับการจัดการข้อมูล

## staging

ใช้จัดเก็บข้อมูลดิบที่ผ่านการทำความสะอาดเบื้องต้น เช่น

* Data Type Casting
* Data Validation
* Basic Cleaning

ตาราง

* `stg_orders`
* `stg_order_items`
* `stg_payments`

## intermediate

ใช้จัดเก็บข้อมูลที่ผ่านการเชื่อมโยง (Join) และแปลงรูปแบบข้อมูลเรียบร้อยแล้ว

ตาราง

* `int_orders_enriched`

## mart

ใช้จัดเก็บตารางที่พร้อมสำหรับการวิเคราะห์และทำ Dashboard

ตาราง

* `mart_daily_revenue`
* `monthly_gmv`
* `aov`
* `on_time_delivery_rate`

---

# 4. Key Architectural Decisions

## Data Layer Rationale

### Why not query staging directly?

แม้ว่าจะสามารถ Query จาก Staging Layer ได้โดยตรง แต่จะทำให้ต้องทำ Join และคำนวณ Business Logic ซ้ำทุกครั้งที่มีการวิเคราะห์ข้อมูล ส่งผลให้

* Query ซับซ้อนขึ้น
* ใช้เวลาประมวลผลมากขึ้น
* ค่าใช้จ่าย BigQuery สูงขึ้น
* มีความเสี่ยงที่แต่ละ Dashboard จะใช้ Logic ไม่ตรงกัน

จึงเลือกแยก Data Warehouse ออกเป็น 3 Layer ดังนี้

### Staging Layer

หน้าที่

* รับข้อมูลดิบจาก Source
* จัดการ Data Type
* ทำความสะอาดข้อมูลเบื้องต้น

ข้อดี

* ลดภาระของ Source System
* เก็บข้อมูลในรูปแบบมาตรฐาน
* ง่ายต่อการตรวจสอบปัญหา

### Intermediate Layer

หน้าที่

* Join ตารางต่าง ๆ เข้าด้วยกัน
* คำนวณ Logic ที่ใช้ร่วมกันหลายจุด
* สร้าง Single Source of Truth

ข้อดี

* ลดการเขียน Join ซ้ำ
* ลดความซับซ้อนของ Query
* ทำให้ Business Logic อยู่ศูนย์กลางเดียว 

### Mart Layer

หน้าที่

* สรุปผลข้อมูลตาม Business Requirement
* เตรียมข้อมูลสำหรับ BI Tools

ข้อดี

* Query เร็วขึ้น
* Dashboard ตอบสนองดีขึ้น
* ลดค่าใช้จ่ายในการ Query
* ผู้ใช้งาน BI สามารถนำข้อมูลไปใช้ได้ทันที

ตัวอย่าง

* Daily Revenue
* Monthly GMV
* AOV
* On-Time Delivery Rate

---

## Null Strategy

### Staging & Intermediate Layer

คงค่า `NULL` ไว้ตามจริงสำหรับข้อมูลที่ไม่มีค่า

เหตุผล

* ป้องกันการบิดเบือนข้อมูล
* ทำให้สถิติ เช่น Average หรือ Median ถูกต้อง
* สะท้อนคุณภาพข้อมูลจริง

นั้นหมายถึงไม่มีข้อมูลจริง ไม่ใช่ค่า 0
---



