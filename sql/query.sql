SELECT * FROM students.cleaning;

-- 1. Dropout & Retention Overview
CREATE VIEW churn_distribution AS
SELECT
	churn_status, 
    count(*) AS total_students,
    round(
		100.0 * COUNT(*) / (SELECT COUNT(*) FROM students.cleaning), 
        2
        ) AS percentage
FROM students.cleaning
GROUP BY churn_status;

-- 2. Dropout Rate
CREATE VIEW dropout_rate AS
SELECT
ROUND(
	100.0 *SUM(CASE WHEN churn_status = 'Churn' THEN 1 ELSE 0 END) / COUNT(*),
    2
    ) AS dropout_rate
FROM students.cleaning

-- 3. Academic Performance vs Churn
CREATE VIEW academic_performance AS
SELECT
	churn_status,
    ROUND(AVG(approval_rate), 2) AS avg_approval_rate,
    ROUND(AVG(total_units_approved),1) AS avg_units_approved
FROM students.cleaning
GROUP BY churn_status;

-- 4. Financial Risk vs Churn
CREATE VIEW financial_risk AS
SELECT
payment_risk,
churn_status,
COUNT(*) AS total_students
FROM students.cleaning
GROUP BY payment_risk, churn_status
ORDER BY payment_risk;

-- 5. Dropout Rate: Debtor vs Non-Debtor
CREATE VIEW dropout_precentage AS
SELECT 
  debtor,
  ROUND(
    100.0 * SUM(CASE WHEN churn_status = 'Churn' THEN 1 ELSE 0 END) / COUNT(*),
    2
  ) AS dropout_rate
FROM cleaning
GROUP BY debtor;

-- 6. High-Risk Student Segment
CREATE VIEW highrisk_student AS
SELECT *
FROM students.cleaning
WHERE approval_rate < 0.5
	AND payment_risk = 1
    AND churn_status = 'Churn';
    
-- 7. Top 10% Highest Dropout Risk (By Performance)
CREATE VIEW tophighest_do AS
SELECT *
FROM students.cleaning
ORDER BY approval_rate ASC
LIMIT 442;

-- 8. Cohort Analysis (By Admission Year)
CREATE VIEW cohort_analysis AS
SELECT
	admission_grade,
    churn_status,
    COUNT(*) AS total_students
FROM students.cleaning
GROUP BY admission_grade, churn_status
ORDER BY admission_grade;

-- 9.KPI Summary
CREATE VIEW kpi_summary AS
SELECT
	COUNT(*) AS total_students,
    SUM(CASE WHEN churn_status = 'Churn' THEN 1 ELSE 0 END) AS total_churn,
    ROUND(AVG(approval_rate), 2) AS avg_approval_rate,
    ROUND(AVG(payment_risk), 2) AS avg_payment_risk
FROM students.cleaning;

-- 10. Data for Dashboard Filters
CREATE VIEW c_status AS
SELECT DISTINCT churn_status FROM students.cleaning;

CREATE VIEW p_risk AS
SELECT DISTINCT payment_risk FROM students.cleaning;

CREATE VIEW debt_status AS
SELECT DISTINCT debtor FROM students.cleaning;

