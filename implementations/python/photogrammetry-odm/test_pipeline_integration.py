"""Synthetic handoff integration test; never represents a live ODM rehearsal.

Exercises acquisition verification through evidence dossier assembly while
keeping processing unexecuted and independent checkpoint acceptance unresolved.
"""
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from delivery_dossier import create_delivery_bundle
from output_inspection import inspect_outputs
from processing_run import create_run_record
from project_preflight import build_preflight
from validation_evidence import build_validation_record
from verify_acquisition import verify_manifest


class SyntheticPipelineIntegrationTests(unittest.TestCase):
    def test_snapshot_to_review_dossier_preserves_open_gates(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            snapshot = root / "snapshot"
            source = snapshot / "datasets" / "drone_heig_2019" / "images" / "frame.jpg"
            source.parent.mkdir(parents=True)
            source_bytes = b"synthetic image bytes; not a real photograph"
            source.write_bytes(source_bytes)

            acquisition_manifest = {
                "resolved_revision": "a" * 40,
                "selected_path": "datasets/drone_heig_2019",
                "file_count": 1,
                "files": [{
                    "path": "datasets/drone_heig_2019/images/frame.jpg",
                    "size_bytes": len(source_bytes),
                    "sha256": hashlib.sha256(source_bytes).hexdigest(),
                }],
            }
            acquisition_path = snapshot / "acquisition-provenance.json"
            acquisition_path.write_text(json.dumps(acquisition_manifest), encoding="utf-8")
            acquisition_report = verify_manifest(acquisition_path)
            self.assertEqual(acquisition_report["status"], "verified")
            acquisition_report_path = snapshot / "acquisition-verification.json"
            acquisition_report_path.write_text(json.dumps(acquisition_report), encoding="utf-8")

            # Work on a separate copy: the acquired snapshot remains unchanged.
            project = root / "working-project"
            (project / "images").mkdir(parents=True)
            shutil.copy2(source, project / "images" / "frame.jpg")
            (project / "model.obj").write_text(
                "v 0 0 0\nv 1 0 0\nv 0 1 0\nf 1 2 3\n",
                encoding="utf-8",
            )

            image = "opendronemap/odm:3.6.1@sha256:" + "a" * 64
            manifest = {
                "schema_version": "1.0",
                "project_id": "SYNTHETIC-PIPELINE-001",
                "title": "Synthetic integration fixture",
                "intended_use": "Exercise the handoff only; not a survey or accuracy test",
                "data_sources": [],
                "dataset": {
                    "project_directory": str(project),
                    "expected_image_count": 1,
                },
                "processing": {
                    "engine": "OpenDroneMap",
                    "container_image": image,
                    "arguments": [],
                },
                "validation": {
                    "horizontal_crs": "Synthetic test CRS",
                    "vertical_reference": "Synthetic test vertical reference",
                    "coordinate_units": "metres",
                    "independent_checkpoints": False,
                    "reference_uncertainty": "Not established; synthetic fixture",
                    "acceptance_criteria": "No accuracy acceptance in this synthetic integration test",
                },
                "deliverables": ["model.obj"],
            }
            manifest_path = root / "project-manifest.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            image_audit = {
                "image_count": 1,
                "image_count_matches_expectation": True,
                "pillow_available": True,
                "valid_images": 1,
                "invalid_images": 0,
                "images": [],
            }
            with patch("project_preflight.inspect_images", return_value=image_audit):
                preflight = build_preflight(manifest, manifest_path)
            self.assertEqual(preflight["status"], "review_required")
            self.assertFalse(preflight["processing_handoff"]["executed"])
            preflight_path = root / "preflight-report.json"
            preflight_path.write_text(json.dumps(preflight), encoding="utf-8")

            run_dir = root / "run-records" / "synthetic-run"
            run = create_run_record(project, image, [], run_dir)
            self.assertEqual(run["status"], "prepared")
            self.assertFalse(run["processing"]["executed"])
            run_path = run_dir / "processing-run.json"

            output = inspect_outputs(project, ["model.obj"])
            self.assertEqual(output["status"], "inspected")
            output_path = root / "output-inspection.json"
            output_path.write_text(json.dumps(output), encoding="utf-8")

            checkpoints = root / "checkpoints.csv"
            checkpoints.write_text(
                "point_id,ref_x,ref_y,ref_z,model_x,model_y,model_z\n"
                "A,0,0,0,1,2,3\nB,10,10,10,11,12,13\n",
                encoding="utf-8",
            )
            context = {
                "project_id": manifest["project_id"],
                "processing_run_id": run["run_id"],
                "horizontal_crs": "Synthetic test CRS",
                "vertical_reference": "Synthetic test vertical reference",
                "coordinate_units": "metres",
                "reference_uncertainty": "Not established; synthetic fixture",
                "sample_design": "Synthetic rows only; not an independent sample",
                "checkpoint_independence": False,
                "acceptance_criteria": "No project acceptance criteria in this synthetic test",
                "acceptance_decision": "pending",
            }
            validation = build_validation_record(
                checkpoints, context, run_record=run_path,
                output_inspection=output_path,
            )
            self.assertEqual(validation["evidence_status"], "not_assessable")
            validation_path = root / "validation-evidence.json"
            validation_path.write_text(json.dumps(validation), encoding="utf-8")

            archive = root / "delivery-dossier.zip"
            bundled = create_delivery_bundle(
                acquisition_path, acquisition_report_path, manifest_path,
                preflight_path, run_path, output_path, validation_path, archive,
            )
            self.assertEqual(bundled["dossier"]["status"], "review_required")
            self.assertFalse(bundled["dossier"]["release_authorized"])
            self.assertEqual(
                bundled["dossier"]["observed_statuses"]["processing_run"], "prepared"
            )
            self.assertEqual(
                bundled["dossier"]["observed_statuses"]["checkpoint_evidence"],
                "not_assessable",
            )
            self.assertEqual(source.read_bytes(), source_bytes)


if __name__ == "__main__":
    unittest.main()
