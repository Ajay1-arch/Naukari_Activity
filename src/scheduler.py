#!/usr/bin/env python3
"""
Scheduler for Naukri Automation
Runs the script on a schedule (hourly or at random intervals)
Tracks progress and statistics for all runs
"""

import time
import random
import logging
import json
from datetime import datetime
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from config_loader import get_config


class NaukriScheduler:
    """Manages scheduling for Naukri automation"""
    
    def __init__(self):
        self.config = get_config()
        self.logger = self._setup_logger()
        self.running = True
        self.progress_file = None
        self.progress_data = {}
        self._load_progress()
    
    def _setup_logger(self):
        """Setup logging"""
        log_file = Path(__file__).parent.parent / self.config.get('Logging', 'LOG_FILE')
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        logger = logging.getLogger(__name__)
        logger.setLevel(self.config.get('Logging', 'LOG_LEVEL'))
        
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Also print to console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def _load_progress(self):
        """Load progress tracking data from file"""
        self.progress_file = Path(__file__).parent.parent / self.config.get('Scheduling', 'PROGRESS_FILE', 'logs/progress.json')
        self.progress_file.parent.mkdir(parents=True, exist_ok=True)
        
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r') as f:
                    self.progress_data = json.load(f)
            except Exception as e:
                self.logger.warning(f"Could not load progress file: {e}")
                self.progress_data = self._init_progress()
        else:
            self.progress_data = self._init_progress()
    
    def _init_progress(self):
        """Initialize progress data structure"""
        return {
            "scheduler_started": datetime.now().isoformat(),
            "total_runs": 0,
            "successful_runs": 0,
            "failed_runs": 0,
            "last_run": None,
            "last_run_status": None,
            "runs": []
        }
    
    def _save_progress(self):
        """Save progress tracking data to file"""
        try:
            with open(self.progress_file, 'w') as f:
                json.dump(self.progress_data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Could not save progress file: {e}")
    
    def _log_progress(self, run_number, success, duration_seconds, error_msg=None):
        """Log a run to progress tracking"""
        run_info = {
            "run_number": run_number,
            "timestamp": datetime.now().isoformat(),
            "success": success,
            "duration_seconds": duration_seconds,
            "error": error_msg
        }
        
        self.progress_data["runs"].append(run_info)
        self.progress_data["last_run"] = datetime.now().isoformat()
        self.progress_data["last_run_status"] = "SUCCESS" if success else "FAILED"
        self.progress_data["total_runs"] += 1
        
        if success:
            self.progress_data["successful_runs"] += 1
        else:
            self.progress_data["failed_runs"] += 1
        
        self._save_progress()
    
    def _print_progress_summary(self):
        """Print current progress summary to console and log"""
        total = self.progress_data["total_runs"]
        success = self.progress_data["successful_runs"]
        failed = self.progress_data["failed_runs"]
        success_rate = (success / total * 100) if total > 0 else 0
        last_status = self.progress_data.get('last_run_status', 'PENDING')
        
        summary = f"""
        ╔════════════════════════════════════════╗
        ║     SCHEDULER PROGRESS SUMMARY        ║
        ╠════════════════════════════════════════╣
        ║ Total Runs:      {total:27} ║
        ║ Successful:      {success:27} ║
        ║ Failed:          {failed:27} ║
        ║ Success Rate:    {success_rate:25.1f}% ║
        ║ Last Run:        {str(last_status):23} ║
        ╚════════════════════════════════════════╝
        """
        
        self.logger.info(summary)
        print(summary)
    
    def get_next_delay(self):
        """Calculate next delay in seconds"""
        use_random = self.config.get('Scheduling', 'USE_RANDOM_TIMES', var_type=bool)
        
        if use_random:
            min_delay = self.config.get('Scheduling', 'RANDOM_DELAY_MIN', var_type=int)
            max_delay = self.config.get('Scheduling', 'RANDOM_DELAY_MAX', var_type=int)
            delay = random.randint(min_delay, max_delay)
            self.logger.info(f"Using random delay: {delay} seconds")
        else:
            interval_hours = self.config.get('Scheduling', 'SCHEDULE_INTERVAL_HOURS', var_type=int)
            delay = interval_hours * 3600
            self.logger.info(f"Using fixed interval: {interval_hours} hours ({delay} seconds)")
        
        return delay
    
    def run_script(self):
        """Run the main Naukri automation script"""
        start_time = time.time()
        run_number = self.progress_data["total_runs"] + 1
        
        try:
            self.logger.info(f"[Run #{run_number}] Starting Naukri automation script...")
            
            # Import and run the main script
            from naukri_main import main
            main()
            
            duration = time.time() - start_time
            self.logger.info(f"[Run #{run_number}] Script completed successfully in {duration:.1f} seconds")
            self._log_progress(run_number, True, duration)
            return True
        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(f"[Run #{run_number}] Script failed after {duration:.1f} seconds: {e}", exc_info=True)
            self._log_progress(run_number, False, duration, str(e))
            return False
    
    def start(self):
        """Start the scheduler"""
        self.logger.info("=" * 80)
        self.logger.info("Naukri Automation Scheduler Started")
        self.logger.info(f"Frequency: 1.5 hours with ±15 minute random variance")
        self.logger.info(f"Configuration: Random execution times enabled")
        self.logger.info("=" * 80)
        
        first_run = True
        
        while self.running:
            try:
                if first_run:
                    self.logger.info("Running initial execution...")
                    self.run_script()
                    self._print_progress_summary()
                    first_run = False
                
                delay = self.get_next_delay()
                next_run = datetime.now().timestamp() + delay
                next_run_time = datetime.fromtimestamp(next_run)
                
                delay_minutes = delay / 60
                self.logger.info(f"Next run scheduled for: {next_run_time} ({delay_minutes:.1f} minutes from now)")
                self.logger.info(f"Waiting {delay} seconds ({delay_minutes:.1f} minutes)...")
                
                time.sleep(delay)
                
                self.logger.info("Running scheduled execution...")
                self.run_script()
                self._print_progress_summary()
                
            except KeyboardInterrupt:
                self.logger.info("Scheduler interrupted by user")
                self.logger.info("=" * 80)
                self._print_progress_summary()
                self.logger.info("=" * 80)
                self.running = False
                break
            except Exception as e:
                self.logger.error(f"Scheduler error: {e}", exc_info=True)
                self.logger.info("Waiting 60 seconds before retry...")
                time.sleep(60)
        
        self.logger.info("=" * 80)
        self.logger.info("Naukri Automation Scheduler Stopped")
        self.logger.info("=" * 80)


def main():
    """Main scheduler entry point"""
    scheduler = NaukriScheduler()
    scheduler.start()


if __name__ == "__main__":
    main()
