#!/usr/bin/env python3
"""
Scheduler for Naukri Automation
Runs the script on a schedule (hourly or at random intervals)
"""

import time
import random
import logging
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
        try:
            self.logger.info("Starting Naukri automation script...")
            
            # Import and run the main script
            from naukri_main import main
            main()
            
            self.logger.info("Script completed successfully")
            return True
        except Exception as e:
            self.logger.error(f"Script failed: {e}", exc_info=True)
            return False
    
    def start(self):
        """Start the scheduler"""
        self.logger.info("=" * 80)
        self.logger.info("Naukri Automation Scheduler Started")
        self.logger.info("=" * 80)
        
        first_run = True
        
        while self.running:
            try:
                if first_run:
                    self.logger.info("Running initial execution...")
                    self.run_script()
                    first_run = False
                
                delay = self.get_next_delay()
                next_run = datetime.now().timestamp() + delay
                next_run_time = datetime.fromtimestamp(next_run)
                
                self.logger.info(f"Next run scheduled for: {next_run_time}")
                self.logger.info(f"Waiting {delay} seconds...")
                
                time.sleep(delay)
                
                self.logger.info("Running scheduled execution...")
                self.run_script()
                
            except KeyboardInterrupt:
                self.logger.info("Scheduler interrupted by user")
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
