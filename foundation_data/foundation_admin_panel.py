"""
Protected Foundation Admin Panel
Provides secure admin configuration for Foundation Data Management
"""

import streamlit as st
import pandas as pd
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from admin_auth import create_foundation_admin

# Configuration directories
CONFIG_DIR = "foundation_configs"
TEMPLATE_DIR = "foundation_templates"
SAMPLE_DIR = "foundation_samples"

def initialize_foundation_directories():
    """Create required directories if they don't exist"""
    for directory in [CONFIG_DIR, TEMPLATE_DIR, SAMPLE_DIR]:
        Path(directory).mkdir(exist_ok=True)

def save_foundation_config(config_type: str, config_data: Any) -> None:
    """Save foundation configuration to file"""
    try:
        config_path = os.path.join(CONFIG_DIR, f"{config_type}_config.json")
        with open(config_path, "w") as f:
            json.dump(config_data, f, indent=2)
        st.success(f"✅ {config_type.title()} configuration saved!")
    except Exception as e:
        st.error(f"❌ Error saving config: {str(e)}")

def load_foundation_config(config_type: str) -> Optional[Any]:
    """Load foundation configuration from file"""
    try:
        config_path = os.path.join(CONFIG_DIR, f"{config_type}_config.json")
        if not os.path.exists(config_path):
            return None
        with open(config_path, "r") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"❌ Error loading config: {str(e)}")
        return None

def show_foundation_configuration_status():
    """Show current foundation configuration status"""
    st.subheader("📋 Foundation Configuration Status")
    st.info("**What this shows:** Current status of your Foundation Data Management configuration")
    
    # Check configurations
    hierarchy_config = load_foundation_config("hierarchy_rules")
    validation_config = load_foundation_config("validation_rules")
    processing_config = load_foundation_config("processing_settings")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if hierarchy_config:
            st.success("✅ **Hierarchy Rules**")
            st.caption(f"{len(hierarchy_config.get('rules', []))} rules configured")
        else:
            st.error("❌ **Hierarchy Rules**")
            st.caption("Not configured")
    
    with col2:
        if validation_config:
            st.success("✅ **Validation Rules**")
            st.caption(f"{len(validation_config.get('rules', []))} rules active")
        else:
            st.error("❌ **Validation Rules**")
            st.caption("Using defaults")
    
    with col3:
        if processing_config:
            st.success("✅ **Processing Settings**")
            st.caption("Custom settings active")
        else:
            st.warning("⚠️ **Processing Settings**")
            st.caption("Using defaults")
    
    # Overall status
    config_count = sum(1 for config in [hierarchy_config, validation_config, processing_config] if config)
    if config_count == 3:
        st.success("🎉 **Foundation Configuration Complete!**")
    elif config_count > 0:
        st.warning(f"⚠️ **Configuration Partial** - {config_count}/3 components configured")
    else:
        st.info("ℹ️ **Configuration Not Started** - Using system defaults")

def configure_hierarchy_rules():
    """Configure foundation hierarchy processing rules"""
    st.subheader("🏗️ Hierarchy Processing Rules")
    st.info("**What this does:** Define how organizational hierarchy should be processed and validated")
    
    # Load current rules
    current_config = load_foundation_config("hierarchy_rules") or {
        "rules": [],
        "max_levels": 10,
        "circular_detection": True,
        "auto_fix": False
    }
    
    # Basic settings
    st.markdown("### ⚙️ Basic Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        max_levels = st.number_input(
            "Maximum Hierarchy Levels",
            min_value=3,
            max_value=20,
            value=current_config.get("max_levels", 10),
            help="Maximum depth of organizational hierarchy"
        )
    
    with col2:
        circular_detection = st.checkbox(
            "Detect Circular References",
            value=current_config.get("circular_detection", True),
            help="Check for and warn about circular organizational references"
        )
    
    auto_fix = st.checkbox(
        "Auto-fix Minor Issues",
        value=current_config.get("auto_fix", False),
        help="Automatically fix minor hierarchy issues during processing"
    )
    
    # Level naming rules
    st.markdown("### 📝 Level Naming Rules")
    st.write("Define what to call each level in your organizational hierarchy:")
    
    # Initialize level names if not exists
    if "level_names" not in current_config:
        current_config["level_names"] = {
            "1": "Organization",
            "2": "Division", 
            "3": "Department",
            "4": "Team",
            "5": "Unit"
        }
    
    level_names = current_config["level_names"]
    
    # Show current level names with editing
    for level in range(1, max_levels + 1):
        level_str = str(level)
        current_name = level_names.get(level_str, f"Level {level}")
        
        new_name = st.text_input(
            f"Level {level} Name:",
            value=current_name,
            key=f"level_name_{level}",
            help=f"What to call hierarchy level {level}"
        )
        level_names[level_str] = new_name
    
    # Custom validation rules
    st.markdown("### ✅ Custom Validation Rules")
    
    validation_rules = st.text_area(
        "Custom Validation Rules (JSON):",
        value=json.dumps(current_config.get("custom_rules", {}), indent=2),
        height=150,
        help="Advanced: Custom validation rules in JSON format"
    )
    
    # Save configuration
    if st.button("💾 Save Hierarchy Configuration", type="primary"):
        try:
            custom_rules = json.loads(validation_rules) if validation_rules.strip() else {}
            
            config_data = {
                "max_levels": max_levels,
                "circular_detection": circular_detection,
                "auto_fix": auto_fix,
                "level_names": level_names,
                "custom_rules": custom_rules,
                "updated": pd.Timestamp.now().isoformat()
            }
            
            save_foundation_config("hierarchy_rules", config_data)
            
            # Show preview
            st.subheader("✅ Configuration Preview")
            st.json(config_data)
            
        except json.JSONDecodeError:
            st.error("❌ Invalid JSON in custom validation rules")
        except Exception as e:
            st.error(f"❌ Error saving configuration: {str(e)}")

