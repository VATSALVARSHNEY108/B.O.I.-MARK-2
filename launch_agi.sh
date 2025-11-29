#!/bin/bash
# B.O.I AGI Desktop Assistant Launcher

echo "🤖 B.O.I - AGI Desktop Assistant"
echo "════════════════════════════════════════"
echo ""
echo "Choose mode:"
echo "1) AGI Enhanced (RECOMMENDED - With reasoning engine)"
echo "2) Standard Modern GUI (Basic mode)"
echo "3) Classic CLI"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo "🧠 Launching AGI Enhanced Mode..."
        python modules/core/gui_app_modern_agi.py
        ;;
    2)
        echo "💬 Launching Modern GUI..."
        python modules/core/gui_app_modern.py
        ;;
    3)
        echo "⚙️ Launching CLI..."
        python modules/core/gui_app.py
        ;;
    *)
        echo "Invalid choice"
        ;;
esac
