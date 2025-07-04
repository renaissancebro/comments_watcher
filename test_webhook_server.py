#!/usr/bin/env python3
"""
Simple webhook server for testing email notifications locally.
This server will receive webhook calls and display them in the console.
"""

from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# Store received webhooks
received_webhooks = []

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming webhook requests."""
    try:
        data = request.get_json()

        # Store the webhook
        webhook_data = {
            'timestamp': datetime.now().isoformat(),
            'headers': dict(request.headers),
            'data': data
        }
        received_webhooks.append(webhook_data)

        # Display the webhook
        print("\n📨 WEBHOOK RECEIVED:")
        print("=" * 50)
        print(f"Time: {webhook_data['timestamp']}")
        print(f"Content-Type: {request.headers.get('Content-Type', 'N/A')}")

        if data:
            if 'subject' in data:
                print(f"Subject: {data['subject']}")
            if 'body' in data:
                print(f"Body: {data['body'][:200]}...")
            if 'html_body' in data:
                print(f"HTML Body: {data['html_body'][:200]}...")
            if '@type' in data and data['@type'] == 'MessageCard':
                print(f"Teams Message: {data.get('summary', 'N/A')}")

        print("=" * 50)

        return jsonify({'status': 'success', 'message': 'Webhook received'}), 200

    except Exception as e:
        print(f"❌ Error processing webhook: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/webhooks', methods=['GET'])
def list_webhooks():
    """List all received webhooks."""
    return jsonify({
        'count': len(received_webhooks),
        'webhooks': received_webhooks
    })

@app.route('/clear', methods=['POST'])
def clear_webhooks():
    """Clear all stored webhooks."""
    global received_webhooks
    received_webhooks = []
    return jsonify({'status': 'success', 'message': 'Webhooks cleared'})

@app.route('/', methods=['GET'])
def home():
    """Home page with instructions."""
    return f"""
    <html>
    <head><title>Test Webhook Server</title></head>
    <body>
        <h1>🧪 Test Webhook Server</h1>
        <p>This server is running to test webhook notifications.</p>

        <h2>Endpoints:</h2>
        <ul>
            <li><strong>POST /webhook</strong> - Receive webhook notifications</li>
            <li><strong>GET /webhooks</strong> - List all received webhooks</li>
            <li><strong>POST /clear</strong> - Clear all stored webhooks</li>
        </ul>

        <h2>Current Status:</h2>
        <p>Webhooks received: {len(received_webhooks)}</p>

        <h2>Setup Instructions:</h2>
        <ol>
            <li>Set your EMAIL_WEBHOOK_URL to: <code>http://localhost:5000/webhook</code></li>
            <li>Set ENABLE_EMAIL_ALERTS=true in your .env file</li>
            <li>Run the test script: <code>python test_notifications.py</code></li>
            <li>Watch this server for incoming webhooks</li>
        </ol>

        <h2>Recent Webhooks:</h2>
        <pre>{json.dumps(received_webhooks[-5:], indent=2)}</pre>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("🚀 Starting test webhook server...")
    print("📡 Server will be available at: http://localhost:5000")
    print("🔗 Webhook endpoint: http://localhost:5000/webhook")
    print("📋 Instructions: http://localhost:5000")
    print("\n💡 To test email notifications:")
    print("   1. Set EMAIL_WEBHOOK_URL=http://localhost:5000/webhook in .env")
    print("   2. Set ENABLE_EMAIL_ALERTS=true in .env")
    print("   3. Run: python test_notifications.py")
    print("\n" + "=" * 60)

    app.run(host='0.0.0.0', port=5000, debug=True)