def configure_processing_settings():
    """Configure foundation data processing settings"""
    st.subheader("⚙️ Processing Settings")
    st.info("**What this does:** Configure how foundation data files (HRP1000 & HRP1001) are processed")
    
    # Load current settings
    current_settings = load_foundation_config("processing_settings") or {
        "batch_size": 1000,
        "memory_optimization": True,
        "progress_reporting": True,
        "error_handling": "continue",
        "output_format": "csv"
    }
    
    # Performance settings
    st.markdown("### 🚀 Performance Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        batch_size = st.number_input(
            "Batch Processing Size",
            min_value=100,
            max_value=10000,
            value=current_settings.get("batch_size", 1000),
            step=100,
            help="Number of records to process at once"
        )
        
        memory_optimization = st.checkbox(
            "Memory Optimization",
            value=current_settings.get("memory_optimization", True),
            help="Use memory-efficient processing for large files"
        )
    
    with col2:
        progress_reporting = st.checkbox(
            "Show Progress Reports",
            value=current_settings.get("progress_reporting", True),
            help="Display progress during processing"
        )
        
        error_handling = st.selectbox(
            "Error Handling Strategy",
            ["continue", "stop", "skip_row"],
            index=["continue", "stop", "skip_row"].index(current_settings.get("error_handling", "continue")),
            help="How to handle processing errors"
        )
    
    # Output settings
    st.markdown("### 📤 Output Settings")
    
    output_format = st.selectbox(
        "Output File Format",
        ["csv", "excel", "json"],
        index=["csv", "excel", "json"].index(current_settings.get("output_format", "csv")),
        help="Format for generated foundation files"
    )
    
    include_metadata = st.checkbox(
        "Include Processing Metadata",
        value=current_settings.get("include_metadata", True),
        help="Add processing timestamps and statistics to output"
    )
    
    # Data quality settings
    st.markdown("### 🎯 Data Quality Settings")
    
    remove_duplicates = st.checkbox(
        "Remove Duplicate Records",
        value=current_settings.get("remove_duplicates", True),
        help="Automatically remove duplicate organizational entries"
    )
    
    validate_references = st.checkbox(
        "Validate Organizational References",
        value=current_settings.get("validate_references", True),
        help="Check that all organizational references are valid"
    )
    
    # Custom field mappings
    st.markdown("### 🔗 Custom Field Mappings")
    
    field_mappings = st.text_area(
        "Custom Field Mappings (JSON):",
        value=json.dumps(current_settings.get("field_mappings", {}), indent=2),
        height=100,
        help="Custom mappings for HRP1000/HRP1001 fields"
    )
    
    # Save settings
    if st.button("💾 Save Processing Settings", type="primary"):
        try:
            custom_mappings = json.loads(field_mappings) if field_mappings.strip() else {}
            
            settings_data = {
                "batch_size": batch_size,
                "memory_optimization": memory_optimization,
                "progress_reporting": progress_reporting,
                "error_handling": error_handling,
                "output_format": output_format,
                "include_metadata": include_metadata,
                "remove_duplicates": remove_duplicates,
                "validate_references": validate_references,
                "field_mappings": custom_mappings,
                "updated": pd.Timestamp.now().isoformat()
            }
            
            save_foundation_config("processing_settings", settings_data)
            
            # Show preview
            st.subheader("✅ Settings Preview")
            st.json(settings_data)
            
        except json.JSONDecodeError:
            st.error("❌ Invalid JSON in field mappings")
        except Exception as e:
            st.error(f"❌ Error saving settings: {str(e)}")

