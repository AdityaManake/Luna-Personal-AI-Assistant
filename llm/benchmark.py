import time 
import json 
import psutil 
from typing import Dict, Any 
from config.settings import load_settings 
from llm.client import OllamaLuna 

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

