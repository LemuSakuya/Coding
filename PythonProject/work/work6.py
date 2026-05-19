# 导入所需库
import jieba
import wordcloud
import os

# 1. 原始文本内容
txt = "湖南师范大学创建于1938年，位于历史文化名城长沙，是国家“211工程”重点建设的大学，国家“双一流”建设高校，教育部与湖南省重点共建“双一流”建设高校，教育部普通高等学校本科教学工作水平评估优秀高校，湖南省“世界一流学科建设高校”。学校现有8个校区，占地2885余亩，建筑面积131万平方米。主校区西偎麓山，东濒湘江，风光秀丽，是全国绿化“400佳”单位之一。"


# 2. 自定义停用词库（过滤无意义词汇、标点、数字、虚词）
stop_words = {
    "的", "是", "于", "有", "为", "现有", "余年", "平方米", "8", "131", "2885", "1938",
    "，", "。", "“", "”", "、", "之一"
}
########### Begin #############
# 3. jieba分词 + 停用词过滤
# 精准模式分词
word_cut = jieba.lcut(txt)

# 自定义规则完成停用词过滤：剔除停用词、符号、单字无效词汇
# 判断条件：不在停用词集合内 且 去除空格后词语长度大于等于2
filter_words = [
    word.strip()
    for word in word_cut
    if word.strip() and word.strip() not in stop_words and len(word.strip()) >= 2
]


# 将过滤后的关键词以空格拼接，满足wordcloud词云文本输入格式
final_text = " ".join(filter_words)

# 4. 输出关键结果
print("文本分词结果：")
print(word_cut)
print("\n过滤停用词后有效关键词：")
print(filter_words)

# 5. 词云可视化配置
# width/height：设置词云图片尺寸；font_path：指定中文字体路径，解决中文乱码（"/usr/share/fonts/SimHei.ttf"）
# background_color：设置画布背景；max_words：限制最大展示关键词数量
# contour_width/contour_color：设置词云外轮廓宽度与颜色，优化展示效果
font_candidates = [
    "C:/Windows/Fonts/simhei.ttf",
    "C:/Windows/Fonts/msyh.ttc",
    "/usr/share/fonts/SimHei.ttf",
]
font_path = next((path for path in font_candidates if os.path.exists(path)), None)

wc = wordcloud.WordCloud(
    width=1000,
    height=700,
    font_path=font_path,
    background_color="white",
    max_words=200,
    contour_width=1,
    contour_color="steelblue",
)

########### End #############

# 6. 生成词云
wc.generate(final_text)
save_path = "/data/workspace/myshixun/pic/hunnu_wordcloud.png"
wc.to_file(save_path)
print(f"\n【词云生成成功】图片已保存至路径：{os.path.abspath(save_path)}")