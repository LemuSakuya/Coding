# ROS1｜ROS2 学习文档

> 目标：从零开始理解机器人操作系统的核心概念，能够独立创建节点、设计通信接口、使用 TF、参数、Launch、Bag 和仿真工具，并完成 ROS1 与 ROS2 之间的迁移。
>
> 建议：新项目优先学习 ROS2。ROS1 适合用于维护旧项目、阅读现有机器人代码和理解 ROS 的历史设计。

---

## 1. 学习路线总览

### 1.1 推荐顺序

1. Linux、Git、Python/C++ 基础
2. ROS 的节点、话题、服务、动作、参数、消息
3. ROS2 的工作空间、包、`colcon`、Launch 和 QoS
4. TF2、URDF、RViz2、仿真和传感器数据
5. 控制、导航、定位、机械臂或视觉方向
6. ROS1 基础和 ROS1/ROS2 迁移
7. 综合项目：移动机器人或机械臂

### 1.2 阶段目标

| 阶段 | 重点 | 结果 |
| --- | --- | --- |
| 入门 | Linux、ROS CLI、节点和话题 | 能运行并观察一个 ROS 系统 |
| 基础开发 | Python/C++ 节点、消息、服务、动作 | 能写出可复用 ROS2 包 |
| 系统理解 | QoS、TF2、参数、Launch、Bag | 能组织多节点系统 |
| 机器人应用 | URDF、RViz2、仿真、传感器 | 能搭建机器人模型和虚拟环境 |
| 工程实践 | 测试、日志、容器、部署、迁移 | 能维护真实项目 |

### 1.3 每周实践建议

- 先运行官方示例，再不看答案重写一遍。
- 每学一个通信机制，都同时完成“发布端 + 使用端 + 命令行验证”。
- 每个阶段保留一个 Git 仓库，并写清楚启动命令、依赖和预期结果。
- 调试时先确认图、节点、话题和 QoS，再检查业务代码。

---

## 2. ROS 是什么

ROS（Robot Operating System）不是传统意义上单一的操作系统，而是一套用于构建机器人软件的通信中间件、工具、消息定义、开发库和社区生态。

一个机器人系统通常由多个相互协作的进程组成：

```text
相机驱动节点 ── image_raw ──> 视觉节点 ── detection ──> 任务节点
激光雷达节点 ── scan ───────> 定位节点 ── pose ──────> 导航节点
控制器节点   <── cmd_vel ──── 导航节点
```

ROS 的核心思想是：

- 将复杂系统拆成职责单一的节点。
- 使用标准化消息描述数据。
- 通过话题、服务和动作完成不同类型的通信。
- 使用工具查看、记录、回放和可视化系统行为。
- 让算法、硬件驱动和应用逻辑尽量解耦。

---

## 3. 核心概念

### 3.1 节点 Node

节点是 ROS 系统中执行具体工作的进程或逻辑单元。例如：

- 相机驱动节点：采集图像。
- 激光雷达节点：发布扫描数据。
- 定位节点：估计机器人位姿。
- 导航节点：规划路径并生成速度指令。

一个节点应尽量只承担一类清晰职责，避免把所有逻辑写进一个“大节点”。

### 3.2 话题 Topic

话题用于连续、异步的数据流通信，采用发布/订阅模型。

适用场景：

- 传感器数据：图像、点云、激光扫描。
- 状态数据：里程计、电池状态、机器人位姿。
- 控制指令：速度、关节目标。

特点：

- 发布者和订阅者可以互不直接知道对方。
- 一个发布者可以有多个订阅者。
- 适合高频数据，但不保证每条消息都被处理。
- ROS2 中需要额外关注 QoS 是否兼容。

### 3.3 服务 Service

服务是同步的请求/响应通信。

适用场景：

- 清空地图。
- 切换模式。
- 查询或修改一次性状态。
- 触发某个短操作。

服务不适合长时间任务。若任务可能持续数秒或更久，并且需要反馈和取消，应使用 Action。

### 3.4 动作 Action

动作适合可持续、可反馈、可取消的任务，例如导航到目标点、机械臂移动到指定姿态。

