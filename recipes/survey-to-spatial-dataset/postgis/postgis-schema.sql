-- Spatial Methods capstone: PostGIS schema
-- Status: design artefact; not yet executed against a live PostgreSQL/PostGIS instance.
-- IMPORTANT: choose and approve the project CRS before inserting project_config.
-- Do not use SRID 0, arbitrary local coordinates, or an assumed Nairobi CRS.

CREATE EXTENSION IF NOT EXISTS postgis;

CREATE SCHEMA IF NOT EXISTS pilot;

-- Exactly one project configuration row is expected for this pilot schema.
-- horizontal_srid must be a real SRID available in this PostGIS installation
-- and supported by the approved project reference decision.
CREATE TABLE pilot.project_config (
    project_config_id smallint PRIMARY KEY CHECK (project_config_id = 1),
    project_name text NOT NULL,
    horizontal_srid integer NOT NULL CHECK (horizontal_srid > 0),
    crs_authority text NOT NULL,
    crs_code text NOT NULL,
    crs_name text NOT NULL,
    coordinate_epoch numeric(8,3),
    axis_units text NOT NULL,
    reference_decision_ref text NOT NULL,
    configured_at timestamptz NOT NULL DEFAULT now(),
    CHECK (length(trim(project_name)) > 0),
    CHECK (length(trim(crs_authority)) > 0),
    CHECK (length(trim(crs_code)) > 0),
    CHECK (length(trim(crs_name)) > 0),
    CHECK (length(trim(reference_decision_ref)) > 0)
);

-- Insert this row only after the CRS and coordinate convention are approved.
-- Example shape (values deliberately omitted; do not copy a guessed SRID):
-- INSERT INTO pilot.project_config
-- (project_config_id, project_name, horizontal_srid, crs_authority,
--  crs_code, crs_name, axis_units, reference_decision_ref)
-- VALUES (1, 'Approved pilot name', <approved_postgis_srid>,
--         '<authority>', '<code>', '<official CRS name>', 'metre',
--         '<reference decision document or record>');

CREATE TABLE pilot.inventory_feature (
    feature_id uuid PRIMARY KEY,
    feature_type text NOT NULL CHECK (feature_type IN ('stop', 'asset')),
    geom geometry(Point) NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    CHECK (NOT ST_IsEmpty(geom)),
    CHECK (ST_IsValid(geom))
);

-- Enforce one explicitly configured project SRID for all feature geometries.
CREATE FUNCTION pilot.enforce_project_srid()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
    expected_srid integer;
BEGIN
    SELECT horizontal_srid
      INTO expected_srid
      FROM pilot.project_config
     WHERE project_config_id = 1;

    IF expected_srid IS NULL THEN
        RAISE EXCEPTION
          'Configure pilot.project_config with the approved CRS before loading geometries';
    END IF;

    IF ST_SRID(NEW.geom) <> expected_srid THEN
        RAISE EXCEPTION 'Geometry SRID % does not match configured project SRID %',
          ST_SRID(NEW.geom), expected_srid;
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER inventory_feature_srid_check
BEFORE INSERT OR UPDATE OF geom ON pilot.inventory_feature
FOR EACH ROW EXECUTE FUNCTION pilot.enforce_project_srid();

CREATE TABLE pilot.stop (
    feature_id uuid PRIMARY KEY
        REFERENCES pilot.inventory_feature(feature_id) ON DELETE RESTRICT,
    observed_name text,
    stop_status text NOT NULL CHECK (
        stop_status IN ('observed_stop', 'signed_stop',
                        'designated_verified', 'uncertain')
    ),
    evidence_basis text NOT NULL,
    route_reference text,
    side_of_road text CHECK (
        side_of_road IS NULL OR side_of_road IN
        ('north', 'east', 'south', 'west', 'median', 'unknown')
    ),
    observation_datetime timestamptz NOT NULL,
    positional_method text NOT NULL,
    position_quality_class text NOT NULL,
    source_observer text NOT NULL,
    notes text,
    CHECK (length(trim(evidence_basis)) > 0),
    CHECK (length(trim(source_observer)) > 0)
);

