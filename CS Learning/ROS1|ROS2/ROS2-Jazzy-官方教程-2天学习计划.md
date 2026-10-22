# ROS 2 Jazzy 官方教程：2 天高强度学习计划

> 依据 ROS 2 Jazzy 官方 Tutorials 与官方 First Steps learning path 制定。
>
> 官方入口：[ROS 2 Jazzy Tutorials](https://docs.ros.org/en/jazzy/Tutorials.html)
>
> 配套知识点整理：[ROS2-Jazzy-官方知识点整理.md](ROS2-Jazzy-官方知识点整理.md)

两天不可能逐页精通官方 Tutorials 的全部内容。本计划采用“核心链路优先”：先完成官方推荐的基础通信闭环，再补齐 Python、工作空间、接口、Launch、Action、TF2、测试、URDF 和 RViz2 的最小可用知识。本文档假设使用 Ubuntu 24.04 LTS 原生系统安装 ROS 2 Jazzy。

## 1. 两天后的目标

完成后你应该能够：

- 解释 Node、Topic、Service、Action、Parameter、Interface 和 Launch。
- 使用 `ros2` CLI 查看和调试 ROS Graph。
- 创建工作空间和 Python 包。
- 编写 Python Publisher、Subscriber、Service Server 和 Client。
- 使用 YAML 参数文件配置节点。
- 用 Launch 同时启动多个节点。
- 理解 Action 的 Goal、Feedback、Result 和 Cancel。
- 用 TF2 查看坐标系变换。
- 编写基础 Python 测试。
- 看懂最小 URDF，并理解 RViz2 的 Fixed Frame、RobotModel 和 TF。
- 录制、查看和回放 Bag。
- 完成一个可构建、可启动、可测试的小型 ROS2 项目。

两天内暂不要求精通：完整 C++ API、Nav2、MoveIt、DDS 实现、组件组合、自定义 RViz 插件和所有 Advanced 教程。

## 2. Ubuntu 环境要求与安装

### 2.1 系统要求

- Ubuntu 24.04 LTS，建议使用 64 位桌面版。
- 当前用户具有 `sudo` 权限。
- 网络可以访问 Ubuntu 和 ROS 软件源。
- 至少 8 GB 内存，建议 20 GB 以上可用磁盘空间。
- 不要在同一个终端混用 ROS1 和 ROS2 环境。

Jazzy 的 Ubuntu deb 包面向 Ubuntu 24.04。本文档不覆盖 Ubuntu 22.04、Windows、macOS、Docker 或源码编译安装。如果你的 Ubuntu 版本不是 24.04，请先切换到 Ubuntu 24.04，再执行本文档命令。

官方安装页：[Ubuntu (deb packages)](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html)

### 2.2 安装 locale 和软件源

```bash
sudo apt update
sudo apt install -y locales software-properties-common curl ca-certificates
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
sudo add-apt-repository universe
```

添加 ROS 2 软件源：

```bash
sudo curl -L https://github.com/ros/rosdistro/raw/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | \
  sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

### 2.3 安装 ROS 2 Jazzy

```bash
sudo apt update
sudo apt install -y ros-jazzy-desktop ros-dev-tools
sudo apt install -y python3-colcon-common-extensions python3-rosdep
```

桌面版包含本计划需要的 `turtlesim`、RViz2 和基础工具。安装完成后配置每次打开终端自动加载 ROS2：

```bash
echo 'source /opt/ros/jazzy/setup.bash' >> ~/.bashrc
source ~/.bashrc
```

初始化依赖工具：

```bash
sudo rosdep init
rosdep update
```

如果 `sudo rosdep init` 提示已经初始化，不要重复执行，直接运行 `rosdep update`。

### 2.4 Ubuntu 安装验收

```bash
lsb_release -a
echo "$UBUNTU_CODENAME"
uname -m
df -h /
free -h
locale
ros2 --help
ros2 doctor
ros2 pkg list | grep turtlesim
```

验收标准：Ubuntu 版本为 24.04 LTS，代号为 `noble`；`ros2 --help`、`ros2 doctor` 和 `turtlesim` 查询均正常。

## 3. 时间与学习方法

每天建议投入 8-10 小时，至少 60% 用于终端和代码实践。

```text
阅读理解       30%
跟随官方教程   30%
独立重写改造   30%
复盘和排错     10%
```

规则：

1. 先读官方教程的目标和概念，再执行命令。
2. 命令成功后，关闭教程，独立重打一遍关键命令。
3. 每个模块必须有可验证产出：终端输出、运行节点、代码或测试结果。
4. 每完成一个大模块就提交一次 Git。
5. 遇到错误先保存完整命令和第一条真实错误，再排查环境、依赖、节点、话题、QoS 和 TF。
6. 不要在同一个终端混用 ROS1 和 ROS2 环境。

## 3. 官方教程取舍

| 官方分组 | 两天安排 | 结果 |
| --- | --- | --- |
| First Steps | 必须完成 | 掌握官方推荐基础路径 |
| Beginner: CLI Tools | 必须完成 | 能观察和操作 ROS Graph |
| Beginner: Client Libraries | Python 必须，C++ 选读 | 能创建包和编写节点 |
| Intermediate: rosdep、Action、Launch | 必须完成核心页面 | 能管理依赖、动作和启动流程 |
| Intermediate: tf2 | 完成 Python 最小实践 | 能理解坐标系和 TF 排错 |
| Intermediate: Testing | 完成 Python 基础测试 | 具备最基本工程能力 |
| Intermediate: URDF、RViz | 阅读并完成最小可视化 | 能理解机器人模型和显示链路 |
| Composition、Pluginlib、C++ 模板 | 延后 | 两天内投入产出较低 |
| Advanced、Simulators | 延后 | 按项目方向继续学习 |

官方 First Steps 的顺序是：概念 -> 安装和 turtlesim -> 节点/话题/服务/参数/Action -> 日志 -> Launch -> Bag。

官方页面：[First steps with ROS](https://docs.ros.org/en/jazzy/First-Steps.html)

---

# 第一天：基础通信与 Python 开发

## 第一天目标

当天结束时，你必须能启动 `turtlesim`，使用 CLI 观察节点和话题，创建 Python 包，完成 Publisher/Subscriber、Service/Client，并用参数配置节点。

## 08:30-09:00 Ubuntu 环境复核

安装步骤见前面的“Ubuntu 环境要求与安装”。本时段只做快速复核：

```bash
source /opt/ros/jazzy/setup.bash
lsb_release -a
echo "$UBUNTU_CODENAME"
ros2 --help
ros2 doctor
ros2 pkg list | grep turtlesim
python3 --version
```

验收：

- Ubuntu 24.04 LTS，代号为 `noble`。
- `ros2 --help` 和 `ros2 doctor` 能执行。
- 可以找到 `turtlesim` 包。

如果失败，先检查 `/etc/apt/sources.list.d/ros2.list`、`sudo apt update` 和 `ros-jazzy-desktop` 是否安装成功，不要继续创建工作空间。

## 09:00-10:00 基础概念

官方参考：

- [About ROS](https://docs.ros.org/en/jazzy/Concepts.html)
- [Nodes](https://docs.ros.org/en/jazzy/Concepts/Basic/About-Nodes.html)
- [Topics](https://docs.ros.org/en/jazzy/Concepts/Basic/About-Topics.html)
- [Services](https://docs.ros.org/en/jazzy/Concepts/Basic/About-Services.html)
- [Actions](https://docs.ros.org/en/jazzy/Concepts/Basic/About-Actions.html)
- [Parameters](https://docs.ros.org/en/jazzy/Concepts/Basic/About-Parameters.html)

| 概念 | 模式 | 典型用途 |
| --- | --- | --- |
| Node | 进程或逻辑单元 | 驱动、算法、控制 |
| Topic | 异步发布/订阅 | 图像、激光、速度、状态 |
| Service | 请求/响应 | 清空地图、查询、切换模式 |
| Action | 目标/反馈/结果，可取消 | 导航、机械臂运动、长任务 |
| Parameter | 节点配置 | 频率、阈值、坐标、模式 |
| Interface | 数据契约 | `msg`、`srv`、`action` |

自测：

1. 为什么图像适合 Topic 而不是 Service？
2. 为什么导航目标适合 Action 而不是 Service？
3. 参数和高频 Topic 的边界是什么？
4. 多个节点如何通过 Topic 解耦？

## 10:00-11:30 turtlesim 与 CLI

官方教程：

- [Configuring ROS 2 environment](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Configuring-ROS2-Environment.html)
- [Using turtlesim, ros2, and rqt](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim.html)

终端 A：

```bash
source /opt/ros/jazzy/setup.bash
ros2 run turtlesim turtlesim_node
```

终端 B：

```bash
source /opt/ros/jazzy/setup.bash
ros2 run turtlesim turtle_teleop_key
```

终端 C：

```bash
source /opt/ros/jazzy/setup.bash
ros2 node list
ros2 topic list
ros2 topic list -t
ros2 service list
ros2 action list
ros2 param list
```

必须完成：

```bash
ros2 node info /turtlesim
ros2 topic type /turtle1/cmd_vel
ros2 interface show geometry_msgs/msg/Twist
ros2 topic echo /turtle1/cmd_vel
ros2 topic hz /turtle1/pose
ros2 service type /clear
ros2 interface show turtlesim/srv/Spawn
ros2 param list /turtlesim
ros2 param get /turtlesim background_r
ros2 param set /turtlesim background_r 100
```

命令行发布速度：

```bash
ros2 topic pub --rate 2 /turtle1/cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 1.0}, angular: {z: 0.5}}"
```

验收：

- 能从节点找到发布和订阅的话题。
- 能从话题找到消息类型。
- 能用 CLI 发布速度。
- 能查询服务和参数。

产出：`day1-turtlesim-commands.md`，记录命令、用途和结果。

## 11:30-12:00 复盘

不看资料回答：当前节点有哪些？`/turtle1/cmd_vel` 的发布者和订阅者是谁？`/turtle1/pose` 的消息类型是什么？哪些操作用 Topic，哪些用 Service？

## 12:00-13:00 午餐和环境恢复

重新开终端后执行：

```bash
source /opt/ros/jazzy/setup.bash
```

## 13:00-14:30 工作空间、colcon 和包

官方教程：

- [Using colcon](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html)
- [Creating a workspace](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html)
- [Creating a package](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html)

创建工作空间：

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
source install/setup.bash
```

