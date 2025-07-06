import rumps
import subprocess
import re


class TemperatureApp(rumps.App):
    def __init__(self):
        super().__init__("温度: 获取中..." )
        # 设置定时器，每 5 秒更新一次
        rumps.Timer(self.update_temperature, 5).start()
        self.update_temperature(None)  # 立即更新一次

    def get_temperatures(self):
        try:
            # 执行 powermetrics 命令获取 SMC 传感器数据
            result = subprocess.run(
                ["sudo", "powermetrics", "--samplers", "smc", "-i1", "-n1"],
                capture_output=True,
                text=True
            )
            output = result.stdout

            # 使用正则表达式提取 CPU 和 GPU 温度
            cpu_temp = re.search(r"CPU die temperature: (\d+\.\d+) C", output)
            gpu_temp = re.search(r"GPU die temperature: (\d+\.\d+) C", output)

            cpu_temp_value = float(cpu_temp.group(1)) if cpu_temp else None
            gpu_temp_value = float(gpu_temp.group(1)) if gpu_temp else None

            return {"CPU": cpu_temp_value, "GPU": gpu_temp_value}
        except Exception as e:
            print(f"错误: {e}")
            return None

    def get_kernel_task_cpu(self):
        """获取 kernel_task 进程的 CPU 使用率"""
        try:
            result = subprocess.run(
                ["sudo", "powermetrics", "--samplers", "tasks", "-n1"],
                capture_output=True,
                text=True
            )
            output = result.stdout
            
            # 查找 kernel_task 进程行
            for line in output.split('\n'):
                if 'kernel_task' in line and line.strip().startswith('kernel_task'):
                    # 解析格式: kernel_task  0  80.51  0.00  1.99  0.00  779.91  78.01
                    parts = line.split()
                    if len(parts) >= 3:
                        # 第三列是 CPU ms/s 值
                        cpu_value = float(parts[2])
                        return cpu_value
            return None
        except Exception as e:
            return None

    def update_temperature(self, _):
        try:
            temps = self.get_temperatures()
            kernel_cpu = self.get_kernel_task_cpu()
            
            # 构建显示文本
            display_parts = []
            
            if temps and temps['CPU']:
                display_parts.append(f"CPU:{temps['CPU']}°C")
            
            if temps and temps['GPU']:
                display_parts.append(f"GPU:{temps['GPU']}°C")
                
            if kernel_cpu is not None:
                # display_parts.append(f"Kernel:{kernel_cpu}ms/s")
                display_parts.append(f"Kernel:{kernel_cpu / 10:.1f}%")
            
            if display_parts:
                self.title = " | ".join(display_parts)
            else:
                self.title = "温度: 无法获取"
                
        except Exception as e:
            self.title = "温度: 错误"
            print(f"错误: {e}")


if __name__ == "__main__":
    app = TemperatureApp()
    app.run()