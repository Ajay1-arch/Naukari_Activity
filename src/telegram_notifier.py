"""
Telegram Notification Module
Sends status updates and results to Telegram via Bot API
"""

import requests
import logging
from typing import Optional
from config_loader import get_secrets

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Send notifications to Telegram"""
    
    def __init__(self):
        """Initialize Telegram notifier with credentials from secrets"""
        try:
            secrets_manager = get_secrets()
            
            self.bot_token = secrets_manager.get('telegram.bot_token')
            self.chat_id = secrets_manager.get('telegram.chat_id')
            self.enabled = bool(self.bot_token and self.chat_id)
            
            if not self.enabled:
                logger.warning("Telegram notifications disabled: Missing bot_token or chat_id in secrets.json")
            else:
                self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
                logger.info("Telegram notifications enabled")
                
        except Exception as e:
            logger.error(f"Failed to initialize Telegram notifier: {e}")
            self.enabled = False
    
    def send_message(self, message: str, parse_mode: str = "HTML") -> bool:
        """
        Send a message to Telegram
        
        Args:
            message: The message text to send
            parse_mode: HTML or Markdown formatting
            
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            return False
        
        try:
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": parse_mode
            }
            
            response = requests.post(self.api_url, json=payload, timeout=10)
            response.raise_for_status()
            
            logger.info("Telegram message sent successfully")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending Telegram message: {e}")
            return False
    
    def send_startup_notification(self) -> bool:
        """Send startup notification"""
        message = """
<b>🚀 Naukri Automation Started</b>

<i>The scheduler is now running and will execute every 1.5 hours</i>

✅ All systems ready
⏰ Next run in ~90 minutes
        """
        return self.send_message(message)
    
    def send_success_notification(self, run_number: int, timestamp: str) -> bool:
        """Send success notification after successful run"""
        message = f"""
<b>✅ Naukri Automation Successful</b>

<b>Run #:</b> {run_number}
<b>Timestamp:</b> {timestamp}

<i>Profile updated and resume uploaded</i>

Tasks Completed:
• ✅ Naukri Login
• ✅ Profile Update
• ✅ Resume Upload
• ✅ Logout

⏰ Next run scheduled in ~90 minutes
        """
        return self.send_message(message)
    
    def send_failure_notification(self, run_number: int, timestamp: str, error: str) -> bool:
        """Send failure notification when run fails"""
        message = f"""
<b>❌ Naukri Automation Failed</b>

<b>Run #:</b> {run_number}
<b>Timestamp:</b> {timestamp}

<b>Error:</b>
<code>{error[:500]}</code>

⚠️ Please check logs at:
<code>logs/naukri.log</code>

⏰ Will retry in ~90 minutes
        """
        return self.send_message(message)
    
    def send_summary_notification(self, total_runs: int, successful: int, 
                                  failed: int, uptime_hours: str) -> bool:
        """Send summary notification with statistics"""
        success_rate = (successful / total_runs * 100) if total_runs > 0 else 0
        
        message = f"""
<b>📊 Naukri Automation Summary</b>

<b>Statistics:</b>
• Total Runs: <b>{total_runs}</b>
• Successful: <b>{successful}</b> ✅
• Failed: <b>{failed}</b> ❌
• Success Rate: <b>{success_rate:.1f}%</b>

<b>Uptime:</b> {uptime_hours}

📝 Full logs available in the project directory
        """
        return self.send_message(message)
    
    def send_critical_alert(self, alert_message: str) -> bool:
        """Send critical alert for important issues"""
        message = f"""
<b>⚠️ CRITICAL ALERT - Naukri Automation</b>

{alert_message}

Please review logs and take action immediately.

📁 Logs: <code>logs/naukri.log</code>
        """
        return self.send_message(message)


def get_notifier() -> TelegramNotifier:
    """Get singleton instance of TelegramNotifier"""
    return TelegramNotifier()
