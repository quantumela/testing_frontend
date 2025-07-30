"""
Payroll Data Management Wrapper
This file provides a clean interface between the main app and the payroll data management system
"""

import os
import sys
import streamlit as st

# Add the payroll paths - try multiple locations
current_dir = os.path.dirname(__file__)
payroll_path = os.path.join(current_dir, 'payroll')
payroll_panels_path = os.path.join(current_dir, 'payroll_panels')

# Add paths to sys.path if they don't exist
paths_to_add = [payroll_path, payroll_panels_path]
for path in paths_to_add:
    if os.path.exists(path) and path not in sys.path:
        sys.path.insert(0, path)

# Import the payroll data management panels - try multiple import strategies
PAYROLL_DATA_AVAILABLE = False
import_error_messages = []

# Strategy 1: Direct import (panels in current directory or already in path)
try:
    from payroll_main_panel import show_payroll_panel
    from payroll_statistics_panel import show_payroll_statistics_panel  
    from payroll_validation_panel import show_payroll_validation_panel
    from payroll_dashboard_panel import show_payroll_dashboard_panel
    from payroll_admin_panel import show_payroll_admin_panel
    PAYROLL_DATA_AVAILABLE = True
    print("✅ Payroll panels imported successfully (direct)")
except ImportError as e:
    import_error_messages.append(f"Direct import failed: {e}")

# Strategy 2: Import from payroll directory
if not PAYROLL_DATA_AVAILABLE:
    try:
        sys.path.insert(0, payroll_path)
        from payroll_main_panel import show_payroll_panel
        from payroll_statistics_panel import show_payroll_statistics_panel  
        from payroll_validation_panel import show_payroll_validation_panel
        from payroll_dashboard_panel import show_payroll_dashboard_panel
        from payroll_admin_panel import show_payroll_admin_panel
        PAYROLL_DATA_AVAILABLE = True
        print("✅ Payroll panels imported successfully (from payroll/)")
    except ImportError as e:
        import_error_messages.append(f"Payroll directory import failed: {e}")

# Strategy 3: Import from payroll_panels directory
if not PAYROLL_DATA_AVAILABLE:
    try:
        sys.path.insert(0, payroll_panels_path)
        from payroll_main_panel import show_payroll_panel
        from payroll_statistics_panel import show_payroll_statistics_panel  
        from payroll_validation_panel import show_payroll_validation_panel
        from payroll_dashboard_panel import show_payroll_dashboard_panel
        from payroll_admin_panel import show_payroll_admin_panel
        PAYROLL_DATA_AVAILABLE = True
        print("✅ Payroll panels imported successfully (from payroll_panels/)")
    except ImportError as e:
        import_error_messages.append(f"Payroll panels directory import failed: {e}")

if not PAYROLL_DATA_AVAILABLE:
    print(f"❌ All payroll import strategies failed:")
    for msg in import_error_messages:
        print(f"  - {msg}")

