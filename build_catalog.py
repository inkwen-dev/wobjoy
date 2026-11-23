"""Render the public Markdown catalog from its shared data. Python 3, no dependencies."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def render():
    data = json.loads((ROOT / 'catalog.json').read_text(encoding='utf-8'))
    assert len({g['id'] for g in data['games']}) == len(data['games'])
    for lang, other in [('en', 'zh-CN'), ('zh-CN', 'en')]:
        zh = lang == 'zh-CN'
        folder = ROOT / 'games' / lang
        folder.mkdir(parents=True, exist_ok=True)
        home = 'README.zh-CN.md' if zh else 'README.md'
        other_home = 'README.md' if zh else 'README.zh-CN.md'
        lines = ['# Wobjoy', '', '![Wobjoy](assets/brand/wordmark.svg)', '',
                 f'[English](README.md) · [简体中文](README.zh-CN.md)', '',
                 '免费浏览器小游戏，打开网页即可游玩。' if zh else 'Free browser games to play without downloading an app.', '',
                 '[访问 Wobjoy](https://wobjoy.com/zh/)' if zh else '[Play on Wobjoy](https://wobjoy.com/)', '',
                 '## 游戏推荐' if zh else '## Featured games', '']
        for game in data['games']:
            text = game[lang]
            play = data['website'] + ('/zh' if zh else '') + game['path']
            image = data['website'] + game['image']
            detail = f"games/{lang}/{game['id']}.md"
            lines.extend([f"### {text['name']}", '', f"[![{text['name']}]({image})]({play})", '', text['summary'], '',
                          f"[{'开始游戏' if zh else 'Play now'}]({play}) · [{'玩法介绍' if zh else 'How to play'}]({detail})", ''])
            page = [f"# {text['name']}", '', f"[English](../en/{game['id']}.md) · [简体中文](../zh-CN/{game['id']}.md)", '',
                    f"![{text['name']}]({image})", '', text['summary'], '',
                    '## 操作与目标' if zh else '## How to play', '', text['controls'], '',
                    f"[{'开始游戏' if zh else 'Play now'}]({play})", '',
                    f"[{'返回游戏目录' if zh else 'Back to the game catalog'}](../../{home})", '']
            (folder / f"{game['id']}.md").write_text('\n'.join(page), encoding='utf-8')
        lines.extend(['## 游戏目录' if zh else '## Game directory', '',
                      '| 游戏 | 介绍 |' if zh else '| Game | Guide |', '| --- | --- |'])
        for game in data['games']:
            play = data['website'] + ('/zh' if zh else '') + game['path']
            lines.append(f"| [{game[lang]['name']}]({play}) | [{'查看玩法' if zh else 'How to play'}](games/{lang}/{game['id']}.md) |")
        lines.extend(['', '本仓库提供游戏介绍与试玩入口，游戏在 Wobjoy 网站运行。' if zh else 'This repository contains game introductions and play links. The games run on the Wobjoy website.', ''])
        (ROOT / home).write_text('\n'.join(lines), encoding='utf-8')

if __name__ == '__main__':
    render()