一个动作通常包含：

- Goal：任务目标。
- Feedback：执行过程中的反馈。
- Result：任务完成后的结果。

### 3.5 参数 Parameter

参数是节点的配置项，例如速度限制、传感器坐标、控制增益和文件路径。

建议：

- 参数用于配置，不用于高频数据传输。
- 给参数提供合理默认值和类型。
- 把参数集中放在 YAML 文件中。
- 记录每次实验使用的参数版本。

### 3.6 接口 Interface

ROS 中的接口包括：

- `msg`：话题消息。
- `srv`：服务请求和响应。
- `action`：动作目标、反馈和结果。

接口是不同节点之间的契约。接口一旦公开，应尽量保持向后兼容，避免随意修改字段含义。

### 3.7 工作空间 Workspace

工作空间是源码包、构建结果和安装结果的组织目录。ROS2 常见结构：

```text
ros2_ws/
├── src/        # 源码包
├── build/      # 构建中间文件
├── install/    # 安装结果和环境脚本
└── log/        # 构建日志
```

通常只把 `src/` 纳入 Git，`build/`、`install/` 和 `log/` 加入 `.gitignore`。

### 3.8 ROS Graph

ROS Graph 是节点及其通信关系组成的图。理解系统时要回答：

1. 当前有哪些节点？
2. 每个节点发布和订阅了什么？
3. 话题使用什么消息类型？
4. 发布者和订阅者的 QoS 是否匹配？
5. 坐标系是否连通？

---

## 4. ROS1 与 ROS2 的主要区别

| 方面 | ROS1 | ROS2 |
| --- | --- | --- |
| 通信基础 | ROS Master + ROS 网络发现 | DDS/RTPS 分布式发现 |
| 命令行构建 | `catkin_make`、`catkin_tools` | `colcon` |
| Python 客户端 | `rospy` | `rclpy` |
| C++ 客户端 | `roscpp` | `rclcpp` |
| 话题 API | `rostopic` | `ros2 topic` |
| 服务 API | `rosservice` | `ros2 service` |
| 参数 | 参数服务器 | 节点私有参数 |
| Launch | XML 为主 | Python、XML、YAML 均可，Python 最灵活 |
| 实时性 | 支持有限 | 更适合实时和嵌入式场景 |
| 生命周期 | 普通节点启动即运行 | 可使用 Lifecycle Node 管理状态 |
| QoS | 选项较少 | 可配置可靠性、历史、深度、持久性等 |
| 安全 | 主要依赖网络环境 | 可使用 DDS Security、SROS2 |
| Windows/嵌入式 | 支持有限 | 跨平台和嵌入式支持更好 |
| 生命周期状态 | 通常由进程管理 | 可显式配置未配置、非激活、激活等状态 |

### 4.1 最重要的思维变化

ROS1 中很多问题由 Master 和参数服务器集中处理；ROS2 更强调分布式系统，因此必须关注：

- DDS Domain ID 是否一致。
- 节点是否使用相容的 QoS。
- 网络是否允许 DDS 的发现和数据通信。
- 参数属于哪个节点。
- 节点的生命周期和启动顺序。

### 4.2 ROS1 的状态

ROS1 的经典发行版已经进入维护结束阶段。学习 ROS1 的主要价值是维护既有项目、阅读旧论文代码和迁移系统。新项目应优先采用 ROS2，并根据目标平台选择仍在支持周期内的 ROS2 发行版。

---

## 5. 环境安装与基础命令

### 5.1 环境选择

建议使用：

- Ubuntu Linux 原生环境。
- Docker 或虚拟机用于隔离实验环境。
- ROS2 的稳定发行版，而不是随意选择尚未验证的开发版本。

安装前应确认 ROS2 发行版与 Ubuntu 版本的官方兼容矩阵。不同发行版的安装命令和包名可能不同，因此不要混用不同教程的命令。

### 5.2 加载环境

ROS2 安装后，先加载环境：

```bash
source /opt/ros/<ros2_distro>/setup.bash
```

为了每次打开终端自动加载，可以加入 shell 配置文件：

