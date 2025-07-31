"""
Foundation Data Management Wrapper
This file provides a clean interface between the main app and the foundation data management system
"""

import os
import sys
import streamlit as st
import pandas as pd

print("🔍 Foundation wrapper starting...")

# Add the foundation paths - try multiple locations
current_dir = os.path.dirname(__file__)
foundation_data_path = os.path.join(current_dir, 'foundation_data')
foundation_module_path = os.path.join(current_dir, 'foundation_module')

print(f"🔍 Current dir: {current_dir}")
print(f"🔍 Foundation data path: {foundation_data_path}")
print(f"🔍 Foundation data exists: {os.path.exists(foundation_data_path)}")

# Add paths to sys.path if they don't exist
paths_to_add = [foundation_data_path, foundation_module_path]
for path in paths_to_add:
    if os.path.exists(path) and path not in sys.path:
        sys.path.insert(0, path)
        print(f"✅ Added to sys.path: {path}")

# Check what's actually in the foundation_data directory
if os.path.exists(foundation_data_path):
    try:
        contents = os.listdir(foundation_data_path)
        print(f"🔍 Foundation_data contents: {contents}")
        
        panels_path = os.path.join(foundation_data_path, 'panels')
        if os.path.exists(panels_path):
            panels_contents = os.listdir(panels_path)
            print(f"🔍 Panels folder contents: {panels_contents}")
        else:
            print("❌ Panels folder not found")
    except Exception as e:
        print(f"❌ Error reading foundation_data: {e}")

# Import the foundation data management panels - try multiple import strategies
FOUNDATION_DATA_AVAILABLE = False
VALIDATION_ENHANCED = False
STATISTICS_ENHANCED = False
HEALTH_MONITOR_ENHANCED = False
import_error_messages = []

# Strategy 1: Import from foundation_data directory (NEW SYSTEM - PRIORITY)
print("🔍 Trying Strategy 1: Import from foundation_data directory...")
try:
    # Add foundation_data to path if not already there
    if foundation_data_path not in sys.path:
        sys.path.insert(0, foundation_data_path)
    
    print("🔍 Attempting to import hierarchy panel...")
    from panels.hierarchy_panel_fixed import show_hierarchy_panel
    print("✅ Hierarchy panel imported successfully")
    
    # Import enhanced validation panel with fallback
    print("🔍 Attempting to import validation panels...")
    try:
        from panels.enhanced_validation_panel import show_validation_panel
        VALIDATION_ENHANCED = True
        print("✅ Enhanced validation panel imported")
    except ImportError as ve:
        print(f"⚠️ Enhanced validation failed: {ve}")
        try:
            from panels.validation_panel_fixed import show_validation_panel
            VALIDATION_ENHANCED = False
            print("✅ Basic validation panel imported")
        except ImportError as ve2:
            print(f"⚠️ Basic validation failed: {ve2}")
            def show_validation_panel(state):
                st.error("Validation panel not implemented yet")
            VALIDATION_ENHANCED = False

    # Import admin panel with fallbacks
    print("🔍 Attempting to import admin panel...")
    try:
        from config_manager import show_admin_panel
        print("✅ Admin panel imported from config_manager")
    except ImportError as ae:
        print(f"⚠️ Config_manager import failed: {ae}")
        try:
            from panels.config_manager import show_admin_panel
            print("✅ Admin panel imported from panels.config_manager")
        except ImportError as ae2:
            print(f"⚠️ Panels.config_manager import failed: {ae2}")
            def show_admin_panel():
                st.error("Admin panel not found")

    # Import enhanced statistics panel with fallbacks
    print("🔍 Attempting to import statistics panels...")
    try:
        from panels.statistics_panel_enhanced import show_statistics_panel
        STATISTICS_ENHANCED = True
        print("✅ Enhanced statistics panel imported")
    except ImportError as se:
        print(f"⚠️ Enhanced statistics failed: {se}")
        try:
            from panels.statistics_panel import show_statistics_panel
            STATISTICS_ENHANCED = False
            print("✅ Basic statistics panel imported")
        except ImportError as se2:
            print(f"⚠️ Basic statistics failed: {se2}")
            def show_statistics_panel(state):
                st.error("Statistics panel not implemented yet")
            STATISTICS_ENHANCED = False

    # Import health monitor (dashboard) panel with fallbacks
    print("🔍 Attempting to import health monitor panels...")
    try:
        from panels.dashboard_panel_fixed import show_health_monitor_panel
        HEALTH_MONITOR_ENHANCED = True
        print("✅ Enhanced health monitor panel imported")
    except ImportError as he:
        print(f"⚠️ Enhanced health monitor failed: {he}")
        try:
            from panels.dashboard_panel import show_health_monitor_panel
            HEALTH_MONITOR_ENHANCED = False
            print("✅ Basic health monitor panel imported")
        except ImportError as he2:
            print(f"⚠️ Basic health monitor failed: {he2}")
            def show_health_monitor_panel(state):
                st.error("Health Monitor panel not implemented yet")
            HEALTH_MONITOR_ENHANCED = False
    
    FOUNDATION_DATA_AVAILABLE = True
    print("✅ Foundation panels imported successfully (from foundation_data/)")
    