def system_maintenance():
    """System maintenance and cleanup tools"""
    st.subheader("🔧 System Maintenance")
    st.info("**What this does:** Maintenance tools for the Foundation Data Management system")
    
    # Configuration backup/restore
    st.markdown("### 💾 Configuration Backup & Restore")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📥 Backup Configuration**")
        if st.button("📦 Create Backup"):
            try:
                # Collect all configurations
                backup_data = {
                    "hierarchy_rules": load_foundation_config("hierarchy_rules"),
                    "validation_rules": load_foundation_config("validation_rules"),
                    "processing_settings": load_foundation_config("processing_settings"),
                    "backup_timestamp": pd.Timestamp.now().isoformat()
                }
                
                # Create downloadable backup
                backup_json = json.dumps(backup_data, indent=2)
                st.download_button(
                    "📥 Download Backup",
                    data=backup_json,
                    file_name=f"foundation_config_backup_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
                st.success("✅ Backup created successfully!")
                
            except Exception as e:
                st.error(f"❌ Error creating backup: {str(e)}")
    
    with col2:
        st.markdown("**📤 Restore Configuration**")
        restore_file = st.file_uploader(
            "Upload Backup File:",
            type=['json'],
            help="Select a configuration backup file to restore"
        )
        
        if restore_file and st.button("🔄 Restore Configuration"):
            try:
                backup_data = json.load(restore_file)
                
                # Restore each configuration
                for config_type, config_data in backup_data.items():
                    if config_type != "backup_timestamp" and config_data:
                        save_foundation_config(config_type, config_data)
                
                st.success("✅ Configuration restored successfully!")
                st.info("Please refresh the page to see restored settings")
                
            except Exception as e:
                st.error(f"❌ Error restoring configuration: {str(e)}")
    
    # Clear cache and reset
    st.markdown("### 🗑️ Clear Data & Reset")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🧹 Clear Session Cache"):
            # Clear foundation-related session state
            keys_to_clear = [key for key in st.session_state.keys() if 'foundation' in key.lower()]
            for key in keys_to_clear:
                del st.session_state[key]
            st.success("✅ Session cache cleared!")
    
    with col2:
        if st.button("⚠️ Reset All Configuration", type="secondary"):
            st.warning("This will delete all configuration files!")
            if st.checkbox("I understand this cannot be undone"):
                try:
                    # Remove configuration files
                    for config_file in Path(CONFIG_DIR).glob("*.json"):
                        config_file.unlink()
                    st.success("✅ All configurations reset!")
                except Exception as e:
                    st.error(f"❌ Error resetting: {str(e)}")

def show_foundation_admin_panel():
    """Main foundation admin panel with authentication"""
    auth = create_foundation_admin()
    
    def foundation_admin_content():
        # Clean header
        st.markdown("""
        <div style="background: linear-gradient(90deg, #059669 0%, #10b981 100%); 
                    color: white; padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
            <h1 style="margin: 0; font-size: 2.5rem;">🏢 Foundation Configuration Center</h1>
            <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
                Configure how your HRP1000 & HRP1001 files are processed for organizational hierarchy
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize directories
        initialize_foundation_directories()
        
        # Configuration status at top
        show_foundation_configuration_status()
        
        st.markdown("---")
        
        # Main tabs
        tabs = st.tabs([
            "🏗️ Hierarchy Rules",
            "⚙️ Processing Settings", 
            "🔧 System Maintenance"
        ])
        
        with tabs[0]:
            configure_hierarchy_rules()
        
        with tabs[1]:
            configure_processing_settings()
        
        with tabs[2]:
            system_maintenance()
        
        # Help section
        st.markdown("---")
        with st.expander("❓ Foundation Configuration Help", expanded=False):
            st.markdown("""
            **Foundation Configuration Overview:**
            
            🏗️ **Hierarchy Rules:** Define how organizational structures are processed and validated
            ⚙️ **Processing Settings:** Control performance, output format, and data quality settings
            🔧 **System Maintenance:** Backup/restore configurations and system cleanup
            
            **Important Files:**
            - **HRP1000:** Contains organizational objects (departments, positions, etc.)
            - **HRP1001:** Contains organizational relationships (who reports to whom)
            
            **Common Tasks:**
            1. **Set Hierarchy Levels:** Define names for organizational levels (Division, Department, etc.)
            2. **Configure Processing:** Set batch sizes and error handling for large files
            3. **Backup Settings:** Save your configuration before making major changes
            
            **Tips:**
            - Start with default settings and adjust based on your data size
            - Use circular reference detection to catch organizational loops
            - Regular backups prevent configuration loss
            """)
    
    # Apply authentication wrapper
    auth.require_auth(foundation_admin_content)