```bash
echo "source /opt/ros/<ros2_distro>/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

工作空间构建后，还要加载工作空间环境：

```bash
source ~/ros2_ws/install/setup.bash
```

### 5.3 ROS2 常用 CLI

```bash
ros2 --help
ros2 doctor
ros2 node list
ros2 node info /node_name
ros2 topic list
ros2 topic list -t
ros2 topic info /topic_name -v
ros2 topic echo /topic_name
ros2 topic hz /topic_name
ros2 topic type /topic_name
ros2 interface show <package>/msg/<Message>
ros2 service list
ros2 service type /service_name
ros2 action list
ros2 action info /action_name
ros2 param list
ros2 param get /node_name parameter_name
ros2 run <package> <executable>
ros2 launch <package> <launch_file>
```

### 5.4 ROS1 常用 CLI

```bash
roscore
rosnode list
rosnode info /node_name
rostopic list
rostopic type /topic_name
rostopic info /topic_name
rostopic echo /topic_name
rostopic hz /topic_name
rosservice list
rosservice type /service_name
rosservice call /service_name <args>
rosrun <package> <node>
roslaunch <package> <launch_file>.launch
rosparam list
rosparam get /parameter_name
rqt_graph
rviz
```

### 5.5 命令行排错顺序

当“节点没有数据”时，按以下顺序检查：

```text
进程是否启动？
  -> 节点是否在 ROS Graph 中？
    -> 话题名称是否正确？
      -> 消息类型是否正确？
        -> 是否存在发布者？
          -> ROS2 中 QoS 是否兼容？
            -> 数据内容和时间戳是否有效？
```

---

## 6. ROS2 工作空间与包

### 6.1 创建工作空间

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
source install/setup.bash
```

### 6.2 创建 Python 包

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python ros2_learning_py \
  --dependencies rclpy std_msgs geometry_msgs
```

常见结构：

```text
ros2_learning_py/
├── package.xml
├── setup.py
├── setup.cfg
├── resource/ros2_learning_py
├── ros2_learning_py/
│   ├── __init__.py
│   ├── publisher_node.py
│   └── subscriber_node.py
└── test/
```

### 6.3 创建 C++ 包

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_cmake ros2_learning_cpp \
  --dependencies rclcpp std_msgs geometry_msgs
```

### 6.4 构建与选择性构建

```bash
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash

# 只构建指定包
colcon build --packages-select ros2_learning_py --symlink-install

# 先检查依赖
rosdep install --from-paths src --ignore-src -r -y
```

`--symlink-install` 便于 Python 代码修改后快速测试。构建失败时优先阅读第一个真正的错误，而不是最后一屏的连带错误。

---

## 7. 第一个 ROS2 Python 节点

### 7.1 发布者

文件：`ros2_learning_py/publisher_node.py`

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.declare_parameter('publish_period', 0.5)
        self.publisher = self.create_publisher(String, 'chatter', 10)
        self.count = 0
        period = self.get_parameter('publish_period').value
        self.timer = self.create_timer(period, self.publish_message)

    def publish_message(self):
        message = String()
        message.data = f'hello ros2: {self.count}'
        self.publisher.publish(message)
        self.get_logger().info(message.data)
        self.count += 1


def main(args=None):
    rclpy.init(args=args)
    node = MinimalPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

在 `setup.py` 的 `entry_points` 中注册：

```python
entry_points={
    'console_scripts': [
        'publisher = ros2_learning_py.publisher_node:main',
    ],
},
```

构建并运行：

```bash
cd ~/ros2_ws
colcon build --packages-select ros2_learning_py --symlink-install
source install/setup.bash
ros2 run ros2_learning_py publisher
```

### 7.2 订阅者

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'chatter',
            self.listener_callback,
            10,
        )

    def listener_callback(self, message):
        self.get_logger().info(f'received: {message.data}')


def main(args=None):
    rclpy.init(args=args)
    node = MinimalSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### 7.3 关键 API 解释

