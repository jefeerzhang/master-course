# Agri-Finance 子页构建 HANDOVER

**日期**: 2026-07-11
**任务**: 在 `master-course/` 下新建 `agri-finance/` 子页，挂载 6 张生图（05-10_*.jpeg），保持与主页 nav 一致。

## 已完成
- [x] 主页 `index.html` patch（4 卡 agri-finance + 改标题为"农业信贷的硬科技"，去掉"硬核科技赋能"AI slop）
- [x] CSS `assets/course-index.css` patch（grid-template-rows 3 行 + writing span 3 + 新 `.course-agri-finance` 类）
- [x] `.gitignore` patch（加 `.probe/` `.tmp/`）
- [x] 6 张配图落盘 `第一性原理/第一性原理配图/05-10_*.jpeg`（全 JPEG 合法 head bytes）
- [x] `agri-finance/` 目录已建（PS New-Item -ItemType Directory -Force）
- [x] `agri-finance/index.html` 主体 160 行已写（6271 bytes）

## 待办
- [ ] **修 HTML 收尾**：file_patch 给最后一个 figure (10_数据资产闭环) 加 tag + text + figcaption + figure 闭合 + 全部收尾 HTML（`</p></figcaption></figure></div></div></section></main><footer>...</body></html>`）
- [ ] `git add` 相关文件（**不加** `.baoyu-skills/` `comic/` `tests/test_yuan_mainline.py` 等无关 untracked）
- [ ] `git commit` + `git push`
- [ ] `curl -I https://jefeerzhang.github.io/master-course/agri-finance/` 验证 200
- [ ] `curl -I https://jefeerzhang.github.io/master-course/第一性原理/第一性原理配图/05_卫星俯瞰农田.jpeg` 验证 6 张图都能 200

## 关键事实
- **cwd**：`C:\Users\jefeer\Downloads\testclaw\projects\master-course`
- **线上 URL 模板**：`https://jefeerzhang.github.io/master-course/agri-finance/`
- **nav 必须包含**：首页 / 个人简历 / 硕士课程 / 知识学习 / 小工具（5 项，按用户指令）
- **配色**：`--color-accent: #245642`（森林绿）
- **字体**：Noto Serif CJK SC + Songti SC（衬线优先，反 Inter 默认）
- **6 张图文件名**：`05_卫星俯瞰农田.jpeg` / `06_五道检验漏斗.jpeg` / `07_卫星遥感机理.jpeg` / `08_物联网耳标.jpeg` / `09_区块链存证.jpeg` / `10_数据资产闭环.jpeg`

## caption 6 条（已脱 AI slop）
- 05 视野：晨光下农田按光谱分层，地块边界和作物长势同时显形。（25 字）
- 06 流程：价值、投资、时效、安全、信用五道筛，把数据资产逐级过成信贷额度。（28 字）
- 07 机理：叶绿素反射近红外，NDVI 把光信号译成作物长势的数字刻度。（26 字）
- 08 数据源：耳标记体温与步数，一头活畜变成 24 小时的数据流。（22 字）
- 09 存证：哈希链把每次权属流转写成时间戳笔迹，篡改一笔全网皆知。（27 字）
- 10 闭环：从卫星到耳标，数据汇成主体画像，反哺下一次信贷决策。（22 字）

## intro 段
1. "六张图按生成顺序排列，恰好走完一次放款的决策回路。先看俯瞰图把信贷对象还原成地块边界与作物长势，再过五道漏斗做风险筛分。中间两张解释技术机理，最后一张回到主体画像。"
2. "这套图不替代任何信贷制度文本。它只回答一个问题：当一家银行打算用卫星和耳标来放款时，它在用哪些证据做判别。"

## hero-summary
"六张认知锚点把卫星、物联、区块链和数据闭环串成一套可验证的农业信贷方法。"

## 关键避坑
- **code_run 默认 type=python**，PowerShell 命令必须用 `subprocess.run(['powershell', '-NoProfile', '-Command', '...'])` 调
- **code_run 必须正文附 Python 代码块**（不是只传 tool 参数）
- **file_write 末尾被截**：6271 bytes 写到 line 160 后停在 `<figcaption class="gallery-caption">`（缺最后 9 行收尾 HTML）
- **git status 输出含中文文件名转义**（UTF-8 字节序列）—— 不影响 commit，只要 path 正确
- **不要 commit `.baoyu-skills/` `comic/` `tests/`**（无关 untracked）
- **em-dash 全禁**：caption 用半角逗号 + 全角句号
- **不要"赋能/打造/构建/平台/解决方案/矩阵"AI 套话**
- **3 段式排比必须拆**（caption/intro 已规避）

## tool bug 史
- code_run 早期 4 次 "Code missing" → 真因：tool 调用后正文没附 Python 代码块
- file_write 写 agri-finance/index.html 6271 bytes 被截 → 真因：content 参数过长被 tool 截断（不是文件本身超限）
- 修复策略：file_patch 用唯一 anchor 补全收尾

## 上下游信息
- 用户 prompt 源：用户已批准 Q1=C（改主页+建子页）+ Q2=A（统一布局）
- 用户授权 GitHub ssh 权限（已配置）
- 远端 master-course repo: `jefeerzhang.github.io`（GitHub Pages）