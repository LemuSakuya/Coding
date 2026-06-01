# 抑郁症传播研究网页使用说明

## 文件说明

- `Orange_ovo_2.html`：主网页文件。
- `fonts/smiley-sans/`：得意黑字体文件，用于页面中的栏目标题，例如“文本网络分析”。

## 如何打开

直接双击 `Orange_ovo_2.html`，或在浏览器中打开该文件即可查看页面。

推荐使用最新版 Chrome、Edge、Safari 或 Firefox。

## 打包给别人时

请把整个目录一起打包，不要只发送 HTML 文件：

```text
Orange_ovo_2/
├─ Orange_ovo_2.html
├─ README.md
└─ fonts/
   └─ smiley-sans/
```

当前页面优先使用 Google Fonts 加载 `Noto Serif SC`。如果访问环境无法连接 Google Fonts，标题会自动回退为系统宋体。
栏目标题通过本地 `fonts/smiley-sans/SmileySans-Oblique.ttf.woff2` 加载得意黑，因此打包时不要删除 `fonts` 文件夹。

## 网络依赖

当前页面通过 CDN 加载以下前端资源：

- ECharts
- ECharts WordCloud
- Tailwind CSS
- Font Awesome
- Google Fonts 的 `Noto Serif SC`

因此首次打开时需要联网。若完全离线使用，需要把这些库下载到本地并修改 `Orange_ovo_2.html` 顶部的引用路径。

## 字体策略

页面采用“展示字体 + 系统字体”的组合：

- 大标题、导航品牌名、人物故事引语：优先使用思源宋体 `Noto Serif SC`，更有研究报告和人文叙事气质。
- 栏目标题、小标题：使用得意黑 `Smiley Sans`，更醒目、更适合展示型标题。
- 正文、表格、图表标签：使用系统中文黑体栈，例如 `PingFang SC`、`Microsoft YaHei`、`Noto Sans SC` 等。

这样既能保留标题风格，也能保证正文和数据图表的可读性。

## 注意事项

得意黑和霞鹜文楷均为公开发布的字体项目。正式公开发布或商用前，建议再次阅读对应字体仓库的授权说明。
