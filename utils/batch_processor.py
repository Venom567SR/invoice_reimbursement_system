from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.logger import app_logger
from typing import Callable, List

def process_invoices_in_parallel(
    func: Callable,
    invoice_paths: List[str],
    max_workers: int = 4
):
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_path = {executor.submit(func, path): path for path in invoice_paths}

        for future in as_completed(future_to_path):
            path = future_to_path[future]
            try:
                results.append(future.result())
            except Exception as e:
                app_logger.error(f"Failed to process {path}: {e}")
    return results