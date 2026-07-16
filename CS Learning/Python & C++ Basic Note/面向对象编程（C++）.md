想象你正在建设一座“机器人城”。

城里有许多机器人：足球机器人、救援机器人、巡逻机器人。它们有共同特征，也各自有特殊能力。

**第一幕：图纸与机器人**

`class` 是机器人的设计图，object 是按照图纸造出来的实体。

```cpp
#include <iostream>
using namespace std;

class Robot {
public:
    string name;

    void sayHello() {
        cout << "我是 " << name << endl;
    }
};

int main() {
    Robot r1;
    r1.name = "小明";
    r1.sayHello();
}
```

这里：

- `Robot` 是类，描述机器人应该有什么、能做什么。
- `r1` 是对象，是真实存在的一台机器人。
- `name` 是数据成员。
- `sayHello()` 是成员函数。

**第二幕：城门与封装**

城主发现：任何人都能直接修改机器人的电量，很危险。

于是他把电量藏起来，只允许通过安全接口修改。这就是**封装**。

```cpp
class Robot {
private:
    int energy = 100;

public:
    void charge(int amount) {
        if (amount > 0) {
            energy += amount;
        }
    }

    void showEnergy() {
        cout << "当前电量：" << energy << endl;
    }
};
```

`private` 成员不能从类外直接访问：

```cpp
Robot r;
// r.energy = -100;  // 错误
r.charge(20);       // 通过公开接口操作
```

封装的核心思想是：

> 隐藏内部细节，只暴露安全、必要的操作。

**第三幕：机器人出生**

每台机器人出生时，都必须有名字。于是设计图增加了构造函数。

```cpp
class Robot {
private:
    string name;

public:
    Robot(string robotName) : name(robotName) {
        cout << name << " 出厂了" << endl;
    }

    void sayHello() {
        cout << "我是 " << name << endl;
    }
};

int main() {
    Robot r("小明");
    r.sayHello();
}
```

构造函数会在对象创建时自动执行。

机器人离开城市时，也可以执行清理工作，这叫析构函数：

```cpp
~Robot() {
    cout << name << " 离开了" << endl;
}
```

**第四幕：机器人家族**

足球机器人和救援机器人都属于机器人，但能力不同。这就是**继承**。

```cpp
class Robot {
public:
    void move() {
        cout << "机器人正在移动" << endl;
    }
};

class SoccerRobot : public Robot {
public:
    void kickBall() {
        cout << "足球机器人踢球" << endl;
    }
};
```

`SoccerRobot` 自动拥有 `Robot` 的 `move()`，同时增加了自己的 `kickBall()`。

**第五幕：同一句命令，不同表现**

城主下令：“开始工作！”

足球机器人踢球，救援机器人救人。它们对同一个函数有不同实现，这就是**多态**。

```cpp
class Robot {
public:
    virtual void work() {
        cout << "机器人工作中" << endl;
    }

    virtual ~Robot() = default;
};

class SoccerRobot : public Robot {
public:
    void work() override {
        cout << "足球机器人正在比赛" << endl;
    }
};

class RescueRobot : public Robot {
public:
    void work() override {
        cout << "救援机器人正在救援" << endl;
    }
};

int main() {
    Robot* robots[] = {
        new SoccerRobot(),
        new RescueRobot()
    };

    for (Robot* robot : robots) {
        robot->work();
    }

    for (Robot* robot : robots) {
        delete robot;
    }
}
```

关键在于：

```cpp
virtual void work();
```

`virtual` 告诉 C++：

> 不要只看指针的类型，要看它实际指向的对象。

因此同样调用：

```cpp
robot->work();
```

会产生不同结果。

**第六幕：四个核心法则**

面向对象编程可以记成机器人城的四条法则：

1. **封装**：把数据藏好，通过接口访问。
2. **继承**：子类复用父类的共同能力。
3. **多态**：同一个接口，不同对象表现不同。
4. **抽象**：只关注“能做什么”，暂时忽略“怎么做”。

例如：

```cpp
class Robot {
public:
    virtual void work() = 0; // 纯虚函数
};
```

这表示 `Robot` 只是一个抽象概念，具体机器人必须自己实现 `work()`。

最后，判断是否适合使用类，可以问自己三句话：

> 这个东西有什么数据？  
> 它能做什么？  
> 哪些细节应该隐藏起来？

能回答清楚，通常就能设计出一个不错的 C++ 类。