- `rclpy.init()`：初始化 ROS2 客户端库。
- `Node`：节点基类。
- `create_publisher()`：创建发布者。
- `create_subscription()`：创建订阅者。
- `create_timer()`：创建定时器。
- `rclpy.spin()`：进入事件循环，处理回调。
- `get_logger()`：输出 ROS 日志。
- `destroy_node()`：释放节点资源。

---

## 8. 话题、消息与 QoS

### 8.1 消息类型

常用标准消息：

| 类型 | 用途 |
| --- | --- |
| `std_msgs/msg/String` | 简单文本 |
| `std_msgs/msg/Bool` | 布尔状态 |
| `sensor_msgs/msg/Image` | 相机图像 |
| `sensor_msgs/msg/LaserScan` | 2D 激光扫描 |
| `sensor_msgs/msg/PointCloud2` | 点云 |
| `geometry_msgs/msg/Twist` | 线速度和角速度 |
| `geometry_msgs/msg/PoseStamped` | 带时间戳和坐标系的位姿 |
| `nav_msgs/msg/Odometry` | 里程计 |
| `nav_msgs/msg/Path` | 路径 |
| `tf2_msgs/msg/TFMessage` | TF 变换 |

对于机器人数据，优先使用带 `Header` 的消息，以便记录 `stamp` 和 `frame_id`。

### 8.2 自定义消息

`msg/RobotStatus.msg`：

```text
std_msgs/Header header
string robot_name
float32 battery_percent
bool emergency_stop
```

在 `package.xml` 中加入接口依赖，并使用 `rosidl_generate_interfaces()` 生成语言绑定。自定义接口包最好与业务节点包分离，便于多个包复用。

### 8.3 QoS 的核心参数

- Reliability：`reliable` 或 `best effort`。
- Durability：`volatile` 或 `transient local`。
- History：保留最后 N 条，或保留全部。
- Depth：队列深度。
- Deadline、Lifespan、Liveliness：更高级的时序和存活约束。

典型选择：

| 数据 | 常见 QoS |
| --- | --- |
| 激光、图像等高频传感器 | `best effort`，较小队列 |
| 控制和关键状态 | `reliable` |
| 静态地图或一次性配置 | `transient local` |
| 高频数据且允许丢帧 | `keep last` |

“话题存在但收不到数据”在 ROS2 中经常是 QoS 不兼容。使用以下命令查看详细 QoS：

```bash
ros2 topic info /scan -v
```

### 8.4 QoS 设计原则

- 不要默认把所有话题都设为 `reliable`。
- 传感器生产者和消费者要明确协商 QoS。
- 在代码中使用 `qos_profile_sensor_data` 等已有配置时，确认它是否适合当前设备。
- 对重要话题在 README 中记录消息类型和 QoS 约定。

---

## 9. 服务、动作和参数

### 9.1 服务调用

查看服务：

```bash
ros2 service list
ros2 service type /clear_map
ros2 interface show std_srvs/srv/Empty
```

调用空请求服务：

```bash
ros2 service call /clear_map std_srvs/srv/Empty
```

服务回调应快速完成。如果需要等待硬件、规划路径或执行运动，不要在服务回调中长时间阻塞，改用 Action 或异步任务。

### 9.2 动作调用

```bash
ros2 action list
ros2 action info /navigate_to_pose
ros2 interface show nav2_msgs/action/NavigateToPose
```

动作客户端需要处理：

- 是否成功发送 Goal。
- 是否收到反馈。
- 是否被拒绝。
- 是否取消。
- Result 的状态和具体内容。

### 9.3 参数命令

```bash
ros2 param list
ros2 param describe /minimal_publisher use_sim_time
ros2 param get /minimal_publisher use_sim_time
ros2 param set /minimal_publisher use_sim_time false
```

YAML 示例：

```yaml
minimal_publisher:
  ros__parameters:
    publish_period: 0.5
    message_prefix: "hello"
```

参数文件通过 Launch 加载，而不是依赖开发者手动在多个终端输入命令。

---

## 10. Launch 系统

### 10.1 为什么使用 Launch

真实系统通常需要同时启动驱动、算法、控制器、可视化和日志节点。Launch 可以统一管理：

