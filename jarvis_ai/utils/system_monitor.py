"""
System Monitor for Jarvis AI
Monitors CPU, RAM, and system resources
"""

import os
from typing import Dict, Optional


class SystemMonitor:
    """
    Monitors system resources and provides status reports.
    """
    
    def __init__(self):
        """Initialize system monitor."""
        self._psutil_available = False
        self._initialize()
        
    def _initialize(self):
        """Initialize monitoring libraries."""
        try:
            import psutil
            self._psutil_available = True
            print("[MONITOR] psutil initialized")
        except ImportError:
            print("[WARNING] psutil not installed. System monitoring disabled.")
            
    def get_cpu_usage(self) -> Optional[float]:
        """
        Get current CPU usage percentage.
        
        Returns:
            CPU usage percentage or None if unavailable
        """
        if not self._psutil_available:
            return None
            
        try:
            import psutil
            return psutil.cpu_percent(interval=1)
        except Exception as e:
            print(f"[ERROR] Failed to get CPU usage: {e}")
            return None
            
    def get_ram_usage(self) -> Optional[Dict[str, any]]:
        """
        Get RAM usage statistics.
        
        Returns:
            Dictionary with percent, used, total or None if unavailable
        """
        if not self._psutil_available:
            return None
            
        try:
            import psutil
            memory = psutil.virtual_memory()
            return {
                'percent': memory.percent,
                'used': memory.used / (1024 ** 3),  # GB
                'total': memory.total / (1024 ** 3),  # GB
                'available': memory.available / (1024 ** 3)  # GB
            }
        except Exception as e:
            print(f"[ERROR] Failed to get RAM usage: {e}")
            return None
            
    def get_disk_usage(self, path: str = "/") -> Optional[Dict[str, any]]:
        """
        Get disk usage statistics.
        
        Args:
            path: Path to check (default: root)
            
        Returns:
            Dictionary with percent, used, total or None if unavailable
        """
        if not self._psutil_available:
            return None
            
        try:
            import psutil
            disk = psutil.disk_usage(path)
            return {
                'percent': disk.percent,
                'used': disk.used / (1024 ** 3),  # GB
                'total': disk.total / (1024 ** 3),  # GB
                'free': disk.free / (1024 ** 3)  # GB
            }
        except Exception as e:
            print(f"[ERROR] Failed to get disk usage: {e}")
            return None
            
    def get_network_stats(self) -> Optional[Dict[str, any]]:
        """
        Get network I/O statistics.
        
        Returns:
            Dictionary with bytes_sent, bytes_recv or None if unavailable
        """
        if not self._psutil_available:
            return None
            
        try:
            import psutil
            net = psutil.net_io_counters()
            return {
                'bytes_sent': net.bytes_sent,
                'bytes_recv': net.bytes_recv,
                'packets_sent': net.packets_sent,
                'packets_recv': net.packets_recv
            }
        except Exception as e:
            print(f"[ERROR] Failed to get network stats: {e}")
            return None
            
    def get_status_report(self) -> str:
        """
        Generate a human-readable status report.
        
        Returns:
            Formatted status string
        """
        if not self._psutil_available:
            return "System monitoring not available"
            
        cpu = self.get_cpu_usage()
        ram = self.get_ram_usage()
        disk = self.get_disk_usage()
        
        report_parts = []
        
        if cpu is not None:
            report_parts.append(f"CPU: {cpu}%")
            
        if ram:
            report_parts.append(f"RAM: {ram['percent']}% ({ram['used']:.1f}GB / {ram['total']:.1f}GB)")
            
        if disk:
            report_parts.append(f"Disk: {disk['percent']}% ({disk['free']:.1f}GB free)")
            
        # Check for critical conditions
        warnings = []
        if cpu and cpu > 80:
            warnings.append("High CPU usage!")
        if ram and ram['percent'] > 90:
            warnings.append("Critical RAM usage!")
        if disk and disk['percent'] > 90:
            warnings.append("Low disk space!")
            
        report = ", ".join(report_parts)
        if warnings:
            report += " WARNING: " + " ".join(warnings)
            
        return report
        
    def is_healthy(self) -> bool:
        """
        Check if system is operating within normal parameters.
        
        Returns:
            True if all metrics are within acceptable ranges
        """
        cpu = self.get_cpu_usage()
        ram = self.get_ram_usage()
        disk = self.get_disk_usage()
        
        if cpu and cpu > 95:
            return False
        if ram and ram['percent'] > 95:
            return False
        if disk and disk['percent'] > 95:
            return False
            
        return True
