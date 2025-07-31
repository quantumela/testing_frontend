"""
Protected Payroll Admin Panel
Provides secure admin configuration for Payroll Data Management
"""

import streamlit as st
import pandas as pd
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from admin_auth import create_payroll_admin

# Configuration directories
CONFIG_DIR = "payroll_configs"
TEMPLATE_DIR = "payroll_templates"
WAGE_TYPE_DIR = "wage_type_configs"

def initialize_payroll_directories():
    """Create required directories if they don't exist"""
    for directory in [CONFIG_DIR, TEMPLATE_DIR, WAGE_TYPE_DIR]:
        Path(directory).mkdir(exist_ok=True)

def save_payroll_config(config_type: str, config_data: Any) -> None:
    """Save payroll configuration to file"""
    try:
        config_path = os.path.join(CONFIG_DIR, f"{config_type}_config.json")
        with open(config_path, "w") as f:
            json.dump(config_data, f, indent=2)
        st.success(f"✅ {config_type.title()} configuration saved!")
    except Exception as e:
        st.error(f"❌ Error saving config: {str(e)}")

def load_payroll_config(config_type: str) -> Optional[Any]:
    """Load payroll configuration from file"""
    try:
        config_path = os.path.join(CONFIG_DIR, f"{config_type}_config.json")
        if not os.path.exists(config_path):
            return None
        with open(config_path, "r") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"❌ Error loading config: {str(e)}")
        return None

def get_default_wage_types():
    """Get default wage type mappings"""
    return {
        "1000": {"name": "Basic Pay", "category": "regular", "taxable": True},
        "1010": {"name": "Overtime Pay", "category": "overtime", "taxable": True},
        "1020": {"name": "Holiday Pay", "category": "premium", "taxable": True},
        "2000": {"name": "Health Insurance", "category": "benefit", "taxable": False},
        "2010": {"name": "Retirement Contribution", "category": "benefit", "taxable": False},
        "3000": {"name": "Federal Tax", "category": "deduction", "taxable": False},
        "3010": {"name": "State Tax", "category": "deduction", "taxable": False},
        "3020": {"name": "Social Security", "category": "deduction", "taxable": False},
        "4000": {"name": "Bonus", "category": "bonus", "taxable": True},
        "9000": {"name": "Other Pay", "category": "other", "taxable": True}
    }

def show_payroll_configuration_status():
    """Show current payroll configuration status"""
    st.subheader("📋 Payroll Configuration Status")
    st.info("**What this shows:** Current status of your Payroll Data Management configuration")
    
    # Check configurations
    wage_type_config = load_payroll_config("wage_types")
    validation_config = load_payroll_config("validation_rules")
    processing_config = load_payroll_config("processing_settings")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if wage_type_config:
            st.success("✅ **Wage Type Mappings**")
            st.caption(f"{len(wage_type_config)} wage types configured")
        else:
            st.warning("⚠️ **Wage Type Mappings**")
            st.caption("Using system defaults")
    
    with col2:
        if validation_config:
            st.success("✅ **Validation Rules**")
            st.caption(f"{len(validation_config.get('rules', []))} rules active")
        else:
            st.error("❌ **Validation Rules**")
            st.caption("Using basic validation")
    
    with col3:
        if processing_config:
            st.success("✅ **Processing Settings**")
            st.caption("Custom settings active")
        else:
            st.warning("⚠️ **Processing Settings**")
            st.caption("Using defaults")
    
    # Overall status
    config_count = sum(1 for config in [wage_type_config, validation_config, processing_config] if config)
    if config_count == 3:
        st.success("🎉 **Payroll Configuration Complete!**")
    elif config_count > 0:
        st.warning(f"⚠️ **Configuration Partial** - {config_count}/3 components configured")
    else:
        st.info("ℹ️ **Configuration Not Started** - Using system defaults")

