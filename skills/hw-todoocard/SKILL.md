---
name: hw-todoocard (การ์ดอีเปเปอร์)
version: 1.2.0
description: "TodooCard (土豆片 / NEWSTONE) six-colour e-paper push; sub-skill today-eats."
compatibility: >
  Minis iOS with apple-bluetooth; py3-pillow; font-noto-cjk.
  Sub-skills may need apple-location / apple-maps / apple-weather.
tags: [7. Devices + UI, vm, KEEP, OpenMinis/MinisSkills]
---

# todoocard

TodooCard / 土豆片的**父技能**。

- 设备绑定与公共配置
- 共享传输层（六色转换 + BLE 整帧发送）
- 路由到子技能

## 子技能

| 子技能 | 目录 | 触发示例 |
|--------|------|----------|
| 今天吃点啥 | `today-eats/` | 今天吃点啥、中午吃啥、随机外卖、附近吃什么 |

匹配子技能意图时，**先加载该子技能的 `SKILL.md`**，再执行其流程。  
推屏与编码统一用本目录 `scripts/` 与 `references/protocol.md`。

## 设备命令

```bash
ROOT=/srv/repos/hq/vm-hq-core/skills/hw-todoocard
CLI="python3 $ROOT/scripts/safe_send.py"

$CLI scan
$CLI probe --device-id <UUID> --save
$CLI config --show
```

```bash
mkdir -p /srv/repos/hq/vm-hq-core/todoocard
cp $ROOT/references/config.example.json /srv/repos/hq/vm-hq-core/todoocard/config.json
```

## 新增子技能

1. 在 `todoocard/` 下新建目录（如 `weather/`）
2. 编写 `SKILL.md`（name + description + 流程）
3. 脚本放 `scripts/`；需要推屏时引用父级 `../scripts/`（即 `todoocard/scripts`）
4. 更新本文件子技能表

## 依赖

- `apple-bluetooth`、`py3-pillow`、`font-noto-cjk`
- 可选 macOS：`scripts/build_native_sender.sh`

协议：`references/protocol.md`
