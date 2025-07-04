#!/usr/bin/env python3
"""
Test script for Teams and Email webhook notifications.
Run this to test your webhook configurations.
"""

from notifier import test_notifications
from config import (
    TEAMS_WEBHOOK_URL,
    EMAIL_WEBHOOK_URL,
    ENABLE_TEAMS_ALERTS,
    ENABLE_EMAIL_ALERTS
)

def main():
    """Main test function."""
    print("🧪 Comment Watcher - Notification Test")
    print("=" * 60)

    # Show current configuration
    print("📋 Current Configuration:")
    print(f"   Teams Alerts: {'✅ Enabled' if ENABLE_TEAMS_ALERTS else '❌ Disabled'}")
    print(f"   Teams Webhook: {'✅ Set' if TEAMS_WEBHOOK_URL else '❌ Not set'}")
    print(f"   Email Alerts: {'✅ Enabled' if ENABLE_EMAIL_ALERTS else '❌ Disabled'}")
    print(f"   Email Webhook: {'✅ Set' if EMAIL_WEBHOOK_URL else '❌ Not set'}")

    # Run the test
    test_notifications()

    print("\n📝 Setup Instructions:")
    print("=" * 60)

    if not ENABLE_TEAMS_ALERTS:
        print("\n💬 To enable Teams alerts:")
        print("   1. Add to your .env file:")
        print("      TEAMS_WEBHOOK_URL=https://your-org.webhook.office.com/webhookb2/...")
        print("      ENABLE_TEAMS_ALERTS=true")
        print("   2. Get webhook URL from Teams:")
        print("      - Go to your Teams channel")
        print("      - Click '...' → 'Connectors'")
        print("      - Configure 'Incoming Webhook'")
        print("      - Copy the webhook URL")

    if not ENABLE_EMAIL_ALERTS:
        print("\n📧 To enable Email alerts:")
        print("   1. Add to your .env file:")
        print("      EMAIL_WEBHOOK_URL=https://your-email-service.com/webhook")
        print("      ENABLE_EMAIL_ALERTS=true")
        print("   2. Set up email webhook service (e.g., Zapier, IFTTT, or custom)")
        print("      - Configure webhook to send emails")
        print("      - Expect JSON payload with 'subject', 'body', 'html_body'")

    print("\n🔄 After updating .env, run this script again to test!")

if __name__ == "__main__":
    main()
