\set ON_ERROR_STOP on

-- Disposable integration test. This is a software test only.
-- EPSG:3857 is used as a known test SRID; coordinates are synthetic (0,0).
-- This does NOT select a CRS for the Nairobi pilot.

DROP SCHEMA IF EXISTS pilot CASCADE;
\i /tests/postgis-schema.sql

-- 1. Geometry insertion must fail until project CRS is configured.
DO $$
DECLARE rejected boolean := false;
BEGIN
    BEGIN
        INSERT INTO pilot.inventory_feature(feature_id, feature_type, geom)
        VALUES ('00000000-0000-0000-0000-000000000001', 'stop',
                ST_SetSRID(ST_MakePoint(0, 0), 3857));
    EXCEPTION WHEN OTHERS THEN
        rejected := true;
    END;
    IF NOT rejected THEN
        RAISE EXCEPTION 'FAIL: geometry accepted before CRS configuration';
    END IF;
END;
$$;

-- 2. Configure the isolated test CRS, not the eventual project CRS.
INSERT INTO pilot.project_config (
    project_config_id, project_name, horizontal_srid, crs_authority,
    crs_code, crs_name, axis_units, reference_decision_ref
) VALUES (
    1, 'Disposable PostGIS integration test', 3857, 'EPSG', '3857',
    'WGS 84 / Pseudo-Mercator (software test only)', 'metre',
    'Integration fixture declaration; not a project reference decision'
);

-- 3. A point with the configured SRID must insert and retain its SRID.
INSERT INTO pilot.inventory_feature(feature_id, feature_type, geom)
VALUES ('00000000-0000-0000-0000-000000000001', 'stop',
        ST_SetSRID(ST_MakePoint(0, 0), 3857));

DO $$
DECLARE actual_srid integer;
BEGIN
    SELECT ST_SRID(geom) INTO actual_srid
      FROM pilot.inventory_feature
     WHERE feature_id = '00000000-0000-0000-0000-000000000001';
    IF actual_srid <> 3857 THEN
        RAISE EXCEPTION 'FAIL: expected SRID 3857, got %', actual_srid;
    END IF;
END;
$$;

-- 4. A geometry with a different SRID must be rejected.
DO $$
DECLARE rejected boolean := false;
BEGIN
    BEGIN
        INSERT INTO pilot.inventory_feature(feature_id, feature_type, geom)
        VALUES ('00000000-0000-0000-0000-000000000002', 'stop',
                ST_SetSRID(ST_MakePoint(1, 1), 4326));
    EXCEPTION WHEN OTHERS THEN
        rejected := true;
    END;
    IF NOT rejected THEN
        RAISE EXCEPTION 'FAIL: mismatched SRID was accepted';
    END IF;
END;
$$;

-- 5. A valid stop subtype must reference a base feature of type stop.
INSERT INTO pilot.stop (
    feature_id, stop_status, evidence_basis, observation_datetime,
    positional_method, position_quality_class, source_observer
) VALUES (
    '00000000-0000-0000-0000-000000000001', 'observed_stop',
    'Synthetic integration fixture', now(), 'other', 'test_only', 'test_runner'
);

-- 6. A subtype/type mismatch must be rejected.
DO $$
DECLARE rejected boolean := false;
BEGIN
    BEGIN
        INSERT INTO pilot.asset (
            feature_id, asset_type, presence, observation_datetime
        ) VALUES (
            '00000000-0000-0000-0000-000000000001',
            'shelter', 'present', now()
        );
    EXCEPTION WHEN OTHERS THEN
        rejected := true;
    END;
    IF NOT rejected THEN
        RAISE EXCEPTION 'FAIL: stop feature accepted as asset subtype';
    END IF;
END;
$$;

-- 7. Foreign-key integrity must reject an asset linked to a missing stop.
INSERT INTO pilot.inventory_feature(feature_id, feature_type, geom)
VALUES ('00000000-0000-0000-0000-000000000003', 'asset',
        ST_SetSRID(ST_MakePoint(2, 2), 3857));

DO $$
DECLARE rejected boolean := false;
BEGIN
    BEGIN
        INSERT INTO pilot.asset (
            feature_id, stop_id, asset_type, presence, observation_datetime
        ) VALUES (
            '00000000-0000-0000-0000-000000000003',
            '00000000-0000-0000-0000-000000000099',
            'shelter', 'present', now()
        );
    EXCEPTION WHEN OTHERS THEN
        rejected := true;
    END;
    IF NOT rejected THEN
        RAISE EXCEPTION 'FAIL: unknown stop foreign key was accepted';
    END IF;
END;
$$;

-- 8. Controlled-value constraints must reject an unknown asset type.
DO $$
DECLARE rejected boolean := false;
BEGIN
    BEGIN
        INSERT INTO pilot.asset (
            feature_id, asset_type, presence, observation_datetime
        ) VALUES (
            '00000000-0000-0000-0000-000000000003',
            'imaginary_asset', 'present', now()
        );
    EXCEPTION WHEN OTHERS THEN
        rejected := true;
    END;
    IF NOT rejected THEN
        RAISE EXCEPTION 'FAIL: invalid asset type was accepted';
    END IF;
END;
$$;

SELECT 'PASS: CRS configuration, SRID enforcement, subtype integrity, foreign key, controlled values and SRID retrieval' AS integration_result;
