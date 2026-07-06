"""
System Health Agent — CPU, RAM, GPU, Disk, Battery, Network, Temperature
"""
import psutil
import platform
from typing import Any, Dict
from loguru import logger

try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

from agents.base import BaseAgent


class SystemAgent(BaseAgent):
    name = "system"
    refresh_interval = 120  # 2 min

    async def fetch_data(self) -> Dict[str, Any]:
        data = {}

        # CPU
        data["cpu_percent"] = psutil.cpu_percent(interval=1)
        data["cpu_freq"] = psutil.cpu_freq().current if psutil.cpu_freq() else None
        data["cpu_cores"] = psutil.cpu_count()

        # RAM
        mem = psutil.virtual_memory()
        data["ram_total_gb"] = round(mem.total / (1024**3), 1)
        data["ram_used_gb"] = round(mem.used / (1024**3), 1)
        data["ram_percent"] = mem.percent

        # Disk
        disks = []
        for part in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(part.mountpoint)
                disks.append({
                    "device": part.device,
                    "mountpoint": part.mountpoint,
                    "total_gb": round(usage.total / (1024**3), 1),
                    "used_gb": round(usage.used / (1024**3), 1),
                    "percent": usage.percent,
                })
            except Exception:
                pass
        data["disks"] = disks

        # Battery
        bat = psutil.sensors_battery()
        if bat:
            data["battery_percent"] = bat.percent
            data["battery_plugged"] = bat.power_plugged
            data["battery_secs_left"] = bat.secsleft

        # Network
        net = psutil.net_io_counters()
        data["net_bytes_sent"] = net.bytes_sent
        data["net_bytes_recv"] = net.bytes_recv

        # GPU (if available)
        if GPU_AVAILABLE:
            try:
                gpus = GPUtil.getGPUs()
                data["gpus"] = [
                    {
                        "name": g.name,
                        "load": g.load * 100,
                        "memory_used": g.memoryUsed,
                        "memory_total": g.memoryTotal,
                        "temperature": g.temperature,
                    }
                    for g in gpus
                ]
            except Exception:
                data["gpus"] = []

        # Temperature (if available on Windows)
        try:
            temps = psutil.sensors_temperatures()
            data["temperatures"] = {k: [t.current for t in v] for k, v in temps.items()}
        except Exception:
            data["temperatures"] = {}

        return data

    async def analyze(self, data: Dict[str, Any]) -> str:
        alerts = []

        if data.get("cpu_percent", 0) > 85:
            alerts.append(f"⚠️ CPU usage critical: {data['cpu_percent']}%")
        if data.get("ram_percent", 0) > 85:
            alerts.append(f"⚠️ RAM usage critical: {data['ram_percent']}%")

        battery = data.get("battery_percent")
        if battery and battery < 20 and not data.get("battery_plugged"):
            alerts.append(f"🔋 Battery low: {battery}%")

        for disk in data.get("disks", []):
            if disk["percent"] > 90:
                alerts.append(f"💾 Disk {disk['device']} almost full: {disk['percent']}%")

        if not alerts:
            return (
                f"✅ System healthy | CPU: {data.get('cpu_percent', 'N/A')}% | "
                f"RAM: {data.get('ram_percent', 'N/A')}% | "
                f"Battery: {data.get('battery_percent', 'N/A')}%"
            )

        return "SYSTEM ALERTS:\n" + "\n".join(alerts)