except ImportError as e:
    error_msg = f"Foundation_data directory import failed: {e}"
    import_error_messages.append(error_msg)
    print(f"❌ {error_msg}")

# Strategy 2: Import from foundation_module directory (EXISTING SYSTEM)
if not FOUNDATION_DATA_AVAILABLE:
    print("🔍 Trying Strategy 2: Import from foundation_module directory...")
    try:
        if foundation_module_path not in sys.path:
            sys.path.insert(0, foundation_module_path)
        
        from foundation_app import render as render_foundation_basic
        
        # Create wrapper functions for the basic system
        def show_hierarchy_panel(state):
            render_foundation_basic()
            
        def show_validation_panel(state):
            st.info("Basic foundation validation not available")
            
        def show_statistics_panel(state):
            st.info("Basic foundation statistics not available")
            
        def show_health_monitor_panel(state):
            st.info("Basic foundation health monitor not available")
            
        def show_admin_panel():
            st.info("Basic foundation admin not available")
        
        VALIDATION_ENHANCED = False
        STATISTICS_ENHANCED = False
        HEALTH_MONITOR_ENHANCED = False
        FOUNDATION_DATA_AVAILABLE = True
        print("✅ Foundation basic system imported (from foundation_module/)")
        
    except ImportError as e:
        error_msg = f"Foundation_module directory import failed: {e}"
        import_error_messages.append(error_msg)
        print(f"❌ {error_msg}")

if not FOUNDATION_DATA_AVAILABLE:
    print(f"❌ All foundation import strategies failed:")
    for msg in import_error_messages:
        print(f"  - {msg}")
else:
    print(f"✅ Foundation system ready! Enhanced features: Validation={VALIDATION_ENHANCED}, Statistics={STATISTICS_ENHANCED}, Health={HEALTH_MONITOR_ENHANCED}")

def get_default_level_names():
    """Get improved default level names"""
    return {
        1: "Level1_LegalEntity",
        2: "Level2_BusinessUnit", 
        3: "Level3_Division",
        4: "Level4_SubDivision",
        5: "Level5_Department",
        6: "Level6_SubDepartment",
        7: "Level7_Team",
        8: "Level8_Unit",
        9: "Level9_Unit", 
        10: "Level10_Unit",
        11: "Level11_Unit",
        12: "Level12_Unit",
        13: "Level13_Unit",
        14: "Level14_Unit",
        15: "Level15_Unit",
        16: "Level16_Unit",
        17: "Level17_Unit",
        18: "Level18_Unit",
        19: "Level19_Unit",
        20: "Level20_Unit"
    }

