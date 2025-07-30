"""
Employee Data Management Wrapper
This file provides a clean interface between the main app and the employee data management system
"""

import os
import sys
import streamlit as st

# Add the employee_data_management path
current_dir = os.path.dirname(__file__)
employee_data_path = os.path.join(current_dir, 'employee_data_management')
panels_path = os.path.join(employee_data_path, 'panels')

sys.path.insert(0, employee_data_path)
sys.path.insert(0, panels_path)

# Import the employee data management panels
try:
    from employee_main_panel import show_employee_panel
    from employee_statistics_panel import show_employee_statistics_panel  
    from employee_validation_panel import show_employee_validation_panel
    from employee_dashboard_panel import show_employee_dashboard_panel
    from employee_admin_panel import show_employee_admin_panel
    EMPLOYEE_DATA_AVAILABLE = True
except ImportError as e:
    EMPLOYEE_DATA_AVAILABLE = False
    st.error(f"Employee data management modules not available: {e}")

def render_employee_data_management():
    """Render the complete employee data management system"""
    if not EMPLOYEE_DATA_AVAILABLE:
        st.error("❌ Employee Data Management system not available. Please check your installation.")
        st.info("Make sure the 'employee_data_management' folder is in the same directory as your main app.py")
        return
    
    # Initialize employee session state if not exists
    if 'employee_state' not in st.session_state:
        st.session_state.employee_state = {}
    
    employee_state = st.session_state.employee_state
    
    # Create a container for the employee management system
    with st.container():
        st.markdown("### 👥 Employee Data Management System")
        st.markdown("*Advanced processing, validation, and analytics for SAP HCM → SuccessFactors migration*")
        
        # Navigation for employee panels
        panel_choice = st.selectbox(
            "**Choose Panel:**",
            [
                "🏠 Employee Processing",
                "📊 Statistics & Detective", 
                "✅ Data Validation",
                "📈 Dashboard",
                "⚙️ Admin Configuration"
            ],
            key="employee_panel_selection",
            help="Select the panel you want to work with"
        )
        
        # Show quick status in columns
        st.markdown("#### 📋 Quick Status")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            pa_files_loaded = sum(1 for file_key in ['PA0001', 'PA0002', 'PA0006', 'PA0105'] 
                                 if employee_state.get(f'source_{file_key.lower()}') is not None)
            st.metric("📂 PA Files", f"{pa_files_loaded}/4", help="PA files loaded for processing")
        
        with col2:
            output_generated = 'generated_employee_files' in employee_state and employee_state['generated_employee_files']
            st.metric("📤 Output", "✅ Ready" if output_generated else "❌ Pending", help="Output file generation status")
        
        with col3:
            if pa_files_loaded >= 2:
                st.metric("🎯 Status", "✅ Ready", help="System ready for processing")
            else:
                st.metric("🎯 Status", "⚠️ Waiting", help="Need at least PA0001 & PA0002 to proceed")
        
        with col4:
            # Show data quality score if available
            validation_score = employee_state.get('last_validation_score', 'N/A')
            st.metric("🔍 Quality", f"{validation_score}%" if validation_score != 'N/A' else 'N/A', help="Data quality score from last validation")
        
        st.markdown("---")
        
        # Show helpful tips
        if pa_files_loaded < 2:
            st.info("💡 **Getting Started:** Upload PA0001 (Basic Personal/Organizational Assignment) and PA0002 (Personal Data) files in the Employee Processing panel to begin.")
        
        # Show selected panel
        try:
            if panel_choice == "🏠 Employee Processing":
                with st.expander("ℹ️ About Employee Processing", expanded=False):
                    st.markdown("""
                    **Employee Processing Panel** handles:
                    - Upload and processing of PA files (PA0001, PA0002, PA0006, PA0105)
                    - Data transformation and mapping
                    - Generation of SuccessFactors-ready output files
                    - Preview and validation of processed data
                    """)
                show_employee_panel(employee_state)
                
            elif panel_choice == "📊 Statistics & Detective":
                with st.expander("ℹ️ About Statistics & Detective", expanded=False):
                    st.markdown("""
                    **Statistics & Detective Panel** provides:
                    - Comprehensive data analysis and insights
                    - Data quality assessment
                    - Pattern detection and anomaly identification
                    - Detailed statistics on employee data
                    """)
                # Add warning for large datasets
                pa0002_data = employee_state.get('source_pa0002')
                if pa0002_data is not None and len(pa0002_data) > 10000:
                    st.warning("⚠️ Large dataset detected. Statistics panel may take a moment to load...")
                
                with st.spinner("Loading statistics..."):
                    show_employee_statistics_panel(employee_state)
                    
            elif panel_choice == "✅ Data Validation":
                with st.expander("ℹ️ About Data Validation", expanded=False):
                    st.markdown("""
                    **Data Validation Panel** performs:
                    - Comprehensive data quality checks
                    - Business rule validation
                    - Data consistency verification
                    - Error reporting and remediation guidance
                    """)
                with st.spinner("Running validation checks..."):
                    show_employee_validation_panel(employee_state)
                    
            elif panel_choice == "📈 Dashboard":
                with st.expander("ℹ️ About Dashboard", expanded=False):
                    st.markdown("""
                    **Dashboard Panel** displays:
                    - Real-time migration progress
                    - Key performance indicators
                    - Visual data summaries
                    - Migration status overview
                    """)
                show_employee_dashboard_panel(employee_state)
                
            elif panel_choice == "⚙️ Admin Configuration":
                with st.expander("ℹ️ About Admin Configuration", expanded=False):
                    st.markdown("""
                    **Admin Configuration Panel** manages:
                    - System settings and preferences
                    - Mapping configurations
                    - Business rules setup
                    - Advanced system parameters
                    """)
                show_employee_admin_panel()

        except Exception as e:
            st.error(f"❌ **Panel Error:** {str(e)}")
            st.info("**What to do:** Try refreshing the page or switching to a different panel")
            
            # Show error details in expander
            with st.expander("🔍 Technical Details", expanded=False):
                st.code(str(e))
                if st.button("🔄 Reset Employee Session", key="reset_employee_session"):
                    if 'employee_state' in st.session_state:
                        del st.session_state['employee_state']
                    st.rerun()
                    
        # Footer with helpful information
        st.markdown("---")
        st.markdown("**💡 Tips for Success:**")
        st.markdown("""
        1. **Start with Processing:** Upload your PA files and generate output first
        2. **Validate Early:** Run validation checks to catch issues before final migration
        3. **Monitor Progress:** Use the dashboard to track your migration status
        4. **Analyze Data:** Use statistics panel to understand your data better
        """)

def get_employee_system_status():
    """Get current status of the employee data management system"""
    if not EMPLOYEE_DATA_AVAILABLE:
        return {"available": False, "error": "Modules not loaded"}
    
    if 'employee_state' not in st.session_state:
        return {"available": True, "initialized": False}
    
    employee_state = st.session_state.employee_state
    pa_files_loaded = sum(1 for file_key in ['PA0001', 'PA0002', 'PA0006', 'PA0105'] 
                         if employee_state.get(f'source_{file_key.lower()}') is not None)
    
    return {
        "available": True,
        "initialized": True,
        "pa_files_loaded": pa_files_loaded,
        "ready_to_process": pa_files_loaded >= 2,
        "output_generated": employee_state.get('generated_employee_files', False)
    }