- 节点启动。
- 参数文件。
- 命名空间。
- 重映射。
- 条件启动。
- 模拟时间。
- 环境变量。

### 10.2 Python Launch 示例

```python
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ros2_learning_py',
            executable='publisher',
            name='publisher',
            output='screen',
            parameters=[{'publish_period': 0.5}],
            remappings=[('chatter', 'demo/chatter')],
        ),
    ])
```

运行：

```bash
ros2 launch ros2_learning_py demo.launch.py
```

### 10.3 Launch 设计建议

- 启动文件只负责编排，不要把业务算法写进 Launch。
- 使用参数、命名空间和重映射提高复用性。
- 给每个重要节点设置明确的 `name`。
- 仿真时统一设置 `use_sim_time: true`。
- 把真实硬件和仿真硬件的差异收敛在参数或 Launch 中。

---

## 11. TF2 与坐标系

### 11.1 TF2 是什么

TF2 管理机器人各坐标系之间随时间变化的空间变换。例如：

```text
map
└── odom
    └── base_link
        ├── laser
        └── camera_link
```

常见坐标系：

- `map`：全局地图坐标系，通常由定位系统维护。
- `odom`：连续但可能漂移的里程计坐标系。
- `base_link`：机器人主体坐标系。
- `base_footprint`：机器人投影到地面的坐标系。
- `laser`、`camera_link`：传感器坐标系。

### 11.2 常见 TF 错误

- `frame_id` 拼写不一致。
- TF 树断裂。
- 时间戳过旧或使用了错误的时钟。
- 多个节点同时发布同一条动态变换。
- 静态传感器变换没有发布。
- 把 `map -> base_link` 和 `odom -> base_link` 都交给同一节点发布。

### 11.3 检查命令

```bash
ros2 run tf2_tools view_frames
ros2 run tf2_ros tf2_echo map base_link
ros2 topic echo /tf
ros2 topic echo /tf_static
```

### 11.4 时间和坐标系原则

传感器消息的 `header.stamp` 和 `header.frame_id` 同样重要。算法接收数据前，应确认：

1. 时间戳来自正确的时钟。
2. 所需坐标系存在。
3. 在消息时间点可以查询对应 TF。
4. 坐标变换方向和单位正确。

---

## 12. URDF、RViz2 与仿真

### 12.1 URDF

URDF 用 XML 描述机器人的 link 和 joint：

```xml
<robot name="simple_robot">
  <link name="base_link" />
  <link name="laser_link" />
  <joint name="laser_joint" type="fixed">
    <parent link="base_link" />
    <child link="laser_link" />
    <origin xyz="0.2 0 0.15" rpy="0 0 0" />
  </joint>
</robot>
```

大型模型建议使用 Xacro，以支持宏、参数和模块化结构。

### 12.2 RViz2

RViz2 用于可视化：

- TF 坐标系。
- LaserScan。
- PointCloud2。
- Image。
- Map。
- RobotModel。
- Path 和 Pose。

排查 RViz2 不显示数据时，检查：

- `Fixed Frame` 是否存在。
- 话题名称和消息类型是否正确。
- QoS 是否匹配。
- 消息中的 `frame_id` 是否能连接到 Fixed Frame。
- 时间是否正常。

### 12.3 仿真工具

常见组合包括 Gazebo/新 Gazebo、机器人描述、控制器和导航栈。仿真中的关键配置包括：

- 仿真时钟：`use_sim_time`。
- 机器人模型和传感器插件。
- 控制器接口。
- 碰撞模型与视觉模型。
- 传感器噪声。
- TF 和坐标系命名。

仿真结果只能作为软件验证，不能完全替代真实硬件测试。尤其要关注延迟、噪声、摩擦、电机饱和和通信丢包。

---

## 13. ROS1 基础开发

### 13.1 ROS1 工作空间

```bash
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```

### 13.2 ROS1 Python 发布者