创建 Python 包：

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python --license Apache-2.0 py_pubsub
cd ~/ros2_ws
colcon build --packages-select py_pubsub --symlink-install
source install/setup.bash
```

必须理解：

| 文件/目录 | 作用 |
| --- | --- |
| `src` | 源码包 |
| `build` | 构建中间文件 |
| `install` | 安装结果和环境脚本 |
| `log` | 构建日志 |
| `package.xml` | 包信息和依赖 |
| `setup.py` | Python 安装和可执行入口 |
| `test` | 测试代码 |

验收：能解释 `src`、`build`、`install`、`log`，并能创建、构建和查找自己的包。

## 14:30-16:00 Python Publisher 和 Subscriber

官方教程：[Writing a simple publisher and subscriber (Python)](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html)

目标：

```text
publisher -- /chatter --> subscriber
```

核心 API：

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class PublisherNode(Node):
    def __init__(self):
        super().__init__('publisher_node')
        self.declare_parameter('period', 0.5)
        self.publisher = self.create_publisher(String, 'chatter', 10)
        period = self.get_parameter('period').value
        self.timer = self.create_timer(period, self.publish)
        self.count = 0

    def publish(self):
        message = String()
        message.data = f'hello {self.count}'
        self.publisher.publish(message)
        self.get_logger().info(message.data)
        self.count += 1


def main(args=None):
    rclpy.init(args=args)
    node = PublisherNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

订阅者必须掌握：

```python
self.subscription = self.create_subscription(
    String,
    'chatter',
    self.listener_callback,
    10,
)