CREATE TABLE pilot.asset (
    feature_id uuid PRIMARY KEY
        REFERENCES pilot.inventory_feature(feature_id) ON DELETE RESTRICT,
    stop_id uuid REFERENCES pilot.stop(feature_id) ON DELETE RESTRICT,
    asset_type text NOT NULL CHECK (
        asset_type IN ('shelter', 'seat', 'sign', 'light', 'kerb_ramp',
                       'crossing', 'footway_link', 'obstruction', 'other')
    ),
    presence text NOT NULL CHECK (
        presence IN ('present', 'absent_after_inspection',
                     'not_assessed', 'obscured', 'inaccessible')
    ),
    condition text CHECK (
        condition IS NULL OR condition IN
        ('good', 'fair', 'poor', 'damaged', 'unknown')
    ),
    accessibility_observation text,
    observation_datetime timestamptz NOT NULL,
    evidence_ref text,
    notes text
);

CREATE TABLE pilot.equipment_register (
    instrument_id text PRIMARY KEY,
    make text,
    model text,
    serial_or_asset_id text,
    firmware_version text,
    configuration text,
    verification_or_calibration_ref text,
    verification_date date,
    verification_scope text,
    limitations text,
    register_status text NOT NULL CHECK (
        register_status IN ('available', 'not_verified', 'restricted', 'retired')
    ),
    CHECK (length(trim(instrument_id)) > 0)
);

CREATE TABLE pilot.control_reference (
    reference_id text PRIMARY KEY,
    reference_name text NOT NULL,
    reference_source text NOT NULL,
    horizontal_srid integer NOT NULL CHECK (horizontal_srid > 0),
    coordinate_epoch numeric(8,3),
    height_reference text,
    uncertainty_description text NOT NULL,
    permitted_use text NOT NULL,
    source_record_ref text NOT NULL,
    CHECK (length(trim(reference_source)) > 0),
    CHECK (length(trim(uncertainty_description)) > 0),
    CHECK (length(trim(permitted_use)) > 0)
);

CREATE TABLE pilot.raw_record (
    raw_record_id uuid PRIMARY KEY,
    source_filename text NOT NULL,
    source_sha256 char(64) NOT NULL,
    record_locator text NOT NULL,
    acquired_at timestamptz,
    received_at timestamptz NOT NULL DEFAULT now(),
    storage_uri text NOT NULL,
    media_type text,
    immutable boolean NOT NULL DEFAULT true CHECK (immutable),
    notes text,
    CHECK (source_sha256 ~ '^[0-9a-fA-F]{64}$'),
    CHECK (length(trim(storage_uri)) > 0)
);

CREATE TABLE pilot.survey_observation (
    observation_id uuid PRIMARY KEY,
    feature_id uuid NOT NULL
        REFERENCES pilot.inventory_feature(feature_id) ON DELETE RESTRICT,
    raw_record_id uuid NOT NULL
        REFERENCES pilot.raw_record(raw_record_id) ON DELETE RESTRICT,
    method text NOT NULL CHECK (
        method IN ('gnss', 'total_station', 'level', 'tape_offset',
                   'image_derived', 'digitised_reference', 'other')
    ),
    instrument_id text REFERENCES pilot.equipment_register(instrument_id),
    setup_id text,
    observed_at timestamptz NOT NULL,
    operator_id text NOT NULL,
    reference_id text REFERENCES pilot.control_reference(reference_id),
    processing_status text NOT NULL CHECK (
        processing_status IN ('raw', 'processed', 'checked', 'rejected')
    ),
    rejection_reason text,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    CHECK (
        (processing_status = 'rejected' AND rejection_reason IS NOT NULL)
        OR processing_status <> 'rejected'
    )
);