```python
#!/usr/bin/env python3
import rospy
from std_msgs.msg import String


def main():
    rospy.init_node('minimal_publisher')
    publisher = rospy.Publisher('chatter', String, queue_size=10)
    rate = rospy.Rate(2)
    count = 0

    while not rospy.is_shutdown():
        message = f'hello ros1: {count}'
        publisher.publish(message)
        rospy.loginfo(message)
        count += 1
        rate.sleep()


if __name__ == '__main__':
    main()
```

### 13.3 ROS1 与 ROS2 代码差异

| 任务 | ROS1 | ROS2 |
| --- | --- | --- |
| 初始化 | `rospy.init_node()` | `rclpy.init()` |
| 节点 | `rospy` 全局接口 | `Node` 对象 |
| 循环 | `rospy.Rate` | `create_timer` + `spin` |
| 日志 | `rospy.loginfo` | `node.get_logger().info` |
| 构建 | `catkin_make` | `colcon build` |
| 启动 | `roslaunch` | `ros2 launch` |
| 运行 | `rosrun` | `ros2 run` |
| 参数 | 全局参数服务器 | 节点参数 |

---

## 14. ROS1 到 ROS2 迁移

### 14.1 迁移顺序

建议按以下层次迁移：

1. 消息、服务和动作接口。
2. 独立工具库和纯算法代码。
3. 硬件驱动。
4. 普通节点。
5. Launch 和参数。
6. TF、控制器和导航集成。
7. 部署、监控和测试。

先迁移接口和基础库，可以减少后续节点迁移中的不确定性。

### 14.2 常见迁移映射

```text
catkin_make        -> colcon build
roscore            -> 通常不再需要 ROS Master
rospy              -> rclpy
roscpp             -> rclcpp
roslaunch          -> ros2 launch
rosrun             -> ros2 run
rostopic           -> ros2 topic
rosservice         -> ros2 service
rosparam           -> ros2 param
dynamic_reconfigure -> 参数回调或专用配置接口
nodelet            -> component/composable node
```

### 14.3 迁移时不能只做字符串替换

以下内容必须重新设计：

- ROS2 QoS。
- 参数声明和参数类型。
- Launch 参数传递。
- 生命周期节点。
- Executor、Callback Group 和线程模型。
- 时间源和 `use_sim_time`。
- ROS1 中依赖 Master 行为的代码。
- ROS1 nodelet 到 ROS2 component 的进程内组合方式。

### 14.4 迁移检查清单

- 所有话题、服务和动作都明确记录接口类型。
- 传感器话题 QoS 与驱动一致。
- 参数都有声明和默认值。
- 节点启动顺序不依赖隐式延迟。
- TF 树在真实时间和仿真时间下都可用。
- Launch 可通过参数切换真实设备、仿真和录包回放。
- Bag 回放可以重现关键问题。
- 关键节点有单元测试或集成测试。

---

## 15. 常见机器人功能栈

### 15.1 移动机器人

典型数据流：

```text
传感器驱动
  -> /scan, /odom, /camera/image
  -> 定位/建图
  -> /map, TF map->odom
  -> 导航规划
  -> /cmd_vel
  -> 底盘控制器
```

需要掌握：

- 里程计和 TF。
- 激光或视觉传感器。
- SLAM 与定位。
- 全局规划和局部控制。
- 代价地图。
- 速度限制和安全停止。

ROS2 中通常使用 Nav2 生态，具体版本和插件需匹配所使用的 ROS2 发行版。

### 15.2 机械臂

需要掌握：

- URDF/Xacro。
- 关节状态和控制器。
- 正向/逆向运动学。
- 碰撞检测。
- 轨迹规划。
- MoveIt 生态。

机械臂系统尤其要注意：关节限位、速度/加速度限制、控制周期、急停和真实硬件保护。

### 15.3 视觉

常见数据：

- `Image`：原始图像。
- `CameraInfo`：相机内参。
- 深度图和点云。
- 检测结果、跟踪结果和目标位姿。

必须区分：

- 图像像素坐标。
- 相机坐标系。
- 机器人坐标系。
- 世界或地图坐标系。

---

## 16. rosbag、日志与可复现性

### 16.1 ROS2 录制与回放

