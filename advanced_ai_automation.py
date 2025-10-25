"""
🤖 Advanced AI Automation
Email summarizer, document generator, code review, and AI macro suggestions
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Any

class AdvancedAIAutomation:
    """Advanced AI-powered automation features"""
    
    def __init__(self):
        self.macros_file = "ai_macros.json"
        self.workflows_file = "visual_workflows.json"
        self.observed_patterns_file = "observed_patterns.json"
        self.macros = self.load_macros()
        self.workflows = self.load_workflows()
        self.observed_patterns = self.load_observed_patterns()
        
    def load_macros(self):
        """Load AI-generated macros"""
        if os.path.exists(self.macros_file):
            try:
                with open(self.macros_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def save_macros(self):
        """Save macros"""
        try:
            with open(self.macros_file, 'w') as f:
                json.dump(self.macros, f, indent=2)
        except Exception as e:
            print(f"Error saving macros: {e}")
    
    def load_workflows(self):
        """Load visual workflows"""
        if os.path.exists(self.workflows_file):
            try:
                with open(self.workflows_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def save_workflows(self):
        """Save workflows"""
        try:
            with open(self.workflows_file, 'w') as f:
                json.dump(self.workflows, f, indent=2)
        except Exception as e:
            print(f"Error saving workflows: {e}")
    
    def load_observed_patterns(self):
        """Load observed action patterns"""
        if os.path.exists(self.observed_patterns_file):
            try:
                with open(self.observed_patterns_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def save_observed_patterns(self):
        """Save observed patterns"""
        try:
            with open(self.observed_patterns_file, 'w') as f:
                json.dump(self.observed_patterns, f, indent=2)
        except Exception as e:
            print(f"Error saving observed patterns: {e}")
    
    def summarize_email(self, email_content: str):
        """Shorten long email threads into bullet points"""
        lines = email_content.split('\n')
        
        summary = []
        
        for line in lines:
            line = line.strip()
            if line and len(line) > 20:
                if any(keyword in line.lower() for keyword in ['important', 'deadline', 'urgent', 'action required']):
                    summary.append(f"🔴 {line[:100]}")
                elif any(keyword in line.lower() for keyword in ['meeting', 'schedule', 'time']):
                    summary.append(f"📅 {line[:100]}")
                elif line.startswith('>') or line.startswith('On '):
                    continue
                else:
                    if len(summary) < 5:
                        summary.append(f"• {line[:100]}")
        
        output = "\n📧 EMAIL SUMMARY\n" + "="*60 + "\n"
        output += "\n".join(summary[:10])
        output += "\n" + "="*60 + "\n"
        
        return output
    
    def generate_document(self, doc_type: str, topic: str, details: Dict = None):
        """Auto-create reports, notes, or meeting summaries"""
        if details is None:
            details = {}
        
        document = f"\n{'='*60}\n"
        
        if doc_type == "report":
            document += f"📄 REPORT: {topic}\n"
            document += f"{'='*60}\n\n"
            document += f"Date: {datetime.now().strftime('%Y-%m-%d')}\n\n"
            document += "Executive Summary:\n"
            document += f"This report covers {topic}.\n\n"
            document += "Key Findings:\n"
            document += "1. Finding one\n"
            document += "2. Finding two\n"
            document += "3. Finding three\n\n"
            document += "Recommendations:\n"
            document += "- Recommendation one\n"
            document += "- Recommendation two\n\n"
        
        elif doc_type == "meeting_summary":
            document += f"📝 MEETING SUMMARY: {topic}\n"
            document += f"{'='*60}\n\n"
            document += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            document += f"Attendees: {details.get('attendees', 'N/A')}\n\n"
            document += "Discussion Points:\n"
            document += "- Point 1\n"
            document += "- Point 2\n"
            document += "- Point 3\n\n"
            document += "Action Items:\n"
            document += "- [ ] Task 1\n"
            document += "- [ ] Task 2\n"
            document += "- [ ] Task 3\n\n"
            document += "Next Steps:\n"
            document += "Follow up on action items by [date]\n\n"
        
        elif doc_type == "notes":
            document += f"📓 NOTES: {topic}\n"
            document += f"{'='*60}\n\n"
            document += f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
            document += "Key Points:\n"
            document += "• Point 1\n"
            document += "• Point 2\n"
            document += "• Point 3\n\n"
            document += "Additional Information:\n"
            document += f"{details.get('content', 'Add your notes here...')}\n\n"
        
        document += f"{'='*60}\n"
        
        filename = f"{doc_type}_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write(document)
            return {"success": True, "message": f"Document created: {filename}", "content": document}
        except Exception as e:
            return {"success": False, "message": f"Error creating document: {e}", "content": document}
    
    def review_code(self, code: str, language: str = "python"):
        """Lint, optimize, and annotate code with inline comments"""
        review = f"\n🔍 CODE REVIEW ({language.upper()})\n"
        review += "="*60 + "\n\n"
        
        lines = code.split('\n')
        
        review += "Issues Found:\n\n"
        
        if language.lower() == "python":
            if not any('def ' in line for line in lines):
                review += "⚠️ No functions detected - consider organizing code into functions\n"
            
            long_lines = [i+1 for i, line in enumerate(lines) if len(line) > 79]
            if long_lines:
                review += f"⚠️ Lines exceed 79 characters: {long_lines}\n"
            
            if 'import' in code and 'import *' in code:
                review += "🔴 Avoid wildcard imports (import *)\n"
        
        elif language.lower() == "javascript":
            if 'var ' in code:
                review += "⚠️ Consider using 'let' or 'const' instead of 'var'\n"
            
            if '==' in code:
                review += "⚠️ Consider using strict equality (===) instead of ==\n"
        
        review += "\nSuggestions:\n"
        review += "• Add docstrings/comments for complex logic\n"
        review += "• Consider error handling for edge cases\n"
        review += "• Use meaningful variable names\n"
        review += "• Keep functions focused on single responsibility\n"
        
        review += "\n" + "="*60 + "\n"
        
        return review
    
    def build_workflow(self, workflow_name: str, steps: List[Dict]):
        """Create a visual automation workflow"""
        workflow = {
            "name": workflow_name,
            "created": datetime.now().isoformat(),
            "steps": steps,
            "enabled": True
        }
        
        self.workflows.append(workflow)
        self.save_workflows()
        
        return {"success": True, "message": f"Workflow '{workflow_name}' created with {len(steps)} steps"}
    
    def list_workflows(self):
        """List all visual workflows"""
        if not self.workflows:
            return "No workflows created yet."
        
        output = "\n" + "="*60 + "\n"
        output += "🔄 VISUAL WORKFLOWS\n"
        output += "="*60 + "\n\n"
        
        for i, workflow in enumerate(self.workflows, 1):
            status = "✅ Enabled" if workflow.get("enabled", True) else "❌ Disabled"
            output += f"{i}. {workflow['name']} - {status}\n"
            output += f"   Steps: {len(workflow.get('steps', []))}\n"
            output += f"   Created: {workflow.get('created', 'Unknown')}\n\n"
        
        output += "="*60 + "\n"
        return output
    
    def suggest_macro(self, repeated_actions: List[str]):
        """Observe repeated manual actions and suggest automation"""
        if len(repeated_actions) < 3:
            return {"success": False, "message": "Need at least 3 repeated actions to suggest a macro"}
        
        macro_name = f"macro_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        macro = {
            "name": macro_name,
            "actions": repeated_actions,
            "frequency": len(repeated_actions),
            "suggested_at": datetime.now().isoformat(),
            "status": "suggested"
        }
        
        self.macros.append(macro)
        self.save_macros()
        
        return {
            "success": True,
            "message": f"Detected repeated pattern! Suggested macro: {macro_name}",
            "actions": repeated_actions,
            "suggestion": "Would you like to automate this sequence?"
        }
    
    def get_ai_connector_status(self):
        """Status of AI app connector"""
        return {
            "success": True,
            "message": "AI App Connector ready",
            "supported_apps": ["Notion", "Google Calendar", "Trello", "Slack", "Discord"],
            "info": "Describe any integration in natural language to create it"
        }


def create_advanced_ai_automation():
    """Factory function to create an AdvancedAIAutomation instance"""
    return AdvancedAIAutomation()