def listener_callback(self, message):
    self.get_logger().info(f'received: {message.data}')
```

在 `setup.py` 注册：

```python
entry_points={
    'console_scripts': [
        'talker = py_pubsub.publisher_node:main',
        'listener = py_pubsub.subscriber_node:main',
    ],
},
```

运行和验证：

```bash
cd ~/ros2_ws
colcon build --packages-select py_pubsub --symlink-install
source install/setup.bash
ros2 run py_pubsub talker
```

另开终端：

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run py_pubsub listener
ros2 topic info /chatter
ros2 topic hz /chatter
ros2 topic echo /chatter
```

独立改造三项：

1. 消息包含递增序号和时间戳。
2. 发布周期通过参数配置。
3. 订阅者每 10 条消息输出一次统计。

## 16:00-17:00 Python Service 和 Client

官方教程：[Writing a simple service and client (Python)](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Service-And-Client.html)

先使用 `example_interfaces/srv/AddTwoInts`，再改造为计数器服务。

```bash
ros2 service list
ros2 service type /add_two_ints
ros2 interface show example_interfaces/srv/AddTwoInts
```

必须理解：

- 客户端发送 request，服务端返回 response。
- 客户端应等待服务可用。
- 服务回调不应长时间阻塞。
- 长任务应改为 Action。

