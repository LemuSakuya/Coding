# -*- coding: utf-8 -*-
import os
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from stu_test import test_graph

# 定义结果图片保存目录
OUTPUT_DIR = "/data/workspace/myshixun/result_fig/"
# 定义结果图片文件名
IMAGE_NAME = "honglou_graph.png"
# 拼接完整图片保存路径
IMAGE_PATH = os.path.join(OUTPUT_DIR, IMAGE_NAME)
# 定义本地中文字体文件路径
FONT_PATH = "/data/workspace/myshixun/SimHei.ttf"


# 定义一个函数，用来加载本地中文字体文件
def set_chinese_font():
    # 判断字体文件是否存在
    if os.path.exists(FONT_PATH):
        # 将本地字体文件加入 matplotlib 字体管理器
        fm.fontManager.addfont(FONT_PATH)
        # 设置全局中文字体为 SimHei
        plt.rcParams["font.sans-serif"] = ["SimHei"]
        # 设置负号正常显示
        plt.rcParams["axes.unicode_minus"] = False
    else:
        # 如果字体文件不存在，则输出警告信息
        print("警告：未找到字体文件 {}".format(FONT_PATH))
        # 设置负号正常显示
        plt.rcParams["axes.unicode_minus"] = False


# 定义一个函数，用来构建《红楼梦》人物关系图谱
def build_graph():
    # 创建一张有向图，因为人物关系具有方向性，所以使用 DiGraph
    G = nx.DiGraph()

    # 添加系统预置人物：贾宝玉节点
    G.add_node("jby", label="贾宝玉", gender="男", group="system")
    # 添加系统预置人物：林黛玉节点
    G.add_node("ldy", label="林黛玉", gender="女", group="system")
    # 添加系统预置人物：薛宝钗节点
    G.add_node("xbc", label="薛宝钗", gender="女", group="system")
    # 添加系统预置人物：贾母节点
    G.add_node("jm", label="贾母", gender="女", group="system")
    # 添加系统预置人物：王夫人节点
    G.add_node("wfr", label="王夫人", gender="女", group="system")

    # 添加系统预置关系：贾母和贾宝玉是祖孙关系
    G.add_edge("jm", "jby", label="祖孙")
    # 添加系统预置关系：贾母和林黛玉是外祖孙关系
    G.add_edge("jm", "ldy", label="外祖孙")
    # 添加系统预置关系：王夫人和贾宝玉是母子关系
    G.add_edge("wfr", "jby", label="母子")
    # 添加系统预置关系：贾宝玉和林黛玉是木石前盟关系
    G.add_edge("jby", "ldy", label="木石前盟")
    # 添加系统预置关系：贾宝玉和薛宝钗是金玉良缘关系
    G.add_edge("jby", "xbc", label="金玉良缘")
    # 添加系统预置关系：王夫人和薛宝钗是姨甥关系
    G.add_edge("wfr", "xbc", label="姨甥")

    ########## Begin ##########
    # 添加学生补充人物：史湘云节点
    G.add_node("sxy", label="史湘云", gender="女", group="student", alias="枕霞旧友")
    # 添加史湘云与贾母的关系：侄孙女
    G.add_edge("sxy", "jm", label="侄孙女")
    # 添加贾宝玉与史湘云的关系：青梅竹马
    G.add_edge("jby", "sxy", label="青梅竹马")

    # 添加学生补充人物：袭人节点
    G.add_node("xr", label="袭人", gender="女", group="student")
    # 添加袭人与贾宝玉的关系：丫鬟
    G.add_edge("xr", "jby", label="丫鬟")
    # 添加王夫人与袭人的关系：器重
    G.add_edge("wfr", "xr", label="器重")
    ########## End ##########

    # 返回构建完成的人物关系图谱
    return G


# 定义一个函数，用来绘制并保存人物关系图谱
def draw_graph(G):
    # 如果结果目录不存在，就创建结果目录
    if not os.path.exists(OUTPUT_DIR):
        # 创建结果目录，exist_ok=True 表示目录已存在时不报错
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 加载本地中文字体，避免中文显示乱码
    set_chinese_font()

    # 创建一个画布，并设置图像大小
    plt.figure(figsize=(12, 10))
    # 使用弹簧布局自动计算各个节点的位置
    pos = nx.spring_layout(G, k=0.8, seed=42)

    # 筛选系统预置节点
    system_nodes = [n for n, attr in G.nodes(data=True) if attr.get("group") == "system"]
    # 筛选学生补充节点
    student_nodes = [n for n, attr in G.nodes(data=True) if attr.get("group") == "student"]

    # 绘制系统预置节点，颜色为蓝色
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=system_nodes,
        node_color="#97C2FC",
        node_size=2500,
        edgecolors="#666666"
    )

    # 绘制学生补充节点，颜色为粉色
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=student_nodes,
        node_color="#FB7E81",
        node_size=2500,
        edgecolors="#666666"
    )

    # 绘制关系边
    nx.draw_networkx_edges(
        G,
        pos,
        edge_color="#888888",
        arrowstyle="-|>",
        arrowsize=20,
        width=1.5
    )

    # 构造节点标签字典
    node_labels = {n: attr["label"] for n, attr in G.nodes(data=True)}
    # 绘制节点标签
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=12)

    # 构造边标签字典
    edge_labels = {(u, v): d["label"] for u, v, d in G.edges(data=True)}
    # 绘制边标签
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

    # 关闭坐标轴显示
    plt.axis("off")
    # 设置图谱标题
    plt.title("红楼梦人物关系图谱", fontsize=15)
    # 保存图片到指定路径
    plt.savefig(IMAGE_PATH, format="png", bbox_inches="tight", dpi=100)
    # 关闭画布，释放资源
    plt.close()
    # 输出图片生成提示信息
    print("图谱图片已生成：{}".format(IMAGE_PATH))


# 如果当前文件作为主程序运行，则执行下面的流程
if __name__ == "__main__":
    # 调用函数构建人物关系图谱
    graph = build_graph()
    # 调用测试函数对图谱进行评测
    test_graph(graph)
    # 调用绘图函数生成并保存图谱图片
    draw_graph(graph)