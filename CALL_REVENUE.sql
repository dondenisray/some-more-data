--Total Calls por país

SELECT
    country,
    COUNT(call_id) AS total_calls
FROM calls
GROUP BY country
ORDER BY total_calls DESC;

---Handled Rate por país

SELECT
    country,
    COUNT(call_id) AS total_calls,
    SUM(handled) AS total_handled,
    SUM(handled) * 1.0 / COUNT(call_id) AS handled_rate
FROM calls
GROUP BY country;

--Average Wait Time (solo handled)

SELECT
    country,
    AVG(wait_time_seconds) AS avg_wait_time
FROM calls
WHERE handled = 1
GROUP BY country;

-- Total MICE Revenue por mes

SELECT
    DATEFROMPARTS(YEAR(booking_date), MONTH(booking_date), 1) AS month,
    SUM(revenue) AS total_mice_revenue
FROM group_sales
WHERE segment = 'MICE'
GROUP BY DATEFROMPARTS(YEAR(booking_date), MONTH(booking_date), 1)
ORDER BY month DESC;