```bash
ros2 bag record /scan /odom /tf /tf_static
ros2 bag info <bag_directory>
ros2 bag play <bag_directory>
```

录包时记录最小但完整的输入集合，并保存：

- ROS2 发行版。
- 软件 commit。
- 参数文件。
- 传感器配置。
- 录制时间和场景说明。

### 16.2 日志等级

常见等级：`DEBUG`、`INFO`、`WARN`、`ERROR`、`FATAL`。

好的日志应包含：

- 发生了什么。
- 相关对象或话题。
- 关键数值。
- 是否可以恢复。
- 下一步应检查什么。

避免在高频回调中无节制打印日志，否则会影响实时性和性能。

### 16.3 可复现运行

一个实验至少应该能通过以下信息复现：

```text
代码版本 + ROS 发行版 + 依赖版本 + 参数文件 + Launch 命令 + 输入 Bag/硬件配置
```

---

## 17. 测试与工程实践

### 17.1 测试层次

1. 单元测试：测试纯函数、数学计算和数据转换。
2. 节点测试：测试参数、发布、订阅、服务和动作。
3. 集成测试：启动多个节点，验证通信和状态转换。
4. 仿真测试：在固定世界和固定输入下验证行为。
5. 硬件测试：低速、限位、急停和故障恢复。

### 17.2 代码质量

- 节点只做编排，算法尽量放在可测试的普通类或函数中。
- 明确单位：米、弧度、秒，避免变量名含糊。
- 对输入消息做空值、时间戳、坐标系和范围检查。
- 对外发布的接口写清楚字段含义和单位。
- 避免用全局变量保存可变系统状态。
- 对控制系统设置超时、限幅和安全停止。

### 17.3 Git 目录建议

```text
robot_project/
├── src/
├── config/
├── launch/
├── urdf/
├── worlds/
├── scripts/
├── test/
├── README.md
└── .gitignore
```

---

## 18. 高频问题排查

### 18.1 `ros2: command not found`

原因通常是没有加载 ROS 环境：

```bash
source /opt/ros/<ros2_distro>/setup.bash
```

如果命令仍不存在，检查安装路径、发行版名称和 shell 配置。

### 18.2 `ros2 run` 找不到包或可执行文件

依次检查：

```bash
colcon list
colcon build --packages-select <package>
source install/setup.bash
ros2 pkg executables <package>
```

Python 包还要检查 `setup.py` 的 `entry_points` 和脚本的可执行入口。

### 18.3 话题有名称但没有数据

```bash
ros2 topic info /topic_name -v
ros2 topic type /topic_name
ros2 topic echo /topic_name
```

检查发布者数量、消息类型、QoS、命名空间和重映射。

### 18.4 RViz2 报 TF 错误

检查 Fixed Frame、`frame_id`、TF 树和时间戳。不要通过随意修改 Fixed Frame 掩盖 TF 树断裂。

### 18.5 仿真机器人不动

检查：

- 控制器是否加载并激活。
- 关节名称是否一致。
- 命令话题名称是否正确。
- 时间是否使用仿真时钟。
- 传感器插件是否发布数据。
- 速度指令是否被安全节点或限幅器过滤。

### 18.6 多机通信失败

检查：

- 两台机器的 ROS2 Domain ID。
- 网络接口和防火墙。
- 主机名解析。
- DDS 实现是否一致或已验证互通。
- 容器是否使用正确的网络模式。
- 是否存在跨网段组播限制。

---

## 19. 综合练习项目

### 练习 1：话题通信

要求：

- 创建一个发布温度的节点。
- 创建一个订阅节点，计算滑动平均值。
- 使用参数配置发布周期和窗口大小。
- 用 Launch 同时启动两个节点。
- 用 Bag 录制并回放数据。

### 练习 2：服务控制

要求：

- 创建一个计数器节点。
- 用服务清零、暂停和恢复计数器。
- 为非法请求返回明确的失败结果。
- 为服务添加测试。

### 练习 3：Action 任务

要求：

- 定义一个“移动到目标数值”的 Action。
- Goal 包含目标值和最大速度。
- Feedback 发布当前值和剩余距离。
- 支持取消 Goal。
- Result 区分成功、取消和失败。

