import os
import sys

# Add foundation_data to path
foundation_data_path = os.path.join(os.path.dirname(__file__), 'foundation_data')
print(f"Foundation data path exists: {os.path.exists(foundation_data_path)}")

if os.path.exists(foundation_data_path):
    sys.path.insert(0, foundation_data_path)
    
    # Check panels folder
    panels_path = os.path.join(foundation_data_path, 'panels')
    print(f"Panels path exists: {os.path.exists(panels_path)}")
    
    if os.path.exists(panels_path):
        files = os.listdir(panels_path)
        print(f"Files in panels folder: {files}")
        
        # Try to import the main panel
        try:
            from panels.hierarchy_panel_fixed import show_hierarchy_panel
            print("✅ Successfully imported hierarchy_panel_fixed")
        except Exception as e:
            print(f"❌ Failed to import hierarchy_panel_fixed: {e}")
