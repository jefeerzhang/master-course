# master-course 维护手册

> 这份文档是给后续 agent 看的"操作手册"。**任何人 / agent 在改这个仓库前请先读完这份文档。**

## 项目结构

```
master-course/
├── index.html                # 主页 (本仓库唯一门户)
├── assets/course-index.css   # 主页样式 (与 4 个子站共享设计 token)
├── course-focus.json         # 主页派生数据源 (聚合本页用)
├── MAINTENANCE.md            # ← 你正在读这份
│
├── yuan-yunfen-writing/      # 子站 1: 硕士论文框架讲座 (主推)
│   ├── index.html
│   ├── md2_skeleton.png      # 主页用到的配图
│   ├── md2_sample.png
│   └── sample-thesis.pdf     # 94 页论文样本
│
├── research-methods/         # 子站 2: 核心研究方法指南
│   ├── index.html
│   ├── md1_path.png
│   └── md1_spectrum.png
│
├── 第一性原理/               # 子站 3: 第一性原理思维 (URL 保留中文)
│   ├── index.html
│   └── 第一性原理配图/
│       └── 01-10_*.jpeg      # 10 张认知锚点
│
└── agri-finance/             # 子站 4: 农业信贷的硬科技
    ├── index.html
    └── HANDOVER.md           # 子站内部交接笔记 (非聚合源)
```

## 关键规则

1. **配色 token**：`--accent: #245642`（森林绿）。所有页面用同一组 CSS 变量，不另起。
2. **字体**：衬线优先 `Noto Serif CJK SC / Source Han Serif SC / Songti SC`；sans 兜底；mono 用 `Cascadia Mono / SFMono`。
3. **字重档位**（与首页 / CV v6 完全一致）：
   - body: 500
   - h1/h2 主标题: 800
   - h3 次级标题: 800
   - 数字 metric / meta: 700-800
4. **导航条 5 项**：首页 / 个人简历 / 硕士课程 / 知识学习 / 小工具（绝对不能少/多）。
5. **GitHub Pages 边缘缓存 10 分钟**：CSS link 必须带 `?v=N` 破缓存（每次 push 升 N+1）。

## 主页派生数据: `course-focus.json`

主页 `index.html` 中的两个核心区是**派生视图**，数据源是 `course-focus.json`：

- **`<aside class="course-focus">` 区**：右侧"课程重点" 01-04 编号清单，**对应 `items[]`**
- **`<section class="course-section">` 区**：4 张课程卡片（1 主推 + 3 次卡），**对应 `courseMaterials[]`**

### Agent 更新流程（推送新内容后）

**触发条件**：用户告知"master-course 推送了新的内容"，或子站首页发生变化。

**步骤**：

1. **扫描子站目录**：列出 `yuan-yunfen-writing/`, `research-methods/`, `第一性原理/`, `agri-finance/` 四个子站的 `index.html` 与最近 commit。

2. **提取每个子站的"标题 + 摘要 + 配图"**：
   - 主标题 `<h1>`（如 "硕士论文框架讲座"）
   - 首段 `<p>` 或 `<section class="lead">`（如"以农村'三资'管理..."）
   - 主配图 `<figure img src>`（如 `md2_skeleton.png`）
   - 配图旁的 caption / 子标题（如 "94 页样本 / 5 章拆解 / 答辩指南"）

3. **重新校准 `course-focus.json` 的 `items[]` 与 `courseMaterials[]`**：
   - 四个 `items[]` 的标题与描述**保持稳定不变**——它们是"课程定位四件事"，是相对稳定的论点
   - `courseMaterials[]` 的内容**跟着子站推送走**——子站换了配图、改了标题、删了样本，这里都要同步

4. **重渲染 `index.html` 的两个区**（不要动其它结构）：
   - `<aside class="course-focus">` 里的 4 个 `<li>` 不变
   - `<section class="course-section">` 里的 4 张卡：`<a href>`/`<img src>`/`<p>`/`<h3>`/`.meta-pill` 跟着 `courseMaterials[]` 更新
   - 同时把 `course-focus.json` 的 `lastUpdated` 改成今天

5. **破缓存**：CSS link `?v=N` 升一档。

6. **验证**：
   - `curl -I https://jefeerzhang.github.io/master-course/...` 拿 200
   - 用 `browser_take_screenshot` 截图主页确认主推卡 + 3 张次卡的图都是新的

7. **commit + push**：
   ```
   git add -A
   git commit -m "sync: 派生主页 (来自 [子站名] 推送)"
   git push origin main
   ```

### 自动化脚本（未来可选）

`tools/aggregate-summary.js`（待实现）预期能做：
- 读取每个子站 `index.html`，提取 h1 / lead / figure
- 跟 `course-focus.json` 默认值合并，写回
- 生成 `index.html` 的两个区
- 更新 `lastUpdated` 字段

不强制自动化——纯手工也行。

## 已知坑

- **CSS 顺序覆盖**：变体样式（如 `.course-card--lead h3`）必须放在通用样式（`.course-card h3`）**之后**，否则被覆盖（主推卡变深墨那次坑过）
- **GitHub Pages CDN 缓存**：push 后要等 30-60 秒再 `curl`，否则拿到旧内容
- **中文字段名**：`第一性原理/` 目录名带中文，URL 里 `%E7%AC%AC...` 编码，注意主页 `href` 要用 `<a href="./第一性原理/">` 让浏览器处理，不要预先编码

## 工作区路径

- 临时仓库：`C:\Users\jefeer\Downloads\GenericAgent-Desktop-Windows-Portable\GenericAgent-Desktop-Windows-Portable\runtime\app\temp\master_course_repo`
- 远端：`https://github.com/jefeerzhang/master-course.git`（main 分支）
- 线上：`https://jefeerzhang.github.io/master-course/`