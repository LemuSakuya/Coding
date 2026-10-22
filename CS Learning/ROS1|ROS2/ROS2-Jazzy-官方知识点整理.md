# ROS 2 Jazzy 官方教程知识点整理

> 本笔记依据 ROS 2 Jazzy 官方 Tutorials 编写。内容将官方核心概念、命令、注意事项和练习重新整理成中文，方便学习和复盘；不逐字复制官方页面。
>
> 官方入口：https://docs.ros.org/en/jazzy/Tutorials.html

## 使用方法

1. 先阅读本节列出的官方页面。
2. 再阅读知识点说明。
3. 在 Ubuntu 24.04 + ROS 2 Jazzy 中执行命令。
4. 完成每节的自测题。
5. 将实验命令、结果和错误记录在项目 README 中。

---

## 1. 环境、工作空间和 colcon

官方页面：

- https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Configuring-ROS2-Environment.html
- https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html
- https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html

### 1.1 ROS 2 环境脚本

ROS2 的命令、Python 模块、C++ 库和包索引依赖环境变量。系统安装后加载：

~~~bash
source /opt/ros/jazzy/setup.bash
~~~

工作空间构建后加载：

~~~bash
source ~/ros2_ws/install/setup.bash
~~~

加载顺序：

~~~text
系统 ROS2 环境 -> 自己的工作空间环境
~~~

后加载的工作空间可以扩展或覆盖前面的包。多个工作空间都写入 .bashrc 容易造成版本混乱，建议只自动加载系统环境，实验时手动加载目标工作空间。

### 1.2 常见环境变量

~~~bash
printenv | grep -E 'ROS|RMW'
echo "$ROS_DISTRO"
echo "$ROS_DOMAIN_ID"
~~~

ROS_DOMAIN_ID 用于 DDS 网络隔离：

~~~bash
export ROS_DOMAIN_ID=10
~~~

同一 ROS2 网络中的节点通常要使用相同 Domain ID。多机通信失败时，检查 Domain ID、网络接口、防火墙和 DDS 配置。

### 1.3 工作空间结构

~~~text
ros2_ws/
├── src/        源码包，应该进入 Git
├── build/      构建中间文件，通常不进入 Git
├── install/    安装结果和环境脚本，通常不进入 Git
└── log/        构建日志，通常不进入 Git
~~~

创建和构建：

~~~bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
source install/setup.bash
~~~

常用 colcon 命令：

~~~bash
colcon list
colcon build
colcon build --symlink-install
colcon build --packages-select <package_name>
colcon build --packages-up-to <package_name>
colcon test
colcon test-result --verbose
~~~

构建失败时先看第一条真实错误，然后检查依赖、包名、入口配置和 log 目录。不要一遇到错误就删除整个工作空间。

### 1.4 ROS2 包

创建 Python 包：

~~~bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python --license Apache-2.0 py_pubsub
~~~

创建 C++ 包：

~~~bash
ros2 pkg create --build-type ament_cmake --license Apache-2.0 cpp_pubsub
~~~

Python 包常见文件：

~~~text
package.xml       包信息和依赖
setup.py          Python 安装和可执行入口
setup.cfg         Python 安装路径
resource/         ROS2 包索引资源
<package>/        Python 模块
test/             测试
~~~

---

## 2. turtlesim、ros2 和 rqt

官方页面：
https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim.html

### 2.1 turtlesim

turtlesim 是一个轻量级二维模拟器，用于学习 ROS2 通信模型。它不是完整机器人仿真器，但可以直观展示 Topic、Service、Action 和参数。

~~~bash
ros2 run turtlesim turtlesim_node
ros2 run turtlesim turtle_teleop_key
~~~

ros2 run 的格式：

~~~text
ros2 run <package_name> <executable_name>
~~~

### 2.2 rqt

rqt 是基于 Qt 的插件式工具框架，可以观察日志和系统状态：

~~~bash
rqt
~~~

CLI 适合精确排错，rqt 适合快速观察。

---

## 3. 节点 Node

官方页面：
https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes.html

### 3.1 节点职责

节点是执行特定任务的 ROS2 单元，例如传感器驱动、视觉处理、定位、控制或硬件管理。节点职责清晰时，系统更容易复用、测试、替换和部署。