改造任务：请求一个整数，服务端增加计数器并返回当前值；再增加清零服务或清零参数。

验收：能解释 Topic、Service、Action 的选型区别，并能从 CLI 找到服务类型。

## 17:00-18:00 参数与日志

官方教程：

- [Using parameters in a class (Python)](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-Python.html)
- [Understanding parameters](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters.html)
- [Using rqt_console](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Using-Rqt-Console/Using-Rqt-Console.html)

```bash
ros2 param list /publisher_node
ros2 param get /publisher_node period
ros2 param set /publisher_node period 1.0
```

`config/params.yaml`：

```yaml
publisher_node:
  ros__parameters:
    period: 0.5
```

加载参数：

```bash
ros2 run py_pubsub talker --ros-args --params-file config/params.yaml
```

日志等级：

```python
self.get_logger().debug('debug')
self.get_logger().info('normal status')
self.get_logger().warn('recoverable issue')
self.get_logger().error('operation failed')
```

验收：能不改代码地改变节点行为，能区分参数配置和高频 Topic 数据。

## 18:00-18:30 第一天测验

不看教程完成：

1. 创建 Python 包。
2. 写每秒发布计数器的节点。
3. 写订阅节点并统计接收数量。
4. 用参数改变发布周期。
5. 用服务将计数器清零。
6. 用 `ros2 topic`、`ros2 service`、`ros2 param` 验证。

少于 4 项完成时，第二天先补齐 Publisher/Subscriber、Service/Client 和参数，不要进入扩展内容。

第一天产出：

```text
~/ros2_ws/src/py_pubsub/
├── package.xml
├── setup.py
├── py_pubsub/
│   ├── publisher_node.py
│   ├── subscriber_node.py
│   └── counter_service.py
├── config/params.yaml
└── README.md
```

---

# 第二天：Launch、Action、TF2、测试与模型

## 第二天目标

使用 Launch 启动第一天系统，理解 Action，完成 rosdep、TF2、测试、URDF/RViz 和 Bag 的最小实践，最后完成综合项目。

## 08:30-09:30 Launch

官方教程：

- [Launching nodes](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Launching-Multiple-Nodes/Launching-Multiple-Nodes.html)
- [Launch main](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Launch-Main.html)
- [Creating a launch file](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Creating-Launch-Files.html)
- [Integrating launch files](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Launch-system.html)

`launch/demo.launch.py`：

```python
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='py_pubsub',
            executable='talker',
            name='publisher_node',
            output='screen',
        ),
        Node(
            package='py_pubsub',
            executable='listener',
            name='subscriber_node',
            output='screen',
        ),
    ])
```

运行：

```bash
ros2 launch py_pubsub demo.launch.py
```

必须掌握 `Node`、`name`、`namespace`、`parameters`、`remappings`、`output`。

改造：加载 YAML 参数，并把 `chatter` 重映射到 `demo/chatter`。

验收：一条 Launch 命令启动至少两个节点，关闭 Launch 后相关节点退出。

## 09:30-10:45 Action

官方教程：