### 练习 4：移动机器人仿真

要求：

- 用 URDF/Xacro 描述差速底盘。
- 添加激光雷达和里程计。
- 在 RViz2 中显示 TF、LaserScan 和机器人模型。
- 播放速度指令，让机器人在仿真中移动。
- 记录一段 Bag 并复现问题。

### 练习 5：ROS1 到 ROS2 迁移

要求：

- 将一个 ROS1 Python 发布/订阅包迁移到 ROS2。
- 将 `.launch` 迁移为 Python Launch。
- 将参数服务器用法改为节点参数。
- 写出迁移前后的接口和 QoS 说明。
- 添加至少一个集成测试。

---

## 20. 30 天学习计划

### 第 1 周：基础认知

- Day 1：Linux、终端、环境变量、Git。
- Day 2：ROS Graph、节点和话题。
- Day 3：服务、动作和参数。
- Day 4：ROS2 CLI 和常见接口。
- Day 5：创建工作空间和 Python 包。
- Day 6：发布者、订阅者和日志。
- Day 7：复习并完成练习 1。

### 第 2 周：ROS2 开发

- Day 8：C++ 包和 `rclcpp`。
- Day 9：自定义消息和接口包。
- Day 10：服务和 Action。
- Day 11：YAML 参数文件。
- Day 12：Python Launch。
- Day 13：QoS 和回调执行模型。
- Day 14：完成练习 2、练习 3。

### 第 3 周：机器人系统

- Day 15：TF2 和时间戳。
- Day 16：URDF/Xacro。
- Day 17：RViz2。
- Day 18：仿真时钟和机器人模型。
- Day 19：传感器消息和坐标转换。
- Day 20：rosbag 和可复现调试。
- Day 21：完成练习 4。

### 第 4 周：ROS1 与工程化

- Day 22：ROS1 工作空间、节点和话题。
- Day 23：ROS1 参数、服务和 Launch。
- Day 24：ROS1/ROS2 API 对照。
- Day 25：QoS、参数和 Launch 迁移。
- Day 26：测试、日志和目录组织。
- Day 27：多机通信与容器化。
- Day 28-30：完成练习 5，并整理项目 README。

---

## 21. 学习验收标准

完成基础阶段后，你应该可以解释并实践：

- 节点、话题、服务、动作、参数和接口的区别。
- 如何查看一个节点的发布、订阅和参数。
- 为什么 ROS2 需要 QoS，以及传感器数据为什么常使用 Best Effort。
- 如何使用 Launch 启动一组节点。
- 如何检查 TF 树、时间戳和 `frame_id`。
- 如何录制和回放 Bag。
- 如何创建并构建一个 Python 或 C++ 包。
- ROS1 的 Master 与 ROS2 DDS 发现机制的差异。
- ROS1 参数服务器与 ROS2 节点参数的差异。
- ROS1 节点迁移到 ROS2 时为什么不能只替换 API 名称。

完成项目阶段后，你还应该能够：

- 从驱动、感知、定位到控制画出完整数据流。
- 通过 CLI、日志、图和 Bag 独立定位常见问题。
- 用参数和 Launch 支持仿真、真实设备和录包回放三种模式。
- 为关键节点编写最小单元测试和集成测试。
- 写出别人可以复现的安装、启动和排错说明。

---

## 22. 推荐查阅顺序

学习具体命令时，以所用 ROS2 发行版的官方文档和对应软件包文档为准。建议查阅顺序：

1. ROS2 官方概念：节点、话题、服务、Action、参数和 QoS。
2. `rclpy` 或 `rclcpp` API。
3. `tf2`、URDF/Xacro 和 RViz2。
4. 目标机器人平台的驱动文档。
5. Nav2、MoveIt 等功能栈文档。
6. 目标 DDS 实现和系统部署文档。

不同 ROS2 发行版之间的包名、API 和默认配置可能变化。遇到冲突时，优先使用当前项目的 `package.xml`、README、锁定的依赖版本和官方发行版文档。
