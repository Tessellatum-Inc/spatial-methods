\set ON_ERROR_STOP on

-- Spatial QA for the disposable pilot database.
-- The 100 m asset-to-stop distance is an explicit review trigger for this
-- synthetic exercise, not a universal specification or acceptance tolerance.

WITH config AS (
    SELECT horizontal_srid
    FROM pilot.project_config
    WHERE project_config_id = 1
),
checks AS (
    SELECT 'project_crs_configured' AS check_name, 'error' AS severity,
           CASE WHEN count(*) = 1 THEN 0 ELSE 1 END AS issue_count,
           jsonb_build_object('configured_rows', count(*)) AS details
    FROM pilot.project_config WHERE project_config_id = 1

    UNION ALL
    SELECT 'geometry_srid_consistency', 'error',
           count(*) FILTER (WHERE c.horizontal_srid IS NULL OR ST_SRID(f.geom) <> c.horizontal_srid),
           jsonb_build_object('feature_count', count(*),
             'configured_srid', (SELECT horizontal_srid FROM config))
    FROM pilot.inventory_feature f CROSS JOIN (SELECT 1) seed
    LEFT JOIN config c ON true

    UNION ALL
    SELECT 'geometry_validity', 'error',
           count(*) FILTER (WHERE ST_IsEmpty(geom) OR NOT ST_IsValid(geom)),
           jsonb_build_object('feature_count', count(*))
    FROM pilot.inventory_feature

    UNION ALL
    SELECT 'feature_subtype_completeness', 'error',
           count(*) FILTER (
             WHERE (f.feature_type = 'stop' AND s.feature_id IS NULL)
                OR (f.feature_type = 'asset' AND a.feature_id IS NULL)),
           jsonb_build_object('feature_count', count(*))
    FROM pilot.inventory_feature f
    LEFT JOIN pilot.stop s ON s.feature_id = f.feature_id
    LEFT JOIN pilot.asset a ON a.feature_id = f.feature_id

    UNION ALL
    SELECT 'asset_parent_stop_link', 'error',
           count(*) FILTER (WHERE a.stop_id IS NULL OR s.feature_id IS NULL),
           jsonb_build_object('asset_count', count(*))
    FROM pilot.asset a
    LEFT JOIN pilot.stop s ON s.feature_id = a.stop_id

    UNION ALL
    SELECT 'coincident_feature_points', 'review',
           count(*),
           jsonb_build_object('coincident_pairs', COALESCE(jsonb_agg(pair_ids), '[]'::jsonb))
    FROM (
      SELECT jsonb_build_array(a.feature_id::text, b.feature_id::text) AS pair_ids
      FROM pilot.inventory_feature a
      JOIN pilot.inventory_feature b
        ON a.feature_id < b.feature_id AND ST_Equals(a.geom, b.geom)
    ) duplicates

    UNION ALL
    SELECT 'asset_parent_distance_over_100m', 'review',
           count(*) FILTER (WHERE ST_Distance(a_feature.geom, s_feature.geom) > 100),
           jsonb_build_object('review_threshold_m', 100,
             'flagged_asset_ids', COALESCE(jsonb_agg(a.feature_id::text)
               FILTER (WHERE ST_Distance(a_feature.geom, s_feature.geom) > 100), '[]'::jsonb))
    FROM pilot.asset a
    JOIN pilot.inventory_feature a_feature ON a_feature.feature_id = a.feature_id
    JOIN pilot.inventory_feature s_feature ON s_feature.feature_id = a.stop_id
),
summary AS (
    SELECT
      count(*) FILTER (WHERE severity = 'error' AND issue_count > 0) AS failed_checks,
      count(*) FILTER (WHERE severity = 'review' AND issue_count > 0) AS review_checks,
      COALESCE(sum(issue_count) FILTER (WHERE severity = 'error'), 0) AS error_issues,
      COALESCE(sum(issue_count) FILTER (WHERE severity = 'review'), 0) AS review_issues
    FROM checks
)
SELECT jsonb_pretty(jsonb_build_object(
  'report_type', 'spatial_methods_spatial_qa',
  'report_version', '0.1.0',
  'dataset_status', 'synthetic',
  'project_srid', (SELECT horizontal_srid FROM config),
  'feature_count', (SELECT count(*) FROM pilot.inventory_feature),
  'stop_count', (SELECT count(*) FROM pilot.stop),
  'asset_count', (SELECT count(*) FROM pilot.asset),
  'status', CASE WHEN s.error_issues > 0 THEN 'FAIL'
                 WHEN s.review_issues > 0 THEN 'PASS_WITH_REVIEW_FLAGS'
                 ELSE 'PASS' END,
  'summary', jsonb_build_object(
    'failed_checks', s.failed_checks,
    'review_checks', s.review_checks,
    'error_issues', s.error_issues,
    'review_issues', s.review_issues),
  'checks', (SELECT jsonb_agg(jsonb_build_object(
      'name', check_name, 'severity', severity, 'issue_count', issue_count,
      'status', CASE WHEN issue_count = 0 THEN 'pass'
                     WHEN severity = 'error' THEN 'fail' ELSE 'review' END,
      'details', details) ORDER BY severity, check_name) FROM checks),
  'limitations', jsonb_build_array(
    'All input features are synthetic software fixtures, not field observations.',
    'A successful report does not establish positional accuracy or operational fitness.',
    'The 100 m asset-to-parent distance is a configurable review trigger for this exercise, not a universal tolerance.',
    'Point-only geometry checks do not assess line or polygon topology.',
    'No independent positional reference observations are available.'
  )
)) AS spatial_qa_report
FROM summary s;

DO $$
DECLARE error_issues bigint;
BEGIN
  SELECT count(*) FILTER (WHERE issue_count > 0)
    INTO error_issues
    FROM (
      SELECT count(*) AS issue_count
      FROM pilot.inventory_feature f
      LEFT JOIN pilot.project_config c ON c.project_config_id = 1
      WHERE c.horizontal_srid IS NULL OR ST_SRID(f.geom) <> c.horizontal_srid
      UNION ALL
      SELECT count(*) FROM pilot.inventory_feature
      WHERE ST_IsEmpty(geom) OR NOT ST_IsValid(geom)
      UNION ALL
      SELECT count(*) FROM pilot.inventory_feature f
      LEFT JOIN pilot.stop s ON s.feature_id = f.feature_id
      LEFT JOIN pilot.asset a ON a.feature_id = f.feature_id
      WHERE (f.feature_type = 'stop' AND s.feature_id IS NULL)
         OR (f.feature_type = 'asset' AND a.feature_id IS NULL)
    ) hard_failures;
  IF error_issues > 0 THEN
    RAISE EXCEPTION 'Spatial QA failed: % hard-failure groups detected', error_issues;
  END IF;
END;
$$;