### 3.2 节点命令

~~~bash
ros2 node list
ros2 node info /node_name
~~~

node info 重点查看：

- 节点名称和命名空间。
- 发布的 Topic。
- 订阅的 Topic。
- 提供的 Service。
- 使用的 Action。
- 节点参数。

### 3.3 命名空间和重映射

完整节点名称可能是：

~~~text
/robot1/sensors/camera
~~~

使用命名空间可以隔离多机器人系统中的相同节点和话题。

节点重映射：

~~~bash
ros2 run turtlesim turtlesim_node --ros-args --remap __node:=my_turtle
~~~

话题重映射：

~~~bash
ros2 run turtlesim turtle_teleop_key --ros-args \
  --remap /turtle1/cmd_vel:=/robot/cmd_vel
~~~

重映射适合复用节点，但必须记录在 README 或 Launch 文件中。

### 3.4 自测

1. 一个节点能否同时发布和订阅多个 Topic？
2. 如何查看节点提供了哪些 Service？
3. 如何让两个相同节点运行在不同命名空间？
4. 重映射和修改源代码有什么区别？

---

## 4. 话题 Topic

官方页面：
https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html

### 4.1 话题模型

Topic 是命名的数据通道。发布者写入消息，订阅者读取消息，双方不需要直接调用对方。

~~~text
publisher A ─┐
publisher B ─┼─> /topic_name ─┬─> subscriber A
             │                └─> subscriber B
~~~

适合 Topic 的数据包括图像、点云、激光、机器人状态、速度指令、路径和检测结果。

### 4.2 话题命令

~~~bash
ros2 topic list
ros2 topic list -t
ros2 topic type /topic_name
ros2 topic info /topic_name
ros2 topic info /topic_name --verbose
ros2 topic echo /topic_name
ros2 topic hz /topic_name
ros2 topic bw /topic_name
~~~

查看接口：

~~~bash
ros2 interface show geometry_msgs/msg/Twist
ros2 interface show turtlesim/msg/Pose
~~~

重点关注字段类型、嵌套消息、Header、stamp、frame_id 和单位。

### 4.3 命令行发布

~~~bash
ros2 topic pub --rate 2 /turtle1/cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 1.0}, angular: {z: 0.5}}"
~~~

命令行发布适合验证连接和消息格式，不适合替代真实机器人控制节点。真实控制需要限速、急停、超时和安全区域。

### 4.4 QoS

ROS2 Topic 通信包含 QoS，核心参数：

- Reliability：可靠传输或允许丢失。
- Durability：是否向后来加入的订阅者提供历史数据。
- History：保留多少历史消息。
- Depth：消息队列深度。

查看 QoS：

~~~bash
ros2 topic info /topic_name --verbose
~~~

传感器常允许丢帧以降低延迟，控制和关键状态通常更重视可靠性。QoS 不兼容时，Topic 可能存在但订阅者收不到数据。

### 4.5 话题排错

~~~text
节点是否运行？
  -> 话题名称是否正确？
    -> 是否有发布者？
      -> 消息类型是否一致？
        -> QoS 是否兼容？
          -> frame_id 和时间戳是否正确？
~~~

---

## 5. 服务 Service

官方页面：
https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html

### 5.1 服务模型

Service 是请求/响应模型：客户端发送一次请求，服务端处理并返回一次响应。

适合查询配置、清空地图、切换模式和触发快速操作。不适合连续传感器数据、执行时间很长的任务或需要持续 Feedback 的任务。

### 5.2 服务命令

~~~bash
ros2 service list
ros2 service list -t
ros2 service type /service_name
ros2 service find std_srvs/srv/Empty
ros2 interface show turtlesim/srv/Spawn
~~~

调用示例：

~~~bash
ros2 service call /clear std_srvs/srv/Empty
ros2 service call /spawn turtlesim/srv/Spawn \
  "{x: 2.0, y: 2.0, theta: 0.0, name: 'new_turtle'}"
~~~

### 5.3 服务设计原则

- 服务端应尽快返回。
- 验证请求参数。
- 响应说明成功、失败和原因。
- 客户端等待服务可用。
- 长任务改用 Action。
- 不要在服务回调中长时间阻塞。

