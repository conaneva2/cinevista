"""Limited XML structure preview. CSS pixels approximate dp; no Android renderer."""
import html
import json
import xml.etree.ElementTree as ET

A = '{http://schemas.android.com/apk/res/android}'


def render(root):
    strings = {n.get('name'): n.text or '' for n in ET.parse(root/'app/res/values/strings.xml').getroot()}
    styles = {n.get('name'): {A+i.get('name').split(':')[-1]: i.text for i in n}
              for n in ET.parse(root/'app/res/values/styles.xml').getroot()}
    tree = ET.parse(root/'app/res/layout/probe_viewfinder.xml').getroot()

    def node(n):
        if n.tag not in ('LinearLayout', 'FrameLayout', 'TextView', 'Button', 'SurfaceView'):
            raise ValueError('Unsupported sketch view: '+n.tag)
        attrs = dict(styles.get(n.get('style', '').split('/')[-1], {}))
        attrs.update(n.attrib)
        def get(k, default=''):
            return attrs.get(A+k, default)
        css = ['box-sizing:border-box']
        if n.tag == 'LinearLayout':
            css += ['display:flex', 'flex-direction:'+('column' if get('orientation') == 'vertical' else 'row')]
        if n.tag == 'FrameLayout':
            css += ['position:relative', 'overflow:hidden']
        if n.tag == 'SurfaceView':
            # No photo or mock camera feed is injected into the preview.
            return '<div class="empty-feed">未连接相机<br>仅布局预览</div>'
        for axis in ('width', 'height'):
            value = get('layout_'+axis)
            if value == 'match_parent': css.append(axis+':100%')
            elif value.endswith('dp'): css.append(axis+':'+value[:-2]+'px')
        if get('layout_weight'): css += ['flex-grow:'+get('layout_weight'), 'flex-basis:0', 'min-height:0']
        else: css.append('flex-shrink:0')
        mapping = {'minHeight':'min-height', 'padding':'padding', 'paddingLeft':'padding-left',
                   'paddingRight':'padding-right', 'paddingTop':'padding-top', 'paddingBottom':'padding-bottom',
                   'layout_margin':'margin', 'textSize':'font-size', 'textColor':'color'}
        for src, dst in mapping.items():
            value = get(src)
            if value: css.append(dst+':'+value.replace('dp','px').replace('sp','px'))
        if get('background').startswith('#'): css.append('background:'+get('background'))
        if get('gravity') == 'center_vertical': css.append('align-items:center')
        text = get('text')
        if text.startswith('@string/'): text = strings[text.split('/')[-1]]
        elif text.startswith(('@','?')): raise ValueError('Unresolved resource '+text)
        ident = get('id').split('/')[-1]
        tag = 'button' if n.tag == 'Button' else 'div'
        body = html.escape(text.replace('\\n','\n'))+''.join(node(c) for c in n)
        return '<'+tag+' id="'+html.escape(ident)+'" style="'+html.escape(';'.join(css), quote=True)+'">'+body+'</'+tag+'>'

    body = node(tree)
    labels = json.dumps({k:v.replace('\\n','\n') for k,v in strings.items()}, ensure_ascii=True).replace('<','\\u003c')
    return '''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>幕野 · 中文取景页布局</title><style>
body{background:#151619;color:#f7f8f8;font:16px system-ui;margin:24px}main{max-width:980px;margin:auto}
h1{font-size:24px}p{line-height:1.65;color:#cbd0da}a{color:#b1b5ff}
#wrap{overflow:auto;padding:0;background:#070709}#screen{width:640px;height:480px}
#screen div,#screen button{white-space:pre-line}button{font-family:inherit;cursor:pointer}
#screen button{background:#191a1e;border:1px solid #454750;border-radius:6px}
#screen button:focus{outline:3px solid #949aff;outline-offset:-3px;background:#30365c}
.empty-feed{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;text-align:center;color:#9297a1;font-size:18px}
select{font:inherit;margin:12px;padding:6px}dialog{background:#191a1e;color:#f7f8f8;border:2px solid #949aff;max-width:440px}
dialog button{padding:10px;font-size:18px}output{display:block;margin:18px 0;color:#b1b5ff}
</style><main><h1>幕野 · 中文取景页布局</h1>
<p>读取 APK 的 XML 与默认中文资源；这是浏览器结构近似，<strong>不是相机截图或 Android 原生渲染</strong>。
顶部贴边，取景区独立。无设备画面；下方操作仅演示界面状态。</p>
<label>假设视口<select id="viewport"><option value="640,480">640 × 480</option><option value="480,320">480 × 320</option><option value="800,480">800 × 480</option></select></label>
<div id="wrap"><div id="screen">'''+body+'''</div></div>
<output id="message" aria-live="polite">左右键移动焦点，中键可用 Enter 代替。实际 Sony 按键待机测。</output>
<dialog id="settingsDialog"><h2>探针设置</h2><p>相机 APK 的设置中保留 Surface 尺寸实验、重启取景、完整诊断及返回入口。此页不执行相机操作。</p><button id="closeDialog">关闭</button></dialog>
<p><a href="index.html">探针首页</a> · <a href="approved-reference.png">已确认的视觉参考（概念图）</a></p>
<script>
const labels='''+labels+''';
const buttons=[...document.querySelectorAll('#screen button')];
const ratios=['1.0','1.33','1.5','1.6','1.8','2.0'],frames=['65:24','2.39',labels.frame_auto];let r=0,f=0;
const message=document.getElementById('message');
document.getElementById('lens_control').onclick=function(){r=(r+1)%ratios.length;this.textContent=labels.lens_value.replace('%1$s',ratios[r]);message.textContent='仅示意镜头选项；未变换真实内容。'};
document.getElementById('frame_control').onclick=function(){f=(f+1)%frames.length;this.textContent=labels.frame_value.replace('%1$s',frames[f]);message.textContent='仅示意画幅选项；镜头倍率保持不变。'};
document.getElementById('settings_control').onclick=()=>document.getElementById('settingsDialog').showModal();
document.getElementById('closeDialog').onclick=()=>document.getElementById('settingsDialog').close();
buttons.forEach((b,i)=>b.addEventListener('keydown',e=>{if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();buttons[(i+(e.key==='ArrowLeft'?2:1))%3].focus();}}));
document.getElementById('viewport').onchange=function(){const[w,h]=this.value.split(',');const s=document.getElementById('screen');s.style.width=w+'px';s.style.height=h+'px';};
document.getElementById('frame_control').focus({preventScroll:true});
</script></main></html>'''
