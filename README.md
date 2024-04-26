# large_dram_data_capture_fat

## Usage

- 主页面

![main.png](docs%2Fmain.png)

- 操作步骤

1. 拉取项目代码
   ```shell
   git clone git@gitlab.com:qlink21/large_dram_data_capture_fat.git
   ```
2. 编译驱动
   ```
   cd driver/AFHBA404-2.4
   make
   sudo ./scripts/install-hotplug
   ```
3. [编译客户端](#Build-for-source)

## Build for source

- python3+

```shell
// 安装依赖
pip install -r requirements.txt

// 编译可执行程序
pyinstaller main.spec
