import psutil
from typing import List, Tuple
import pandas as pd
import subprocess
import io


class CPUMonitor:
    def __init__(self):
        pass

    def get_per_core_usage(self) -> List[float]:
        """
        Returns the CPU usage percentages for each core
        """
        return psutil.cpu_percent(percpu=True)

    def get_per_core_frequency(self) -> List[float]:
        """
        Returns the CPU frequency for each core
        """
        freqs = psutil.cpu_freq(percpu=True)
        return [f.current for f in freqs]
    
    def get_cpu_temperature(self):
        temps = psutil.sensors_temperatures()
        return temps
        # for name, entries in temps.items():
        #     for entry in entries:
        #         print(f"{name}: {entry.current}°C")


class MemoryMonitor:
    def __init__(self):
        pass

    def get_memory_usage(self) -> Tuple[float, float]:
        """
        Returns the memory usage: (used, total) in bytes
        """
        mem_info = psutil.virtual_memory()
        return mem_info.used, mem_info.total

    def get_swap_usage(self) -> Tuple[float, float]:
        """
        Returns the swap usage: (used, total) in bytes
        """
        swap_info = psutil.swap_memory()
        return swap_info.used, swap_info.total


class GPUMonitor:
    def __init__(self) -> None:
        pass

    def get_everything_df(self) -> pd.DataFrame:
        """
        Fetches all GPU data in CSV format
        """
        try:
            cmd = ['nvidia-smi', '--query-gpu=index,name,temperature.gpu,utilization.gpu,utilization.memory,memory.total,memory.free,memory.used,driver_version,pstate,pcie.link.gen.max,pcie.link.gen.current,timestamp', '--format=csv']
            output = subprocess.check_output(cmd)
            print(output)
            return pd.read_csv(io.StringIO(output.decode()))
        except Exception as e:
            print(f"An error occurred: {e}")
            return pd.DataFrame()


class HardDriveMonitor:
    def __init__(self, device_name: str) -> None:
        pass

    def get_hard_drive_bandwidth(self) -> Tuple[float, float]:
        pass

    def get_hard_drive_iops(self) -> Tuple[float, float]:
        pass

    def get_hard_drive_latency(self) -> Tuple[float, float]:
        pass

    def get_hard_drive_smart(self) -> Tuple[float, float]:
        pass


class NetworkMonitor:
    def __init__(self, if_name: str) -> None:
        pass

    def get_listen_ports(self) -> List[int]:
        pass

    def get_network_bandwidth(self) -> Tuple[float, float]:
        pass

    def get_network_received(self) -> Tuple[float, float]:
        pass

    def get_network_sent(self) -> Tuple[float, float]:
        pass


if __name__ == "__main__":
    monitor = GPUMonitor()
    print(monitor.get_everything_df())
    cpu_monitor = CPUMonitor()
    print(cpu_monitor.get_cpu_temperature())
