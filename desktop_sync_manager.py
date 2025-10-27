"""
Desktop Sync Manager - Auto-download batch file and sync desktop files
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime


class DesktopSyncManager:
    """Manages desktop file synchronization and batch file distribution"""
    
    def __init__(self):
        self.replit_desktop = Path.home() / "Desktop"
        self.sync_config_file = "desktop_sync_config.json"
        self.batch_file = "desktop_file_controller.bat"
        self.downloads_ready_file = "downloads_ready.txt"
        
    def prepare_batch_file_download(self):
        """Prepare batch file for download with instructions"""
        try:
            if not os.path.exists(self.batch_file):
                return {
                    "success": False,
                    "message": "Batch file not found in project"
                }
            
            # Create download instructions
            instructions = f"""
╔══════════════════════════════════════════════════════════╗
║        DESKTOP FILE CONTROLLER - READY TO DOWNLOAD       ║
╚══════════════════════════════════════════════════════════╝

✅ Batch file ready: {self.batch_file}
📦 File size: {os.path.getsize(self.batch_file)} bytes

📥 HOW TO DOWNLOAD:

Option 1 - Direct Download (Easiest):
  1. Look for '{self.batch_file}' in the Replit file browser
  2. Right-click → Download
  3. Save to your Windows PC
  4. Double-click to run!

Option 2 - Download All Files:
  1. Click ⋮ (three dots) in Replit menu
  2. Select "Download as ZIP"
  3. Extract on your PC
  4. Double-click {self.batch_file}

🎯 QUICK START AFTER DOWNLOAD:
  1. Double-click {self.batch_file} on Windows
  2. Choose option 6 to list your desktop
  3. Use options 1-13 to manage files

💡 The batch file will manage YOUR real Windows desktop!

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
            
            with open(self.downloads_ready_file, 'w') as f:
                f.write(instructions)
            
            return {
                "success": True,
                "message": "Batch file ready for download",
                "instructions_file": self.downloads_ready_file,
                "batch_file": self.batch_file
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error preparing batch file: {str(e)}"
            }
    
    def create_desktop_structure_json(self):
        """Create JSON representation of desktop structure"""
        try:
            structure = {
                "generated": datetime.now().isoformat(),
                "desktop_path": str(self.replit_desktop),
                "folders": [],
                "files": []
            }
            
            if not self.replit_desktop.exists():
                self.replit_desktop.mkdir(parents=True, exist_ok=True)
            
            for item in self.replit_desktop.iterdir():
                item_info = {
                    "name": item.name,
                    "path": str(item),
                    "size": item.stat().st_size if item.is_file() else 0
                }
                
                if item.is_dir():
                    # Count items in folder
                    try:
                        item_info["item_count"] = len(list(item.iterdir()))
                    except:
                        item_info["item_count"] = 0
                    structure["folders"].append(item_info)
                else:
                    structure["files"].append(item_info)
            
            # Save to file
            json_file = "desktop_structure.json"
            with open(json_file, 'w') as f:
                json.dump(structure, f, indent=2)
            
            return {
                "success": True,
                "structure": structure,
                "json_file": json_file,
                "total_folders": len(structure["folders"]),
                "total_files": len(structure["files"])
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error creating structure: {str(e)}"
            }
    
    def setup_sample_desktop(self):
        """Create sample desktop structure for testing"""
        try:
            # Create desktop if it doesn't exist
            self.replit_desktop.mkdir(parents=True, exist_ok=True)
            
            # Create sample folders
            sample_folders = [
                "coding",
                "projects", 
                "documents",
                "downloads",
                "work",
                "personal"
            ]
            
            created = []
            for folder in sample_folders:
                folder_path = self.replit_desktop / folder
                if not folder_path.exists():
                    folder_path.mkdir()
                    created.append(folder)
                    
                    # Add sample files
                    if folder == "coding":
                        (folder_path / "main.py").write_text("# Python code here")
                        (folder_path / "app.js").write_text("// JavaScript code here")
                    elif folder == "documents":
                        (folder_path / "notes.txt").write_text("Sample notes")
                        (folder_path / "report.txt").write_text("Sample report")
            
            return {
                "success": True,
                "created_folders": created,
                "total_folders": len(sample_folders),
                "desktop_path": str(self.replit_desktop)
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error setting up desktop: {str(e)}"
            }
    
    def auto_startup_sequence(self):
        """Run automatic startup sequence"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "steps": []
        }
        
        # Step 1: Setup sample desktop (if empty)
        setup_result = self.setup_sample_desktop()
        results["steps"].append({
            "step": "Setup Desktop Structure",
            "status": "success" if setup_result["success"] else "failed",
            "details": setup_result
        })
        
        # Step 2: Prepare batch file download
        batch_result = self.prepare_batch_file_download()
        results["steps"].append({
            "step": "Prepare Batch File",
            "status": "success" if batch_result["success"] else "failed",
            "details": batch_result
        })
        
        # Step 3: Create desktop structure JSON
        structure_result = self.create_desktop_structure_json()
        results["steps"].append({
            "step": "Create Desktop Structure",
            "status": "success" if structure_result["success"] else "failed",
            "details": structure_result
        })
        
        # Overall success
        results["success"] = all(
            step["status"] == "success" for step in results["steps"]
        )
        
        return results
    
    def get_download_instructions(self):
        """Get formatted download instructions"""
        if os.path.exists(self.downloads_ready_file):
            with open(self.downloads_ready_file, 'r') as f:
                return f.read()
        return "Download instructions not generated yet. Run auto_startup_sequence() first."


def auto_initialize_on_gui_start():
    """Called automatically when GUI starts"""
    print("\n" + "="*60)
    print("🚀 DESKTOP SYNC MANAGER - AUTO STARTUP")
    print("="*60)
    
    manager = DesktopSyncManager()
    results = manager.auto_startup_sequence()
    
    print("\n📊 Startup Sequence Results:")
    print("-"*60)
    
    for step in results["steps"]:
        status_icon = "✅" if step["status"] == "success" else "❌"
        print(f"{status_icon} {step['step']}: {step['status'].upper()}")
        
        if step["status"] == "success" and "details" in step:
            details = step["details"]
            if "created_folders" in details and details["created_folders"]:
                print(f"   Created: {', '.join(details['created_folders'])}")
            if "total_folders" in details:
                print(f"   Total folders: {details['total_folders']}")
            if "batch_file" in details:
                print(f"   Batch file: {details['batch_file']}")
    
    print("\n" + "="*60)
    
    if results["success"]:
        print("✅ ALL SYSTEMS READY!")
        print("\n📥 DOWNLOAD YOUR BATCH FILE:")
        print(f"   Right-click '{manager.batch_file}' → Download")
        print("\n📂 Desktop synchronized with test folders")
        print(f"   View: {manager.replit_desktop}")
    else:
        print("⚠️  Some steps had issues. Check details above.")
    
    print("="*60 + "\n")
    
    return results


if __name__ == "__main__":
    # Run standalone test
    auto_initialize_on_gui_start()
