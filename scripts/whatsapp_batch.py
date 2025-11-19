#!/usr/bin/env python3
"""
WhatsApp Batch Messaging System
Send WhatsApp messages to multiple recipients with templates and logging
"""

import sys
import os
import csv
import json
import time
import logging
from datetime import datetime
from typing import List, Dict, Optional

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from modules.communication.whatsapp_automation import WhatsAppAutomation


class WhatsAppBatchMessenger:
    """Handles batch WhatsApp messaging with templates and logging"""
    
    def __init__(self, log_file: Optional[str] = None):
        """
        Initialize batch messenger
        
        Args:
            log_file: Optional path to log file (default: data/whatsapp_batch_log.json)
        """
        self.wa = WhatsAppAutomation()
        
        if log_file is None:
            log_file = os.path.join(project_root, "data", "whatsapp_batch_log.json")
        
        self.log_file = log_file
        self.log_dir = os.path.dirname(log_file)
        
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(self.log_dir, 'whatsapp_batch.log')),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def process_template(self, template: str, data: Dict[str, str]) -> str:
        """
        Process message template with data placeholders
        
        Args:
            template: Message template with {placeholders}
            data: Dictionary of placeholder values
        
        Returns:
            Processed message
        
        Examples:
            template = "Hi {name}, your order {order_id} is ready!"
            data = {"name": "John", "order_id": "12345"}
            result = "Hi John, your order 12345 is ready!"
        """
        try:
            return template.format(**data)
        except KeyError as e:
            self.logger.warning(f"Missing placeholder {e} in template")
            return template
    
    def send_from_csv(
        self,
        csv_file: str,
        message_template: Optional[str] = None,
        delay_seconds: int = 20,
        skip_errors: bool = True
    ) -> Dict[str, any]:
        """
        Send WhatsApp messages to contacts from CSV file
        
        Args:
            csv_file: Path to CSV file with columns: phone, name, message (optional), and custom fields
            message_template: Optional template string with {placeholders}
            delay_seconds: Delay between messages (default: 20s)
            skip_errors: Continue on errors (default: True)
        
        Returns:
            Summary dict with success/failure counts
        
        CSV Format:
            phone,name,custom1,custom2,...
            +1234567890,John,value1,value2
            +0987654321,Jane,value1,value2
        """
        if not os.path.exists(csv_file):
            self.logger.error(f"CSV file not found: {csv_file}")
            return {"success": False, "error": "File not found"}
        
        results = {
            "total": 0,
            "success": 0,
            "failed": 0,
            "skipped": 0,
            "details": []
        }
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                contacts = list(reader)
                results["total"] = len(contacts)
                
                print(f"\n{'='*60}")
                print(f"📱 BATCH WHATSAPP MESSAGING")
                print(f"{'='*60}")
                print(f"Total contacts: {results['total']}")
                print(f"Delay between messages: {delay_seconds}s")
                print(f"{'='*60}\n")
                
                for i, contact in enumerate(contacts, 1):
                    phone = contact.get('phone', '').strip()
                    name = contact.get('name', 'Unknown').strip()
                    
                    if not phone:
                        self.logger.warning(f"Skipping row {i}: No phone number")
                        results["skipped"] += 1
                        continue
                    
                    if message_template:
                        message = self.process_template(message_template, contact)
                    elif 'message' in contact:
                        message = contact['message']
                    else:
                        self.logger.warning(f"Skipping {name}: No message provided")
                        results["skipped"] += 1
                        continue
                    
                    print(f"\n[{i}/{results['total']}] Sending to {name} ({phone})")
                    print(f"Message: {message[:50]}{'...' if len(message) > 50 else ''}")
                    
                    try:
                        result = self.wa.send_message_instantly(phone, message)
                        
                        log_entry = {
                            "timestamp": datetime.now().isoformat(),
                            "phone": phone,
                            "name": name,
                            "message": message,
                            "success": result.get("success", False),
                            "response": result.get("message", "")
                        }
                        
                        if result.get("success"):
                            results["success"] += 1
                            print(f"✅ Sent successfully!")
                        else:
                            results["failed"] += 1
                            print(f"❌ Failed: {result.get('message')}")
                            if not skip_errors:
                                break
                        
                        results["details"].append(log_entry)
                        self._save_log(log_entry)
                        
                        if i < results["total"]:
                            print(f"⏳ Waiting {delay_seconds}s before next message...")
                            time.sleep(delay_seconds)
                    
                    except Exception as e:
                        self.logger.error(f"Error sending to {name}: {e}")
                        results["failed"] += 1
                        results["details"].append({
                            "timestamp": datetime.now().isoformat(),
                            "phone": phone,
                            "name": name,
                            "success": False,
                            "error": str(e)
                        })
                        if not skip_errors:
                            break
                
                print(f"\n{'='*60}")
                print(f"📊 BATCH SUMMARY")
                print(f"{'='*60}")
                print(f"Total: {results['total']}")
                print(f"✅ Success: {results['success']}")
                print(f"❌ Failed: {results['failed']}")
                print(f"⏭️  Skipped: {results['skipped']}")
                print(f"{'='*60}\n")
                
                return results
        
        except Exception as e:
            self.logger.error(f"Error processing CSV: {e}")
            return {"success": False, "error": str(e)}
    
    def send_batch_images(
        self,
        csv_file: str,
        image_path: str,
        caption_template: Optional[str] = None,
        delay_seconds: int = 25,
        skip_errors: bool = True
    ) -> Dict[str, any]:
        """
        Send same image to multiple contacts from CSV
        
        Args:
            csv_file: Path to CSV file with columns: phone, name, and custom fields
            image_path: Path to image file (JPG only)
            caption_template: Optional caption template with {placeholders}
            delay_seconds: Delay between messages (default: 25s)
            skip_errors: Continue on errors (default: True)
        
        Returns:
            Summary dict with success/failure counts
        """
        if not os.path.exists(csv_file):
            self.logger.error(f"CSV file not found: {csv_file}")
            return {"success": False, "error": "CSV file not found"}
        
        if not os.path.exists(image_path):
            self.logger.error(f"Image file not found: {image_path}")
            return {"success": False, "error": "Image file not found"}
        
        results = {
            "total": 0,
            "success": 0,
            "failed": 0,
            "skipped": 0,
            "details": []
        }
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                contacts = list(reader)
                results["total"] = len(contacts)
                
                print(f"\n{'='*60}")
                print(f"🖼️  BATCH IMAGE SENDING")
                print(f"{'='*60}")
                print(f"Total contacts: {results['total']}")
                print(f"Image: {os.path.basename(image_path)}")
                print(f"Delay: {delay_seconds}s")
                print(f"{'='*60}\n")
                
                for i, contact in enumerate(contacts, 1):
                    phone = contact.get('phone', '').strip()
                    name = contact.get('name', 'Unknown').strip()
                    
                    if not phone:
                        self.logger.warning(f"Skipping row {i}: No phone number")
                        results["skipped"] += 1
                        continue
                    
                    caption = ""
                    if caption_template:
                        caption = self.process_template(caption_template, contact)
                    elif 'caption' in contact:
                        caption = contact['caption']
                    
                    print(f"\n[{i}/{results['total']}] Sending to {name} ({phone})")
                    if caption:
                        print(f"Caption: {caption[:50]}{'...' if len(caption) > 50 else ''}")
                    
                    try:
                        result = self.wa.send_image(phone, image_path, caption)
                        
                        log_entry = {
                            "timestamp": datetime.now().isoformat(),
                            "phone": phone,
                            "name": name,
                            "image": image_path,
                            "caption": caption,
                            "success": result.get("success", False),
                            "response": result.get("message", "")
                        }
                        
                        if result.get("success"):
                            results["success"] += 1
                            print(f"✅ Image sent successfully!")
                        else:
                            results["failed"] += 1
                            print(f"❌ Failed: {result.get('message')}")
                            if not skip_errors:
                                break
                        
                        results["details"].append(log_entry)
                        self._save_log(log_entry)
                        
                        if i < results["total"]:
                            print(f"⏳ Waiting {delay_seconds}s before next image...")
                            time.sleep(delay_seconds)
                    
                    except Exception as e:
                        self.logger.error(f"Error sending to {name}: {e}")
                        results["failed"] += 1
                        if not skip_errors:
                            break
                
                print(f"\n{'='*60}")
                print(f"📊 BATCH SUMMARY")
                print(f"{'='*60}")
                print(f"Total: {results['total']}")
                print(f"✅ Success: {results['success']}")
                print(f"❌ Failed: {results['failed']}")
                print(f"⏭️  Skipped: {results['skipped']}")
                print(f"{'='*60}\n")
                
                return results
        
        except Exception as e:
            self.logger.error(f"Error processing CSV: {e}")
            return {"success": False, "error": str(e)}
    
    def _save_log(self, log_entry: Dict):
        """Save log entry to JSON file"""
        try:
            logs = []
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            
            logs.append(log_entry)
            
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2)
        
        except Exception as e:
            self.logger.error(f"Error saving log: {e}")
    
    def get_logs(self, limit: int = 50) -> List[Dict]:
        """
        Get recent batch messaging logs
        
        Args:
            limit: Number of recent logs to return (default: 50)
        
        Returns:
            List of log entries
        """
        try:
            if not os.path.exists(self.log_file):
                return []
            
            with open(self.log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
            
            return logs[-limit:]
        
        except Exception as e:
            self.logger.error(f"Error reading logs: {e}")
            return []
    
    def create_csv_template(self, output_file: str, template_type: str = "basic"):
        """
        Create CSV template file for batch messaging
        
        Args:
            output_file: Path to output CSV file
            template_type: Template type - "basic", "personalized", or "image"
        """
        try:
            templates = {
                "basic": {
                    "headers": ["phone", "name", "message"],
                    "sample": [
                        ["+1234567890", "John Doe", "Hello John! This is a test message."],
                        ["+0987654321", "Jane Smith", "Hi Jane! How are you doing?"]
                    ]
                },
                "personalized": {
                    "headers": ["phone", "name", "company", "product"],
                    "sample": [
                        ["+1234567890", "John Doe", "ABC Corp", "Premium Plan"],
                        ["+0987654321", "Jane Smith", "XYZ Inc", "Basic Plan"]
                    ]
                },
                "image": {
                    "headers": ["phone", "name", "caption"],
                    "sample": [
                        ["+1234567890", "John Doe", "Hi John! Check out this image."],
                        ["+0987654321", "Jane Smith", "Hi Jane! Thought you'd like this."]
                    ]
                }
            }
            
            if template_type not in templates:
                template_type = "basic"
            
            template = templates[template_type]
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(template["headers"])
                writer.writerows(template["sample"])
            
            print(f"✅ Created CSV template: {output_file}")
            print(f"   Type: {template_type}")
            print(f"   Headers: {', '.join(template['headers'])}")
            
            return True
        
        except Exception as e:
            self.logger.error(f"Error creating template: {e}")
            return False


def main():
    """CLI interface for batch messaging"""
    import argparse
    
    parser = argparse.ArgumentParser(description="WhatsApp Batch Messaging System")
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    send_parser = subparsers.add_parser('send', help='Send batch messages from CSV')
    send_parser.add_argument('csv_file', help='Path to CSV file')
    send_parser.add_argument('--template', '-t', help='Message template with {placeholders}')
    send_parser.add_argument('--delay', '-d', type=int, default=20, help='Delay between messages (seconds)')
    send_parser.add_argument('--no-skip', action='store_true', help='Stop on first error')
    
    image_parser = subparsers.add_parser('image', help='Send batch images from CSV')
    image_parser.add_argument('csv_file', help='Path to CSV file')
    image_parser.add_argument('image_path', help='Path to image file')
    image_parser.add_argument('--caption', '-c', help='Caption template with {placeholders}')
    image_parser.add_argument('--delay', '-d', type=int, default=25, help='Delay between messages (seconds)')
    image_parser.add_argument('--no-skip', action='store_true', help='Stop on first error')
    
    template_parser = subparsers.add_parser('create-template', help='Create CSV template')
    template_parser.add_argument('output_file', help='Output CSV file path')
    template_parser.add_argument('--type', '-t', choices=['basic', 'personalized', 'image'], default='basic', help='Template type')
    
    logs_parser = subparsers.add_parser('logs', help='View batch messaging logs')
    logs_parser.add_argument('--limit', '-l', type=int, default=20, help='Number of logs to show')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    messenger = WhatsAppBatchMessenger()
    
    if args.command == 'send':
        skip_errors = not args.no_skip
        results = messenger.send_from_csv(
            args.csv_file,
            message_template=args.template,
            delay_seconds=args.delay,
            skip_errors=skip_errors
        )
        sys.exit(0 if results.get("success", 0) > 0 else 1)
    
    elif args.command == 'image':
        skip_errors = not args.no_skip
        results = messenger.send_batch_images(
            args.csv_file,
            args.image_path,
            caption_template=args.caption,
            delay_seconds=args.delay,
            skip_errors=skip_errors
        )
        sys.exit(0 if results.get("success", 0) > 0 else 1)
    
    elif args.command == 'create-template':
        success = messenger.create_csv_template(args.output_file, args.type)
        sys.exit(0 if success else 1)
    
    elif args.command == 'logs':
        logs = messenger.get_logs(args.limit)
        if not logs:
            print("ℹ️  No logs found")
            return
        
        print(f"\n{'='*80}")
        print(f"📋 BATCH MESSAGING LOGS (Last {len(logs)})")
        print(f"{'='*80}\n")
        
        for i, log in enumerate(logs, 1):
            status = "✅" if log.get("success") else "❌"
            print(f"{i}. {status} {log.get('name', 'Unknown')} ({log.get('phone', 'N/A')})")
            print(f"   Time: {log.get('timestamp', 'Unknown')}")
            if 'message' in log:
                msg = log['message'][:60]
                print(f"   Message: {msg}{'...' if len(log['message']) > 60 else ''}")
            if 'image' in log:
                print(f"   Image: {os.path.basename(log['image'])}")
            print()


if __name__ == "__main__":
    main()