def render_foundation_data_management():
    """Render the complete foundation data management system"""
    if not FOUNDATION_DATA_AVAILABLE:
        st.error("❌ Foundation Data Management system not available.")
        
        # Show debug information
        st.markdown("### 🔍 Debug Information")
        st.write(f"**Foundation data path exists:** {os.path.exists(foundation_data_path)}")
        st.write(f"**Foundation module path exists:** {os.path.exists(foundation_module_path)}")
        
        with st.expander("🔍 Detailed Troubleshooting", expanded=True):
            st.markdown("""
            **Common issues:**
            1. Make sure the foundation panel files exist in the `foundation_data/panels/` directory
            2. Check that required panel files exist and have the correct names
            3. Verify there are no syntax errors in the panel files
            
            **Expected files in `foundation_data/panels/`:**
            - `hierarchy_panel_fixed.py` ✅ (required)
            - `enhanced_validation_panel.py` (optional, falls back to basic)
            - `validation_panel_fixed.py` (fallback for validation)
            - `statistics_panel_enhanced.py` (optional, falls back to basic)
            - `statistics_panel.py` (fallback for statistics)
            - `dashboard_panel_fixed.py` (optional, falls back to basic)
            - `dashboard_panel.py` (fallback for health monitor)
            """)
            
            # Show what we actually found
            if os.path.exists(foundation_data_path):
                st.write("**Foundation_data directory contents:**")
                try:
                    contents = os.listdir(foundation_data_path)
                    st.code(str(contents))
                    
                    panels_path = os.path.join(foundation_data_path, 'panels')
                    if os.path.exists(panels_path):
                        st.write("**Panels directory contents:**")
                        panels_contents = os.listdir(panels_path)
                        st.code(str(panels_contents))
                        
                        # Check for specific required files
                        required_files = [
                            'hierarchy_panel_fixed.py',
                            'validation_panel_fixed.py', 
                            'enhanced_validation_panel.py',
                            'statistics_panel.py',
                            'statistics_panel_enhanced.py',
                            'dashboard_panel.py',
                            'dashboard_panel_fixed.py'
                        ]
                        
                        st.write("**Required file check:**")
                        for file in required_files:
                            file_path = os.path.join(panels_path, file)
                            if os.path.exists(file_path):
                                st.success(f"✅ {file}")
                            else:
                                st.error(f"❌ {file}")
                    else:
                        st.error("❌ Panels directory not found!")
                except Exception as e:
                    st.error(f"Error reading directory: {e}")
            
            # Show detailed error information
            st.markdown("**Import Error Details:**")
            for i, msg in enumerate(import_error_messages, 1):
                st.code(f"{i}. {msg}")
                
        return
    
    # Initialize foundation session state if not exists
    if 'foundation_state' not in st.session_state:
        st.session_state.foundation_state = {
            'hrp1000': None,
            'hrp1001': None,
            'hierarchy': None,
            'level_names': get_default_level_names(),
            'transformations': [],
            'validation_results': None,
            'statistics': None,
            'pending_transforms': [],
            'admin_mode': False,
            'generated_output_files': {},
            'output_generation_metadata': {}
        }
    
    foundation_state = st.session_state.foundation_state
    
    # Create a container for the foundation management system
    with st.container():
        st.markdown("### 🏢 Foundation Data Management System")
        st.markdown("*Advanced organizational hierarchy processing, validation, and analytics for SAP HCM → SuccessFactors migration*")
        
        # Show enhancement status
        col1, col2, col3 = st.columns(3)
        with col1:
            if STATISTICS_ENHANCED:
                st.success("🚀 Enhanced Statistics")
                st.caption("End-to-end pipeline analysis")
            else:
                st.info("📊 Basic Statistics")
                
        with col2:
            if VALIDATION_ENHANCED:
                st.success("🚀 Enhanced Validation")
                st.caption("Complete pipeline validation")
            else:
                st.info("✅ Basic Validation")
                
        with col3:
            if HEALTH_MONITOR_ENHANCED:
                st.success("🚀 Enhanced Health Monitor")
                st.caption("System health monitoring")
            else:
                st.info("🏥 Basic Health Monitor")
        
        # Navigation for foundation panels
        panel_choice = st.selectbox(
            "**Choose Panel:**",
            [
                "🏢 Hierarchy Processing",
                "✅ Data Validation", 
                "📊 Statistics & Analytics",
                "🏥 Health Monitor",
                "⚙️ Admin Configuration"
            ],
            key="foundation_panel_selection",
            help="Select the foundation panel you want to work with"
        )
        
        # Show quick status in columns
        st.markdown("#### 📋 Quick Status")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            hrp1000_loaded = foundation_state.get('source_hrp1000') is not None or foundation_state.get('hrp1000') is not None
            hrp1001_loaded = foundation_state.get('source_hrp1001') is not None or foundation_state.get('hrp1001') is not None
            files_loaded = sum([hrp1000_loaded, hrp1001_loaded])
            st.metric("📂 HRP Files", f"{files_loaded}/2", help="HRP1000 & HRP1001 files loaded for foundation processing")
        
        with col2:
            hierarchy_processed = foundation_state.get('hierarchy_structure') is not None or foundation_state.get('hierarchy') is not None
            st.metric("🏗️ Hierarchy", "✅ Processed" if hierarchy_processed else "❌ Pending", help="Organizational hierarchy processing status")
        
        with col3:
            output_generated = foundation_state.get('generated_output_files') and len(foundation_state.get('generated_output_files', {})) > 0
            st.metric("📤 Output", "✅ Generated" if output_generated else "❌ Pending", help="Foundation output file generation status")
        
        with col4:
            if hierarchy_processed:
                max_level = 0
                hierarchy_data = foundation_state.get('hierarchy_structure') or foundation_state.get('hierarchy')
                if hierarchy_data:
                    if isinstance(hierarchy_data, dict):
                        max_level = max([info.get('level', 1) for info in hierarchy_data.values()]) if hierarchy_data else 0
                    else:
                        max_level = 1  # Basic processing
                st.metric("🏢 Levels", max_level if max_level > 0 else 'N/A', help="Number of organizational levels processed")
            else:
                st.metric("🏢 Levels", 'N/A', help="Process hierarchy first")
        
        st.markdown("---")
        
        # Show helpful tips
        if not hrp1000_loaded or not hrp1001_loaded:
            st.info("💡 **Getting Started:** Upload HRP1000 (Objects) and HRP1001 (Relationships) files in the Hierarchy Processing panel to begin organizational structure analysis.")
        
        # Show selected panel
        try:
            if panel_choice == "🏢 Hierarchy Processing":
                with st.expander("ℹ️ About Hierarchy Processing", expanded=False):
                    st.markdown("""
                    **Hierarchy Processing Panel** handles:
                    - Upload and processing of HRP1000 (Objects) and HRP1001 (Relationships) files
                    - Organizational structure analysis and hierarchy building
                    - Level naming and classification (Legal Entity → Business Unit → Division → Department → Team)
                    - Generation of SuccessFactors-ready organizational output files
                    - Visual hierarchy exploration and validation
                    """)
                show_hierarchy_panel(foundation_state)
                
            elif panel_choice == "✅ Data Validation":
                with st.expander("ℹ️ About Data Validation", expanded=False):
                    st.markdown("""
                    **Data Validation Panel** performs:
                    - Comprehensive organizational data quality checks
                    - Hierarchy consistency validation and relationship verification
                    - Object type validation and business rule verification
                    - Missing relationship detection and circular reference checks
                    - Error reporting and remediation guidance for organizational data
                    """)
                    if VALIDATION_ENHANCED:
                        st.success("🚀 Enhanced validation with complete pipeline analysis available")
                    else:
                        st.info("📋 Basic validation mode")
                        
                with st.spinner("Running foundation validation checks..."):
                    show_validation_panel(foundation_state)
                    
            elif panel_choice == "📊 Statistics & Analytics":
                with st.expander("ℹ️ About Statistics & Analytics", expanded=False):
                    st.markdown("""
                    **Statistics & Analytics Panel** provides:
                    - Comprehensive organizational data analysis and insights
                    - Hierarchy distribution and structure analysis
                    - Object type statistics and relationship patterns
                    - Data quality assessment for organizational records
                    - End-to-end pipeline analysis from source to target files
                    """)
                    if STATISTICS_ENHANCED:
                        st.success("🚀 Enhanced statistics with complete pipeline analysis available")
                    else:
                        st.info("📊 Basic statistics mode")
                
                # Add warning for large datasets
                hrp1000_data = foundation_state.get('source_hrp1000') or foundation_state.get('hrp1000')
                if hrp1000_data is not None and len(hrp1000_data) > 10000:
                    st.warning("⚠️ Large organizational dataset detected. Statistics panel may take a moment to load...")
                
                with st.spinner("Loading foundation statistics..."):
                    show_statistics_panel(foundation_state)
                    
            elif panel_choice == "🏥 Health Monitor":
                with st.expander("ℹ️ About Health Monitor", expanded=False):
                    st.markdown("""
                    **Health Monitor Panel** displays:
                    - Real-time foundation migration progress and system health
                    - Key organizational performance indicators
                    - Visual organizational data summaries and hierarchy health
                    - Migration status overview for foundation components
                    - System performance monitoring and optimization suggestions
                    """)
                    if HEALTH_MONITOR_ENHANCED:
                        st.success("🚀 Enhanced health monitoring with system diagnostics available")
                    else:
                        st.info("🏥 Basic health monitor mode")
                        
                show_health_monitor_panel(foundation_state)
                
            elif panel_choice == "⚙️ Admin Configuration":
                with st.expander("ℹ️ About Admin Configuration", expanded=False):
                    st.markdown("""
                    **Admin Configuration Panel** manages:
                    - Foundation system settings and preferences
                    - Organizational hierarchy mapping configurations
                    - Object type and relationship business rules setup
                    - Level naming conventions and advanced processing parameters
                    - Template configurations and data transformation rules
                    """)
                
                # Admin mode check
                admin_enabled = st.checkbox("Enable Admin Mode", help="Enable configuration options")
                
                if admin_enabled:
                    # Simple admin mode for foundation
                    foundation_state['admin_mode'] = True
                    st.success("Admin mode activated for Foundation")
                    show_admin_panel()
                else:
                    foundation_state['admin_mode'] = False
                    st.info("Admin mode disabled. Enable to access configuration options.")

        except Exception as e:
            st.error(f"❌ **Panel Error:** {str(e)}")
            st.info("**What to do:** Try refreshing the page or switching to a different panel")
            
            # Show error details in expander
            with st.expander("🔍 Technical Details", expanded=False):
                st.code(str(e))
                if st.button("🔄 Reset Foundation Session", key="reset_foundation_session"):
                    if 'foundation_state' in st.session_state:
                        del st.session_state['foundation_state']
                    st.rerun()
                    
        # Footer with helpful information
        st.markdown("---")
        st.markdown("**💡 Tips for Foundation Success:**")
        st.markdown("""
        1. **Start with Hierarchy:** Upload HRP1000 & HRP1001 files and process organizational structure first
        2. **Validate Early:** Run validation checks to catch organizational issues before final migration
        3. **Monitor Health:** Use the health monitor to track your foundation migration status
        4. **Analyze Structure:** Use statistics panel to understand organizational patterns and hierarchy depth
        5. **Configure Levels:** Use admin panel to customize level naming conventions for your organization
        """)

