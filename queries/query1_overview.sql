-- Token Launch Statistics (Overview)
SELECT 
  CASE 
    WHEN max_mcap < 7000 THEN '1. Dead on Arrival (<$7K)'
    WHEN max_mcap < 20000 THEN '2. Low Traction ($7K-$20K)'
    WHEN max_mcap < 100000 THEN '3. Medium Traction ($20K-$100K)'
    WHEN max_mcap < 1000000 THEN '4. High Traction ($100K-$1M)'
    ELSE '5. Over $1M'
  END as tier,
  COUNT(*) as token_count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM dune.bumaye17.result_clean_pump_fun
GROUP BY 1
ORDER BY 1