---

## 6. 参数 Parameter

官方页面：
https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters.html

### 6.1 参数作用

参数是节点配置值，例如发布频率、阈值、文件路径、坐标系、仿真时间和运行模式。参数不应承担高频数据传输，也不应作为隐式节点通信通道。

### 6.2 参数命令

~~~bash
ros2 param list
ros2 param list /node_name
ros2 param describe /node_name parameter_name
ros2 param get /node_name parameter_name
ros2 param set /node_name parameter_name value
ros2 param dump /node_name
ros2 param load /node_name params.yaml
~~~

ROS2 参数属于节点，节点通常需要声明参数、默认值和参数类型。

### 6.3 YAML

~~~yaml
node_name:
  ros__parameters:
    publish_period: 0.5
    use_sim_time: false
    frame_id: base_link
~~~

节点名、ros__parameters 和缩进必须正确。参数文件应该进入版本控制。

### 6.4 设计建议

- 为参数提供默认值。
- 检查范围，例如频率必须大于零。
- 记录单位。
- 保存实验使用的 YAML 文件。
- 对允许运行时修改的参数实现回调。
- 拒绝非法参数值。

---

## 7. Action

官方页面：
https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html

### 7.1 Action 模型

Action 用于可持续、可反馈和可取消的任务：

~~~text
Client -- Goal ------> Server
Client <-- Feedback -- Server
Client <-- Result ---- Server
Client -- Cancel ----> Server
~~~

典型任务包括导航、机械臂轨迹、旋转、抓取和长时间计算。

### 7.2 Action 命令

~~~bash
ros2 action list
ros2 action list -t
ros2 action info /action_name
ros2 interface show turtlesim/action/RotateAbsolute
~~~

发送 Goal：

~~~bash
ros2 action send_goal /turtle1/rotate_absolute \
  turtlesim/action/RotateAbsolute \
  "{theta: 1.57}" --feedback
~~~

客户端要处理 Goal 接受、Feedback、Result、Cancel 和服务端异常退出。

### 7.3 机制选型

| 需求 | 选择 |
| --- | --- |
| 快速请求并返回 | Service |
| 持续执行并需要进度 | Action |
| 需要取消 | Action |
| 连续数据流 | Topic |

---

## 8. 日志和 rqt_console

官方页面：
https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Using-Rqt-Console/Using-Rqt-Console.html

### 8.1 日志等级

~~~text
DEBUG  详细调试信息
INFO   正常运行状态
WARN   可恢复问题
ERROR  当前操作失败
FATAL  严重错误
~~~

Python 示例：

~~~python
self.get_logger().debug('debug details')
self.get_logger().info('node is running')
self.get_logger().warn('battery is low')
self.get_logger().error('sensor read failed')
~~~

日志要说明发生了什么、相关对象、关键数值、是否可以恢复和下一步检查什么。高频回调中不要无限打印日志。

~~~bash
rqt_console
~~~

---

## 9. Launch

官方页面：

- https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Launching-Multiple-Nodes/Launching-Multiple-Nodes.html
- https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Creating-Launch-Files.html
- https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Launch-system.html

### 9.1 作用

Launch 文件统一启动和配置多个节点，可以管理节点名、命名空间、参数、重映射、条件和事件。

### 9.2 Python Launch

~~~python
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
    ])
~~~

Node 常用配置：

~~~python
Node(
    package='py_pubsub',
    executable='talker',
    name='publisher_node',
    namespace='robot1',
    output='screen',
    parameters=['config/params.yaml'],
    remappings=[('chatter', 'robot1/chatter')],
)
~~~

### 9.3 设计原则

- Launch 负责编排，不负责业务算法。
- 复杂参数通过 YAML 或 Launch 传入。
- 真实设备、仿真和 Bag 回放尽量共用结构。
- 大型系统拆分子 Launch。
- 明确节点名称。
- 记录重映射关系。

运行和验证：

~~~bash
ros2 launch py_pubsub demo.launch.py
ros2 node list
ros2 topic list
~~~

---

## 10. rosbag

官方页面：
https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.html

### 10.1 用途

