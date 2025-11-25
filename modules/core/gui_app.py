()
            workflow = workflows[selection[0]]
            command = f"run workflow: {workflow['name']}"
            self.workflow_log(f"Executing workflow: {workflow['name']}", "INFO")
            self.command_input.delete(0, tk.END)
            self.command_input.insert(0, command)
            self.execute_command()

        refresh_btn = tk.Button(saved_frame,
                                text="🔄 Refresh List",
                                bg="#3d4466",
                                fg="#e0e0e0",
                                font=("Segoe UI", 9),
                                relief="flat",
                                cursor="hand2",
                                command=refresh_saved_list,
                                pady=6)
        refresh_btn.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=(0, 10))

        run_btn = tk.Button(saved_frame,
                            text="▶️ Run Selected",
                            bg="#00ff88",
                            fg="#0f0f1e",
                            font=("Segoe UI", 9, "bold"),
                            relief="flat",
                            cursor="hand2",
                            command=run_saved_workflow,
                            pady=6)
        run_btn.pack(side="right", fill="x", expand=True, padx=(5, 10), pady=(0, 10))

        log_frame = tk.Frame(builder_window, bg="#252941")
        log_frame.pack(fill="x", padx=20, pady=(0, 15))

        log_label = tk.Label(log_frame,
                             text="📊 Activity Log",
                             bg="#252941",
                             fg="#f9e2af",
                             font=("Segoe UI", 9, "bold"))
        log_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.workflow_output_text = tk.Text(log_frame,
                                            bg="#16182a",
                                            fg="#e0e0e0",
                                            font=("Consolas", 9),
                                            height=6,
                                            state='disabled',
                                            relief="flat",
                                            padx=10,
                                            pady=10)
        self.workflow_output_text.pack(fill="x", padx=10, pady=(0, 10))

        self.workflow_output_text.tag_config("timestamp", foreground="#6c7086")
        self.workflow_output_text.tag_config("info", foreground="#89b4fa")
        self.workflow_output_text.tag_config("success", foreground="#a6e3a1")
        self.workflow_output_text.tag_config("error", foreground="#f38ba8")
        self.workflow_output_text.tag_config("warning", foreground="#f9e2af")

        refresh_saved_list()
        self.workflow_log("Workflow Builder ready!", "SUCCESS")
    
    # Phone Link & Contact Management Methods
    
    def make_phone_call(self):
        """Make a phone call using Phone Link"""
        name = self.phone_name_input.get().strip()
        number = self.phone_number_input.get().strip()
        
        if not name and not number:
            messagebox.showwarning("Input Required", "Please enter a contact name or phone number")
            return
        
        try:
            if name:
                # Call by name
                result = self.phone_dialer.call_contact(name)
            else:
                # Call by number
                result = self.phone_dialer.dial_with_phone_link(number)
            
            # Show result
            if result['success']:
                message = result['message']
                self.phone_history_text.insert("1.0", f"✅ {message}\n")
                self.phone_name_input.delete(0, tk.END)
                self.phone_number_input.delete(0, tk.END)
                messagebox.showinfo("Call Initiated", message)
            else:
                message = result['message']
                self.phone_history_text.insert("1.0", f"❌ {message}\n")
                messagebox.showerror("Call Failed", message)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to make call: {str(e)}")
    
    def refresh_contacts(self):
        """Refresh the contacts list"""
        self.contacts_listbox.delete(0, tk.END)
        
        try:
            contacts = self.contact_manager.list_contacts()
            for contact in sorted(contacts, key=lambda x: x['name']):
                display = f"{contact['name']}: {contact.get('phone', 'No phone')}"
                self.contacts_listbox.insert(tk.END, display)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load contacts: {str(e)}")
    
    def search_contacts(self):
        """Search and filter contacts"""
        query = self.contact_search_input.get().strip()
        self.contacts_listbox.delete(0, tk.END)
        
        try:
            if query:
                contacts = self.contact_manager.search_contacts(query)
            else:
                contacts = self.contact_manager.list_contacts()
            
            for contact in sorted(contacts, key=lambda x: x['name']):
                display = f"{contact['name']}: {contact.get('phone', 'No phone')}"
                self.contacts_listbox.insert(tk.END, display)
        except Exception as e:
            pass
    
    def call_selected_contact(self, event):
        """Call the selected contact (double-click handler)"""
        selection = self.contacts_listbox.curselection()
        if not selection:
            return
        
        selected_text = self.contacts_listbox.get(selection[0])
        contact_name = selected_text.split(':')[0].strip()
        
        try:
            result = self.phone_dialer.call_contact(contact_name)
            
            if result['success']:
                message = result['message']
                self.phone_history_text.insert("1.0", f"✅ {message}\n")
                messagebox.showinfo("Call Initiated", message)
            else:
                message = result['message']
                self.phone_history_text.insert("1.0", f"❌ {message}\n")
                messagebox.showerror("Call Failed", message)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to call contact: {str(e)}")
    
    def add_contact(self):
        """Add a new contact"""
        from tkinter import simpledialog
        
        name = simpledialog.askstring("Add Contact", "Enter contact name:")
        if not name:
            return
        
        phone = simpledialog.askstring("Add Contact", "Enter phone number\n(with country code, e.g., +1234567890):")
        if not phone:
            return
        
        email = simpledialog.askstring("Add Contact", "Enter email (optional):", initialvalue="")
        
        try:
            if self.contact_manager.add_contact(name, phone, email or None):
                messagebox.showinfo("Success", f"Contact '{name}' added successfully!")
                self.refresh_contacts()
            else:
                messagebox.showerror("Error", "Failed to add contact")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add contact: {str(e)}")
    
    def edit_contact(self):
        """Edit the selected contact"""
        from tkinter import simpledialog
        
        selection = self.contacts_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a contact to edit")
            return
        
        selected_text = self.contacts_listbox.get(selection[0])
        contact_name = selected_text.split(':')[0].strip()
        
        contact = self.contact_manager.get_contact(contact_name)
        if not contact:
            messagebox.showerror("Error", "Contact not found")
            return
        
        phone = simpledialog.askstring("Edit Contact",
                                       f"Enter new phone number for '{contact['name']}':",
                                       initialvalue=contact.get('phone', ''))
        if phone is None:
            return
        
        email = simpledialog.askstring("Edit Contact",
                                       f"Enter new email for '{contact['name']}':",
                                       initialvalue=contact.get('email', ''))
        
        try:
            if self.contact_manager.update_contact(contact_name, phone=phone or None, email=email or None):
                messagebox.showinfo("Success", f"Contact '{contact['name']}' updated!")
                self.refresh_contacts()
            else:
                messagebox.showerror("Error", "Failed to update contact")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update contact: {str(e)}")
    
    def delete_contact(self):
        """Delete the selected contact"""
        selection = self.contacts_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a contact to delete")
            return
        
        selected_text = self.contacts_listbox.get(selection[0])
        contact_name = selected_text.split(':')[0].strip()
        
        if not messagebox.askyesno("Confirm Delete", f"Delete contact '{contact_name}'?"):
            return
        
        try:
            if self.contact_manager.delete_contact(contact_name):
                messagebox.showinfo("Success", f"Contact '{contact_name}' deleted!")
                self.refresh_contacts()
            else:
                messagebox.showerror("Error", "Failed to delete contact")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete contact: {str(e)}")

    def run(self):
        """Start the GUI"""
        self.root.mainloop()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = ModernBOIGUI(root)
    app.run()


if __name__ == "__main__":
    main()