def configure_wage_types():
    """Configure wage type mappings and categories"""
    st.subheader("💰 Wage Type Configuration")
    st.info("**What this does:** Define how wage types from PA0008 and PA0014 should be interpreted and categorized")
    
    # Load current wage types or use defaults
    current_wage_types = load_payroll_config("wage_types") or get_default_wage_types()
    
    st.markdown("### 📋 Current Wage Type Mappings")
    
    # Convert to DataFrame for easier editing
    wage_type_rows = []
    for code, info in current_wage_types.items():
        wage_type_rows.append({
            "Wage Type Code": code,
            "Name": info.get("name", ""),
            "Category": info.get("category", "other"),
            "Taxable": info.get("taxable", True),
            "Description": info.get("description", "")
        })
    
    # Show current mappings in editable form
    if wage_type_rows:
        wage_type_df = pd.DataFrame(wage_type_rows)
        
        # Show current mappings
        st.dataframe(wage_type_df, use_container_width=True)
        
        # Download current mappings
        csv_data = wage_type_df.to_csv(index=False)
        st.download_button(
            "📥 Download Current Wage Types",
            data=csv_data,
            file_name="wage_type_mappings.csv",
            mime="text/csv"
        )
    
    # Add new wage type
    st.markdown("### ➕ Add New Wage Type")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        new_code = st.text_input(
            "Wage Type Code:",
            placeholder="e.g., 5000",
            help="4-digit code from your PA files"
        )
        
        new_name = st.text_input(
            "Display Name:",
            placeholder="e.g., Commission Pay",
            help="Human-readable name"
        )
    
    with col2:
        category_options = ["regular", "overtime", "premium", "bonus", "benefit", "deduction", "other"]
        new_category = st.selectbox(
            "Category:",
            category_options,
            help="Type of wage/deduction"
        )
        
        new_taxable = st.checkbox(
            "Taxable",
            value=True,
            help="Is this wage type subject to taxes?"
        )
    
    with col3:
        new_description = st.text_area(
            "Description:",
            placeholder="Optional description...",
            height=100,
            help="Additional details about this wage type"
        )
    
    if st.button("➕ Add Wage Type", type="primary"):
        if new_code and new_name:
            current_wage_types[new_code] = {
                "name": new_name,
                "category": new_category,
                "taxable": new_taxable,
                "description": new_description
            }
            save_payroll_config("wage_types", current_wage_types)
            st.success(f"✅ Added wage type: {new_code} - {new_name}")
            st.rerun()
        else:
            st.error("❌ Please provide both code and name")
    
    # Bulk upload wage types
    st.markdown("### 📤 Bulk Upload Wage Types")
    
    upload_file = st.file_uploader(
        "Upload Wage Type CSV:",
        type=['csv'],
        help="CSV with columns: Wage Type Code, Name, Category, Taxable, Description"
    )
    
    if upload_file:
        try:
            df = pd.read_csv(upload_file)
            
            # Validate required columns
            required_cols = ["Wage Type Code", "Name", "Category"]
            if all(col in df.columns for col in required_cols):
                
                st.subheader("📋 Preview Upload")
                st.dataframe(df.head(), use_container_width=True)
                
                if st.button("📤 Import Wage Types"):
                    # Convert DataFrame to wage type format
                    for _, row in df.iterrows():
                        code = str(row["Wage Type Code"])
                        current_wage_types[code] = {
                            "name": row["Name"],
                            "category": row.get("Category", "other"),
                            "taxable": row.get("Taxable", True),
                            "description": row.get("Description", "")
                        }
                    
                    save_payroll_config("wage_types", current_wage_types)
                    st.success(f"✅ Imported {len(df)} wage types!")
                    st.rerun()
            else:
                st.error(f"❌ Missing required columns: {', '.join(required_cols)}")
                
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")

