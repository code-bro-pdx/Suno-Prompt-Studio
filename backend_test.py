"""Backend API tests for Suno Song Prompt Generator - Iteration 2
Tests the new async job pattern with polling.
"""
import requests
import sys
import time
from datetime import datetime

BASE_URL = "https://melody-prompt-hub-1.preview.emergentagent.com/api"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

class APITester:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0

    def log(self, message, color=Colors.BLUE):
        print(f"{color}{message}{Colors.END}")

    def test(self, name, method, endpoint, expected_status, data=None, timeout=10):
        """Run a single API test"""
        url = f"{BASE_URL}/{endpoint}"
        self.tests_run += 1
        
        self.log(f"\n🔍 Test {self.tests_run}: {name}")
        
        try:
            if method == 'GET':
                response = requests.get(url, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, timeout=timeout)
            elif method == 'DELETE':
                response = requests.delete(url, timeout=timeout)
            
            success = response.status_code == expected_status
            
            if success:
                self.tests_passed += 1
                self.log(f"✅ PASSED - Status: {response.status_code}", Colors.GREEN)
                try:
                    return True, response.json()
                except:
                    return True, {}
            else:
                self.tests_failed += 1
                self.log(f"❌ FAILED - Expected {expected_status}, got {response.status_code}", Colors.RED)
                try:
                    self.log(f"   Response: {response.text[:200]}", Colors.YELLOW)
                except:
                    pass
                return False, {}
                
        except requests.exceptions.Timeout:
            self.tests_failed += 1
            self.log(f"❌ FAILED - Request timeout after {timeout}s", Colors.RED)
            return False, {}
        except Exception as e:
            self.tests_failed += 1
            self.log(f"❌ FAILED - Error: {str(e)}", Colors.RED)
            return False, {}

    def poll_job(self, job_id, max_wait=180, poll_interval=3):
        """Poll a job until it's done or errors out"""
        self.log(f"\n⏳ Polling job {job_id} (max {max_wait}s, interval {poll_interval}s)")
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            try:
                response = requests.get(f"{BASE_URL}/jobs/{job_id}", timeout=10)
                if response.status_code != 200:
                    self.log(f"❌ Job polling failed with status {response.status_code}", Colors.RED)
                    return None
                
                job = response.json()
                status = job.get('status')
                elapsed = int(time.time() - start_time)
                
                self.log(f"   [{elapsed}s] Status: {status}")
                
                if status == 'done':
                    self.log(f"✅ Job completed in {elapsed}s", Colors.GREEN)
                    return job
                elif status == 'error':
                    error = job.get('error', 'Unknown error')
                    self.log(f"❌ Job failed: {error}", Colors.RED)
                    return job
                
                time.sleep(poll_interval)
                
            except Exception as e:
                self.log(f"❌ Polling error: {str(e)}", Colors.RED)
                return None
        
        self.log(f"❌ Job timeout after {max_wait}s", Colors.RED)
        return None

    def print_summary(self):
        print(f"\n{'='*70}")
        print(f"TEST SUMMARY")
        print(f"{'='*70}")
        print(f"Total tests: {self.tests_run}")
        print(f"{Colors.GREEN}Passed: {self.tests_passed}{Colors.END}")
        print(f"{Colors.RED}Failed: {self.tests_failed}{Colors.END}")
        percentage = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"Success rate: {percentage:.1f}%")
        print(f"{'='*70}\n")


