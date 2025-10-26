ask in enumerate(prioritized[:10], 1):
                    score = task.get('priority_score', 0)
                    self.update_output(f"\n{i}. [{score:.0f}/100] {task.get('title', 'N/A')}\n", "info")
                    if task.get('deadline'):
                        self.update_output(f"   Deadline: {task['deadline'][:10]}\n", "success")
                    if task.get('priority_reason'):
                        self.update_output(f"   Why: {task['priority_reason']}\n", "info")
                
                suggestions = self.smart_automation.task_prioritizer.get_task_suggestions()
                if suggestions:
                    self.update_output(f"\n💡 Suggestions:\n", "success")
                    for suggestion in suggestions:
                        self.update_output(f"• {suggestion}\n", "info")
            else:
                self.update_output("ℹ️ No tasks to prioritize. Add tasks first!\n", "info")
        
        threading.Thread(target=execute, daemon=True).start()
    
    def smart_workflow_optimizer(self):
        """Workflow Auto-Optimizer interface"""
        def execute():
            self.update_output("\n🔧 Workflow Auto-Optimizer\n", "command")
            self.update_output("=" * 60 + "\n", "info")
            
            self.update_output("Analyzing workflow patterns...\n", "info")
            report = self.smart_automation.workflow_optimizer.get_efficiency_report()
            
            self.update_output(f"\n📊 Efficiency Report\n", "success")
            self.update_output(f"Total Actions: {report.get('total_actions', 0)}\n", "info")
            self.update_output(f"Detected Patterns: {report.get('detected_patterns', 0)}\n", "info")
            self.update_output(f"Optimizable Actions: {report.get('optimizable_actions', 0)}\n", "info")
            self.update_output(f"Efficiency Score: {report.get('efficiency_score', 0)}/100\n", "success")
            
            if report.get('top_patterns'):
                self.update_output(f"\n🔄 Top Repeated Patterns:\n", "success")
                for pattern in report['top_patterns'][:5]:
                    self.update_output(f"• {pattern.get('pattern', 'N/A')} ({pattern.get('occurrences', 0)}x)\n", "info")
            
            if report.get('recommendations'):
                self.update_output(f"\n💡 Recommendations:\n", "success")
                for rec in report['recommendations']:
                    self.update_output(f"• {rec}\n", "info")
            
            self.update_output("\nGenerating optimization suggestions...\n", "info")
            optimizations = self.smart_automation.workflow_optimizer.suggest_optimizations()
            
            if optimizations:
                self.update_output(f"\n✅ Optimization Suggestions:\n", "success")
                for i, opt in enumerate(optimizations[:5], 1):
                    self.update_output(f"\n{i}. Pattern: {opt.get('pattern', 'N/A')}\n", "info")
                    self.update_output(f"   Suggestion: {opt.get('suggestion', 'N/A')}\n", "success")
                    self.update_output(f"   Time Saved: {opt.get('time_saved', 'N/A')}\n", "info")
                    self.update_output(f"   Difficulty: {opt.get('difficulty', 'N/A')}\n", "info")
        
        threading.Thread(target=execute, daemon=True).start()
    
    def smart_template_generator(self):
        """Smart Template Generator interface"""
        def execute():
            self.update_output("\n📋 Smart Template Generator\n", "command")
            self.update_output("=" * 60 + "\n", "info")
            
            template_type = self.show_input_dialog(
                "Template Type",
                "What type of template?\n1. Code template\n2. Email template\n3. Document template\n\nEnter number (1-3):"
            )
            
            if template_type == "1":
                language = self.show_input_dialog("Language", "Programming language (e.g., python, javascript):")
                template_kind = self.show_input_dialog("Type", "Template type (e.g., class, function, api):")
                
                if language and template_kind:
                    self.update_output(f"Generating {language} {template_kind} template...\n", "info")
                    template = self.smart_automation.template_generator.generate_code_template(
                        language, template_kind
                    )
                    self.update_output(f"\n✅ Code Template Generated!\n", "success")
                    self.update_output(f"{template[:500]}...\n", "info")
            
            elif template_type == "2":
                purpose = self.show_input_dialog("Purpose", "Email purpose (e.g., job application, follow-up):")
                tone = self.show_input_dialog("Tone", "Tone (professional/casual/friendly):", "professional")
                
                if purpose:
                    self.update_output(f"Generating email template...\n", "info")
                    template = self.smart_automation.template_generator.generate_email_template(
                        purpose, tone if tone else "professional"
                    )
                    self.update_output(f"\n✅ Email Template Generated!\n", "success")
                    self.update_output(f"{template[:400]}...\n", "info")
            
            elif template_type == "3":
                doc_type = self.show_input_dialog("Document Type", "Document type (e.g., proposal, report):")
                
                if doc_type:
                    self.update_output(f"Generating document template...\n", "info")
                    template = self.smart_automation.template_generator.generate_document_template(doc_type)
                    self.update_output(f"\n✅ Document Template Generated!\n", "success")
                    self.update_output(f"{template[:400]}...\n", "info")
            
            templates = self.smart_automation.template_generator.list_templates()
            self.update_output(f"\n📋 Total Templates Created: {len(templates)}\n", "success")
        
        threading.Thread(target=execute, daemon=True).start()
    
    def smart_automation_dashboard(self):
        """Show Smart Automation Dashboard"""
        def execute():
            self.update_output("\n📊 Smart Automation Dashboard\n", "command")
            self.update_output("=" * 60 + "\n", "info")
            
            summary = self.smart_automation.get_dashboard_summary()
            
            self.update_output(f"\n🐛 Auto-Bug Fixer\n", "success")
            self.update_output(f"Fixes Applied: {summary['auto_bug_fixer']['fixes_applied']}\n", "info")
            
            self.update_output(f"\n📅 Meeting Scheduler\n", "success")
            self.update_output(f"Upcoming Meetings: {summary['meeting_scheduler']['upcoming_meetings']}\n", "info")
            
            self.update_output(f"\n📁 File Recommender\n", "success")
            self.update_output(f"Tracked Files: {summary['file_recommender']['tracked_files']}\n", "info")
            
            self.update_output(f"\n⚡ Command Shortcuts\n", "success")
            self.update_output(f"Shortcuts Created: {summary['command_shortcuts']['shortcuts_created']}\n", "info")
            
            self.update_output(f"\n🔀 Project Contexts\n", "success")
            self.update_output(f"Saved Contexts: {summary['project_contexts']['saved_contexts']}\n", "info")
            
            self.update_output(f"\n🎯 Task Prioritizer\n", "success")
            self.update_output(f"Pending Tasks: {summary['task_prioritizer']['pending_tasks']}\n", "info")
            
            self.update_output(f"\n🔧 Workflow Optimizer\n", "success")
            self.update_output(f"Patterns Detected: {summary['workflow_optimizer']['patterns_detected']}\n", "info")
            self.update_output(f"Efficiency Score: {summary['workflow_optimizer']['efficiency_score']}/100\n", "info")
            
            self.update_output(f"\n📋 Template Generator\n", "success")
            self.update_output(f"Templates Created: {summary['template_generator']['templates_created']}\n", "info")
            
            self.update_output("\n" + "=" * 60 + "\n", "info")
        
        threading.Thread(target=execute, daemon=True).start()
    
    def show_input_dialog(self, title, prompt, default=""):
        """Helper method to show input dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("500x200")
        dialog.configure(bg="#1a1a2e")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text=prompt,
                bg="#1a1a2e", fg="#ffffff",
                font=("Segoe UI", 10),
                wraplength=450).pack(pady=20, padx=20)
        
        entry = tk.Entry(dialog, font=("Segoe UI", 11), width=40)
        entry.insert(0, default)
        entry.pack(pady=10)
        entry.focus()
        
        result: list = [None]
        
        def on_ok():
            result[0] = entry.get()
            dialog.destroy()
        
        def on_cancel():
            dialog.destroy()
        
        entry.bind("<Return>", lambda e: on_ok())
        entry.bind("<Escape>", lambda e: on_cancel())
        
        btn_frame = tk.Frame(dialog, bg="#1a1a2e")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="OK", command=on_ok,
                 bg="#89b4fa", fg="#0f0f1e",
                 font=("Segoe UI", 10, "bold"),
                 padx=20, pady=5).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="Cancel", command=on_cancel,
                 bg="#313244", fg="#ffffff",
                 font=("Segoe UI", 10),
                 padx=20, pady=5).pack(side="left", padx=5)
        
        dialog.wait_window()
        return result[0]

def main():
    root = tk.Tk()
    app = AutomationControllerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
