import os
import subprocess
import logging
from pathlib import Path, PureWindowsPath, PurePosixPath
from xdg.DesktopEntry import DesktopEntry
from typing import Dict, List, Optional, Any

# Configure logging
logger = logging.getLogger(__name__)

class WSLPathConverter:
    """Handles path conversion between Windows and WSL paths."""
    
    @staticmethod
    def windows_to_wsl(windows_path: str) -> str:
        """Convert Windows path to WSL path."""
        try:
            path = Path(windows_path)
            if path.is_absolute() and path.drive:
                # Convert absolute Windows path to WSL path
                drive_letter = path.drive[0].lower()
                wsl_path = PurePosixPath(f"/mnt/{drive_letter}")
                return str(wsl_path / PurePosixPath(*path.parts[1:]))
            return str(PurePosixPath(path))
        except (AttributeError, ValueError) as e:
            logger.error(f"Path conversion error for {windows_path}: {e}")
            return windows_path

class WSLCommandRunner:
    """Handles WSL command execution with proper error handling."""
    
    def __init__(self, machine: str, script_path: str):
        self.machine = machine
        self.script_path = WSLPathConverter.windows_to_wsl(script_path)
    
    def run_command(self, command: str, args: str = "", timeout: int = 30) -> str:
        """Execute a WSL command with proper error handling."""
        try:
            cmd = ['wsl.exe', '-d', self.machine, self.script_path, command]
            if args:
                cmd.extend(args.split())
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=True
            )
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            logger.error(f"WSL command timed out: {' '.join(cmd)}")
            return ""
        except subprocess.CalledProcessError as e:
            logger.error(f"WSL command failed: {e}\nStderr: {e.stderr}")
            return ""
        except Exception as e:
            logger.error(f"Unexpected error executing WSL command: {e}")
            return ""

class WSLApp:
    """Represents a WSL application from .desktop files."""
    
    def __init__(self, name: str, generic_name: str, cmd: str, gui: bool, icon: str):
        self.name = name
        self.generic_name = generic_name
        self.cmd = cmd
        self.gui = gui
        self.icon = icon
    
    @classmethod
    def from_dotdesktop(cls, app_def: str) -> Optional['WSLApp']:
        """Create a WSLApp from a .desktop file."""
        try:
            de = DesktopEntry(app_def)
            return cls(
                name=de.getName(),
                generic_name=de.getGenericName(),
                cmd=de.getExec(),
                gui=not de.getTerminal(),
                icon=de.getIcon()
            )
        except Exception as e:
            logger.error(f"Failed to parse .desktop file {app_def}: {e}")
            return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "name": self.name,
            "generic_name": self.generic_name,
            "cmd": self.cmd,
            "gui": self.gui,
            "icon": self.icon
        }