- [Understanding actions](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html)
- [Creating an action](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Creating-an-Action.html)
- [Python Action server/client](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Writing-an-Action-Server-Client/Py.html)

```text
Client -- Goal ------> Server
Client <-- Feedback -- Server
Client <-- Result ---- Server
Client -- Cancel ----> Server
```

先观察已有 Action：

```bash
ros2 action list
ros2 action info /turtle1/rotate_absolute
ros2 interface show turtlesim/action/RotateAbsolute
```

完成官方 Python Action server/client 示例，再做三项改造：修改 Goal、在 Feedback 中增加完成百分比、测试 Cancel 和非法目标。

验收：能说出 Goal、Feedback、Result、Cancel 的作用，并解释为什么长时间运动任务应该用 Action。

## 10:45-11:00 休息

复盘：Topic 是持续数据流；Service 是短请求/响应；Action 是可反馈、可取消的长任务；Launch 是多节点编排。

## 11:00-12:00 rosdep 和依赖

官方教程：[Managing Dependencies with rosdep](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Rosdep.html)

```bash
cd ~/ros2_ws
rosdep update
rosdep install --from-paths src --ignore-src -r -y
```

检查 `package.xml`：补齐运行时依赖，删除未使用依赖，确认新机器可以根据源码重建环境。

验收：能解释 `package.xml`、`rosdep` 和 `colcon` 的关系。

## 12:00-13:00 午餐和系统图复盘

画出项目架构：

```text
parameter file -> publisher -- topic --> subscriber
                                  ^          |
                                  |          v
                              service ---- report

                         launch starts all nodes
```

回答：哪些是 Topic？哪些是 Service？如果操作持续 10 秒如何改成 Action？如何用 Bag 复现错误？

## 13:00-14:30 TF2 和时间

官方教程：

- [Introducing tf2](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Introduction-To-Tf2.html)
- [Static broadcaster Python](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Writing-A-Tf2-Static-Broadcaster-Py.html)
- [Broadcaster Python](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Writing-A-Tf2-Broadcaster-Py.html)
- [Listener Python](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Writing-A-Tf2-Listener-Py.html)
- [Debugging tf2](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Debugging-Tf2-Problems.html)

典型树：

```text
map
└── odom
    └── base_link
        ├── laser
        └── camera_link
```

完成官方 Python static broadcaster 和 listener，建立 `world -> robot` 变换。

```bash
ros2 run tf2_tools view_frames
ros2 run tf2_ros tf2_echo world robot
ros2 topic echo /tf_static
```

排错顺序：`frame_id` 拼写、Fixed Frame、TF 树连通性、时间戳、重复发布、`use_sim_time`。

验收：能解释 `map`、`odom`、`base_link` 的常见职责，并能查看两坐标系之间的变换。

## 14:30-15:30 测试

官方教程：

- [Testing](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Testing/Testing-Main.html)
- [CLI testing](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Testing/CLI.html)
- [Python tests](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Testing/Python.html)

为第一天项目添加：

- 一个纯 Python 函数测试。
- 一个参数默认值测试。
- 一个消息处理函数测试。

```bash
cd ~/ros2_ws
colcon test --packages-select py_pubsub
colcon test-result --verbose
```

先测试自己的业务逻辑，不要一开始测试 ROS 中间件本身。

## 15:30-16:30 URDF 和 RViz2

官方教程：

- [URDF](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/URDF-Main.html)
- [Visual robot model](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/Building-a-Visual-Robot-Model-from-Scratch.html)
- [Xacro](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/Using-Xacro-to-Clean-Up-a-URDF-File.html)
- [RViz](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/RViz/RViz-Main.html)

必须理解：`link` 是刚体，`joint` 是连接关系，`visual` 是显示模型，`collision` 是碰撞模型，`inertial` 是物理属性，Xacro 用于模块化生成 URDF，`robot_state_publisher` 用 URDF 和关节状态发布 TF。

最小结构：

```xml
<robot name="simple_robot">
  <link name="base_link" />
  <link name="sensor_link" />
  <joint name="sensor_joint" type="fixed">
    <parent link="base_link" />
    <child link="sensor_link" />
    <origin xyz="0.2 0 0.15" rpy="0 0 0" />
  </joint>
</robot>
```

