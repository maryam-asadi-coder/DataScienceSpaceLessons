# ------------------------------------------
# SpaceX Data Analysis using SQLite & Pandas
# Author: Maryam Asadi
# ------------------------------------------

import pandas as pd
from sqlalchemy import create_engine

# 1️⃣ بارگذاری داده‌ها
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv"
df = pd.read_csv(url)

# 2️⃣ ساخت دیتابیس SQLite و ذخیره جدول
engine = create_engine('sqlite:///spacex.db')


# ذخیره جدول در دیتابیس بدون خطای cursor
df.to_sql("SPACEXTBL", con=engine, if_exists='replace', index=False)

# 3️⃣ پرس‌وجوها (Queries)
queries = {
    "distinct_sites": "SELECT DISTINCT Launch_Site FROM SPACEXTBL",
    "starts_with_CCA": "SELECT * FROM SPACEXTBL WHERE Launch_Site LIKE 'CCA%'",
    "total_mass_nasa": "SELECT SUM(PAYLOAD_MASS__KG_) AS total_mass_nasa FROM SPACEXTBL WHERE Customer = 'NASA (CRS)'",
    "avg_mass_f9v1_1": "SELECT AVG(PAYLOAD_MASS__KG_) AS avg_mass_f9v1_1 FROM SPACEXTBL WHERE Booster_Version = 'F9 v1.1'",
    "first_ground_success": "SELECT MIN(Date) AS first_success_ground_pad FROM SPACEXTBL WHERE Landing_Outcome = 'Success (ground pad)'",
    "drone_success_4000_6000": """
        SELECT Booster_Version
        FROM SPACEXTBL
        WHERE Landing_Outcome = 'Success (drone ship)'
        AND PAYLOAD_MASS__KG_ BETWEEN 4000 AND 6000
    """,
    "mission_outcome_count": "SELECT Mission_Outcome, COUNT(*) AS count FROM SPACEXTBL GROUP BY Mission_Outcome",
    "max_payload_boosters": """
        SELECT Booster_Version
        FROM SPACEXTBL
        WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTBL)
    """,
    "failures_2015": """
        SELECT SUBSTR(Date,6,2) AS Month, Landing_Outcome, Booster_Version, Launch_Site
        FROM SPACEXTBL
        WHERE Date LIKE '2015%' AND Landing_Outcome = 'Failure (drone ship)'
    """,
    "landing_outcomes_between_dates": """
        SELECT Landing_Outcome, COUNT(*) AS Count
        FROM SPACEXTBL
        WHERE Date BETWEEN '2010-06-04' AND '2017-03-20'
        GROUP BY Landing_Outcome
        ORDER BY Count DESC
    """
}

# 4️⃣ اجرای پرس‌وجوها و چاپ نتایج
for name, q in queries.items():
    print(f"\n▶️ Query: {name}")
    df_query = pd.read_sql_query(q, engine)  # استفاده مستقیم از engine
    print(df_query)

print("\n✅ تحلیل کامل شد.")
