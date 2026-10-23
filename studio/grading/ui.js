/* SPDX-License-Identifier: MIT */
(function(){
'use strict';
const G=CineVistaGrade,$=s=>document.getElementById(s);
let params=G.parameters(),lut=null,source=null,graded=null,width=0,height=0;
let wanted=0,accepted=0,inflight=false,pending=null,loading=0,files=[],selected=0,held=false;
let history=[],future=[],editKey=null,dirty=false;
const status=t=>$('status').textContent=t;
const error=t=>$('error').textContent=t||'';
const clone=p=>JSON.parse(JSON.stringify(p));
const workerText=$('worker-core').textContent+'\n'+$('worker-body').textContent;
const workerUrl=URL.createObjectURL(new Blob([workerText],{type:'text/javascript'}));
let worker;
try{worker=new Worker(workerUrl);}catch(e){error('浏览器未允许本地计算 Worker：'+e.message);return;}
worker.onerror=e=>{inflight=false;error('图像计算失败：'+(e.message||'Worker unavailable'));toggleExports();};
function toggleExports(){
 const ready=!!lut&&accepted===wanted;
 $('exportCube').disabled=!ready;$('exportPackage').disabled=!ready||!source||!$('confirmInput').checked;
 $('exportImage').disabled=!ready||!graded;
}
function dispatch(){if(inflight||!pending)return;const m=pending;pending=null;inflight=true;worker.postMessage(m);}
function render(){
 error('');wanted++;toggleExports();
 pending={type:'render',id:wanted,parameters:clone(params),size:Number($('size').value)};
 status('正在更新颜色…');dispatch();
}
worker.onmessage=e=>{
 const m=e.data;inflight=false;
 if(m.id===wanted){
   if(m.type==='error'){error(m.message);status('调色失败；没有导出旧颜色。');}
   else{lut={size:m.size,values:new Float32Array(m.lut)};graded=m.pixels?new Uint8ClampedArray(m.pixels):null;
     accepted=m.id;draw();status((source?'已更新样张':'等待导入样张')+' · '+m.size+'³ LUT · 本次计算 '+Math.round(m.ms)+' ms（当前环境，不是相机速度）');
     document.body.dataset.renderId=String(accepted);
   }
 }
 toggleExports();dispatch();
};
function ctx(canvas){const c=canvas.getContext('2d',{colorSpace:'srgb',willReadFrequently:true,alpha:false});if(!c)throw Error('Canvas 2D unavailable');return c;}
function draw(){
 if(!source||!graded)return;
 const canvas=$('preview');canvas.width=width;canvas.height=height;
 const out=new Uint8ClampedArray(graded),mode=held?'before':$('compare').value;
 const cut=Math.round(width*Number($('split').value)/100);
 if(mode==='before')out.set(source);
 else if(mode==='split')for(let y=0;y<height;y++)out.set(source.subarray(y*width*4,(y*width+cut)*4),y*width*4);
 const c=ctx(canvas);c.putImageData(new ImageData(out,width,height),0,0);
 if(mode==='split'){c.fillStyle='#f8f5e9';c.fillRect(cut,0,1,height);}
 $('empty').hidden=true;canvas.hidden=false;
 $('compareLabel').textContent=mode==='split'?'左：原图 / 右：调色':mode==='before'?'原图':'当前调色';
}
function push(){history.push(clone(params));if(history.length>40)history.shift();future=[];updateUndo();}
function updateUndo(){$('undo').disabled=!history.length;$('redo').disabled=!future.length;}
function commit(key,fn){if(editKey!==key){push();editKey=key;}fn();dirty=true;updateControlValues();render();}
function makeSlider(key,label,min,max,step,read,write,parent){
 const line=document.createElement('div');line.className='param';
 const lab=document.createElement('label');lab.htmlFor='p_'+key;lab.textContent=label;
 const row=document.createElement('div');row.className='sliderline';
 const input=document.createElement('input');input.type='range';input.id='p_'+key;input.min=min;input.max=max;input.step=step;input.value=read();
 const output=document.createElement('output');output.id='v_'+key;output.htmlFor=input.id;output.textContent=read();
 input.addEventListener('input',()=>commit(key,()=>write(Number(input.value))));
 input.addEventListener('change',()=>{editKey=null;});
 line.append(lab);row.append(input,output);line.append(row);parent.append(line);
 input._read=read;
}
function setupControls(){
 G.fields.forEach((f,i)=>makeSlider(f.key,f.label,f.min,f.max,f.step,()=>params[f.key],v=>params[f.key]=v,$(i<9?'basic':'splitTone')));
 ['黑端','暗部','中间调','亮部','白端'].forEach((label,i)=>makeSlider('curve'+i,label,0,100,1,()=>Math.round(params.curve[i]*100),v=>{
   params.curve[i]=Math.min(i===4?1:params.curve[i+1],Math.max(i===0?0:params.curve[i-1],v/100));
 },$('curve')));
 ['红','黄','绿','青','蓝','品红'].forEach((label,i)=>{
   makeSlider('hue'+i,label+' · 色相 / °',-30,30,1,()=>params.hue[i],v=>params.hue[i]=v,$('selective'));
   makeSlider('chroma'+i,label+' · 饱和度',-100,100,1,()=>params.chroma[i],v=>params.chroma[i]=v,$('selective'));
 });
}
function updateControlValues(){
 document.querySelectorAll('input[type=range][id^=p_]').forEach(el=>{el.value=el._read();$('v_'+el.id.slice(2)).textContent=el.value;});
 const curve=$('curvePreview'),c=ctx(curve);c.clearRect(0,0,curve.width,curve.height);c.fillStyle='#f2f1ed';c.fillRect(0,0,curve.width,curve.height);
 c.strokeStyle='#cbd5ce';c.lineWidth=1;c.beginPath();c.moveTo(0,curve.height);c.lineTo(curve.width,0);c.stroke();
 c.strokeStyle='#224e41';c.lineWidth=2;c.beginPath();params.curve.forEach((v,i)=>{const x=i*curve.width/4,y=(1-v)*curve.height;if(i)c.lineTo(x,y);else c.moveTo(x,y);});c.stroke();
}
function meta(){return {id:$('id').value.trim(),name:$('name').value.trim(),size:Number($('size').value),baseline:$('baseline').value.trim()};}
function download(text,name,type){const u=URL.createObjectURL(new Blob([text],{type:type||'text/plain;charset=utf-8'}));const a=document.createElement('a');a.href=u;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(u),5000);}
function ready(){if(!lut||accepted!==wanted)throw Error('颜色仍在更新；请等当前效果完成后再导出');}
function action(fn){try{error('');fn();}catch(e){error(e.message);}}
function tabs(){
 $('sampleTabs').replaceChildren();files.forEach((f,i)=>{const b=document.createElement('button');b.className=i===selected?'small':'small secondary';b.textContent=(i+1)+' · '+f.name;b.title=f.name;
 b.addEventListener('click',()=>{selected=i;tabs();load(f);});$('sampleTabs').append(b);});
}
async function load(file){
 const token=++loading;wanted++;pending=null;accepted=0;source=null;graded=null;worker.postMessage({type:'image',pixels:null});
 $('preview').hidden=true;$('empty').hidden=false;$('empty').textContent='正在读取样张…';$('photoMeta').textContent='';
 $('confirmInput').checked=false;toggleExports();error('');status('正在读取本地样张…');
 if(!['image/jpeg','image/png'].includes(file.type)){error('当前只接收 JPEG / PNG；RAW、HEIC、Log/HDR 管线不在此版支持范围。');return;}
 if(file.size>50*1024*1024){error('单张文件上限 50 MiB');return;}
 let u=URL.createObjectURL(file);
 try{
  const image=new Image();await new Promise((resolve,reject)=>{image.onload=resolve;image.onerror=()=>reject(Error('无法解码该图片'));image.src=u;});
  if(token!==loading)return;
  if(image.naturalWidth*image.naturalHeight>65000000)throw Error('此原型限制输入为 6500 万像素以内');
  const max=Number($('resolution').value),s=Math.min(1,max/Math.max(image.naturalWidth,image.naturalHeight));
  width=Math.max(1,Math.round(image.naturalWidth*s));height=Math.max(1,Math.round(image.naturalHeight*s));
  const temp=document.createElement('canvas');temp.width=width;temp.height=height;const c=ctx(temp);c.fillStyle='#fff';c.fillRect(0,0,width,height);c.drawImage(image,0,0,width,height);
  const a=c.getContextAttributes?.();if(a?.colorSpace&&a.colorSpace!=='srgb')throw Error('未获得 sRGB 画布，停止调色');
  const pixels=c.getImageData(0,0,width,height,{colorSpace:'srgb'});source=new Uint8ClampedArray(pixels.data);graded=null;
  const sent=source.slice();worker.postMessage({type:'image',pixels:sent.buffer},[sent.buffer]);
  $('photoMeta').textContent=file.name+' · 源 '+image.naturalWidth+'×'+image.naturalHeight+' · 预览 '+width+'×'+height+' · sRGB 画布';
  render();
 }catch(e){error(e.message);status('没有载入该图片');}finally{URL.revokeObjectURL(u);}
}
$('photos').addEventListener('change',e=>{
 const chosen=Array.from(e.target.files||[]).slice(0,6);if(!chosen.length)return;
 files=chosen;selected=0;tabs();load(files[0]);e.target.value='';
});
$('resolution').addEventListener('change',()=>{if(files[selected])load(files[selected]);});
$('size').addEventListener('change',()=>{dirty=true;render();});
$('compare').addEventListener('change',draw);$('split').addEventListener('input',draw);
$('hold').addEventListener('pointerdown',e=>{held=true;e.target.setPointerCapture(e.pointerId);draw();});
for(const type of ['pointerup','pointercancel','lostpointercapture'])$('hold').addEventListener(type,()=>{held=false;draw();});
$('hold').addEventListener('keydown',e=>{if(e.code==='Space'||e.code==='Enter'){e.preventDefault();held=true;draw();}});
$('hold').addEventListener('keyup',()=>{held=false;draw();});$('hold').addEventListener('blur',()=>{held=false;draw();});
$('undo').addEventListener('click',()=>{if(!history.length)return;future.push(clone(params));params=history.pop();editKey=null;dirty=true;updateUndo();updateControlValues();render();});
$('redo').addEventListener('click',()=>{if(!future.length)return;history.push(clone(params));params=future.pop();editKey=null;dirty=true;updateUndo();updateControlValues();render();});
$('reset').addEventListener('click',()=>{push();params=G.parameters();editKey=null;dirty=true;updateControlValues();render();});
$('saveProject').addEventListener('click',()=>action(()=>{const p=G.project(params,meta());download(JSON.stringify(p,null,2)+'\n',p.id+'.CVG','application/json');dirty=false;status('已导出可继续编辑的工程；不包含样张。');}));
$('exportCube').addEventListener('click',()=>action(()=>{ready();const p=G.project(params,meta());download(G.cube(lut,p.id),p.id+'.CUBE');status('已导出当前预览所用 LUT。使用方须按 sRGB 全范围、三线性插值解释。');}));
$('exportPackage').addEventListener('click',()=>action(()=>{ready();if(!$('confirmInput').checked||!source)throw Error('先载入样张并确认 sRGB 输入基线');
 const pack=G.makePackage(params,meta(),lut);download(JSON.stringify(pack,null,2)+'\n',pack.project.id+'.CVP','application/json');
 status('已导出相机素材包草稿；Camera 导入/应用尚未接入，不是 Sony 原生预设。');}));
$('exportImage').addEventListener('click',()=>action(()=>{ready();if(!graded)throw Error('尚未载入样张');
 const p=G.project(params,meta()),c=document.createElement('canvas');c.width=width;c.height=height;ctx(c).putImageData(new ImageData(graded,width,height),0,0);
 c.toBlob(blob=>{if(!blob){error('PNG 导出失败');return;}download(blob,p.id+'_PREVIEW.png','image/png');status('已导出 '+width+'×'+height+' 预览 PNG，不是原尺寸相机成片。');},'image/png');}));
$('openProject').addEventListener('change',async e=>{const f=e.target.files[0];try{if(!f)return;if(f.size>65536)throw Error('工程文件超过 64 KiB');const p=G.parseProject(await f.text());
 push();params=p.parameters;editKey=null;$('id').value=p.id;$('name').value=p.name;$('size').value=p.size;$('baseline').value=p.input.camera_baseline;
 $('confirmInput').checked=false;updateControlValues();render();dirty=false;
 }catch(err){error(err.message);}finally{e.target.value='';}});
$('confirmInput').addEventListener('change',toggleExports);
for(const key of ['name','id','baseline'])$(key).addEventListener('input',()=>{dirty=true;});
window.addEventListener('beforeunload',e=>{if(dirty){e.preventDefault();e.returnValue='';}});
window.addEventListener('pagehide',()=>{worker.terminate();URL.revokeObjectURL(workerUrl);});
setupControls();updateControlValues();updateUndo();render();
})();
