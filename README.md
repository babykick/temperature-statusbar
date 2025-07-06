# temperature-statusbar

一个 macOS 菜单栏温度监控工具，基于 Python 和 rumps 实现。可实时显示 CPU、GPU 温度及 kernel_task 进程的 CPU 占用率。

## 功能

- 菜单栏实时显示 CPU、GPU 温度
- 显示 kernel_task 进程的 CPU 占用率
- 每 5 秒自动刷新

## 安装

1. 安装依赖：

   ```bash
   pip install rumps
   ```

2. 需要使用 `powermetrics`，需确保 macOS 系统自带。

## 使用

1. 运行脚本前，建议赋予 `powermetrics` sudo 权限，避免频繁输入密码：

   ```bash
   sudo visudo
   # 添加如下内容（将 stephen 替换为你的用户名）：
   stephen ALL=(ALL) NOPASSWD: /usr/bin/powermetrics
   ```

2. 启动应用：

   ```bash
   python show_temp.py
   ```

3. 菜单栏会显示温度信息，如 `CPU:55.0°C | GPU:45.0°C | K:2.5%`

## 注意事项

- 需要在 macOS 上运行
- 需有管理员权限以获取温度数据

## License

MIT