def render_payroll_data_management():
    """Render the complete payroll data management system"""
    if not PAYROLL_DATA_AVAILABLE:
        st.error("❌ Payroll Data Management system not available.")
        with st.expander("🔍 Troubleshooting", expanded=False):
            st.markdown("""
            **Common issues:**
            1. Make sure the payroll panel files exist in one of these locations:
               - `payroll/` directory (same level as app.py)
               - `payroll_panels/` directory (same level as app.py)
               - Current directory
            2. Check that all panel files exist:
               - payroll_main_panel.py
               - payroll_statistics_panel.py
               - payroll_validation_panel.py
               - payroll_dashboard_panel.py
               - payroll_admin_panel.py
            3. Verify your folder structure matches one of these:
            
            **Option 1 - Panels in payroll directory:**
            ```
            your_project/
            ├── app.py
            ├── payroll_data_wrapper.py
            └── payroll/
                ├── payroll_main_panel.py
                ├── payroll_statistics_panel.py
                ├── payroll_validation_panel.py
                ├── payroll_dashboard_panel.py
                ├── payroll_admin_panel.py
                ├── payroll_configs/
                └── payroll_picklists/
            ```
            
            **Option 2 - Separate payroll_panels directory:**
            ```
            your_project/
            ├── app.py
            ├── payroll_data_wrapper.py
            ├── payroll/
            │   ├── payroll_configs/
            │   └── payroll_picklists/
            └── payroll_panels/
                ├── payroll_main_panel.py
                ├── payroll_statistics_panel.py
                ├── payroll_validation_panel.py
                ├── payroll_dashboard_panel.py
                └── payroll_admin_panel.py
            ```
            """)
            
            # Show detailed error information
            st.markdown("**Import Error Details:**")
            for i, msg in enumerate(import_error_messages, 1):
                st.code(f"{i}. {msg}")
                
        return
    
    # Initialize payroll session state if not exists
    if 'payroll_state' not in st.session_state:
        st.session_state.payroll_state = {}
    
    payroll_state = st.session_state.payroll_state
    
    # Create a container for the payroll management system
    with st.container():
        st.markdown("### 💰 Payroll Data Management System")
        st.markdown("*Advanced processing, validation, and analytics for SAP HCM → SuccessFactors payroll migration*")
        
        # Navigation for payroll panels
        panel_choice = st.selectbox(
            "**Choose Panel:**",
            [
                "🏠 Payroll Processing",
                "📊 Statistics & Analytics", 
                "✅ Data Validation",
                "📈 Dashboard",
                "⚙️ Admin Configuration"
            ],
            key="payroll_panel_selection",
            help="Select the payroll panel you want to work with"
        )
        
        # Show quick status in columns
        st.markdown("#### 📋 Quick Status")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            pa_files_loaded = sum(1 for file_key in ['PA0008', 'PA0014'] 
                                 if payroll_state.get(f'source_{file_key.lower()}') is not None)
            st.metric("📂 PA Files", f"{pa_files_loaded}/2", help="PA0008 & PA0014 files loaded for payroll processing")
        
        with col2:
            output_generated = 'generated_payroll_files' in payroll_state and payroll_state['generated_payroll_files']
            st.metric("📤 Output", "✅ Ready" if output_generated else "❌ Pending", help="Payroll output file generation status")
        
        with col3:
            if pa_files_loaded >= 2:
                st.metric("🎯 Status", "✅ Ready", help="System ready for payroll processing")
            else:
                st.metric("🎯 Status", "⚠️ Waiting", help="Need PA0008 & PA0014 to proceed")
        
        with col4:
            # Show wage types processed if available
            wage_types_count = payroll_state.get('wage_types_processed', 0)
            st.metric("💵 Wage Types", wage_types_count if wage_types_count > 0 else 'N/A', help="Number of wage types processed")
        
        st.markdown("---")
        
        # Show helpful tips
        if pa_files_loaded < 2:
            st.info("💡 **Getting Started:** Upload PA0008 (Basic Pay) and PA0014 (Recurring Payments/Deductions) files in the Payroll Processing panel to begin.")
        
        # Show selected panel
        try:
            if panel_choice == "🏠 Payroll Processing":
                with st.expander("ℹ️ About Payroll Processing", expanded=False):
                    st.markdown("""
                    **Payroll Processing Panel** handles:
                    - Upload and processing of PA0008 (Basic Pay) and PA0014 (Recurring Payments/Deductions) files
                    - Wage type mapping and transformation
                    - Generation of SuccessFactors-ready payroll output files
                    - Preview and validation of processed payroll data
                    """)
                show_payroll_panel(payroll_state)
                
            elif panel_choice == "📊 Statistics & Analytics":
                with st.expander("ℹ️ About Statistics & Analytics", expanded=False):
                    st.markdown("""
                    **Statistics & Analytics Panel** provides:
                    - Comprehensive payroll data analysis and insights
                    - Wage type distribution and trends
                    - Payment pattern analysis
                    - Data quality assessment for payroll records
                    """)
                # Add warning for large datasets
                pa0008_data = payroll_state.get('source_pa0008')
                if pa0008_data is not None and len(pa0008_data) > 10000:
                    st.warning("⚠️ Large payroll dataset detected. Statistics panel may take a moment to load...")
                
                with st.spinner("Loading payroll statistics..."):
                    show_payroll_statistics_panel(payroll_state)
                    
            elif panel_choice == "✅ Data Validation":
                with st.expander("ℹ️ About Data Validation", expanded=False):
                    st.markdown("""
                    **Data Validation Panel** performs:
                    - Comprehensive payroll data quality checks
                    - Wage type validation and business rule verification
                    - Payment amount and currency validation
                    - Error reporting and remediation guidance for payroll data
                    """)
                with st.spinner("Running payroll validation checks..."):
                    show_payroll_validation_panel(payroll_state)
                    
            elif panel_choice == "📈 Dashboard":
                with st.expander("ℹ️ About Dashboard", expanded=False):
                    st.markdown("""
                    **Dashboard Panel** displays:
                    - Real-time payroll migration progress
                    - Key payroll performance indicators
                    - Visual payroll data summaries
                    - Migration status overview for payroll components
                    """)
                show_payroll_dashboard_panel(payroll_state)
                
            elif panel_choice == "⚙️ Admin Configuration":
                with st.expander("ℹ️ About Admin Configuration", expanded=False):
                    st.markdown("""
                    **Admin Configuration Panel** manages:
                    - Payroll system settings and preferences
                    - Wage type mapping configurations
                    - Payroll business rules setup
                    - Advanced payroll processing parameters
                    """)
                show_payroll_admin_panel()

        except Exception as e:
            st.error(f"❌ **Panel Error:** {str(e)}")
            st.info("**What to do:** Try refreshing the page or switching to a different panel")
            
            # Show error details in expander
            with st.expander("🔍 Technical Details", expanded=False):
                st.code(str(e))
                if st.button("🔄 Reset Payroll Session", key="reset_payroll_session"):
                    if 'payroll_state' in st.session_state:
                        del st.session_state['payroll_state']
                    st.rerun()
                    
        # Footer with helpful information
        st.markdown("---")
        st.markdown("**💡 Tips for Payroll Success:**")
        st.markdown("""
        1. **Start with Processing:** Upload PA0008 & PA0014 files and generate payroll output first
        2. **Validate Early:** Run validation checks to catch payroll issues before final migration
        3. **Monitor Progress:** Use the dashboard to track your payroll migration status
        4. **Analyze Wage Types:** Use statistics panel to understand wage type distribution and patterns
        """)

def get_payroll_system_status():
    """Get current status of the payroll data management system"""
    if not PAYROLL_DATA_AVAILABLE:
        return {"available": False, "error": "Modules not loaded"}
    
    if 'payroll_state' not in st.session_state:
        return {"available": True, "initialized": False}
    
    payroll_state = st.session_state.payroll_state
    pa_files_loaded = sum(1 for file_key in ['PA0008', 'PA0014'] 
                         if payroll_state.get(f'source_{file_key.lower()}') is not None)
    
    return {
        "available": True,
        "initialized": True,
        "pa_files_loaded": pa_files_loaded,
        "ready_to_process": pa_files_loaded >= 2,
        "output_generated": payroll_state.get('generated_payroll_files', False),
        "wage_types_processed": payroll_state.get('wage_types_processed', 0)
    }