RViz2 排错顺序：Fixed Frame -> RobotModel -> TF 连通性 -> `frame_id` -> 时间 -> QoS。

两天内只要求看懂和运行最小模型，不要求完成复杂材质、碰撞和物理仿真。

## 16:30-17:00 Bag

官方教程：[Recording and playing back data](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.html)

```bash
ros2 bag record /chatter /parameter_events /tf /tf_static
ros2 bag info <bag_directory>
ros2 bag play <bag_directory>
```

记录代码版本、发行版、Launch 命令、参数文件和录制话题，确保实验可复现。

## 17:00-18:30 综合项目：机器人状态监控系统

项目结构：

```text
state_publisher -- /robot_state --> state_monitor
       ^                                |
       |                                v
       +------- reset service ------ status report

parameter file + launch + TF2 + tests + rosbag
```

最低功能：

1. 状态发布节点：发布名称、计数器、电量或温度；频率由参数控制。
2. 监控节点：订阅状态，检查阈值，用日志输出正常和异常状态。
3. 重置服务：将计数器归零，客户端处理服务不可用情况。
4. Launch：一条命令启动所有节点，加载 YAML，支持重映射。
5. TF2：发布 `world -> robot` 静态变换，并可用 `tf2_echo` 查询。
6. 测试：测试阈值判断、重置逻辑和参数默认值。
7. Bag：录制状态话题，回放后监控节点重新工作。

推荐目录：

```text
ros2_two_day_demo/
├── package.xml
├── setup.py
├── resource/ros2_two_day_demo
├── ros2_two_day_demo/
│   ├── __init__.py
│   ├── state_publisher.py
│   ├── state_monitor.py
│   ├── reset_server.py
│   └── static_tf_broadcaster.py
├── launch/demo.launch.py
├── config/params.yaml
├── test/test_state_logic.py
└── README.md
```

最终运行：

```bash
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
ros2 launch ros2_two_day_demo demo.launch.py
```

另开终端验证：

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 node list
ros2 topic list
ros2 topic echo /robot_state
ros2 service list
ros2 param list
ros2 run tf2_ros tf2_echo world robot
```

验收清单：

- [ ] 一条 Launch 命令启动全部节点。
- [ ] `ros2 node list` 显示预期节点。
- [ ] `ros2 topic echo` 显示持续数据。
- [ ] YAML 参数改变了运行行为。
- [ ] 服务可以重置状态。
- [ ] TF2 变换可以查询。
- [ ] `colcon test` 通过。
- [ ] Bag 可以录制和回放。
- [ ] README 能让别人从零运行。

---

## 4. 两天内延后的官方内容

以下内容仍然重要，但放到两天后：

- C++ Publisher/Subscriber、Service/Client、Action。
- 自定义 `msg`、`srv` 和 Action 接口。
- Pluginlib、Composable Node、Composition。
- Node Interfaces Template Class。
- Launch substitutions、event handlers 和大型项目管理。
- TF2 时间旅行、四元数和 MessageFilter。
- C++ GTest、launch_testing 和 Build Farm。
- 自定义 RViz Display/Panel。
- Fast DDS Discovery Server、RMW、内存分配器和 ros2 tracing。
- Webots 和高级仿真。

## 5. 常见排错流程

### 命令不存在

```bash
source /opt/ros/jazzy/setup.bash
which ros2
ros2 --help
```

### 找不到包或可执行文件

```bash
colcon list
colcon build --packages-select <package_name>
source install/setup.bash
ros2 pkg list | grep <package_name>
ros2 pkg executables <package_name>
```

Python 包重点检查 `setup.py` 的 `entry_points`、入口函数、包目录和构建后的 `source`。

### 话题没有数据

```bash
ros2 topic list
ros2 topic type /topic_name
ros2 topic info /topic_name -v
ros2 topic echo /topic_name
ros2 topic hz /topic_name
```

依次检查节点、名称、发布者、消息类型、QoS、命名空间和重映射。

### RViz2 不显示

```bash
ros2 topic echo /tf
ros2 run tf2_tools view_frames
```

优先检查 Fixed Frame、`frame_id`、TF 连通性、时间戳和 QoS。

### 依赖错误

```bash
sudo apt update
sudo apt install -y python3-rosdep python3-colcon-common-extensions
rosdep update
rosdep install --from-paths src --ignore-src -r -y
```

构建失败时优先看第一条真实错误，不要只看最后一屏的连带错误。

### Ubuntu 软件源或密钥错误

检查 Ubuntu 版本和 ROS 软件源：

```bash
cat /etc/os-release
cat /etc/apt/sources.list.d/ros2.list
sudo apt update
```

确认 `UBUNTU_CODENAME` 为 `noble`。不要把 `jammy`、`focal` 等其他发行版代号写进 Jazzy 软件源。

### 权限和图形界面问题

- `apt`、`rosdep init` 等系统操作使用 `sudo`。
- `colcon build` 和 `ros2 run` 尽量不要使用 `sudo`，否则可能导致工作空间文件归 root 用户所有。
- RViz2 无法打开时，先确认当前使用的是 Ubuntu 桌面会话，并检查显卡驱动和 `DISPLAY` 环境变量。
- SSH 远程运行图形程序时，需要配置 X11 转发或使用本地桌面终端；两天学习建议直接在 Ubuntu 桌面本机运行。

## 6. 高频命令速查

```bash
# 环境和构建
source /opt/ros/jazzy/setup.bash
ros2 doctor
colcon build --symlink-install
colcon test
colcon test-result --verbose

