# Entry point for WhatsApp Automation Bot
# Starts the Flask webhook server

from core.main import app
import os

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"🤖 WhatsApp Automation Bot Starting...")
    print(f"📡 Webhook server running on port {port}")
    print(f"🌐 Webhook URL: https://<your-replit-url>/webhook")
    print(f"\n{'='*50}\n")
    app.run(host='0.0.0.0', port=port, debug=False)