Bag 用于重现测试、复现异常、离线开发算法、分享数据和回归测试。

### 10.2 命令

~~~bash
ros2 bag record /chatter
ros2 bag record /chatter /robot_state /tf /tf_static
ros2 bag info <bag_directory>
ros2 bag play <bag_directory>
~~~

只录制足以重现问题的话题。图像和点云通常很大，不要无目的录制全部 Topic。

### 10.3 可复现记录

每个 Bag 最好同时记录：

- 代码版本。
- ROS2 发行版。
- 参数文件。
- Launch 命令。
- 录制场景。
- 录制的话题。
- 是否使用仿真时间。

---

## 11. rosdep

官方页面：
https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Rosdep.html

### 11.1 作用

rosdep 根据包的依赖声明查找并安装系统依赖，把 ROS 依赖名称映射成 Ubuntu apt 包或其他平台的安装方式。

~~~bash
cd ~/ros2_ws
rosdep update
rosdep install --from-paths src --ignore-src -r -y
~~~

参数：

- from-paths：从指定目录读取包。
- ignore-src：忽略源码中已经存在的包。
- r：某个依赖失败时继续处理。
- y：自动确认安装。

### 11.2 package.xml

项目应在 package.xml 中声明构建、运行和测试依赖，让其他机器和 CI 可以重建环境。不要只依赖某台电脑手动安装过的包。

---

## 12. TF2

官方页面：

- https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Introduction-To-Tf2.html
- https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Writing-A-Tf2-Static-Broadcaster-Py.html
- https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Writing-A-Tf2-Listener-Py.html
- https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Debugging-Tf2-Problems.html

### 12.1 解决的问题

机器人中的传感器和部件使用不同坐标系。TF2 保存并查询这些坐标系随时间变化的空间关系，使算法可以把数据转换到需要的坐标系。

典型树：

~~~text
map
└── odom
    └── base_link
        ├── laser
        └── camera_link
~~~

### 12.2 静态和动态变换

- 静态变换：固定传感器关系，例如 base_link 到 laser。
- 动态变换：随时间变化，例如 odom 到 base_link。

不要让多个节点发布同一条 TF。父子关系必须清晰且连通。

### 12.3 命令

~~~bash
ros2 run tf2_tools view_frames
ros2 run tf2_ros tf2_echo map base_link
ros2 topic echo /tf
ros2 topic echo /tf_static
~~~

### 12.4 常见问题

- 坐标系名称拼写错误。
- TF 树断裂。
- 时间戳过旧。
- 系统时间和仿真时间不一致。
- 消息缺少正确 frame_id。
- 旋转单位或坐标方向错误。

---

## 13. 测试

官方页面：

- https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Testing/Testing-Main.html
- https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Testing/CLI.html
- https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Testing/Python.html

### 13.1 测试层次

1. 单元测试：纯函数和数学逻辑。
2. 节点测试：参数、回调和状态转换。
3. 集成测试：多节点通信。
4. 仿真测试：固定场景和固定输入。
5. 硬件测试：低速、限位、急停和故障恢复。

### 13.2 命令

~~~bash
colcon test --packages-select py_pubsub
colcon test-result --verbose
~~~

先测试自己的业务逻辑，不要一开始测试 ROS2 中间件。至少覆盖正常输入、空输入、边界值和错误输入。

~~~python
def calculate_average(values):
    if not values:
        return 0.0
    return sum(values) / len(values)
~~~

---

## 14. URDF、Xacro 和 robot_state_publisher

官方页面：

- https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/URDF-Main.html
- https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/Building-a-Visual-Robot-Model-from-Scratch.html
- https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/Using-Xacro-to-Clean-Up-a-URDF-File.html

### 14.1 URDF 元素

- robot：整个机器人。
- link：刚体。
- joint：连接两个 link。
- visual：显示几何模型。
- collision：碰撞模型。
- inertial：质量和惯性。
- origin：相对父坐标系的位姿。

~~~xml
<robot name="simple_robot">
  <link name="base_link" />
  <link name="sensor_link" />
  <joint name="sensor_joint" type="fixed">
    <parent link="base_link" />
    <child link="sensor_link" />
    <origin xyz="0.2 0 0.15" rpy="0 0 0" />
  </joint>
