import os
import sys

# Test if foundation_data folder exists
foundation_data_path = os.path.join(os.path.dirname(__file__), 'foundation_data')
print(f"Foundation data path: {foundation_data_path}")
print(f"Foundation data exists: {os.path.exists(foundation_data_path)}")

if os.path.exists(foundation_data_path):
    sys.path.insert(0, foundation_data_path)
    
    # Test panel imports
    try:
        from panels.hierarchy_panel_fixed import show_hierarchy_panel
        print("✅ Hierarchy panel imported successfully")
    except Exception as e:
        print(f"❌ Hierarchy panel failed: {e}")

    # List what's actually in the panels folder
    panels_path = os.path.join(foundation_data_path, 'panels')
    if os.path.exists(panels_path):
        files = os.listdir(panels_path)
        print(f"Panels folder contents: {files}")
    else:
        print("❌ Panels folder doesn't exist")