def main():
    tester = APITester()
    
    print(f"\n{'='*70}")
    print(f"SUNO SONG PROMPT GENERATOR - BACKEND API TESTS")
    print(f"Testing async job pattern (Iteration 2)")
    print(f"Base URL: {BASE_URL}")
    print(f"{'='*70}\n")
    
    # ========== BASIC ENDPOINTS ==========
    tester.log("\n" + "="*70, Colors.BLUE)
    tester.log("SECTION 1: BASIC ENDPOINTS", Colors.BLUE)
    tester.log("="*70, Colors.BLUE)
    
    # Test 1: Health check
    tester.test("Health check", "GET", "", 200)
    
    # Test 2: Knowledge endpoint
    success, knowledge = tester.test("Get knowledge taxonomies", "GET", "knowledge", 200)
    if success:
        required_keys = ['mother_genres', 'italian_tempos', 'vocal_ranges', 'banned_words', 'scale_presets']
        missing = [k for k in required_keys if k not in knowledge]
        if missing:
            tester.log(f"   ⚠️  Missing keys: {missing}", Colors.YELLOW)
        else:
            tester.log(f"   ✓ All required taxonomies present", Colors.GREEN)
    
    # ========== ASYNC JOB PATTERN - GENERATE ==========
    tester.log("\n" + "="*70, Colors.BLUE)
    tester.log("SECTION 2: ASYNC JOB PATTERN - /api/generate", Colors.BLUE)
    tester.log("="*70, Colors.BLUE)
    
    # Test 3: POST /api/generate returns job_id immediately
    concept = "uplifting indie folk duet about a found family, 118 BPM, female mezzo-soprano, stomp-clap percussion, wet mix"
    success, generate_response = tester.test(
        "POST /api/generate (async) - returns job_id",
        "POST",
        "generate",
        200,
        data={"concept": concept, "auto_repair": True}
    )
    
    generate_job_id = None
    if success:
        generate_job_id = generate_response.get('job_id')
        status = generate_response.get('status')
        if generate_job_id and status == 'queued':
            tester.log(f"   ✓ Got job_id: {generate_job_id}, status: {status}", Colors.GREEN)
        else:
            tester.log(f"   ⚠️  Unexpected response format: {generate_response}", Colors.YELLOW)
    
    # Test 4: Poll the generate job
    if generate_job_id:
        job_result = tester.poll_job(generate_job_id, max_wait=180, poll_interval=3)
        if job_result and job_result.get('status') == 'done':
            tester.tests_passed += 1
            tester.log("✅ Generate job completed successfully", Colors.GREEN)
            
            # Validate result structure
            result = job_result.get('result', {})
            if 'payload' in result and 'validation' in result:
                tester.log("   ✓ Result has payload and validation", Colors.GREEN)
                
                payload = result['payload']
                validation = result['validation']
                
                # Check style_prompt
                style_prompt = payload.get('style_prompt', '')
                style_len = len(style_prompt)
                tester.log(f"   ✓ Style prompt length: {style_len} chars", Colors.GREEN)
                
                # Check validation
                errors = validation.get('errors', [])
                warnings = validation.get('warnings', [])
                tester.log(f"   ✓ Validation: {len(errors)} errors, {len(warnings)} warnings", Colors.GREEN)
                
                if errors:
                    tester.log(f"   ⚠️  Validation errors: {errors}", Colors.YELLOW)
            else:
                tester.log(f"   ⚠️  Result missing payload or validation", Colors.YELLOW)
        else:
            tester.tests_failed += 1
            tester.log("❌ Generate job did not complete successfully", Colors.RED)
    
    # ========== ASYNC JOB PATTERN - ASSEMBLE ==========
    tester.log("\n" + "="*70, Colors.BLUE)
    tester.log("SECTION 3: ASYNC JOB PATTERN - /api/assemble", Colors.BLUE)
    tester.log("="*70, Colors.BLUE)
    
    # Test 5: POST /api/assemble returns job_id immediately
    form_payload = {
        "era": "2020s",
        "bpm": 120,
        "italian_tempo": "Allegro",
        "time_signature": "4/4",
        "mother_genre": "Pop",
        "subgenres": [{"name": "Dance-Pop", "weight_percent": 70}],
        "mood": "Bright",
        "instruments": [{"type": "Synth", "model": "Juno-106", "play_method": "pads"}],
        "vocal_gender": "Female",
        "vocal_range": "Female Mezzo-Soprano A3-A5",
        "vocal_textures": ["warm"],
        "mix": "Wet",
        "section_order": ["[Intro]", "[Verse 1]", "[Chorus]", "[Outro]"],
        "exclude_eras": ["1980s"],
        "exclude_genres": ["Metal"],
        "lyrical_world": ""
    }
    
    success, assemble_response = tester.test(
        "POST /api/assemble (async) - returns job_id",
        "POST",
        "assemble",
        200,
        data={"form": form_payload, "auto_repair": True}
    )
    
    assemble_job_id = None
    if success:
        assemble_job_id = assemble_response.get('job_id')
        status = assemble_response.get('status')
        if assemble_job_id and status == 'queued':
            tester.log(f"   ✓ Got job_id: {assemble_job_id}, status: {status}", Colors.GREEN)
        else:
            tester.log(f"   ⚠️  Unexpected response format: {assemble_response}", Colors.YELLOW)
    
    # Test 6: Poll the assemble job
    if assemble_job_id:
        job_result = tester.poll_job(assemble_job_id, max_wait=180, poll_interval=3)
        if job_result and job_result.get('status') == 'done':
            tester.tests_passed += 1
            tester.log("✅ Assemble job completed successfully", Colors.GREEN)
            
            result = job_result.get('result', {})
            if 'payload' in result and 'validation' in result:
                tester.log("   ✓ Result has payload and validation", Colors.GREEN)
            else:
                tester.log(f"   ⚠️  Result missing payload or validation", Colors.YELLOW)
        else:
            tester.tests_failed += 1
            tester.log("❌ Assemble job did not complete successfully", Colors.RED)
    
    # ========== JOB ENDPOINT TESTS ==========
    tester.log("\n" + "="*70, Colors.BLUE)
    tester.log("SECTION 4: JOB ENDPOINT TESTS", Colors.BLUE)
    tester.log("="*70, Colors.BLUE)
    
    # Test 7: GET /api/jobs/{nonexistent-id} returns 404
    tester.test(
        "GET /api/jobs/{nonexistent-id} returns 404",
        "GET",
        "jobs/nonexistent-job-id-12345",
        404
    )
    
    # ========== SYNC VARIANTS ==========
    tester.log("\n" + "="*70, Colors.BLUE)
    tester.log("SECTION 5: SYNC VARIANTS (for short calls)", Colors.BLUE)
    tester.log("="*70, Colors.BLUE)
    
    # Test 8: POST /api/generate/sync (with short concept)
    short_concept = "happy pop song, 120 BPM"
    success, sync_result = tester.test(
        "POST /api/generate/sync (short concept)",
        "POST",
        "generate/sync",
        200,
        data={"concept": short_concept, "auto_repair": True},
        timeout=90
    )
    if success and 'payload' in sync_result:
        tester.log("   ✓ Sync generate returned payload directly", Colors.GREEN)
    
    # ========== FILL-FORM ==========
    tester.log("\n" + "="*70, Colors.BLUE)
    tester.log("SECTION 6: FILL-FORM (Hybrid helper)", Colors.BLUE)
    tester.log("="*70, Colors.BLUE)
    
    # Test 9: POST /api/fill-form
    success, fill_result = tester.test(
        "POST /api/fill-form",
        "POST",
        "fill-form",
        200,
        data={"concept": "energetic rock song about freedom"},
        timeout=60
    )
    if success and 'form' in fill_result:
        form = fill_result['form']
        tester.log(f"   ✓ Returned structured form with {len(form)} fields", Colors.GREEN)
    
    # ========== VALIDATION ==========
    tester.log("\n" + "="*70, Colors.BLUE)
    tester.log("SECTION 7: VALIDATION", Colors.BLUE)
    tester.log("="*70, Colors.BLUE)
    
    # Test 10: POST /api/validate with intentional errors
    bad_payload = {
        "title": "Test Song",
        "style_prompt": "x" * 1500,  # Too long
        "lyrics": "[Verse 1]\nI love drugs and violence\nShooting guns all day",  # Banned words
        "structure_rhyme_map": {
            "total_bars": 32,
            "sections": [
                {"label": "Verse 1", "bars": 8},
                {"label": "Chorus", "bars": 8}
                # Sum is 16, not 32 - mismatch
            ]
        }
    }
    
    success, validation = tester.test(
        "POST /api/validate (with intentional errors)",
        "POST",
        "validate",
        200,
        data={"payload": bad_payload}
    )
    
    if success:
        errors = validation.get('errors', [])
        if len(errors) >= 2:
            tester.log(f"   ✓ Correctly caught {len(errors)} errors", Colors.GREEN)
            for err in errors:
                code = err.get('code', 'unknown')
                msg = err.get('message', '')
                tester.log(f"     - {code}: {msg[:80]}", Colors.YELLOW)
        else:
            tester.log(f"   ⚠️  Expected multiple errors, got {len(errors)}", Colors.YELLOW)
    
    # ========== LIBRARY CRUD ==========
    tester.log("\n" + "="*70, Colors.BLUE)
    tester.log("SECTION 8: LIBRARY CRUD", Colors.BLUE)
    tester.log("="*70, Colors.BLUE)
    
    # Test 11: POST /api/library (create)
    library_item = {
        "title": f"Test Item {datetime.now().strftime('%H%M%S')}",
        "concept": "test concept",
        "mode": "ai",
        "payload": {"title": "Test", "style_prompt": "test"},
        "validation": {"errors": [], "warnings": []}
    }
    
    success, created = tester.test(
        "POST /api/library (create)",
        "POST",
        "library",
        200,
        data=library_item
    )
    
    item_id = None
    if success:
        item_id = created.get('id')
        tester.log(f"   ✓ Created item with id: {item_id}", Colors.GREEN)
    
    # Test 12: GET /api/library (list)
    success, library_list = tester.test(
        "GET /api/library (list)",
        "GET",
        "library",
        200
    )
    if success and isinstance(library_list, list):
        tester.log(f"   ✓ Retrieved {len(library_list)} items", Colors.GREEN)
    
    # Test 13: GET /api/library/{id} (get one)
    if item_id:
        success, item = tester.test(
            f"GET /api/library/{item_id} (get one)",
            "GET",
            f"library/{item_id}",
            200
        )
        if success and item.get('id') == item_id:
            tester.log(f"   ✓ Retrieved correct item", Colors.GREEN)
    
    # Test 14: DELETE /api/library/{id}
    if item_id:
        success, delete_result = tester.test(
            f"DELETE /api/library/{item_id}",
            "DELETE",
            f"library/{item_id}",
            200
        )
        if success and delete_result.get('deleted'):
            tester.log(f"   ✓ Item deleted successfully", Colors.GREEN)
    
    # ========== SUMMARY ==========
    tester.print_summary()
    
    # Return exit code
    return 0 if tester.tests_failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
