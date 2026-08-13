import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import time 
import json 
from typing import Dict, Any 
from config.settings import load_settings 
from llm.client import OllamaLuna 
from config.logging_config import logger

class BenchmarkResult:
    def __init__(self, test_name: str, duration: float, tps: float, success: bool, output: str):
        self.test_name = test_name
        self.duration = duration 
        self.tps = tps 
        self.success = success
        self.output = output

class LLMBenchmark:
    def __init__(self):
        self.settings = load_settings()
        self.llm = OllamaLuna()

    def run_speed_test(self) -> Dict[str, Any]:
        prompt = "Explain quantum computing in 3 paragraphs."
        messages = [{"role": "user", "content": prompt}]

        start_time = time.perf_counter()
        first_token_time = None 
        full_text = ""
        chunk_count = 0

        for chunk in self.llm.stream_chat(messages):
            if first_token_time is None:
                first_token_time = time.perf_counter()  
            full_text += chunk
            chunk_count += 1

        end_time = time.perf_counter()
        total_duration = end_time - start_time 
        ttft = (first_token_time - start_time) if first_token_time else 0.0
        tps = chunk_count / total_duration if total_duration > 0 else 0.0
        return{
            "test_name": "Speed & Throughput",
            "duration_sec": round(total_duration, 2),
            "ttft_sec": round(ttft, 2),
            "tps": round(tps, 2),
            "chunks_generated": chunk_count,
            "output_sample": full_text[:100] + "..."
        }
    
    def run_reasoning_test(self) -> Dict[str, Any]:
        prompt = "If it takes 5 shirts 5 hours to dry in the sun, how long does it take 10 shirts to dry? Explain in 1 sentence."
        messages = [{"role": "user", "content": prompt}]

        start_time = time.perf_counter()
        full_text = ""

        for chunk in self.llm.stream_chat(messages):
            if "Error: " in chunk:
                return{
                    "test_name": "Reasoning",
                    "duration_sec": round(time.perf_counter()-start_time,2),
                    "success":False,
                    "reason":chunk
                }
            full_text+=chunk

        end_time = time.perf_counter()
        response = full_text.strip()
        correct_answer = "5 hours"  
        is_correct = correct_answer.lower() in response.lower()

        return {
            "test_name": "Reasoning",
            "duration_sec": round(end_time - start_time,2),
            "success":is_correct,
            "output": response,
            "prompt":prompt
        }

    def run_structured_test(self) -> Dict[str, Any]:
        prompt = "Extract into valid JSON with keys 'name' and 'age': 'Hi, I am Alex and I am 28 years old.' Return ONLY JSON."
        messages = [{"role": "user", "content": prompt}]

        start_time = time.perf_counter()
        full_text = ""

        for chunk in self.llm.stream_chat(messages):
            full_text+= chunk
        end_time = time.perf_counter()
        response = full_text.strip()

        is_valid_json = False
        try:
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            json.loads(response)
            is_valid_json = True
        except json.JSONDecodeError:
            is_valid_json = False
        
        return {
            "test_name": "Structured Output",
            "duration_sec": round(end_time - start_time,2),
            "success":is_valid_json,
            "output": response,
            "prompt":prompt
        }

    def run_all(self):
        logger.info("=" * 42)
        logger.info(f"   LUNA LLM BENCHMARK ({self.llm.model})")
        logger.info("=" * 42)
        
        logger.info("Running Test 1/3: Speed & Throughput...")
        speed = self.run_speed_test()
        logger.info(f"  ➜ TPS: {speed['tps']} tokens/sec")
        logger.info(f"  ➜ TTFT: {speed['ttft_sec']} sec")
        logger.info(f"  ➜ Duration: {speed['duration_sec']} sec")
        
        logger.info("Running Test 2/3: Reasoning...")
        reasoning = self.run_reasoning_test()
        logger.info(f"  ➜ Passed: {reasoning['success']}")
        logger.info(f"  ➜ Output: {reasoning['output']}")
        
        logger.info("Running Test 3/3: Structured Output...")
        structured = self.run_structured_test()
        logger.info(f"  ➜ Passed: {structured['success']}")
        logger.info(f"  ➜ Output: {structured['output']}")
        
if __name__ == "__main__":
    bm = LLMBenchmark()
    bm.run_all()