def get_foundation_system_status():
    """Get current status of the foundation data management system"""
    if not FOUNDATION_DATA_AVAILABLE:
        return {"available": False, "error": "Modules not loaded"}
    
    if 'foundation_state' not in st.session_state:
        return {"available": True, "initialized": False}
    
    foundation_state = st.session_state.foundation_state
    hrp1000_loaded = foundation_state.get('source_hrp1000') is not None or foundation_state.get('hrp1000') is not None
    hrp1001_loaded = foundation_state.get('source_hrp1001') is not None or foundation_state.get('hrp1001') is not None
    hierarchy_processed = foundation_state.get('hierarchy_structure') is not None or foundation_state.get('hierarchy') is not None
    
    return {
        "available": True,
        "initialized": True,
        "hrp_files_loaded": sum([hrp1000_loaded, hrp1001_loaded]),
        "ready_to_process": hrp1000_loaded and hrp1001_loaded,
        "hierarchy_processed": hierarchy_processed,
        "output_generated": foundation_state.get('generated_output_files') and len(foundation_state.get('generated_output_files', {})) > 0,
        "enhanced_features": {
            "statistics": STATISTICS_ENHANCED,
            "validation": VALIDATION_ENHANCED, 
            "health_monitor": HEALTH_MONITOR_ENHANCED
        }
    }
