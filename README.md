# Storyboard 与演示文稿治理

以一份稳定页 ID 的 `Storyboard_Manifest.md` 管理逐页草稿、用户批准和演示文稿核验。适用于具有 Storyboard 的发布会和其他演示文稿项目。

## 核心规则

- 在同一份 Manifest 中从 `draft` 修订到 `approved`，不另建竞争性的草稿文档。
- 用户批准指定版本后，才可将其用于成品制作。
- `slide_id` 表示页面语义，页码由 `order` 派生；PPT 备注通过 `STORYBOARD_ID: <slide_id>` 绑定。
- 用户指定的视频和官网网址记入内部项目登记，并关联稳定 `slide_id`；仅在用户明确要求展示来源时，在 Manifest 增加“用户指定来源”章节。旧 PPT 映射和内容改动仍以 Manifest 为准。

## 校验

```bash
python3 scripts/validate_storyboard_manifest.py Storyboard_Manifest.md
python3 scripts/validate_storyboard_manifest.py Storyboard_Manifest.md --require-approved --page-map Storyboard_Page_Map.json
```

在厂商发布会洞察工作流中，[Vendor Keynote Insights](https://github.com/lwyjames/vendor-keynote-insights) 作为用户入口，内部衔接本 skill。本仓库存放源文件；GitHub 版本与已安装的个人 skill 需分别维护和同步。
