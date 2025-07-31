"""
Foundation Data Management Wrapper - Minimal Working Version
"""

import os
import sys
import streamlit as st

# Add foundation_data to path
current_dir = os.path.dirname(__file__)
foundation_data_path = os.path.join(current_dir, 'foundation_data')

if os.path.exists(foundation_data_path):
    sys.path.insert(0, foundation_data_path)

# Try to import foundation panels - with maximum error tolerance
try:
    # Try to import main panel - this is the most important one
    from panels.hierarchy_panel_fixed import show_hierarchy_panel
    FOUNDATION_AVAILABLE = True
    print("✅ Foundation hierarchy panel imported successfully")
    
    # Try other panels with individual error handling
    try:
        from panels.enhanced_validation_panel import show_validation_panel
        VALIDATION_ENHANCED = True
    except:
        try:
            from panels.validation_panel_fixed import show_validation_panel
            VALIDATION_ENHANCED = False
        except:
            def show_validation_panel(state):
                st.info("Validation panel not available")
            VALIDATION_ENHANCED = False
    
    try:
        from panels.statistics_panel_enhanced import show_statistics_panel
        STATISTICS_ENHANCED = True
    except:
        try:
            from panels.statistics_panel import show_statistics_panel
            STATISTICS_ENHANCED = False
        except:
            def show_statistics_panel(state):
                st.info("Statistics panel not available")
            STATISTICS_ENHANCED = False
    
    try:
        from panels.dashboard_panel_fixed import show_health_monitor_panel
        HEALTH_MONITOR_ENHANCED = True
    except:
        try:
            from panels.dashboard_panel import show_health_monitor_panel
            HEALTH_MONITOR_ENHANCED = False
        except:
            def show_health_monitor_panel(state):
                st.info("Health monitor panel not available")
            HEALTH_MONITOR_ENHANCED = False
    
    try:
        from config_manager import show_admin_panel
    except:
        def show_admin_panel():
            st.info("Admin panel not available")
    
except Exception as e:
    print(f"❌ Foundation panels import failed: {e}")
    FOUNDATION_AVAILABLE = False
    VALIDATION_ENHANCED = False
    STATISTICS_ENHANCED = False
    HEALTH_MONITOR_ENHANCED = False
    
    # Create dummy functions
    def show_hierarchy_panel(state):
        st.error("Foundation panels not available")
    def show_validation_panel(state):
        st.error("Validation panel not available")
    def show_statistics_panel(state):
        st.error("Statistics panel not available")
    def show_health_monitor_panel(state):
        st.error("Health monitor panel not available")
    def show_admin_panel():
        st.error("Admin panel not available")

def render_foundation_data_management():
    """Render the foundation data management system"""
    
    if not FOUNDATION_AVAILABLE:
        st.error("❌ Foundation Data Management system not available.")
        st.info("Make sure you have the foundation_data/panels/ folder with the required panel files.")
        return
    
    # Initialize foundation session state
    if 'foundation_state' not in st.session_state:
        st.session_state.foundation_state = {
            'hrp1000': None,
            'hrp1001': None,
            'hierarchy': None,
            'admin_mode': False
        }
    
    foundation_state = st.session_state.foundation_state
    
    st.markdown("### 🏢 Foundation Data Management System")
    st.markdown("*Advanced organizational hierarchy processing for SAP HCM → SuccessFactors migration*")
    
    # Simple panel navigation
    panel_choice = st.selectbox(
        "**Choose Panel:**",
        [
            "🏢 Hierarchy Processing",
            "✅ Data Validation", 
            "📊 Statistics & Analytics",
            "🏥 Health Monitor",
            "⚙️ Admin Configuration"
        ],
        key="foundation_panel_selection"
    )
    
    st.markdown("---")
    
    # Show selected panel
    try:
        if panel_choice == "🏢 Hierarchy Processing":
            show_hierarchy_panel(foundation_state)
        elif panel_choice == "✅ Data Validation":
            show_validation_panel(foundation_state)
        elif panel_choice == "📊 Statistics & Analytics":
            show_statistics_panel(foundation_state)
        elif panel_choice == "🏥 Health Monitor":
            show_health_monitor_panel(foundation_state)
        elif panel_choice == "⚙️ Admin Configuration":
            foundation_state['admin_mode'] = st.checkbox("Enable Admin Mode")
            if foundation_state['admin_mode']:
                show_admin_panel()
            else:
                st.info("Enable admin mode to access configuration options.")
                
    except Exception as e:
        st.error(f"❌ Panel Error: {str(e)}")
        st.info("Try refreshing the page or switching to a different panel")

def get_foundation_system_status():
    """Get foundation system status"""
    return {
        "available": FOUNDATION_AVAILABLE,
        "enhanced_features": {
            "statistics": STATISTICS_ENHANCED,
            "validation": VALIDATION_ENHANCED, 
            "health_monitor": HEALTH_MONITOR_ENHANCED
        }
    }
