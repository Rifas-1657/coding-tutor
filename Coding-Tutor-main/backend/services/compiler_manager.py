"""
Compiler Manager - OBSOLETE
This module is no longer used. All code execution now happens in Docker containers.
The compilers/ folder and host-based compiler detection are not needed.

This file is kept for backward compatibility but should not be used for new code.
All execution should go through DockerSandboxRunner in sandbox_runner.py.
"""

import os
import platform

# NOTE: This class is obsolete. Use DockerSandboxRunner instead.
class CompilerManager:
    """
    OBSOLETE: This class is no longer used.
    All compilers are now available inside Docker containers.
    Use services.sandbox_runner.DockerSandboxRunner instead.
    """
    
    def __init__(self):
        self.base_path = self._get_base_path()
    
    def _get_base_path(self):
        """Determine the base path for compilers based on environment."""
        if hasattr(os, 'getenv') and os.getenv('RESOURCES_PATH'):
            return os.getenv('RESOURCES_PATH')
        # Fallback to relative path
        script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return os.path.join(script_dir, 'compilers')
    
    def get_gcc_path(self):
        """OBSOLETE: Use Docker sandbox instead."""
        if platform.system() == 'Windows':
            gcc_path = os.path.join(self.base_path, 'mingw', 'bin', 'gcc.exe')
            if os.path.exists(gcc_path):
                return gcc_path
        return 'gcc'
    
    def get_gpp_path(self):
        """OBSOLETE: Use Docker sandbox instead."""
        if platform.system() == 'Windows':
            gpp_path = os.path.join(self.base_path, 'mingw', 'bin', 'g++.exe')
            if os.path.exists(gpp_path):
                return gpp_path
        return 'g++'
    
    def get_python_path(self):
        """OBSOLETE: Use Docker sandbox instead."""
        if platform.system() == 'Windows':
            python_path = os.path.join(self.base_path, 'python', 'python.exe')
            if os.path.exists(python_path):
                return python_path
        return 'python3' if platform.system() != 'Windows' else 'python'
    
    def get_java_path(self):
        """OBSOLETE: Use Docker sandbox instead."""
        if platform.system() == 'Windows':
            javac_path = os.path.join(self.base_path, 'jdk', 'bin', 'javac.exe')
            if os.path.exists(javac_path):
                return javac_path
        return 'javac'
    
    def get_java_runtime_path(self):
        """OBSOLETE: Use Docker sandbox instead."""
        if platform.system() == 'Windows':
            java_path = os.path.join(self.base_path, 'jdk', 'bin', 'java.exe')
            if os.path.exists(java_path):
                return java_path
        return 'java'