CREATE TABLE pilot.quality_check (
    check_id uuid PRIMARY KEY,
    feature_id uuid NOT NULL
        REFERENCES pilot.inventory_feature(feature_id) ON DELETE RESTRICT,
    check_type text NOT NULL CHECK (
        check_type IN ('independent_position', 'attribute_recheck',
                       'completeness', 'topology', 'metadata')
    ),
    check_method text NOT NULL,
    reference_source text,
    result_numeric double precision,
    result_text text,
    acceptance_rule text NOT NULL,
    decision text NOT NULL CHECK (
        decision IN ('pass', 'fail', 'conditional', 'not_assessed')
    ),
    checked_at timestamptz NOT NULL,
    reviewer_id text NOT NULL,
    is_independent boolean NOT NULL DEFAULT false,
    evidence_record_id uuid REFERENCES pilot.raw_record(raw_record_id),
    CHECK (result_numeric IS NOT NULL OR result_text IS NOT NULL),
    CHECK (length(trim(acceptance_rule)) > 0),
    CHECK (
        check_type <> 'independent_position'
        OR (is_independent = true AND reference_source IS NOT NULL)
    )
);

CREATE TABLE pilot.processing_run (
    processing_run_id uuid PRIMARY KEY,
    run_name text NOT NULL,
    software_name text NOT NULL,
    software_version text NOT NULL,
    parameters jsonb NOT NULL DEFAULT '{}'::jsonb,
    input_manifest jsonb NOT NULL,
    output_manifest jsonb NOT NULL DEFAULT '{}'::jsonb,
    operator_id text NOT NULL,
    started_at timestamptz NOT NULL,
    completed_at timestamptz,
    run_status text NOT NULL CHECK (
        run_status IN ('planned', 'running', 'succeeded', 'failed')
    ),
    notes text,
    CHECK (completed_at IS NULL OR completed_at >= started_at)
);

CREATE TABLE pilot.data_dictionary (
    dictionary_entry_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    table_name text NOT NULL,
    field_name text NOT NULL,
    definition text NOT NULL,
    data_type text NOT NULL,
    unit text,
    allowed_values text,
    null_semantics text NOT NULL,
    version text NOT NULL,
    UNIQUE (table_name, field_name, version)
);

CREATE INDEX inventory_feature_geom_gix
    ON pilot.inventory_feature USING gist (geom);
CREATE INDEX survey_observation_feature_idx
    ON pilot.survey_observation(feature_id);
CREATE INDEX survey_observation_time_idx
    ON pilot.survey_observation(observed_at);
CREATE INDEX quality_check_feature_idx
    ON pilot.quality_check(feature_id);
CREATE INDEX asset_stop_idx
    ON pilot.asset(stop_id);

-- Prevent the feature subtype from disagreeing with the base feature type.
CREATE FUNCTION pilot.enforce_feature_subtype()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
    expected_type text;
BEGIN
    expected_type := TG_ARGV[0];

    IF NOT EXISTS (
        SELECT 1 FROM pilot.inventory_feature
         WHERE feature_id = NEW.feature_id
           AND feature_type = expected_type
    ) THEN
        RAISE EXCEPTION 'Feature % must exist with feature_type %',
          NEW.feature_id, expected_type;
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER stop_feature_type_check
BEFORE INSERT OR UPDATE OF feature_id ON pilot.stop
FOR EACH ROW EXECUTE FUNCTION pilot.enforce_feature_subtype('stop');

CREATE TRIGGER asset_feature_type_check
BEFORE INSERT OR UPDATE OF feature_id ON pilot.asset
FOR EACH ROW EXECUTE FUNCTION pilot.enforce_feature_subtype('asset');

-- Note: PostGIS installation, SQL execution, CRS authority review, ingestion,
-- GeoPackage export, topology rules and independent positional validation
-- are intentionally separate implementation/verification steps.
