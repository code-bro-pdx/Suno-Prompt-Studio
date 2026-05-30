"""Backend API tests for Suno Song Prompt Generator.

Tests all endpoints using the public REACT_APP_BACKEND_URL.
LLM calls take 15-45 seconds; using 120 second timeout for generate/assemble.
"""
import requests
import sys
import time
from typing import Dict, Any, Optional

# Public endpoint from frontend/.env
BASE_URL = "https://melody-prompt-hub-1.preview.emergentagent.com/api"
TIMEOUT = 120  # 120 seconds for LLM calls


class SunoAPITester:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.library_id = None  # Store created library item ID

    def log(self, emoji: str, message: str):
        """Print formatted log message."""
        print(f"{emoji} {message}")

    def test(self, name: str, method: str, endpoint: str, expected_status: int,
             data: Optional[Dict[str, Any]] = None, timeout: int = 10) -> tuple[bool, Any]:
        """Run a single API test."""
        url = f"{BASE_URL}{endpoint}"
        self.tests_run += 1
        self.log("🔍", f"Testing {name}...")
        
        try:
            if method == "GET":
                response = requests.get(url, timeout=timeout)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=timeout)
            elif method == "DELETE":
                response = requests.delete(url, timeout=timeout)
            else:
                self.log("❌", f"Unknown method: {method}")
                return False, None

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                self.log("✅", f"Passed - Status: {response.status_code}")
                try:
                    return True, response.json()
                except:
                    return True, response.text
            else:
                self.log("❌", f"Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    self.log("📄", f"Response: {response.json()}")
                except:
                    self.log("📄", f"Response: {response.text[:200]}")
                return False, None

        except requests.exceptions.Timeout:
            self.log("❌", f"Failed - Request timed out after {timeout}s")
            return False, None
        except Exception as e:
            self.log("❌", f"Failed - Error: {str(e)}")
            return False, None

    def run_all_tests(self):
        """Execute all backend tests in sequence."""
        self.log("🚀", "Starting Suno API Backend Tests")
        self.log("🌐", f"Base URL: {BASE_URL}")
        print()

        # Test 1: Health check
        success, data = self.test("Health Check", "GET", "/", 200)
        if success and data:
            self.log("📋", f"Health response: {data}")
        print()

        # Test 2: Knowledge endpoint
        success, data = self.test("Knowledge Endpoint", "GET", "/knowledge", 200)
        if success and data:
            self.log("📋", f"Knowledge keys: {list(data.keys())}")
            # Verify expected keys
            expected_keys = [
                "mother_genres", "italian_tempos", "vocal_ranges", "scale_presets",
                "banned_words", "section_meta_tags"
            ]
            missing = [k for k in expected_keys if k not in data]
            if missing:
                self.log("⚠️", f"Missing expected keys: {missing}")
            else:
                self.log("✅", "All expected knowledge keys present")
        print()

        # Test 3: POST /generate (AI Mode) - with 120s timeout
        concept = "uplifting indie folk duet about a found family, stomp-clap percussion, 118 BPM, female mezzo-soprano"
        self.log("⏳", "Generating prompt (may take 15-45 seconds)...")
        success, data = self.test(
            "Generate (AI Mode)",
            "POST",
            "/generate",
            200,
            data={"concept": concept, "auto_repair": True},
            timeout=TIMEOUT
        )
        if success and data:
            payload = data.get("payload", {})
            validation = data.get("validation", {})
            
            # Check payload structure
            self.log("📋", f"Payload keys: {list(payload.keys())}")
            
            # Check style_prompt length
            style_prompt = payload.get("style_prompt", "")
            self.log("📏", f"Style Prompt length: {len(style_prompt)} chars (max 1000)")
            if len(style_prompt) > 1000:
                self.log("❌", "Style Prompt exceeds 1000 characters!")
            
            # Check Italian tempo presence
            srm = payload.get("structure_rhyme_map", {})
            italian_tempo = srm.get("italian_tempo", "")
            if italian_tempo:
                self.log("✅", f"Italian tempo present: {italian_tempo}")
            else:
                self.log("❌", "Italian tempo missing!")
            
            # Check bar math
            total_bars = srm.get("total_bars", 0)
            sections = srm.get("sections", [])
            bars_sum = sum(s.get("bars", 0) for s in sections)
            self.log("🔢", f"Bar math: {bars_sum} (sum) vs {total_bars} (total)")
            if bars_sum == total_bars:
                self.log("✅", "Bar math correct")
            else:
                self.log("❌", f"Bar math mismatch!")
            
            # Check validation
            errors = validation.get("errors", [])
            self.log("🔍", f"Validation errors: {len(errors)}")
            if errors:
                for err in errors:
                    self.log("⚠️", f"  - {err.get('message')}")
            else:
                self.log("✅", "No validation errors (auto-repair worked)")
        print()

        # Test 4: POST /fill-form (Hybrid helper)
        concept_form = "uplifting indie folk duet, 118 BPM, female mezzo-soprano"
        self.log("⏳", "Filling form from concept (may take 10-30 seconds)...")
        success, data = self.test(
            "Fill Form (Hybrid)",
            "POST",
            "/fill-form",
            200,
            data={"concept": concept_form},
            timeout=60
        )
        if success and data:
            form = data.get("form", {})
            self.log("📋", f"Form keys: {list(form.keys())}")
            # Check expected form fields
            expected_form_keys = ["era", "bpm", "italian_tempo", "mother_genre", "subgenres"]
            missing = [k for k in expected_form_keys if k not in form]
            if missing:
                self.log("⚠️", f"Missing expected form keys: {missing}")
            else:
                self.log("✅", "All expected form keys present")
        print()

        # Test 5: POST /assemble (Form Mode)
        form_payload = {
            "era": "2010s",
            "bpm": 118,
            "italian_tempo": "Moderato",
            "time_signature": "4/4",
            "mother_genre": "Folk",
            "subgenres": [{"name": "Indie Folk", "weight_percent": 70}, {"name": "Americana", "weight_percent": 30}],
            "mood": "uplifting, warm",
            "instruments": [
                {"type": "Acoustic Guitar", "model": "Martin D-28", "play_method": "fingerpicking"},
                {"type": "Stomp Box", "model": "DIY", "play_method": "stomp-clap"}
            ],
            "vocal_gender": "Female",
            "vocal_range": "Female Mezzo-Soprano A3-A5",
            "vocal_textures": ["warm", "airy"],
            "mix": "Dry",
            "section_order": ["Intro", "Verse 1", "Pre-Chorus", "Chorus", "Verse 2", "Chorus", "Bridge", "Final Chorus", "Outro"],
            "exclude_eras": ["1980s"],
            "exclude_genres": ["EDM"],
            "lyrical_world": "narrative, found family theme"
        }
        self.log("⏳", "Assembling prompt from form (may take 15-45 seconds)...")
        success, data = self.test(
            "Assemble (Form Mode)",
            "POST",
            "/assemble",
            200,
            data={"form": form_payload, "auto_repair": True},
            timeout=TIMEOUT
        )
        if success and data:
            payload = data.get("payload", {})
            validation = data.get("validation", {})
            self.log("📋", f"Assembled payload keys: {list(payload.keys())}")
            errors = validation.get("errors", [])
            self.log("🔍", f"Validation errors: {len(errors)}")
            if errors:
                for err in errors:
                    self.log("⚠️", f"  - {err.get('message')}")
        print()

        # Test 6: POST /validate with intentional errors
        bad_payload = {
            "style_prompt": "x" * 1100,  # Intentionally too long
            "lyrics": "Walking through the midnight streets with shadows all around",  # Contains banned words
            "structure_rhyme_map": {
                "total_bars": 50,
                "sections": [{"bars": 8}, {"bars": 8}]  # Sum doesn't match
            }
        }
        success, data = self.test(
            "Validate (with intentional errors)",
            "POST",
            "/validate",
            200,
            data={"payload": bad_payload}
        )
        if success and data:
            errors = data.get("errors", [])
            self.log("🔍", f"Validation errors found: {len(errors)}")
            error_codes = [e.get("code") for e in errors]
            expected_errors = ["style_prompt_too_long", "banned_words_in_lyrics", "bars_mismatch"]
            found_expected = [code for code in expected_errors if code in error_codes]
            self.log("📋", f"Expected error codes found: {found_expected}")
            if len(found_expected) >= 2:
                self.log("✅", "Validation correctly caught intentional errors")
            else:
                self.log("⚠️", f"Expected errors {expected_errors}, got {error_codes}")
        print()

        # Test 7: POST /library (create)
        library_item = {
            "title": "Test Folk Duet",
            "concept": concept,
            "mode": "ai",
            "payload": {"style_prompt": "Test prompt", "lyrics": "Test lyrics"},
            "validation": {"errors": [], "warnings": []}
        }
        success, data = self.test(
            "Library Create",
            "POST",
            "/library",
            200,
            data=library_item
        )
        if success and data:
            self.library_id = data.get("id")
            self.log("📋", f"Created library item with ID: {self.library_id}")
        print()

        # Test 8: GET /library (list)
        success, data = self.test("Library List", "GET", "/library", 200)
        if success and data:
            self.log("📋", f"Library contains {len(data)} items")
            if self.library_id:
                found = any(item.get("id") == self.library_id for item in data)
                if found:
                    self.log("✅", "Created item found in library list")
                else:
                    self.log("❌", "Created item NOT found in library list")
        print()

        # Test 9: GET /library/{id} (get one)
        if self.library_id:
            success, data = self.test(
                "Library Get One",
                "GET",
                f"/library/{self.library_id}",
                200
            )
            if success and data:
                self.log("📋", f"Retrieved item title: {data.get('title')}")
            print()

        # Test 10: DELETE /library/{id}
        if self.library_id:
            success, data = self.test(
                "Library Delete",
                "DELETE",
                f"/library/{self.library_id}",
                200
            )
            if success and data:
                self.log("✅", f"Deleted item {self.library_id}")
            print()

        # Final summary
        print("=" * 60)
        self.log("📊", f"Tests passed: {self.tests_passed}/{self.tests_run}")
        print("=" * 60)
        
        return 0 if self.tests_passed == self.tests_run else 1


def main():
    tester = SunoAPITester()
    return tester.run_all_tests()


if __name__ == "__main__":
    sys.exit(main())
