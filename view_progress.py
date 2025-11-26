#!/usr/bin/env python3
"""
Progress Dashboard for Naukri Automation Scheduler
View statistics and historical data about scheduler runs
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from tabulate import tabulate


def load_progress():
    """Load progress data from file"""
    progress_file = Path(__file__).parent / "logs" / "progress.json"
    
    if not progress_file.exists():
        print("❌ No progress data found. Start the scheduler first!")
        sys.exit(1)
    
    with open(progress_file, 'r') as f:
        return json.load(f)


def print_summary(data):
    """Print summary statistics"""
    total = data["total_runs"]
    success = data["successful_runs"]
    failed = data["failed_runs"]
    success_rate = (success / total * 100) if total > 0 else 0
    
    print("\n" + "=" * 60)
    print("SCHEDULER PROGRESS SUMMARY".center(60))
    print("=" * 60)
    print(f"Total Runs:           {total}")
    print(f"Successful:           {success}")
    print(f"Failed:               {failed}")
    print(f"Success Rate:         {success_rate:.1f}%")
    print(f"Last Run Status:      {data['last_run_status']}")
    print(f"Last Run Time:        {data['last_run']}")
    print(f"Scheduler Started:    {data['scheduler_started']}")
    print("=" * 60 + "\n")


def print_recent_runs(data, count=10):
    """Print recent run history"""
    runs = data["runs"][-count:]
    
    if not runs:
        print("No run history yet.\n")
        return
    
    print(f"RECENT RUNS (Last {len(runs)})".center(60))
    print("-" * 60)
    
    table_data = []
    for run in runs:
        run_num = run["run_number"]
        timestamp = datetime.fromisoformat(run["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
        status = "✓ SUCCESS" if run["success"] else "✗ FAILED"
        duration = f"{run['duration_seconds']:.1f}s"
        error = run.get("error", "")[:30] + "..." if run.get("error") else "-"
        
        table_data.append([run_num, timestamp, status, duration, error])
    
    headers = ["Run #", "Timestamp", "Status", "Duration", "Error/Notes"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    print()


def print_statistics(data):
    """Print detailed statistics"""
    runs = data["runs"]
    
    if not runs:
        print("No run data available.\n")
        return
    
    # Calculate duration statistics
    durations = [r["duration_seconds"] for r in runs]
    avg_duration = sum(durations) / len(durations)
    min_duration = min(durations)
    max_duration = max(durations)
    
    print("\nDETAILED STATISTICS".center(60))
    print("-" * 60)
    print(f"Average Run Duration: {avg_duration:.1f} seconds")
    print(f"Minimum Duration:     {min_duration:.1f} seconds")
    print(f"Maximum Duration:     {max_duration:.1f} seconds")
    print(f"Total Run Time:       {sum(durations):.1f} seconds ({sum(durations)/3600:.2f} hours)")
    print("-" * 60 + "\n")


def main():
    """Main entry point"""
    data = load_progress()
    
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + "NAUKRI AUTOMATION - SCHEDULER DASHBOARD".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    
    print_summary(data)
    print_recent_runs(data, count=15)
    print_statistics(data)
    
    print("💡 Tip: Check logs/naukri.log for detailed execution logs")
    print("💡 Tip: Check logs/progress.json for complete run history\n")


if __name__ == "__main__":
    main()
