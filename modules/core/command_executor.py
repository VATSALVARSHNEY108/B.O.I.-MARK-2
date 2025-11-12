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
        
        final_message = humanized_message
        
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
            
            elif action == "get_time":
                from datetime import datetime
                now = datetime.now()
                time_str = now.strftime("%I:%M %p")
                return {"success": True, "message": f"⏰ {time_str}"}
            
            elif action == "get_date":
                from datetime import datetime
                now = datetime.now()
                date_str = now.strftime("%A, %B %d, %Y")
                return {"success": True, "message": f"📅 {date_str}"}
            
            elif action == "get_date_time":
                from datetime import datetime
                now = datetime.now()
                dt_str = now.strftime("%A, %B %d, %Y at %I:%M %p")
                return {"success": True, "message": f"📅 {dt_str}"}
            
            elif action == "get_day_info":
                from datetime import datetime
                now = datetime.now()
                day_str = now.strftime("%A")
                return {"success": True, "message": f"📅 Today is {day_str}"}
            
            elif action == "get_quick_weather":
                city = parameters.get("city", "New York")
                try:
                    import requests
                    url = f"https://wttr.in/{city}?format=j1"
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        current = data['current_condition'][0]
                        weather_report = f"🌤️ {city}: {current['temp_C']}°C ({current['temp_F']}°F), {current['weatherDesc'][0]['value']}"
                        return {"success": True, "message": weather_report}
                    else:
                        return {"success": False, "message": f"Couldn't fetch weather for {city}"}
                except Exception as e:
                    return {"success": False, "message": f"Weather error: {str(e)}"}

            elif action == "get_forecast":
                city = parameters.get("city", "New York")
                days = max(1, int(parameters.get("days", 3)))
                try:
                    import requests
                    url = f"https://wttr.in/{city}?format=j1"
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        forecast_data = data['weather'][:days]
                        forecast = f"📅 {days}-day forecast for {city}:\n"
                        for day in forecast_data:
                            forecast += f"{day['date']}: {day['maxtempC']}°C/{day['mintempC']}°C - {day['hourly'][0]['weatherDesc'][0]['value']}\n"
                        return {"success": True, "message": forecast}
                    else:
                        return {"success": False, "message": f"Couldn't fetch forecast for {city}"}
                except Exception as e:
                    return {"success": False, "message": f"Forecast error: {str(e)}"}
            
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
            
            # TEXT GENERATION AI
            elif action == "story_writer":
                from modules.core.gemini_controller import chat_response
                prompt_text = parameters.get("prompt", "")
                genre = parameters.get("genre", "general")
                length = parameters.get("length", "medium")
                
                full_prompt = f"Write a {length} {genre} story based on: {prompt_text}"
                try:
                    response = chat_response(full_prompt)
                    return {"success": True, "message": f"📖 Story:\n\n{response}"}
                except Exception as e:
                    return {"success": False, "message": f"Error: {str(e)}"}
            
            elif action == "content_creator":
                from modules.core.gemini_controller import chat_response
                topic = parameters.get("topic", "")
                content_type = parameters.get("content_type", "blog post")
                tone = parameters.get("tone", "professional")
                
                prompt = f"Create a {tone} {content_type} about: {topic}"
                try:
                    response = chat_response(prompt)
                    return {"success": True, "message": f"✍️ Content:\n\n{response}"}
                except Exception as e:
                    return {"success": False, "message": f"Error: {str(e)}"}
            
            elif action == "article_generator":
                from modules.core.gemini_controller import chat_response
                title = parameters.get("title", "")
                keywords = parameters.get("keywords", [])
                word_count = parameters.get("word_count", 800)
                
                keyword_str = ", ".join(keywords) if keywords else ""
                prompt = f"Write a {word_count}-word article titled '{title}'"
                if keyword_str:
                    prompt += f" including keywords: {keyword_str}"
                
                try:
                    response = chat_response(prompt)
                    return {"success": True, "message": f"📰 Article:\n\n{response}"}
                except Exception as e:
                    return {"success": False, "message": f"Error: {str(e)}"}
            
            elif action == "copywriting_assistant":
                from modules.core.gemini_controller import chat_response
                product = parameters.get("product", "")
                goal = parameters.get("goal", "persuade")
                
                prompt = f"Create persuasive marketing copy to {goal} for: {product}"
                try:
                    response = chat_response(prompt)
                    return {"success": True, "message": f"💼 Marketing Copy:\n\n{response}"}
                except Exception as e:
                    return {"success": False, "message": f"Error: {str(e)}"}
            
            elif action == "technical_writer":
                from modules.core.gemini_controller import chat_response
                topic = parameters.get("topic", "")
                audience = parameters.get("audience", "technical")
                
                prompt = f"Write technical documentation for {audience} audience about: {topic}"
                try:
                    response = chat_response(prompt)
                    return {"success": True, "message": f"📚 Technical Documentation:\n\n{response}"}
                except Exception as e:
                    return {"success": False, "message": f"Error: {str(e)}"}
            
            # LANGUAGE PROCESSING AI
            elif action == "text_translator":
                from modules.core.gemini_controller import chat_response
                text = parameters.get("text", "")
                target_language = parameters.get("target_language", "")
                source_language = parameters.get("source_language", "auto")
                
                prompt = f"Translate from {source_language} to {target_language}: {text}"
                try:
                    response = chat_response(prompt)
                    return {"success": True, "message": f"🌐 Translation:\n\n{response}"}
                except Exception as e:
                    return {"success": False, "message": f"Error: {str(e)}"}
            
            elif action == "sentiment_analysis":
                from modules.core.gemini_controller import chat_response
                text = parameters.get("text", "")
                
                prompt = f"Analyze the sentiment of this text and provide a detailed emotional analysis: {text}"
                try:
                    response = chat_response(prompt)
                    return {"success": True, "message": f"😊 Sentiment Analysis:\n\n{response}"}
                except Exception as e:
                    return {"success": False, "message": f"Error: {str(e)}"}
            
            elif action == "text_summarizer":
                from modules.core.gemini_controller import chat_response
                text = parameters.get("text", "")
                length = parameters.get("length", "medium")
                
                prompt = f"Provide a {length} summary of: {text}"
                try:
                    response = chat_response(prompt)
                    return {"success": True, "message": f"📝 Summary:\n\n{response}"}
                except Exception as e:
                    return {"success": False, "message": f"Error: {str(e)}"}
            
            elif action == "language_detector":
                from modules.core.gemini_controller import chat_response
                text = parameters.get("text", "")
                
                prompt = f"Identify the language of this text: {text}"
                try:
                    response = chat_response(prompt)
                    return {"success": True, "message": f"🔍 Language Detection:\n\n{response}"}
                except Exception as e:
                    return {"success": False, "message": f"Error: {str(e)}"}
            
            elif action == "content_moderator":
                from modules.core.gemini_controller import chat_response
                text = parameters.get("text", "")
                
                prompt = f"Analyze this content for inappropriate material, hate speech, violence, or policy violations: {text}"
                try:
                    response = chat_response(prompt)
                    return {"success": True, "message": f"🛡️ Content Moderation:\n\n{response}"}
                except Exception as e:
                    return {"success": False, "message": f"Error: {str(e)}"}
            
            # IMAGE GENERATION AI
            elif action == "image_description_generator":
                from modules.core.gemini_controller import chat_response
                concept = parameters.get("concept", "")
                style = parameters.get("style", "realistic")
                
                prompt = f"Generate a detailed AI art prompt in {style} style for: {concept}"
                try:
                    response = chat_response(prompt)
                    return {"success": True, "message": f"🎨 AI Art Prompt:\n\n{response}"}
                except Exception as e:
                    return {"success": False, "message": f"Error: {str(e)}"}
            
            elif action == "style_transfer_description":
                from modules.core.gemini_controller import chat_response
                content = parameters.get("content", "")
                style = parameters.get("style", "")
                
                prompt = f"Describe how to apply {style} style to {content} for style transfer"
                try:
                    response = chat_response(prompt)
                    return {"success": True, "message": f"🎭 Style Transfer:\n\n{response}"}
                except Exception as e:
                    return {"success": False, "message": f"Error: {str(e)}"}

            # SYSTEM MONITORING
            elif action == "system_report":
                from modules.system.system_monitor import get_full_system_report
                report = get_full_system_report()
                return {"success": True, "message": report}
            
            elif action == "check_cpu":
                from modules.system.system_monitor import get_cpu_usage
                cpu = get_cpu_usage()
                msg = f"💻 CPU: {cpu['usage_percent']}% ({cpu['status']}) - {cpu['cpu_count']} cores @ {cpu['current_frequency']}"
                return {"success": True, "message": msg}
            
            elif action == "check_memory":
                from modules.system.system_monitor import get_memory_usage
                mem = get_memory_usage()
                msg = f"💾 RAM: {mem['used_gb']}/{mem['total_gb']} ({mem['usage_percent']}%) - {mem['status']}"
                return {"success": True, "message": msg}
            
            elif action == "check_disk":
                from modules.system.system_monitor import get_disk_usage
                disk = get_disk_usage()
                msg = f"💿 Disk: {disk['used_gb']}/{disk['total_gb']} ({disk['usage_percent']}%) - {disk['status']}"
                return {"success": True, "message": msg}
            
            # CODE GENERATION & EXECUTION
            elif action == "generate_code":
                from modules.ai_features.code_generation import generate_code_with_gemini
                description = parameters.get("description", "")
                language = parameters.get("language", "python")
                try:
                    code = generate_code_with_gemini(description, language)
                    return {"success": True, "message": f"```{language}\n{code}\n```"}
                except Exception as e:
                    return {"success": False, "message": f"Code generation failed: {str(e)}"}
            
            elif action == "execute_code":
                code = parameters.get("code", "")
                language = parameters.get("language", "python")
                if language == "python":
                    import subprocess
                    try:
                        result = subprocess.run(
                            ["python", "-c", code],
                            capture_output=True,
                            text=True,
                            timeout=10
                        )
                        output = result.stdout if result.returncode == 0 else result.stderr
                        return {"success": result.returncode == 0, "message": f"Output:\n{output}"}
                    except Exception as e:
                        return {"success": False, "message": f"Execution error: {str(e)}"}
                else:
                    return {"success": False, "message": f"Language {language} not supported for execution"}
            
            elif action == "explain_code":
                from modules.ai_features.code_generation import explain_code_with_gemini
                code = parameters.get("code", "")
                language = parameters.get("language", "python")
                try:
                    explanation = explain_code_with_gemini(code, language)
                    return {"success": True, "message": explanation}
                except Exception as e:
                    return {"success": False, "message": f"Code explanation failed: {str(e)}"}
            
            # BASIC OPERATIONS
            elif action == "search_web":
                query = parameters.get("query", "")
                import webbrowser
                try:
                    webbrowser.open(f"https://www.google.com/search?q={query}")
                    return {"success": True, "message": f"Opened web search for: {query}"}
                except Exception as e:
                    return {"success": False, "message": f"Search failed: {str(e)}"}
            
            elif action == "screenshot":
                import pyautogui
                filename = parameters.get("filename", f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                try:
                    screenshot = pyautogui.screenshot()
                    screenshot.save(filename)
                    return {"success": True, "message": f"Screenshot saved as {filename}"}
                except Exception as e:
                    return {"success": False, "message": f"Screenshot failed: {str(e)}"}
            
            elif action == "copy_text":
                text = parameters.get("text", "")
                try:
                    import pyperclip
                    pyperclip.copy(text)
                    return {"success": True, "message": "Text copied to clipboard"}
                except Exception as e:
                    return {"success": False, "message": f"Copy failed: {str(e)}"}
            
            elif action == "paste_text":
                try:
                    import pyperclip
                    text = pyperclip.paste()
                    return {"success": True, "message": f"Clipboard: {text}"}
                except Exception as e:
                    return {"success": False, "message": f"Paste failed: {str(e)}"}
            
            # FILE OPERATIONS
            elif action == "search_files":
                import os
                query = parameters.get("query", "")
                directory = parameters.get("directory", ".")
                matches = []
                try:
                    for root, dirs, files in os.walk(directory):
                        for file in files:
                            if query.lower() in file.lower():
                                matches.append(os.path.join(root, file))
                                if len(matches) >= 20:
                                    break
                        if len(matches) >= 20:
                            break
                    
                    if matches:
                        msg = f"Found {len(matches)} files:\n" + "\n".join(matches[:10])
                        if len(matches) > 10:
                            msg += f"\n... and {len(matches) - 10} more"
                        return {"success": True, "message": msg}
                    else:
                        return {"success": False, "message": "No files found"}
                except Exception as e:
                    return {"success": False, "message": f"Search failed: {str(e)}"}
            
            elif action == "find_large_files":
                import os
                directory = parameters.get("directory", ".")
                min_size_mb = parameters.get("min_size_mb", 10)
                large_files = []
                try:
                    for root, dirs, files in os.walk(directory):
                        for file in files:
                            filepath = os.path.join(root, file)
                            try:
                                size_mb = os.path.getsize(filepath) / (1024 * 1024)
                                if size_mb >= min_size_mb:
                                    large_files.append((filepath, size_mb))
                            except:
                                pass
                    
                    large_files.sort(key=lambda x: x[1], reverse=True)
                    if large_files:
                        msg = f"Found {len(large_files)} large files (>{min_size_mb}MB):\n"
                        for filepath, size in large_files[:10]:
                            msg += f"{size:.1f}MB - {filepath}\n"
                        return {"success": True, "message": msg}
                    else:
                        return {"success": False, "message": f"No files larger than {min_size_mb}MB found"}
                except Exception as e:
                    return {"success": False, "message": f"Search failed: {str(e)}"}
            
            elif action == "directory_size":
                import os
                directory = parameters.get("directory", ".")
                total_size = 0
                try:
                    for root, dirs, files in os.walk(directory):
                        for file in files:
                            filepath = os.path.join(root, file)
                            try:
                                total_size += os.path.getsize(filepath)
                            except:
                                pass
                    
                    size_mb = total_size / (1024 * 1024)
                    size_gb = total_size / (1024 * 1024 * 1024)
                    
                    if size_gb >= 1:
                        return {"success": True, "message": f"Directory size: {size_gb:.2f} GB"}
                    else:
                        return {"success": True, "message": f"Directory size: {size_mb:.2f} MB"}
                except Exception as e:
                    return {"success": False, "message": f"Size calculation failed: {str(e)}"}
            
            # SYSTEM CONTROL
            elif action == "set_volume":
                level = parameters.get("level", 50)
                # Note: Volume control varies by OS, this is a stub
                return {"success": False, "message": "Volume control not yet implemented for this system"}
            
            elif action == "mute_system":
                return {"success": False, "message": "Mute control not yet implemented for this system"}
            
            elif action == "set_brightness":
                level = parameters.get("level", 50)
                return {"success": False, "message": "Brightness control not yet implemented for this system"}
            
            elif action == "shutdown_system":
                return {"success": False, "message": "For safety, system shutdown must be done manually"}
            
            elif action == "restart_system":
                return {"success": False, "message": "For safety, system restart must be done manually"}
            
            elif action == "lock_screen":
                import subprocess
                import platform
                try:
                    if platform.system() == "Windows":
                        subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
                    elif platform.system() == "Darwin":  # macOS
                        subprocess.run(["/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession", "-suspend"])
                    else:  # Linux
                        subprocess.run(["xdg-screensaver", "lock"])
                    return {"success": True, "message": "Screen locked"}
                except Exception as e:
                    return {"success": False, "message": f"Lock screen failed: {str(e)}"}

            # DESKTOP AUTOMATION
            elif action == "open_app":
                app_name = parameters.get("app_name", "")
                import subprocess
                import platform
                try:
                    if platform.system() == "Windows":
                        subprocess.Popen(app_name)
                    elif platform.system() == "Darwin":  # macOS
                        subprocess.Popen(["open", "-a", app_name])
                    else:  # Linux
                        subprocess.Popen(app_name, shell=True)
                    return {"success": True, "message": f"Opening {app_name}"}
                except Exception as e:
                    return {"success": False, "message": f"Failed to open {app_name}: {str(e)}"}
            
            elif action == "type_text":
                text = parameters.get("text", "")
                import pyautogui
                try:
                    pyautogui.write(text, interval=0.05)
                    return {"success": True, "message": f"Typed: {text[:50]}..."}
                except Exception as e:
                    return {"success": False, "message": f"Typing failed: {str(e)}"}
            
            elif action == "press_key":
                key = parameters.get("key", "")
                import pyautogui
                try:
                    pyautogui.press(key)
                    return {"success": True, "message": f"Pressed {key}"}
                except Exception as e:
                    return {"success": False, "message": f"Key press failed: {str(e)}"}
            
            elif action == "click_mouse":
                x = parameters.get("x")
                y = parameters.get("y")
                import pyautogui
                try:
                    if x and y:
                        pyautogui.click(x, y)
                        return {"success": True, "message": f"Clicked at ({x}, {y})"}
                    else:
                        pyautogui.click()
                        return {"success": True, "message": "Clicked at current position"}
                except Exception as e:
                    return {"success": False, "message": f"Click failed: {str(e)}"}
            
            elif action == "move_mouse":
                x = parameters.get("x", 0)
                y = parameters.get("y", 0)
                import pyautogui
                try:
                    pyautogui.moveTo(x, y)
                    return {"success": True, "message": f"Moved mouse to ({x}, {y})"}
                except Exception as e:
                    return {"success": False, "message": f"Mouse move failed: {str(e)}"}
            
            elif action == "hotkey":
                keys = parameters.get("keys", [])
                import pyautogui
                try:
                    pyautogui.hotkey(*keys)
                    return {"success": True, "message": f"Pressed hotkey: {'+'.join(keys)}"}
                except Exception as e:
                    return {"success": False, "message": f"Hotkey failed: {str(e)}"}

            elif action == "error":
                error_msg = parameters.get("error", "Unknown error")
                return {
                    "success": False,
                    "message": f"Command parsing error: {error_msg}"
                }

            else:
                # Log unimplemented action for future prioritization
                import logging
                logging.info(f"Unimplemented action requested: {action}")
                
                # Provide helpful stub response
                stub_message = f"The '{action}' feature is not yet implemented. "
                stub_message += "Available features include: system monitoring, code generation, "
                stub_message += "file operations, web search, screenshots, and basic automation."
                
                result = {
                    "success": False,
                    "message": stub_message
                }
                return self._humanize_result(action, result)

        except Exception as e:
            result = {
                "success": False,
                "message": f"Error executing {action}: {str(e)}"
            }
            return self._humanize_result(action, result)