# 节点
ros2 node list
ros2 node info /node_name
ros2 run <package> <executable>

# 话题
ros2 topic list -t
ros2 topic info /topic -v
ros2 topic echo /topic
ros2 topic hz /topic
ros2 topic pub /topic <type> '<value>'

# 服务和 Action
ros2 service list
ros2 service type /service
ros2 service call /service <type> '<request>'
ros2 action list
ros2 action info /action

# 参数、Launch、TF、Bag
ros2 param list
ros2 param get /node parameter
ros2 param set /node parameter value
ros2 launch <package> <launch_file>
ros2 run tf2_tools view_frames
ros2 run tf2_ros tf2_echo <parent> <child>
ros2 bag record /topic
ros2 bag info <bag_directory>
ros2 bag play <bag_directory>
```

## 7. 两天后的 7 天延伸路线

- 第 3 天：C++ Publisher/Subscriber、Service/Client、自定义接口。
- 第 4 天：Launch substitutions、event handlers、大型项目组织。
- 第 5 天：TF2 时间戳、四元数、MessageFilter 和 C++ API。
- 第 6 天：URDF、Xacro、robot_state_publisher、RViz Marker。
- 第 7 天：测试、集成测试、rosdep、Bag 可复现调试。

之后按方向选择：移动机器人学习 Nav2 和 SLAM；机械臂学习 MoveIt；视觉学习 Image、CameraInfo、TF 和检测；系统工程学习 DDS、实时性、组件和 CI。

## 8. 最终验收

### 基础认知

- [ ] 能解释 Node、Topic、Service、Action、Parameter、Interface。
- [ ] 能使用 CLI 查看它们。

### 编程

- [ ] 能创建 Python 包。
- [ ] 能写 Publisher/Subscriber。
- [ ] 能写 Service/Client。
- [ ] 能加载 YAML 参数。
- [ ] 能正确输出日志。

### 系统集成

- [ ] 能写 Python Launch。
- [ ] 能运行 rosdep。
- [ ] 能录制和回放 Bag。
- [ ] 能查看 TF2。
- [ ] 能运行基础测试。
- [ ] 能看懂最小 URDF 和 RViz2 配置。

### 工程交付

- [ ] 有 README、构建命令、启动命令和参数说明。
- [ ] 有接口说明和排错记录。
- [ ] 有 Git 提交。

两天的核心成果不是“看完所有页面”，而是完成这条可运行链路：

```text
环境 -> turtlesim/CLI -> Python 包 -> Topic -> Service
     -> Parameter/日志 -> Launch -> Action/TF2/测试
     -> URDF/RViz -> Bag -> 综合项目
```
