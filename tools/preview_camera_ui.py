#!/usr/bin/env python3
"""Offline structural sketch of probe_home.xml, not an Android renderer.

Only this small home layout is supported. No camera backend, images, or UI
success events are simulated. Native appearance requires Android tooling.
"""
import hashlib
import html
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = 'app/res/layout/probe_home.xml'
A = '{http://schemas.android.com/apk/res/android}'


def node_html(node, strings=None):
    tags = {'ScrollView': 'section', 'LinearLayout': 'div',
            'TextView': 'p', 'Button': 'button'}
    if node.tag not in tags:
        raise ValueError('Unsupported sketch view: ' + node.tag)
    text = node.get(A + 'text', '')
    if text.startswith('@string/') and strings is not None:
        key = text.split('/', 1)[1]
        if key not in strings:
            raise ValueError('Missing default string: ' + key)
        text = strings[key]
    elif text.startswith(('@', '?')):
        raise ValueError('Unresolved resource: ' + text)
    if node.tag == 'LinearLayout' and node.get(A + 'orientation') != 'vertical':
        raise ValueError('Only the vertical home layout is supported')
    tag = tags[node.tag]
    # Platform text is escaped; never inject Android XML into executable HTML.
    content = html.escape(text.replace('\\n', '\n'))
    content += ''.join(node_html(child, strings) for child in node)
    return '<' + tag + '>' + content + '</' + tag + '>'


def render(root=ROOT):
    path = root / LAYOUT
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    strings = {n.get('name'): n.text or '' for n in ET.parse(root/'app/res/values/strings.xml').getroot()}
    content = node_html(ET.parse(path).getroot(), strings)
    return '''<!doctype html><html lang="zh-CN"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>幕野 · 相机首页结构预览</title>
<style>
*{box-sizing:border-box}body{margin:0;padding:28px;background:#15191d;color:#ecf0f2;
font:16px system-ui,sans-serif}main{max-width:1000px;margin:auto}h1{font-size:24px}
.note{color:#cad2db;line-height:1.7;max-width:850px}label{display:block;margin:18px 0}
select{font:inherit;padding:6px;background:#252c34;color:white}
.frame{overflow:auto;padding:12px;background:#252c34;border-radius:12px}
#screen{width:640px;height:480px;background:black;color:white;font:14px sans-serif}
section{height:100%;overflow-y:auto}section>div{display:flex;flex-direction:column}
section p{white-space:pre-wrap;margin:0;line-height:1.3}section p:first-child{font-size:18px}
button{font:14px sans-serif;min-height:48px;margin:2px 0;padding:8px;color:#f7f8f8;
background:#191a1e;border:2px solid #454750;border-radius:3px;flex-shrink:0}
button:focus-visible{outline:3px solid #949aff;outline-offset:-4px;background:#30365c}
output{display:block;min-height:3em;margin:16px 0;color:#f0c674}code{word-break:break-all;font-size:12px}
</style><main><h1>幕野 · 相机首页结构预览</h1><p><a style="color:#b1b5ff" href="viewfinder.html">打开新版取景页布局预览</a></p>
<p class="note">从 APK 使用的同一份 XML 生成。<strong>这是布局草图，不是相机截图，也不是 Android 精确渲染。</strong>
用于检查文字、按钮顺序与小屏滚动；字体、控件尺寸、焦点和像素比例需原生验证。
取景页、自绘框、颜色和相机行为没有被模拟。这仍是工程探针首页。</p>
<label>假设布局视口（CSS 像素，并非已测 A7R II 屏幕）
<select id="size"><option value="640,480">640 × 480</option>
<option value="800,480">800 × 480</option><option value="480,320">480 × 320</option></select></label>
<div class="frame"><div id="screen">''' + content + '''</div></div>
<output id="feedback" aria-live="polite">点击只标记所选入口；Tab / Shift+Tab 检查浏览器焦点顺序。</output>
<p class="note">布局来源：<code>''' + LAYOUT + '''</code><br>SHA256：<code>''' + digest + '''</code></p>
<script>
document.getElementById('size').addEventListener('change',function(){
 const [w,h]=this.value.split(',');const s=document.getElementById('screen');
 s.style.width=w+'px';s.style.height=h+'px';
});
document.querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{
 document.getElementById('feedback').textContent='已选择：'+b.textContent+'。仅结构预览，未执行设备操作。';
}));
</script></main></html>'''


if __name__ == '__main__':
    output = ROOT / 'build/camera-ui/index.html'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(), encoding='utf-8')
    from viewfinder_sketch import render as render_viewfinder
    (output.parent/'viewfinder.html').write_text(render_viewfinder(ROOT), encoding='utf-8')
    print(output)
    print(output.parent/'viewfinder.html')