def configure_validation_rules():
    """Configure payroll validation rules"""
    st.subheader("✅ Payroll Validation Rules")
    st.info("**What this does:** Set up validation rules to ensure payroll data quality and catch errors")
    
    # Load current validation rules
    current_rules = load_payroll_config("validation_rules") or {
        "rules": [],
        "thresholds": {},
        "alerts": {}
    }
    
    st.markdown("### 🎯 Amount Validation Thresholds")
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_regular_pay = st.number_input(
            "Maximum Regular Pay per Period:",
            min_value=0.0,
            value=current_rules.get("thresholds", {}).get("max_regular_pay", 50000.0),
            help="Alert if regular pay exceeds this amount"
        )
        
        max_overtime_hours = st.number_input(
            "Maximum Overtime Hours:",
            min_value=0.0,
            value=current_rules.get("thresholds", {}).get("max_overtime_hours", 80.0),
            help="Alert if overtime hours exceed this limit"
        )
    
    with col2:
        min_wage_rate = st.number_input(
            "Minimum Wage Rate:",
            min_value=0.0,
            value=current_rules.get("thresholds", {}).get("min_wage_rate", 7.25),
            help="Alert if wage rate is below minimum"
        )
        
        max_deduction_percent = st.number_input(
            "Maximum Deduction Percentage:",
            min_value=0.0,
            max_value=100.0,
            value=current_rules.get("thresholds", {}).get("max_deduction_percent", 50.0),
            help="Alert if total deductions exceed this % of pay"
        )
    
    # Date validation
    st.markdown("### 📅 Date Validation Rules")
    
    validate_pay_periods = st.checkbox(
        "Validate Pay Period Dates",
        value=current_rules.get("alerts", {}).get("validate_pay_periods", True),
        help="Check that pay periods are logical and sequential"
    )
    
    check_future_dates = st.checkbox(
        "Alert on Future Dates",
        value=current_rules.get("alerts", {}).get("check_future_dates", True),
        help="Warn about payments dated in the future"
    )
    
    # Employee validation
    st.markdown("### 👥 Employee Validation Rules")
    
    require_employee_match = st.checkbox(
        "Require Employee ID Match",
        value=current_rules.get("alerts", {}).get("require_employee_match", True),
        help="Ensure all payroll records have valid employee IDs"
    )
    
    check_duplicate_payments = st.checkbox(
        "Check for Duplicate Payments",
        value=current_rules.get("alerts", {}).get("check_duplicate_payments", True),
        help="Alert on potential duplicate payment records"
    )
    
    # Custom validation rules
    st.markdown("### 🔧 Custom Validation Rules")
    
    custom_rules = st.text_area(
        "Custom Rules (JSON format):",
        value=json.dumps(current_rules.get("custom_rules", {}), indent=2),
        height=150,
        help="Advanced: Custom validation rules in JSON format"
    )
    
    # Save validation rules
    if st.button("💾 Save Validation Rules", type="primary"):
        try:
            custom_rules_data = json.loads(custom_rules) if custom_rules.strip() else {}
            
            validation_data = {
                "thresholds": {
                    "max_regular_pay": max_regular_pay,
                    "max_overtime_hours": max_overtime_hours,
                    "min_wage_rate": min_wage_rate,
                    "max_deduction_percent": max_deduction_percent
                },
                "alerts": {
                    "validate_pay_periods": validate_pay_periods,
                    "check_future_dates": check_future_dates,
                    "require_employee_match": require_employee_match,
                    "check_duplicate_payments": check_duplicate_payments
                },
                "custom_rules": custom_rules_data,
                "updated": pd.Timestamp.now().isoformat()
            }
            
            save_payroll_config("validation_rules", validation_data)
            
            # Show preview
            st.subheader("✅ Validation Rules Preview")
            st.json(validation_data)
            
        except json.JSONDecodeError:
            st.error("❌ Invalid JSON in custom rules")
        except Exception as e:
            st.error(f"❌ Error saving validation rules: {str(e)}")

