# 可选普通话语音包

核验日期：2026-10-26。

本次使用 Microsoft Edge neural TTS，经 `edge-tts` 生成。音轨是 AI 合成普通话，并非真人录音、名人模仿或声音克隆；不使用 OpenAI 的语音模型。仅提交本项目已经编写的公开导览文字，不提交访客数据。

## 三种声音

| ID | 名称 | 内置声音 | 生成语速 | 音高 | 资源前缀 |
| --- | --- | --- | --- | --- | --- |
| xiaoxiao | 温润讲述 | zh-CN-XiaoxiaoNeural | -8% | +0Hz | assets/audio |
| yunxi | 沉静男声 | zh-CN-YunxiNeural | -10% | +0Hz | assets/audio/packs/yunxi |
| xiaoyi | 清亮女声 | zh-CN-XiaoyiNeural | -6% | +0Hz | assets/audio/packs/xiaoyi |

三种声音已通过实时语音目录核对。语气名称只是帮助用户选择的界面说明，不代表真人或专业配音师。三段试听使用相同原文，便于比较。

## 原文与覆盖范围

每套保留 23 段原有导览：5 馆各 3 章，以及 8 个工艺主题。每个音轨旁的 JSON 保留完全相同的 `text`、供应商句级 `sentences` 时间及声音和语速参数。原有默认包的文字指纹保持兼容。

新增世界遗产简介读取 `dist/world-heritage-data.js` 每项冻结后的 `narrationText`，每套对应 46 个简介。遗产的后续阅读章节仍为阅读内容，未冒充已经配音。

## 音量与时间轴

采用 FFmpeg 两遍 EBU R128 响度处理，目标 -18 LUFS、真峰值上限 -1.5 dBTP、LRA 11。保留单声道 24 kHz、48 kbps MP3；不裁掉头尾，不手动插入停顿，不改写文字。较慢的生成语速与原文句读形成停顿。

处理成功后 JSON 写入 `audioProcessing`，重跑会跳过已处理音轨，避免再次压缩。原始 `build_audio.py` 仍能识别默认包文字缓存；重新生成的原始音轨应再运行新生成器的响度处理。

## 重现

```powershell
python -m pip install --target .runtime edge-tts imageio-ffmpeg
python scripts/build_voice_packs.py --previews
python scripts/build_voice_packs.py
python scripts/build_voice_packs.py --verify
```

生成器以文字、声音、语速、音高作指纹缓存。生成请求并发最多 2，失败最多重试 3 次；未完成文件写为 `.part`，成功后才成为 MP3。仅更新遗产时使用 `--heritage-only`，仅处理已有资源响度使用 `--normalize-only`。

逐段解码与测量结果写入 `research/voice-packs-measurements.json`，包括声音、时长、字节数、实际集成响度和真峰值。验证同时核对当前目录原文、句级时间范围、非静音响度及无削波。该验证不等同于专业普通话配音审听。

## 本次最终结果

`python scripts/build_voice_packs.py --verify` 成功：210 段全部解码并通过原文、声音、语速、句级时间、响度与峰值核验。其中 207 段为正式导览，3 段为试听。没有未完成 `.part` 资源。

| 声音 | 含试听的片段数 | MP3 解码后集成响度范围 |
| --- | ---: | --- |
| 温润讲述 | 70 | -18.59 至 -18.32 LUFS |
| 沉静男声 | 70 | -19.01 至 -18.44 LUFS |
| 清亮女声 | 70 | -18.46 至 -18.30 LUFS |

全体最高解码真峰值为 -0.63 dBTP，没有达到 0 dBTP；MP3 有损编码会令重建峰值与编码前的 -1.5 dBTP 目标产生差异。所有片段合计 38,311,224 字节，时长为 12.29–36.07 秒（含试听）。景德镇三包简介已按最终题名“景德镇手工瓷业遗存”重生并再次核验。
