/* SPDX-License-Identifier: MIT */
'use strict';
const C=CineVistaLook, $=id=>document.getElementById(id);
let draft=C.make('sony-creative-style'),urls={};
function bind(){
  $('engine').value=draft.engine;
  for(const k of ['name','id','revision','notes'])$(k).value=draft[k];
  $('author').value=draft.provenance.author;$('firmware').value=draft.target.firmware||'';$('ev').value=draft.exposure.suggested_ev_thirds;
  $('parameters').replaceChildren();
  C.engines[draft.engine].forEach(f=>{
    const line=document.createElement('div');line.className='param';const lab=document.createElement('label');lab.textContent=f.label;
    const input=document.createElement(f.type==='enum'?'select':'input');input.id='p_'+f.key;input.setAttribute('aria-label',f.label);
    if(f.type==='enum')f.values.forEach(v=>{const opt=document.createElement('option');opt.value=v;opt.textContent=v;input.append(opt);});
    else{input.type='range';input.min=f.min;input.max=f.max;input.step=f.key==='wb_kelvin'?100:1;}
    input.value=draft.parameters[f.key];const val=document.createElement('output');val.textContent=input.value;
    input.addEventListener('input',()=>{draft.parameters[f.key]=f.type==='enum'?input.value:Number(input.value);val.textContent=input.value;refresh();});
    if(f.type==='enum')lab.append(input);line.append(lab);if(f.type!=='enum')line.append(input,val);$('parameters').append(line);
  });refresh();
}
function refresh(){
  const errors=C.validate(draft);$('errors').textContent=errors.join('\n');$('export').disabled=$('manual').disabled=errors.length>0;
  $('json').textContent=JSON.stringify(draft,null,2);$('warnings').replaceChildren();
  C.warnings(draft).forEach(t=>{const p=document.createElement('p');p.textContent=t;$('warnings').append(p);});
}
function download(text,name,type){const u=URL.createObjectURL(new Blob([text],{type}));const a=document.createElement('a');a.href=u;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(u),3000);}
for(const k of ['name','id','revision','notes'])$(k).addEventListener('input',()=>{draft[k]=k==='revision'?Number($(k).value):$(k).value;refresh();});
$('author').addEventListener('input',()=>{draft.provenance.author=$('author').value;refresh();});
$('firmware').addEventListener('input',()=>{draft.target.firmware=$('firmware').value.trim()||null;refresh();});
$('ev').addEventListener('input',()=>{draft.exposure.suggested_ev_thirds=Number($('ev').value);refresh();});
$('engine').addEventListener('change',()=>{
 const keep=draft;const next=C.make($('engine').value);
 if(!confirm('切换颜色路径将重置本页参数。请先导出要保留的草稿。继续？')){$('engine').value=draft.engine;return;}
 for(const k of ['name','id','revision','notes','provenance','target'])next[k]=keep[k];draft=next;bind();
});
$('export').addEventListener('click',()=>{try{download(C.serialize(draft),draft.id+'.CVL','application/json');$('status').textContent='已导出配方草稿。不是相机适配认证，当前 APK 尚不能自动导入。';}catch(e){$('errors').textContent=e.message;}});
$('manual').addEventListener('click',()=>{try{download(C.manual(draft),draft.id+'_SETUP.txt','text/plain;charset=utf-8');$('status').textContent='已导出手工设置单。请先记录原相机设置，按实际菜单逐项核对。';}catch(e){$('errors').textContent=e.message;}});
$('import').addEventListener('change',async e=>{try{const f=e.target.files[0];if(!f)return;if(f.size>C.maxBytes)throw Error('文件超过64 KiB');const d=C.parse(await f.text());draft=d;bind();$('status').textContent='已导入草稿，保留来源信息；设备状态仍未验证。';}catch(err){$('errors').textContent=err.message;}finally{e.target.value='';}});
for(const key of ['A','B'])$('photo'+key).addEventListener('change',e=>{
 const f=e.target.files[0];if(!f)return;
 if(!['image/jpeg','image/png'].includes(f.type)||f.size>30*1024*1024){$('status').textContent='请选不超过30 MiB的JPEG/PNG样片；浏览器显示不代表原生颜色校准。';return;}
 if(urls[key])URL.revokeObjectURL(urls[key]);urls[key]=URL.createObjectURL(f);$('image'+key).src=urls[key];$('image'+key).alt='本地实拍样片 '+key;
 $('caption'+key).textContent=f.name+' · 不应用本页参数，不上传';
});
window.addEventListener('beforeunload',()=>Object.values(urls).forEach(URL.revokeObjectURL));bind();