class WSLManager:
    """Main class for managing WSL operations."""
    
    def __init__(self, machine: str, script_path: str):
        self.machine = machine
        self.runner = WSLCommandRunner(machine, script_path)
    
    def get_themes(self) -> List[str]:
        """Get available themes from WSL distribution."""
        output = self.runner.run_command("listthemes")
        if not output:
            return []
        
        themes = []
        for theme in output.split(":theme:"):
            theme = theme.strip()
            if not theme or theme in ["\n", "\n\n", "/usr/share/themes"]:
                continue
            
            # Extract theme name from path
            theme = self._extract_theme_name(theme)
            if theme:
                themes.append(theme)
        
        return themes
    
    def _extract_theme_name(self, theme_path: str) -> str:
        """Extract theme name from path."""
        patterns = ["/usr/share/themes/", ".themes/"]
        
        for pattern in patterns:
            if pattern in theme_path:
                return theme_path[theme_path.index(pattern) + len(pattern):]
        
        return theme_path
    
    def get_apps(self) -> Dict[str, Dict[str, str]]:
        """Get GUI applications from WSL distribution."""
        output = self.runner.run_command("listapps")
        if not output:
            return {}
        
        apps = {}
        for app_path in output.splitlines():
            if not app_path or "screensaver" in app_path.lower():
                continue
            
            try:
                # Convert to Windows path for DesktopEntry
                windows_path = f"\\\\wsl$\\{self.machine}{app_path}"
                wsl_app = WSLApp.from_dotdesktop(windows_path)
                
                if wsl_app and wsl_app.gui:
                    apps[wsl_app.name] = {
                        "cmd": wsl_app.cmd,
                        "ico": wsl_app.icon
                    }
            except Exception as e:
                logger.debug(f"Skipping app {app_path}: {e}")
                continue
        
        return apps
    
    def export_variable(self, name: str, value: str, shell: str = "bash") -> bool:
        """Export environment variable to WSL distribution."""
        output = self.runner.run_command("export-v", f"{name} {value} {shell}")
        return bool(output)
    
    def set_gtk_scale(self, scale: float, shell: str = "bash") -> bool:
        """Set GDK scale factor."""
        return self.export_variable("GDK_SCALE", str(scale), shell)
    
    def set_qt_scale(self, scale: float, shell: str = "bash") -> bool:
        """Set QT scale factor."""
        return self.export_variable("QT_SCALE_FACTOR", str(scale), shell)
    
    def start_dbus(self) -> bool:
        """Start D-Bus service."""
        output = self.runner.run_command("dbus")
        return bool(output)
    
    def export_display(self, version: str, shell: str = "bash") -> bool:
        """Export display settings."""
        output = self.runner.run_command("export-d", f"{version} {shell}")
        return bool(output)
    
    def export_audio(self, version: str, shell: str = "bash") -> bool:
        """Export audio settings."""
        output = self.runner.run_command("export-a", f"{version} {shell}")
        return bool(output)
    
    def cleanup(self) -> bool:
        """Clean up WSL environment."""
        output = self.runner.run_command("cleanup")
        return bool(output)
    
    def get_profile(self, shell: str = "bash") -> str:
        """Get shell profile content."""
        return self.runner.run_command("profile", shell)

# Backward compatibility functions
def initialize_wsl_manager(machine: str, script_path: str) -> WSLManager:
    """Initialize the WSL manager (replaces global script variable)."""
    global script
    script = script_path
    return WSLManager(machine, script_path)

# Legacy functions for backward compatibility
def pat_con(path: str) -> str:
    return WSLPathConverter.windows_to_wsl(path)

def get_themes(machine: str) -> List[str]:
    manager = WSLManager(machine, script)
    return manager.get_themes()

def get_apps(machine: str, logger=None) -> Dict[str, Dict[str, str]]:
    manager = WSLManager(machine, script)
    return manager.get_apps()

def get_apps_old(machine: str) -> Dict[str, Dict[str, str]]:
    """Legacy function - consider removing if not needed."""
    logger.warning("get_apps_old is deprecated. Use get_apps instead.")
    # Implementation can be added if needed
    return {}

def export_v(machine: str, name: str, value: str, shell: str = "bash") -> None:
    manager = WSLManager(machine, script)
    manager.export_variable(name, value, shell)

def gtk(machine: str, scale: float, shell: str = "bash") -> None:
    manager = WSLManager(machine, script)
    manager.set_gtk_scale(scale, shell)

def qt(machine: str, scale: float, shell: str = "bash") -> None:
    manager = WSLManager(machine, script)
    manager.set_qt_scale(scale, shell)

def dbus(machine: str) -> None:
    manager = WSLManager(machine, script)
    manager.start_dbus()

def export(machine: str, version: str, shell: str = "bash") -> None:
    manager = WSLManager(machine, script)
    manager.export_display(version, shell)

def export_audio(machine: str, version: str, shell: str = "bash") -> None:
    manager = WSLManager(machine, script)
    manager.export_audio(version, shell)

def cleanup(machine: str) -> None:
    manager = WSLManager(machine, script)
    manager.cleanup()

def profile(machine: str, shell: str = "bash") -> str:
    manager = WSLManager(machine, script)
    return manager.get_profile(shell)