def configure_processing_settings():
    """Configure payroll processing settings"""
    st.subheader("⚙️ Payroll Processing Settings")
    st.info("**What this does:** Configure how PA0008 and PA0014 files are processed and analyzed")
    
    # Load current settings
    current_settings = load_payroll_config("processing_settings") or {
        "batch_size": 5000,
        "currency_format": "USD",
        "decimal_places": 2,
        "date_format": "YYYY-MM-DD",
        "include_zero_amounts": False,
        "group_by_employee": True
    }
    
    # Performance settings
    st.markdown("### 🚀 Performance Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        batch_size = st.number_input(
            "Batch Processing Size:",
            min_value=100,
            max_value=50000,
            value=current_settings.get("batch_size", 5000),
            step=500,
            help="Number of payroll records to process at once"
        )
        
        parallel_processing = st.checkbox(
            "Enable Parallel Processing",
            value=current_settings.get("parallel_processing", True),
            help="Process multiple files simultaneously"
        )
    
    with col2:
        memory_optimization = st.checkbox(
            "Memory Optimization",
            value=current_settings.get("memory_optimization", True),
            help="Use memory-efficient processing for large payroll files"
        )
        
        progress_reporting = st.checkbox(
            "Show Detailed Progress",
            value=current_settings.get("progress_reporting", True),
            help="Display detailed progress during processing"
        )
    
    # Data formatting
    st.markdown("### 💱 Data Formatting")
    
    col1, col2 = st.columns(2)
    
    with col1:
        currency_format = st.selectbox(
            "Currency Format:",
            ["USD", "EUR", "GBP", "CAD", "AUD", "Other"],
            index=["USD", "EUR", "GBP", "CAD", "AUD", "Other"].index(current_settings.get("currency_format", "USD")),
            help="Default currency for amount formatting"
        )
        
        decimal_places = st.number_input(
            "Decimal Places:",
            min_value=0,
            max_value=6,
            value=current_settings.get("decimal_places", 2),
            help="Number of decimal places for amounts"
        )
    
    with col2:
        date_format = st.selectbox(
            "Date Format:",
            ["YYYY-MM-DD", "MM/DD/YYYY", "DD/MM/YYYY", "DD-MMM-YYYY"],
            index=["YYYY-MM-DD", "MM/DD/YYYY", "DD/MM/YYYY", "DD-MMM-YYYY"].index(current_settings.get("date_format", "YYYY-MM-DD")),
            help="Format for date fields in output"
        )
        
        include_zero_amounts = st.checkbox(
            "Include Zero Amount Records",
            value=current_settings.get("include_zero_amounts", False),
            help="Include payroll records with zero amounts"
        )
    
    # Grouping and aggregation
    st.markdown("### 📊 Data Grouping & Aggregation")
    
    group_by_employee = st.checkbox(
        "Group by Employee",
        value=current_settings.get("group_by_employee", True),
        help="Group payroll data by employee for analysis"
    )
    
    group_by_pay_period = st.checkbox(
        "Group by Pay Period",
        value=current_settings.get("group_by_pay_period", True),
        help="Group data by pay periods for trend analysis"
    )
    
    calculate_totals = st.checkbox(
        "Calculate Summary Totals",
        value=current_settings.get("calculate_totals", True),
        help="Calculate total pay, deductions, and net pay"
    )
    
    # Output options
    st.markdown("### 📤 Output Options")
    
    output_format = st.selectbox(
        "Output File Format:",
        ["csv", "excel", "json"],
        index=["csv", "excel", "json"].index(current_settings.get("output_format", "csv")),
        help="Format for generated payroll files"
    )
    
    include_analytics = st.checkbox(
        "Include Analytics Sheet",
        value=current_settings.get("include_analytics", True),
        help="Add analytics and summary data to output"
    )
    
    # Save settings
    if st.button("💾 Save Processing Settings", type="primary"):
        settings_data = {
            "batch_size": batch_size,
            "parallel_processing": parallel_processing,
            "memory_optimization": memory_optimization,
            "progress_reporting": progress_reporting,
            "currency_format": currency_format,
            "decimal_places": decimal_places,
            "date_format": date_format,
            "include_zero_amounts": include_zero_amounts,
            "group_by_employee": group_by_employee,
            "group_by_pay_period": group_by_pay_period,
            "calculate_totals": calculate_totals,
            "output_format": output_format,
            "include_analytics": include_analytics,
            "updated": pd.Timestamp.now().isoformat()
        }
        
        save_payroll_config("processing_settings", settings_data)
        
        # Show preview
        st.subheader("✅ Settings Preview")
        st.json(settings_data)

