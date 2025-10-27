"""
Desktop Sync Manager - Auto-download batch file and sync desktop files
"""

import os
import sys
import shutil
import json
from pathlib import Path
from datetime import datetime


class DesktopSyncManager:
    """Manages desktop file synchronization and batch file distribution"""
    
    def __init__(self):
        # Get script directory for finding batch file
        self.script_dir = Path(__file__).parent.absolute()
        
        # Use actual Windows Desktop
        self.desktop = Path.home() / "Desktop"
        
        # Config files
        self.sync_config_file = "desktop_sync_config.json"
        self.batch_file_name = "desktop_file_controller.bat"
        self.batch_file = self.script_dir / self.batch_file_name
        self.downloads_ready_file = "downloads_ready.txt"
        
        # Detect OS
        self.is_windows = sys.platform.startswith('win')
        
    def prepare_batch_file_download(self):
        """Prepare batch file for local Windows use"""
        try:
            # Check if batch file exists in script directory
            if not self.batch_file.exists():
                # Provide helpful message for Windows users
                current_dir = os.getcwd()
                script_dir = str(self.script_dir)
                
                return {
                    "success": False,
                    "message": f"Batch file '{self.batch_file_name}' not found!\n" + 
                              f"   Current directory: {current_dir}\n" +
                              f"   Script directory: {script_dir}\n" +
                              f"   Looking for: {self.batch_file}\n\n" +
                              f"   💡 Please download '{self.batch_file_name}' from Replit\n" +
                              f"      and place it in: {script_dir}"
                }
            
            # Create ready-to-use instructions for local Windows
            instructions = f"""
╔══════════════════════════════════════════════════════════╗
║        DESKTOP FILE CONTROLLER - READY TO USE            ║
╚══════════════════════════════════════════════════════════╝

✅ Batch file found: {self.batch_file.name}
📂 Location: {self.batch_file}
📦 File size: {self.batch_file.stat().st_size} bytes
💻 System: Windows {'✓' if self.is_windows else '(Running on non-Windows OS)'}

🎯 QUICK START:
  1. Double-click '{self.batch_file.name}' to run
  2. Or run from command prompt:
     cd "{self.script_dir}"
     {self.batch_file.name}

📂 Managing your Desktop:
  - Desktop path: {self.desktop}
  - Use the batch file menu to organize files
  - Options 1-13 available for file management

💡 The batch file will manage YOUR real Windows desktop!

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
            
            with open(self.downloads_ready_file, 'w', encoding='utf-8') as f:
                f.write(instructions)
            
            return {
                "success": True,
                "message": "Batch file ready to use on Windows",
                "instructions_file": self.downloads_ready_file,
                "batch_file": str(self.batch_file),
                "file_size": self.batch_file.stat().st_size
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
                "desktop_path": str(self.desktop),
                "folders": [],
                "files": []
            }
            
            if not self.desktop.exists():
                self.desktop.mkdir(parents=True, exist_ok=True)
            
            for item in self.desktop.iterdir():
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
            self.desktop.mkdir(parents=True, exist_ok=True)
            
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
                folder_path = self.desktop / folder
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
                "desktop_path": str(self.desktop)
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
        
        if "details" in step:
            details = step["details"]
            if step["status"] == "success":
                if "created_folders" in details and details["created_folders"]:
                    print(f"   Created: {', '.join(details['created_folders'])}")
                if "total_folders" in details:
                    print(f"   Total folders: {details['total_folders']}")
                if "batch_file" in details:
                    print(f"   Batch file: {details['batch_file']}")
            else:
                if "message" in details:
                    for line in details["message"].split('\n'):
                        if line.strip():
                            print(f"   {line}")
    
    print("\n" + "="*60)
    
    if results["success"]:
        print("✅ ALL SYSTEMS READY!")
        if manager.is_windows:
            print(f"\n🚀 READY TO USE: Double-click '{manager.batch_file_name}'")
            print(f"   Location: {manager.batch_file}")
        else:
            print("\n📥 DOWNLOAD YOUR BATCH FILE:")
            print(f"   Right-click '{manager.batch_file_name}' → Download to Windows PC")
        print("\n📂 Desktop synchronized with test folders")
        print(f"   View: {manager.desktop}")
    else:
        print("⚠️  Some steps had issues. Check details above.")
    
    print("="*60 + "\n")
    
    return results


if __name__ == "__main__":
    # Run standalone test
    auto_initialize_on_gui_start()