</robot>
~~~

### 14.2 Xacro

大型模型直接维护 URDF 会产生重复内容。Xacro 支持参数、宏和表达式，让模型更容易复用和维护。

### 14.3 robot_state_publisher

robot_state_publisher 根据 URDF 和关节状态发布机器人 TF。固定关节、可动关节、关节名称和坐标系名称必须一致。

---

## 15. RViz2

官方页面：

- https://docs.ros.org/en/jazzy/Tutorials/Intermediate/RViz/RViz-Main.html
- https://docs.ros.org/en/jazzy/Tutorials/Intermediate/RViz/RViz-User-Guide.html

RViz2 是 ROS2 数据可视化和调试工具，不是仿真器，也不会自动修复错误数据。

常见 Display：

- TF。
- RobotModel。
- LaserScan。
- PointCloud2。
- Image。
- Map。
- Path。
- Pose。
- Marker。

Fixed Frame 是显示数据的参考坐标系。它必须存在于 TF 树中，并且目标消息的 frame_id 可以通过 TF 连接到它。

RViz2 排错顺序：

1. Topic 是否存在？
2. 消息类型是否正确？
3. 是否有发布者？
4. QoS 是否兼容？
5. frame_id 是否正确？
6. Fixed Frame 是否存在？
7. TF 是否连通？
8. 时间戳是否有效？

---

## 16. Python 客户端库 rclpy

官方页面：
https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries.html

### 16.1 基本流程

~~~text
rclpy.init()
  -> 创建 Node
  -> 创建 Publisher/Subscriber/Service/Action/Timer
  -> rclpy.spin(node)
  -> 销毁 Node
  -> rclpy.shutdown()
~~~

### 16.2 常用 API

~~~python
import rclpy
from rclpy.node import Node

rclpy.init(args=args)
node = Node('node_name')
publisher = node.create_publisher(MessageType, 'topic_name', 10)
subscription = node.create_subscription(
    MessageType,
    'topic_name',
    callback,
    10,
)
timer = node.create_timer(0.5, callback)
rclpy.spin(node)
node.destroy_node()
rclpy.shutdown()
~~~

### 16.3 回调原则

定时器、订阅、服务和 Action 都通过回调执行。回调应尽量短小，不要在回调中长时间阻塞，否则可能阻塞其他消息处理。

复杂系统继续学习 Executor、Callback Group、线程和异步任务。两天入门先掌握单线程基本模型。

### 16.4 推荐分层

~~~text
Node 类：负责 ROS 通信和生命周期
业务函数：负责计算、判断和状态转换
接口文件：负责 msg/srv/action 契约
Launch/YAML：负责启动和配置
测试：负责验证业务函数和节点行为
~~~

---

## 17. 官方知识点综合练习

### 练习 1：CLI 调查报告

使用 turtlesim，记录：

- 当前节点列表。
- /turtle1/cmd_vel 的消息类型。
- /turtle1/pose 的发布频率。
- /clear 的服务类型。
- /turtle1/rotate_absolute 的 Action 类型。
- /turtlesim 的关键参数。

### 练习 2：通信机制选型

为以下需求选择 Topic、Service 或 Action，并说明原因：

- 激光雷达连续扫描。
- 清空地图。
- 导航到目标点。
- 查询电池电量。
- 发布当前速度。
- 执行机械臂抓取任务。

### 练习 3：系统排错

模拟并记录排查步骤：

- 订阅者收不到数据。
- 服务调用失败。
- Launch 找不到可执行文件。
- RViz2 报 Fixed Frame 错误。
- rosdep 找不到依赖。
- Bag 回放后算法没有输出。

### 练习 4：综合项目扩展

在两天综合项目中增加：

- 自定义 RobotStatus 消息。
- 异常状态 Action。
- 参数运行时修改回调。
- 集成测试。
- RViz2 配置文件。

---

## 18. 官方教程索引

- https://docs.ros.org/en/jazzy/First-Steps.html
- https://docs.ros.org/en/jazzy/Tutorials.html
- https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools.html
- https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries.html
- https://docs.ros.org/en/jazzy/Tutorials/Intermediate.html

