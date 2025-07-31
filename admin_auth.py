"""
Reusable Admin Authentication Module for SAP Migration Suite
Provides password protection for admin panels across all systems
"""

import streamlit as st
from typing import Optional, Dict, Any
import hashlib
from datetime import datetime, timedelta

class AdminAuth:
    """Handles admin authentication for different system modules"""
    
    def __init__(self, system_name: str, default_password: str = "admin123"):
        self.system_name = system_name.lower()
        self.default_password = default_password
        self.session_key = f'{self.system_name}_admin_authenticated'
        self.password_key = f'{self.system_name}_admin_password'
        
    def get_system_display_name(self) -> str:
        """Get formatted system name for display"""
        return {
            'employee': 'Employee Data Management',
            'foundation': 'Foundation Data Management', 
            'payroll': 'Payroll Data Management'
        }.get(self.system_name, self.system_name.title())
    
    def get_system_icon(self) -> str:
        """Get icon for the system"""
        return {
            'employee': '👥',
            'foundation': '🏢',
            'payroll': '💰'
        }.get(self.system_name, '⚙️')
    
    def get_system_color(self) -> str:
        """Get color scheme for the system"""
        return {
            'employee': 'linear-gradient(90deg, #1f2937 0%, #374151 100%)',
            'foundation': 'linear-gradient(90deg, #059669 0%, #10b981 100%)',
            'payroll': 'linear-gradient(90deg, #dc2626 0%, #ef4444 100%)'
        }.get(self.system_name, 'linear-gradient(90deg, #6b7280 0%, #9ca3af 100%)')
    
    def is_authenticated(self) -> bool:
        """Check if user is currently authenticated"""
        return st.session_state.get(self.session_key, False)
    
    def get_password(self) -> str:
        """Get the correct password from secrets or use default"""
        try:
            # Try to get from Streamlit secrets
            return st.secrets.get(self.password_key, self.default_password)
        except:
            # Try master admin password as fallback
            try:
                return st.secrets.get("master_admin_password", self.default_password)
            except:
                return self.default_password
    
    def authenticate(self, password: str) -> bool:
        """Authenticate with provided password"""
        correct_password = self.get_password()
        
        if password == correct_password:
            st.session_state[self.session_key] = True
            return True
        return False
    
    def logout(self) -> None:
        """Logout the current user"""
        st.session_state[self.session_key] = False
    
    def show_login_screen(self) -> bool:
        """Show login screen and handle authentication"""
        if self.is_authenticated():
            return True
        
        system_display = self.get_system_display_name()
        system_icon = self.get_system_icon()
        system_color = self.get_system_color()
        
        # Show login header
        st.markdown(f"""
        <div style="background: {system_color}; 
                    color: white; padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
            <h1 style="margin: 0; font-size: 2.5rem;">{system_icon} Admin Access Required</h1>
            <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
                Enter the admin password to access {system_display} Configuration Center
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Password input
        password_input = st.text_input(
            "🔑 **Admin Password:**",
            type="password",
            placeholder="Enter admin password...",
            help="Contact your system administrator if you don't have the password",
            key=f"{self.system_name}_password_input"
        )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("🔓 **Access Admin**", type="primary", key=f"{self.system_name}_login"):
                if self.authenticate(password_input):
                    st.success("✅ Access granted! Refreshing...")
                    st.rerun()
                else:
                    st.error("❌ Invalid password")
                    st.warning("Please check your password and try again")
        
        with col2:
            if st.button("🔄 **Clear**", key=f"{self.system_name}_clear"):
                st.rerun()
        
        with col3:
            st.info(f"💡 **Default password:** {self.default_password} (if not configured)")
        
        # Security notice
        st.markdown("---")
        st.markdown(f"""
        ### 🛡️ Security Notice
        
        **What this protects:** The {system_display} Configuration Center contains sensitive settings that control how your data is processed.
        
        **Why password protection:** 
        - Prevents accidental changes to critical mappings and configurations
        - Ensures only authorized users can modify system templates
        - Protects configuration integrity and data processing rules
        
        **For Administrators:**
        - Password can be configured in Streamlit secrets as `{self.password_key}`
        - Use a strong password in production environments
        - Regularly review who has admin access
        - Master admin password (`master_admin_password`) works for all systems
        """)
        
        return False
    
    def show_logout_sidebar(self) -> None:
        """Show logout option in sidebar for authenticated users"""
        if not self.is_authenticated():
            return
            
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"**🔐 {self.get_system_display_name()} Admin**")
        
        if st.sidebar.button(f"🚪 **Logout from {self.system_name.title()}**", help="Exit admin mode"):
            self.logout()
            st.success("✅ Logged out successfully")
            st.rerun()
        
        # Show current session info
        st.sidebar.caption("🟢 Admin access active")
        st.sidebar.caption("⚠️ Be careful with configuration changes")
    
    def require_auth(self, admin_function):
        """Decorator-like function to require authentication for admin functions"""
        if not self.show_login_screen():
            return  # Exit if not authenticated
        
        # Show logout option
        self.show_logout_sidebar()
        
        # Call the actual admin function
        admin_function()

# Helper functions for quick setup
def create_employee_admin() -> AdminAuth:
    """Create admin auth for employee system"""
    return AdminAuth("employee", "admin123")

def create_foundation_admin() -> AdminAuth:
    """Create admin auth for foundation system"""  
    return AdminAuth("foundation", "admin123")

def create_payroll_admin() -> AdminAuth:
    """Create admin auth for payroll system"""
    return AdminAuth("payroll", "admin123")

# Example usage functions
def protected_employee_admin():
    """Example of how to use admin protection for employee system"""
    auth = create_employee_admin()
    
    def employee_admin_content():
        st.markdown("### Employee Admin Content")
        st.write("This is the protected employee admin area")
        # Your actual employee admin code goes here
    
    auth.require_auth(employee_admin_content)

def protected_foundation_admin():
    """Example of how to use admin protection for foundation system"""
    auth = create_foundation_admin()
    
    def foundation_admin_content():
        st.markdown("### Foundation Admin Content")
        st.write("This is the protected foundation admin area")
        # Your actual foundation admin code goes here
    
    auth.require_auth(foundation_admin_content)

def protected_payroll_admin():
    """Example of how to use admin protection for payroll system"""
    auth = create_payroll_admin()
    
    def payroll_admin_content():
        st.markdown("### Payroll Admin Content") 
        st.write("This is the protected payroll admin area")
        # Your actual payroll admin code goes here
    
    auth.require_auth(payroll_admin_content)

# Advanced features
class SessionManager:
    """Manage admin sessions across multiple systems"""
    
    @staticmethod
    def get_active_admin_sessions() -> Dict[str, bool]:
        """Get all active admin sessions"""
        sessions = {}
        for system in ['employee', 'foundation', 'payroll']:
            sessions[system] = st.session_state.get(f'{system}_admin_authenticated', False)
        return sessions
    
    @staticmethod
    def logout_all_systems() -> None:
        """Logout from all admin systems"""
        for system in ['employee', 'foundation', 'payroll']:
            st.session_state[f'{system}_admin_authenticated'] = False
    
    @staticmethod
    def show_session_status() -> None:
        """Show status of all admin sessions in sidebar"""
        sessions = SessionManager.get_active_admin_sessions()
        active_count = sum(sessions.values())
        
        if active_count > 0:
            st.sidebar.markdown("---")
            st.sidebar.markdown("**🔐 Active Admin Sessions**")
            
            for system, is_active in sessions.items():
                icon = "🟢" if is_active else "⚪"
                st.sidebar.caption(f"{icon} {system.title()}")
            
            if active_count > 1:
                if st.sidebar.button("🚪 **Logout All Systems**"):
                    SessionManager.logout_all_systems()
                    st.success("✅ Logged out from all systems")
                    st.rerun()