def system_maintenance():
    """System maintenance and cleanup tools"""
    st.subheader("🔧 Payroll System Maintenance")
    st.info("**What this does:** Maintenance tools for the Payroll Data Management system")
    
    # Configuration backup/restore
    st.markdown("### 💾 Configuration Backup & Restore")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📥 Backup Configuration**")
        if st.button("📦 Create Payroll Backup"):
            try:
                # Collect all configurations
                backup_data = {
                    "wage_types": load_payroll_config("wage_types"),
                    "validation_rules": load_payroll_config("validation_rules"),
                    "processing_settings": load_payroll_config("processing_settings"),
                    "backup_timestamp": pd.Timestamp.now().isoformat(),
                    "system": "payroll"
                }
                
                # Create downloadable backup
                backup_json = json.dumps(backup_data, indent=2)
                st.download_button(
                    "📥 Download Payroll Backup",
                    data=backup_json,
                    file_name=f"payroll_config_backup_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
                st.success("✅ Payroll backup created successfully!")
                
            except Exception as e:
                st.error(f"❌ Error creating backup: {str(e)}")
    
    with col2:
        st.markdown("**📤 Restore Configuration**")
        restore_file = st.file_uploader(
            "Upload Payroll Backup:",
            type=['json'],
            help="Select a payroll configuration backup file"
        )
        
        if restore_file and st.button("🔄 Restore Payroll Config"):
            try:
                backup_data = json.load(restore_file)
                
                # Verify it's a payroll backup
                if backup_data.get("system") != "payroll":
                    st.warning("⚠️ This doesn't appear to be a payroll backup file")
                
                # Restore each configuration
                for config_type, config_data in backup_data.items():
                    if config_type not in ["backup_timestamp", "system"] and config_data:
                        save_payroll_config(config_type, config_data)
                
                st.success("✅ Payroll configuration restored successfully!")
                st.info("Please refresh the page to see restored settings")
                
            except Exception as e:
                st.error(f"❌ Error restoring configuration: {str(e)}")
    
    # Clear cache and reset
    st.markdown("### 🗑️ Clear Data & Reset")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🧹 Clear Payroll Cache"):
            # Clear payroll-related session state
            keys_to_clear = [key for key in st.session_state.keys() if 'payroll' in key.lower()]
            for key in keys_to_clear:
                del st.session_state[key]
            st.success("✅ Payroll cache cleared!")
    
    with col2:
        if st.button("⚠️ Reset Payroll Configuration", type="secondary"):
            st.warning("This will delete all payroll configuration files!")
            if st.checkbox("I understand this cannot be undone", key="payroll_reset_confirm"):
                try:
                    # Remove configuration files
                    for config_file in Path(CONFIG_DIR).glob("*.json"):
                        config_file.unlink()
                    st.success("✅ All payroll configurations reset!")
                except Exception as e:
                    st.error(f"❌ Error resetting: {str(e)}")

def show_payroll_admin_panel():
    """Main payroll admin panel with authentication"""
    auth = create_payroll_admin()
    
    def payroll_admin_content():
        # Clean header
        st.markdown("""
        <div style="background: linear-gradient(90deg, #dc2626 0%, #ef4444 100%); 
                    color: white; padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
            <h1 style="margin: 0; font-size: 2.5rem;">💰 Payroll Configuration Center</h1>
            <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
                Configure how your PA0008 & PA0014 files are processed for payroll analysis
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize directories
        initialize_payroll_directories()
        
        # Configuration status at top
        show_payroll_configuration_status()
        
        st.markdown("---")
        
        # Main tabs
        tabs = st.tabs([
            "💰 Wage Types",
            "✅ Validation Rules",
            "⚙️ Processing Settings",
            "🔧 System Maintenance"
        ])
        
        with tabs[0]:
            configure_wage_types()
        
        with tabs[1]:
            configure_validation_rules()
        
        with tabs[2]:
            configure_processing_settings()
        
        with tabs[3]:
            system_maintenance()
        
        # Help section
        st.markdown("---")
        with st.expander("❓ Payroll Configuration Help", expanded=False):
            st.markdown("""
            **Payroll Configuration Overview:**
            
            💰 **Wage Types:** Define how wage type codes are interpreted and categorized
            ✅ **Validation Rules:** Set thresholds and checks for data quality
            ⚙️ **Processing Settings:** Control performance, formatting, and output options
            🔧 **System Maintenance:** Backup/restore configurations and system cleanup
            
            **Important Files:**
            - **PA0008:** Contains basic pay information (salary, hourly rates)
            - **PA0014:** Contains recurring payments and deductions
            
            **Common Tasks:**
            1. **Map Wage Types:** Define what each 4-digit wage type code means
            2. **Set Validation Thresholds:** Configure alerts for unusual amounts
            3. **Configure Processing:** Set batch sizes and output formats
            4. **Backup Settings:** Save your configuration before making changes
            
            **Tips:**
            - Start by mapping the most common wage types in your data
            - Set realistic validation thresholds based on your payroll ranges
            - Use bulk upload for large wage type lists
            - Regular backups prevent configuration loss
            """)
    
    # Apply authentication wrapper
    auth.require_auth(payroll_admin_content)
