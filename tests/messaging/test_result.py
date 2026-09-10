# Copyright Axis Communications AB.
#
# For a full list of individual contributors, please see the commit history.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for the shutdown Result conclusion and verdict validation."""

import json
import unittest

from pydantic import ValidationError

from etos_lib.messaging.events import Shutdown
from etos_lib.messaging.types import Conclusion, Result, Verdict


class TestResultValidation(unittest.TestCase):
    """Test that Result validates conclusion and verdict against the allowed values."""

    def test_valid_result_serializes_string_values(self):
        """Test that a valid Result serializes conclusion and verdict as their string values."""
        data = json.loads(Result(conclusion="Successful", verdict="Passed").model_dump_json())
        self.assertEqual(data["conclusion"], "Successful")
        self.assertEqual(data["verdict"], "Passed")

    def test_enum_members_are_accepted(self):
        """Test that enum members can be used directly."""
        result = Result(conclusion=Conclusion.FAILED, verdict=Verdict.FAILED)
        self.assertEqual(result.conclusion, Conclusion.FAILED)
        self.assertEqual(result.verdict, Verdict.FAILED)

    def test_invalid_conclusion_is_rejected(self):
        """Test that a conclusion outside the allowed values raises a ValidationError."""
        with self.assertRaises(ValidationError):
            Result(conclusion="Great", verdict="Passed")

    def test_invalid_verdict_is_rejected(self):
        """Test that a verdict outside the allowed values raises a ValidationError."""
        with self.assertRaises(ValidationError):
            Result(conclusion="Successful", verdict="Winner")

    def test_shutdown_serialization_and_str(self):
        """Test that a Shutdown serializes and renders the values without the enum prefix."""
        shutdown = Shutdown(
            data=Result(conclusion="Successful", verdict="Passed", description="ok")
        )
        data = json.loads(shutdown.model_dump_json())["data"]
        self.assertEqual(data["conclusion"], "Successful")
        self.assertEqual(data["verdict"], "Passed")
        self.assertIn("conclusion=Successful", str(shutdown))
        self.assertIn("verdict=Passed", str(shutdown))


if __name__ == "__main__":
    unittest.main()
