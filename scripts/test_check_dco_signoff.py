import unittest

from check_dco_signoff import audit_messages, has_dco_signoff


class DcoSignoffTests(unittest.TestCase):
    def test_accepts_standard_signoff_trailer(self):
        self.assertTrue(
            has_dco_signoff(
                "Add a method\n\nSigned-off-by: Example Author <author@example.org>\n"
            )
        )

    def test_accepts_signoff_after_other_trailers(self):
        self.assertTrue(
            has_dco_signoff(
                "Fix edge case\n\nReviewed-by: Reviewer <review@example.org>\n"
                "Signed-off-by: Example Author <author@example.org>\n"
            )
        )

    def test_rejects_missing_signoff(self):
        self.assertFalse(has_dco_signoff("Add a method\n\nReviewed-by: Reviewer"))

    def test_rejects_malformed_email(self):
        self.assertFalse(has_dco_signoff("Add a method\n\nSigned-off-by: Name <no-email>"))

    def test_audit_reports_only_unsigned_commits(self):
        commits = [
            ("abc123456789", "Signed change", "Signed-off-by: A <a@example.org>"),
            ("def123456789", "Unsigned change", "No trailer"),
        ]
        self.assertEqual(
            audit_messages(commits),
            ["def123456789 Unsigned change"],
        )


if __name__ == "__main__":
    unittest.main()
