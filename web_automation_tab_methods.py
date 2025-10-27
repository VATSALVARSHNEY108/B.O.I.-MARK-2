# Methods to add to AutomationControllerGUI class for Web Automation tab

def create_web_automation_tab(self, notebook):
    """Web Automation with Selenium"""
    tab = tk.Frame(notebook, bg="#1e1e2e")
    notebook.add(tab, text="🌐 Web Auto")
    
    header_frame = tk.Frame(tab, bg="#1a1a2e")
    header_frame.pack(fill="x", pady=(10, 0), padx=10)
    
    header = tk.Label(header_frame,
                      text="🌐 Intelligent Web Automation",
                      bg="#1a1a2e",
                      fg="#89dceb",
                      font=("Segoe UI", 14, "bold"))
    header.pack(pady=12)
    
    info = tk.Label(header_frame,
                    text="🤖 AI-Powered Browser Control • Works in Replit Cloud",
                    bg="#1a1a2e",
                    fg="#a6adc8",
                    font=("Segoe UI", 9, "italic"))
    info.pack(pady=(0, 12))
    
    # Command input section
    input_section = tk.Frame(tab, bg="#1e1e2e")
    input_section.pack(fill="x", padx=10, pady=10)
    
    input_label = tk.Label(input_section,
                           text="💬 Natural Language Command:",
                           bg="#1e1e2e",
                           fg="#a6adc8",
                           font=("Segoe UI", 9, "bold"))
    input_label.pack(anchor="w", padx=5, pady=(5, 2))
    
    input_box_frame = tk.Frame(input_section, bg="#1e1e2e")
    input_box_frame.pack(fill="x", padx=5, pady=(0, 5))
    
    self.web_auto_input = tk.Entry(input_box_frame,
                                   bg="#313244",
                                   fg="#ffffff",
                                   font=("Segoe UI", 11),
                                   relief="solid",
                                   bd=2,
                                   insertbackground="#89dceb")
    self.web_auto_input.pack(side="left", fill="x", expand=True, ipady=8)
    self.web_auto_input.bind("<Return>", lambda e: self.execute_web_automation())
    
    execute_btn = tk.Button(input_box_frame,
                            text="🚀 Execute",
                            bg="#89dceb",
                            fg="#0f0f1e",
                            font=("Segoe UI", 10, "bold"),
                            relief="flat",
                            cursor="hand2",
                            command=self.execute_web_automation,
                            padx=20,
                            pady=8)
    execute_btn.pack(side="right", padx=(5, 0))
    self.add_hover_effect(execute_btn, "#89dceb", "#74c7ec")
    
    # Quick Actions section
    quick_frame = tk.Frame(tab, bg="#1a1a2e")
    quick_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    quick_label = tk.Label(quick_frame,
                           text="⚡ Quick Actions",
                           bg="#1a1a2e",
                           fg="#f9e2af",
                           font=("Segoe UI", 11, "bold"))
    quick_label.pack(pady=10)
    
    # Create scrollable area for buttons
    canvas = tk.Canvas(quick_frame, bg="#1a1a2e", highlightthickness=0)
    scrollbar = ttk.Scrollbar(quick_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#1a1a2e")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Quick action buttons
    quick_actions = [
        ("🎯 LeetCode Problem 34", "open leetcode problem 34"),
        ("🎯 LeetCode Problem 1", "open leetcode problem 1"),
        ("📚 LeetCode Problemset", "open https://leetcode.com/problemset/all/"),
        ("🔍 Search GitHub Python", "search github for python automation"),
        ("🌟 GitHub Trending Python", "open https://github.com/trending/python"),
        ("🌟 GitHub Trending", "open https://github.com/trending"),
        ("💡 Search Google ML", "search google for machine learning"),
        ("🔎 Search StackOverflow", "search stackoverflow for python async"),
        ("📺 YouTube Python Tutorial", "search youtube for python tutorial"),
        ("📺 YouTube Coding Channel", "search youtube for coding tutorials"),
        ("🆕 Custom Website", "open https://www.example.com"),
    ]
    
    for text, command in quick_actions:
        btn = tk.Button(scrollable_frame,
                        text=text,
                        bg="#313244",
                        fg="#ffffff",
                        font=("Segoe UI", 9),
                        relief="flat",
                        cursor="hand2",
                        command=lambda c=command: self.quick_web_automation(c),
                        anchor="w",
                        padx=15,
                        pady=8,
                        activebackground="#45475a")
        btn.pack(fill="x", padx=8, pady=2)
        self.add_hover_effect(btn, "#313244", "#45475a")
    
    # Control buttons
    control_frame = tk.Frame(tab, bg="#1e1e2e")
    control_frame.pack(fill="x", padx=10, pady=(0, 10))
    
    init_btn = tk.Button(control_frame,
                         text="▶️ Initialize Browser",
                         bg="#313244",
                         fg="#ffffff",
                         font=("Segoe UI", 9, "bold"),
                         relief="flat",
                         cursor="hand2",
                         command=self.initialize_web_browser,
                         padx=12,
                         pady=6)
    init_btn.pack(side="left", padx=5)
    self.add_hover_effect(init_btn, "#313244", "#45475a")
    
    close_btn = tk.Button(control_frame,
                          text="🔒 Close Browser",
                          bg="#313244",
                          fg="#ffffff",
                          font=("Segoe UI", 9, "bold"),
                          relief="flat",
                          cursor="hand2",
                          command=self.close_web_browser,
                          padx=12,
                          pady=6)
    close_btn.pack(side="left", padx=5)
    self.add_hover_effect(close_btn, "#313244", "#45475a")
    
    screenshot_btn = tk.Button(control_frame,
                               text="📸 Screenshot",
                               bg="#313244",
                               fg="#ffffff",
                               font=("Segoe UI", 9, "bold"),
                               relief="flat",
                               cursor="hand2",
                               command=self.take_web_screenshot,
                               padx=12,
                               pady=6)
    screenshot_btn.pack(side="left", padx=5)
    self.add_hover_effect(screenshot_btn, "#313244", "#45475a")

def execute_web_automation(self):
    """Execute web automation from input"""
    if not self.web_automator:
        self.output("❌ Web automation not available", "error")
        return
    
    command = self.web_auto_input.get().strip()
    if not command:
        self.output("⚠️  Please enter a command", "warning")
        return
    
    self.output(f"\n🤖 EXECUTING WEB AUTOMATION", "info")
    self.output(f"📋 Command: {command}", "info")
    
    def run_automation():
        try:
            result = self.web_automator.execute_task(command, interactive=False)
            
            if result.get('success'):
                self.output(f"\n✅ Task completed successfully!", "success")
                self.output(f"📊 Success rate: {result['successful_steps']}/{result['total_steps']}", "info")
            else:
                self.output(f"\n⚠️  Task completed with issues", "warning")
                
            # Show detailed results
            for i, step_result in enumerate(result.get('results', []), 1):
                if step_result.get('success'):
                    self.output(f"   Step {i}: ✅ {step_result.get('message', 'Done')}", "success")
                else:
                    self.output(f"   Step {i}: ❌ {step_result.get('error', 'Failed')}", "error")
            
            self.web_auto_input.delete(0, tk.END)
            
        except Exception as e:
            self.output(f"❌ Error: {str(e)}", "error")
    
    thread = threading.Thread(target=run_automation, daemon=True)
    thread.start()

def quick_web_automation(self, command):
    """Quick web automation action"""
    if not self.web_automator:
        self.output("❌ Web automation not available", "error")
        return
    
    self.web_auto_input.delete(0, tk.END)
    self.web_auto_input.insert(0, command)
    self.execute_web_automation()

def initialize_web_browser(self):
    """Initialize the web browser"""
    if not self.web_automator:
        self.output("❌ Web automation not available", "error")
        return
    
    self.output("🌐 Initializing browser...", "info")
    
    def init():
        try:
            if self.web_automator.initialize_browser():
                self.output("✅ Browser initialized successfully!", "success")
                self.output(f"📍 Ready for automation commands", "info")
            else:
                self.output("❌ Failed to initialize browser", "error")
        except Exception as e:
            self.output(f"❌ Error: {str(e)}", "error")
    
    thread = threading.Thread(target=init, daemon=True)
    thread.start()

def close_web_browser(self):
    """Close the web browser"""
    if not self.web_automator:
        self.output("❌ Web automation not available", "error")
        return
    
    try:
        self.web_automator.close_browser()
        self.output("🔒 Browser closed", "info")
    except Exception as e:
        self.output(f"❌ Error closing browser: {str(e)}", "error")

def take_web_screenshot(self):
    """Take a screenshot of the current page"""
    if not self.web_automator:
        self.output("❌ Web automation not available", "error")
        return
    
    try:
        filename = f"web_screenshot_{int(time.time())}.png"
        if self.web_automator.take_screenshot(filename):
            self.output(f"📸 Screenshot saved: {filename}", "success")
            self.output(f"📍 URL: {self.web_automator.get_current_url()}", "info")
        else:
            self.output("❌ Screenshot failed - browser not initialized", "error")
    except Exception as e:
        self.output(f"❌ Error: {str(e)}", "error")
