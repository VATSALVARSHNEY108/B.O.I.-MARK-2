"""
⚙️ Command Executor Module
Executes commands with intelligence, personality, and humanized feedback
Integrates Desktop RAG, Communication Enhancements, and Persona services
"""

from modules.intelligence.persona_response_service import create_persona_service
from modules.intelligence.desktop_rag import DesktopRAG
from modules.communication.communication_enhancements import CommunicationEnhancements


class CommandExecutor:
    """
    Enhanced command executor with:
    - Persona-based humanized responses
    - Desktop RAG integration for file intelligence
    - Communication enhancements for messages/emails
    - Milestone celebrations and helpful tips
    - Multi-step workflow execution
    """
    
    def __init__(self):
        """Initialize command executor with all intelligence modules"""
        self.persona_service = create_persona_service()
        self.desktop_rag = DesktopRAG()
        self.comm_enhancements = CommunicationEnhancements()
        self.command_count = 0
        self.error_count = 0
        
        print("⚙️ Command Executor initialized")
        print("   🤖 Persona Service: Active")
        print("   🧠 Desktop RAG: Active")
        print("   💬 Communication Enhancements: Active")
    
    def _humanize_result(self, action: str, result: dict) -> dict:
        """
        Wrap results with persona humanization
        Add milestone celebrations and helpful tips
        """
        self.command_count += 1
        
        if not result.get("success", False):
            self.error_count += 1
        
        humanized_message = self.persona_service.humanize_response(
            action=action,
            result=result,
            context={"command_count": self.command_count}
        )
        
        milestone_msg = ""
        if self.command_count % 10 == 0:
            milestone_msg = self.persona_service.celebrate_milestone(
                self.command_count, 
                action
            )
        
        tip_msg = ""
        if self.command_count % 8 == 0 and result.get("success", False):
            tip_msg = self.persona_service.provide_helpful_tip()
        
        final_message = humanized_message
        if milestone_msg:
            final_message += f"\n\n{milestone_msg}"
        if tip_msg:
            final_message += f"\n\n{tip_msg}"
        
        return {
            "success": result.get("success", False),
            "message": final_message,
            "original_result": result
        }
    
    def execute(self, command_dict: dict) -> dict:
        """
        Main entry point for executing commands.
        Routes to execute_workflow for multi-step commands or execute_single_action for single actions.
        
        Args:
            command_dict: Parsed command dictionary with keys:
                - action: str - Action name
                - parameters: dict - Action parameters
                - steps: list - Workflow steps (empty for single actions)
                - description: str - Human-readable description
        
        Returns:
            Dict with execution result and humanized message
        """
        try:
            if not isinstance(command_dict, dict):
                return {
                    "success": False,
                    "message": "Invalid command format: expected dictionary"
                }
            
            action = command_dict.get("action", "")
            parameters = command_dict.get("parameters", {})
            steps = command_dict.get("steps", [])
            
            if not action:
                return {
                    "success": False,
                    "message": "No action specified in command"
                }
            
            if steps and len(steps) > 0:
                return self.execute_workflow(steps)
            else:
                result = self.execute_single_action(action, parameters)
                
                if isinstance(result, dict) and "original_result" in result:
                    return result
                
                return self._humanize_result(action, result)
        
        except Exception as e:
            error_result = {
                "success": False,
                "message": f"Error executing command: {str(e)}"
            }
            return self._humanize_result("command_execution", error_result)
    
    def execute_workflow(self, workflow_steps: list) -> dict:
        """
        Execute multi-step workflows with humanized feedback
        
        Args:
            workflow_steps: List of action dictionaries to execute in sequence
        
        Returns:
            Dict with workflow results and humanized messages
        """
        results = []
        all_success = True
        
        intro_msg = self.persona_service.handle_processing()
        print(intro_msg)
        
        for i, step in enumerate(workflow_steps, 1):
            action = step.get("action")
            parameters = step.get("parameters", {})
            
            print(f"\n📋 Step {i}/{len(workflow_steps)}: {action}")
            
            step_result = self.execute_single_action(action, parameters)
            results.append({
                "step": i,
                "action": action,
                "result": step_result
            })
            
            if not step_result.get("success", False):
                all_success = False
                error_msg = self.persona_service.handle_misunderstanding()
                print(f"❌ {error_msg}")
                break
        
        workflow_result = {
            "success": all_success,
            "message": f"Workflow completed: {len(results)}/{len(workflow_steps)} steps executed",
            "steps": results
        }
        
        return self._humanize_result("workflow", workflow_result)
    
    def execute_single_action(self, action: str, parameters: dict = None) -> dict:
        """
        Execute a single action with Desktop RAG and Communication enhancements
        
        Args:
            action: Action name to execute
            parameters: Action parameters
        
        Returns:
            Dict with execution result and humanized message
        """
        parameters = parameters or {}
        
        try:
            if action == "index_desktop_rag":
                folder_path = parameters.get("folder_path", ".")
                result = self.desktop_rag.index_folder(folder_path)
                if result.get("success"):
                    msg = f"✅ Desktop indexed successfully!\n\n"
                    msg += f"📊 Indexed {result['files_indexed']} files\n"
                    msg += f"💾 Total size: {result['total_size_mb']} MB\n"
                    msg += f"⏱️  Time: {result['time_taken']:.2f}s\n"
                    return {"success": True, "message": msg}
                else:
                    return {"success": False, "message": f"❌ Error: {result.get('error', 'Unknown error')}"}

            elif action == "search_files_rag":
                query = parameters.get("query", "")
                if not query:
                    return {"success": False, "message": "Please provide a search query"}
                
                result = self.desktop_rag.search_files(query)
                if result.get("success"):
                    msg = f"🔍 Search Results for: '{query}'\n\n"
                    msg += f"Found {result['total_results']} relevant files\n\n"
                    if result.get('relevant_files'):
                        msg += "Top matches:\n"
                        for f in result.get('relevant_files')[:5]:
                            msg += f"  • {f}\n"
                    return {"success": True, "message": msg}
                else:
                    return {"success": False, "message": f"❌ Error: {result.get('error', 'Unknown error')}"}

            elif action == "summarize_folder_rag":
                folder_path = parameters.get("folder_path", ".")
                result = self.desktop_rag.summarize_folder(folder_path)
                if result.get("success"):
                    msg = f"📊 Folder Summary: {folder_path}\n\n"
                    msg += f"📁 Files: {result['file_count']}\n"
                    msg += f"💾 Size: {result['total_size_mb']} MB\n\n"
                    msg += f"AI Analysis:\n{result['summary']}\n"
                    return {"success": True, "message": msg}
                else:
                    return {"success": False, "message": f"❌ Error: {result.get('error', 'Unknown error')}"}

            elif action == "find_duplicates_rag":
                result = self.desktop_rag.find_duplicates_smart()
                if result.get("success"):
                    msg = f"🔍 Smart Duplicate Detection\n\n"
                    msg += f"Found {result['duplicates_found']} potential duplicates\n"
                    msg += f"💾 Potential savings: {result['potential_savings_mb']:.2f} MB\n\n"
                    if result.get('duplicates'):
                        msg += "Top duplicates:\n"
                        for dup in result['duplicates'][:10]:
                            msg += f"\n  • {dup['name']}\n"
                            msg += f"    File 1: {dup['file1']}\n"
                            msg += f"    File 2: {dup['file2']}\n"
                            msg += f"    Confidence: {dup['confidence']}\n"
                    return {"success": True, "message": msg}
                else:
                    return {"success": False, "message": "❌ Error finding duplicates"}

            elif action == "get_rag_stats":
                stats = self.desktop_rag.get_index_stats()
                msg = f"📊 Desktop RAG Index Statistics\n\n"
                msg += f"Total files indexed: {stats['total_files']}\n"
                if stats['total_files'] > 0:
                    msg += f"Files with text content: {stats['files_with_text_content']}\n"
                    msg += f"Total size: {stats['total_size_mb']} MB\n"
                    msg += f"Last updated: {stats['last_updated']}\n\n"
                    msg += "Top file types:\n"
                    for ext, count in list(stats['file_types'].items())[:10]:
                        msg += f"  {ext}: {count} files\n"
                else:
                    msg += "\nNo files indexed yet. Try 'Index my desktop files' first."
                return {"success": True, "message": msg}

            elif action == "transcribe_voice":
                audio_file = parameters.get("audio_file")
                audio_url = parameters.get("audio_url")
                result = self.comm_enhancements.transcribe_voice_message(audio_file, audio_url)
                if result.get("success"):
                    return {"success": True, "message": f"🎤 Voice Transcription:\n\n{result['transcription']}"}
                else:
                    return {"success": False, "message": result.get("message", "Transcription failed")}

            elif action == "generate_smart_replies":
                message_data = parameters.get("message_data", {})
                context = parameters.get("context", "professional")
                result = self.comm_enhancements.generate_smart_replies(message_data, context)
                if result.get("success"):
                    msg = f"💬 {result['message']}\n\n"
                    for i, reply in enumerate(result['replies'], 1):
                        msg += f"Option {i} ({reply['type']}):\n{reply['text']}\n\n"
                    return {"success": True, "message": msg}
                else:
                    return {"success": False, "message": result.get("message")}

            elif action == "rank_emails":
                emails = parameters.get("emails", [])
                result = self.comm_enhancements.rank_emails_by_priority(emails)
                if result.get("success"):
                    msg = f"📊 {result['message']}\n\n"
                    summary = result.get("summary", {})
                    msg += f"Critical: {summary.get('critical', 0)} | High: {summary.get('high', 0)} | "
                    msg += f"Medium: {summary.get('medium', 0)} | Low: {summary.get('low', 0)}\n\n"
                    msg += "Top Priority Emails:\n"
                    for i, email in enumerate(result['ranked_emails'][:5], 1):
                        msg += f"\n{i}. [{email['priority_level']}] {email.get('subject', 'No subject')}\n"
                        msg += f"   From: {email.get('from', 'Unknown')}\n"
                        msg += f"   Score: {email['priority_score']}/100\n"
                    return {"success": True, "message": msg}
                else:
                    return {"success": False, "message": result.get("message")}

            elif action == "add_followup":
                message_data = parameters.get("message_data", {})
                days = parameters.get("days", 3)
                result = self.comm_enhancements.add_follow_up_reminder(message_data, days)
                if result.get("success"):
                    return {"success": True, "message": f"⏰ {result['message']}\nRemind at: {result['remind_date']}"}
                else:
                    return {"success": False, "message": result.get("message")}

            elif action == "check_followups":
                result = self.comm_enhancements.check_follow_up_reminders()
                if result.get("success"):
                    msg = f"{result['message']}\n\n"
                    if result['due_reminders']:
                        msg += "Due Follow-ups:\n"
                        for reminder in result['due_reminders']:
                            msg += f"\n• {reminder['message'].get('subject', 'Message')}\n"
                            msg += f"  From: {reminder['message'].get('from')}\n"
                            msg += f"  Platform: {reminder['message'].get('platform')}\n"
                    return {"success": True, "message": msg}
                else:
                    return {"success": False, "message": result.get("message")}

            elif action == "send_meeting_notes":
                meeting_data = parameters.get("meeting_data", {})
                recipients = parameters.get("recipients", [])
                result = self.comm_enhancements.send_meeting_notes(meeting_data, recipients)
                return result

            elif action == "summarize_chat":
                messages = parameters.get("messages", [])
                platform = parameters.get("platform", "Slack")
                result = self.comm_enhancements.summarize_chat_thread(messages, platform)
                if result.get("success"):
                    return {"success": True, "message": f"📝 {result['message']}\n\n{result['summary']}"}
                else:
                    return {"success": False, "message": result.get("message")}

            elif action == "multilingual_reply":
                message_data = parameters.get("message_data", {})
                detect = parameters.get("detect_language", True)
                result = self.comm_enhancements.generate_multilingual_reply(message_data, detect)
                if result.get("success"):
                    msg = f"🌐 {result['message']}\n\n"
                    msg += f"Language: {result['detected_language']}\n\n"
                    msg += f"Reply:\n{result['reply']}"
                    return {"success": True, "message": msg}
                else:
                    return {"success": False, "message": result.get("message")}

            elif action == "voice_to_task":
                voice_text = parameters.get("voice_text", "")
                add_to_calendar = parameters.get("add_to_calendar", True)
                result = self.comm_enhancements.convert_voice_to_task(voice_text, add_to_calendar)
                if result.get("success"):
                    extracted = result['extracted']
                    msg = f"✅ {result['message']}\n\n"
                    msg += f"Type: {extracted.get('type', 'task').upper()}\n"
                    msg += f"Title: {extracted.get('title')}\n"
                    msg += f"Priority: {extracted.get('priority')}\n"
                    if extracted.get('datetime'):
                        msg += f"Date/Time: {extracted['datetime']}\n"
                    msg += f"Category: {extracted.get('category')}\n\n"
                    msg += f"Action Items:\n"
                    for item in extracted.get('action_items', []):
                        msg += f"  • {item}\n"
                    return {"success": True, "message": msg}
                else:
                    return {"success": False, "message": result.get("message")}

            elif action == "comm_features_summary":
                summary = self.comm_enhancements.get_feature_summary()
                return {"success": True, "message": summary}
            
            elif action == "chatbot" or action == "chat" or action == "ask":
                from modules.core.gemini_controller import chat_response
                message = parameters.get("message", "")
                if not message:
                    return {"success": False, "message": "Please provide a message to chat"}
                
                try:
                    response = chat_response(message)
                    return {"success": True, "message": f"🤖 {response}"}
                except Exception as e:
                    return {"success": False, "message": f"Chat error: {str(e)}"}
            
            elif action == "conversational_ai":
                from modules.core.gemini_controller import chat_response
                message = parameters.get("message", "")
                context = parameters.get("context", "general")
                
                try:
                    response = chat_response(message)
                    return {"success": True, "message": response}
                except Exception as e:
                    return {"success": False, "message": f"Error: {str(e)}"}
            
            elif action == "customer_service_bot":
                from modules.core.gemini_controller import chat_response
                query = parameters.get("query", "")
                company_context = parameters.get("company_context", "")
                
                prompt = f"Customer query: {query}\nCompany context: {company_context}" if company_context else query
                try:
                    response = chat_response(prompt)
                    return {"success": True, "message": response}
                except Exception as e:
                    return {"success": False, "message": f"Error: {str(e)}"}
            
            elif action == "educational_assistant":
                from modules.core.gemini_controller import chat_response
                topic = parameters.get("topic", "")
                question = parameters.get("question", "")
                level = parameters.get("level", "intermediate")
                
                prompt = f"Topic: {topic}\nLevel: {level}\nQuestion: {question}"
                try:
                    response = chat_response(prompt)
                    return {"success": True, "message": response}
                except Exception as e:
                    return {"success": False, "message": f"Error: {str(e)}"}
            
            elif action == "domain_expert":
                from modules.core.gemini_controller import chat_response
                domain = parameters.get("domain", "")
                question = parameters.get("question", "")
                
                prompt = f"As an expert in {domain}, please answer: {question}"
                try:
                    response = chat_response(prompt)
                    return {"success": True, "message": response}
                except Exception as e:
                    return {"success": False, "message": f"Error: {str(e)}"}

            elif action == "error":
                error_msg = parameters.get("error", "Unknown error")
                return {
                    "success": False,
                    "message": f"Command parsing error: {error_msg}"
                }

            else:
                result = {
                    "success": False,
                    "message": f"Unknown action: {action}"
                }
                return self._humanize_result(action, result)

        except Exception as e:
            result = {
                "success": False,
                "message": f"Error executing {action}: {str(e)}"
            }
            return self._humanize_result(action, result)
