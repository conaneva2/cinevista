/* SPDX-License-Identifier: MIT
 * CineVista software-look prototype. NOT a Sony CS/PP emulator.
 * Browser decoding/colour conversion/resampling are provided by the platform.
 * Small bounded RGB LUT contract; no general RAW, ICC or LUT framework here.
 */
(function (root) {
  'use strict';
  const VERSION = 'cinevista-rgb-look/0.2';
  const fields = [
    ['exposure','数字亮度 / EV',0,-2,2,0.05],
    ['temperature','冷暖（创作偏色，非相机 K 值）',0,-100,100,1],
    ['tint','绿 / 洋红（创作偏色）',0,-100,100,1],
    ['contrast','对比度',0,-100,100,1],
    ['saturation','饱和度',0,-100,100,1],
    ['vibrance','低饱和色增强',0,-100,100,1],
    ['shadows','暗部亮度',0,-100,100,1],
    ['highlights','亮部亮度',0,-100,100,1],
    ['fade','黑位抬升',0,0,100,1],
    ['shadowWarmth','阴影冷暖',0,-100,100,1],
    ['highlightWarmth','高光冷暖',0,-100,100,1],
    ['shadowTint','阴影绿 / 洋红',0,-100,100,1],
    ['highlightTint','高光绿 / 洋红',0,-100,100,1]
  ].map(x=>({key:x[0],label:x[1],value:x[2],min:x[3],max:x[4],step:x[5]}));
  const clamp = x => Math.min(1,Math.max(0,x));
  const cleanText = (s,n) => typeof s==='string' && s.length<=n && !/[\x00-\x08\x0b\x0c\x0e-\x1f]/.test(s);
  function parameters() {
    const p={}; fields.forEach(f=>p[f.key]=f.value);
    p.curve=[0,0.25,0.5,0.75,1];p.hue=[0,0,0,0,0,0];p.chroma=[0,0,0,0,0,0];return p;
  }
  function validate(p) {
    if(!p || typeof p!=='object' || Array.isArray(p))throw Error('调色参数必须为对象');
    const allowed=fields.map(f=>f.key).concat(['curve','hue','chroma']);
    if(Object.keys(p).some(k=>!allowed.includes(k)))throw Error('不支持的调色参数');
    fields.forEach(f=>{if(typeof p[f.key]!=='number'||!Number.isFinite(p[f.key])||p[f.key]<f.min||p[f.key]>f.max)throw Error('参数超出范围: '+f.key);});
    for(const [key,n,lo,hi] of [['curve',5,0,1],['hue',6,-30,30],['chroma',6,-100,100]]){
      if(!Array.isArray(p[key])||p[key].length!==n||p[key].some(v=>typeof v!=='number'||!Number.isFinite(v)||v<lo||v>hi))throw Error('无效数组: '+key);
    }
    if(p.curve.some((v,i)=>i>0&&v<p.curve[i-1]))throw Error('明暗曲线必须单调；不能让高输入点低于前一点');
    return p;
  }
  const decode = x => x<=0.04045?x/12.92:Math.pow((x+0.055)/1.055,2.4);
  const encode = x => x<=0.0031308?12.92*x:1.055*Math.pow(x,1/2.4)-0.055;
  function curve(x,a){x=clamp(x)*4;const i=Math.min(3,Math.floor(x));return a[i]+(a[i+1]-a[i])*(x-i);}
  function rgbToHsv(r,g,b){
    const max=Math.max(r,g,b),min=Math.min(r,g,b),d=max-min;let h=0;
    if(d>1e-12){if(max===r)h=(g-b)/d+(g<b?6:0);else if(max===g)h=(b-r)/d+2;else h=(r-g)/d+4;h/=6;}
    return [h,max===0?0:d/max,max];
  }
  function hsvToRgb(h,s,v){h=((h%1)+1)%1*6;const i=Math.floor(h),f=h-i,p=v*(1-s),q=v*(1-f*s),t=v*(1-(1-f)*s);
    return [[v,t,p],[q,v,p],[p,v,t],[p,q,v],[t,p,v],[v,p,q]][i%6];}
  function transform(r,g,b,p){
    const e=Math.pow(2,p.exposure);
    const warm=p.temperature/100,tint=p.tint/100;
    r=encode(decode(r)*e*Math.pow(2,0.30*warm+0.10*tint));
    g=encode(decode(g)*e*Math.pow(2,-0.20*tint));
    b=encode(decode(b)*e*Math.pow(2,-0.30*warm+0.10*tint));
    const y=clamp(0.2126*r+0.7152*g+0.0722*b), dark=(1-y)*(1-y), light=y*y;
    const offset=0.22*(p.shadows/100*dark+p.highlights/100*light);
    const w=(p.shadowWarmth*dark+p.highlightWarmth*light)/100*0.075;
    const t=(p.shadowTint*dark+p.highlightTint*light)/100*0.060;
    r+=offset+w+t*.5;g+=offset-t;b+=offset-w+t*.5;
    const k=Math.pow(2,p.contrast/100);
    const adjust=x=>curve(clamp((x-0.5)*k+0.5)+p.fade/100*0.1*Math.pow(1-clamp(x),2),p.curve);
    r=adjust(r);g=adjust(g);b=adjust(b);
    let lum=.2126*r+.7152*g+.0722*b;
    const hi=Math.max(r,g,b),lo=Math.min(r,g,b),sat0=hi>0?(hi-lo)/hi:0;
    const sat=Math.max(0,(1+p.saturation/100)*(1+p.vibrance/100*(1-sat0)));
    r=clamp(lum+(r-lum)*sat);g=clamp(lum+(g-lum)*sat);b=clamp(lum+(b-lum)*sat);
    if(p.hue.some(x=>x!==0)||p.chroma.some(x=>x!==0)){
      let [h,s,v]=rgbToHsv(r,g,b);const pos=h*6,i=Math.floor(pos)%6,f=pos-Math.floor(pos),j=(i+1)%6;
      h+=(p.hue[i]*(1-f)+p.hue[j]*f)/360;
      s=clamp(s*(1+(p.chroma[i]*(1-f)+p.chroma[j]*f)/100));
      [r,g,b]=hsvToRgb(h,s,v);
    }
    return [clamp(r),clamp(g),clamp(b)];
  }
  function buildLut(p,size=33){
    validate(p);if(![17,33].includes(size))throw Error('本原型仅支持 17³ 或 33³');
    const values=new Float32Array(3*size*size*size);let o=0;
    // Iridas .cube: red varies fastest, then green, then blue.
    for(let b=0;b<size;b++)for(let g=0;g<size;g++)for(let r=0;r<size;r++){
      const v=transform(r/(size-1),g/(size-1),b/(size-1),p);
      values[o++]=v[0];values[o++]=v[1];values[o++]=v[2];
    }
    return {size,values};
  }
  function checkLut(lut){
    if(!lut||![17,33].includes(lut.size)||!(lut.values instanceof Float32Array)||lut.values.length!==3*lut.size**3)throw Error('无效 LUT');
    for(const v of lut.values)if(!Number.isFinite(v)||v<0||v>1)throw Error('LUT 仅支持有限 0–1 数值');return lut;
  }
  function sample(lut,r,g,b,out=[0,0,0]){
    const n=lut.size,m=n-1;
    const x=clamp(r)*m,y=clamp(g)*m,z=clamp(b)*m;
    const ix=Math.min(m-1,Math.floor(x)),iy=Math.min(m-1,Math.floor(y)),iz=Math.min(m-1,Math.floor(z));
    const dx=x-ix,dy=y-iy,dz=z-iz,a=lut.values;
    const i=3*(ix+n*(iy+n*iz)),sy=n*3,sz=n*n*3;
    for(let c=0;c<3;c++){
      const p=i+c;
      const u0=a[p]*(1-dx)+a[p+3]*dx,u1=a[p+sy]*(1-dx)+a[p+sy+3]*dx;
      const u2=a[p+sz]*(1-dx)+a[p+sz+3]*dx,u3=a[p+sz+sy]*(1-dx)+a[p+sz+sy+3]*dx;
      out[c]=(u0*(1-dy)+u1*dy)*(1-dz)+(u2*(1-dy)+u3*dy)*dz;
    }return out;
  }
  function apply(lut,rgba){
    checkLut(lut);if(!rgba||rgba.length%4)throw Error('需要 RGBA 像素');
    const out=new Uint8ClampedArray(rgba.length),v=[0,0,0];
    for(let i=0;i<rgba.length;i+=4){sample(lut,rgba[i]/255,rgba[i+1]/255,rgba[i+2]/255,v);
      out[i]=Math.floor(clamp(v[0])*255+.5);out[i+1]=Math.floor(clamp(v[1])*255+.5);out[i+2]=Math.floor(clamp(v[2])*255+.5);out[i+3]=rgba[i+3];}
    return out;
  }
  function cube(lut,id='MYLOOK01'){
    checkLut(lut);if(!/^[A-Z0-9_]{1,8}$/.test(id))throw Error('文件代号须为 1–8 位大写字母、数字或下划线');
    const rows=['TITLE "'+id+'"','# CineVista software look. sRGB full-range -> sRGB full-range.',
      '# Interpolation contract: trilinear; no Sony PP/CS emulation.',
      'LUT_3D_SIZE '+lut.size,'DOMAIN_MIN 0 0 0','DOMAIN_MAX 1 1 1'];
    for(let i=0;i<lut.values.length;i+=3)rows.push([lut.values[i],lut.values[i+1],lut.values[i+2]].map(x=>x.toPrecision(9)).join(' '));
    return rows.join('\n')+'\n';
  }
  function project(p,meta){
    validate(p);meta=meta||{};
    if(!/^[A-Z0-9_]{1,8}$/.test(meta.id||''))throw Error('配方代号须为 1–8 位大写字母、数字或下划线');
    if(!cleanText(meta.name,64)||!meta.name.trim())throw Error('请填写配方名称');
    if(!cleanText(meta.baseline||'',600))throw Error('源设置说明过长或包含控制字符');
    if(![17,33].includes(meta.size))throw Error('无效 LUT 尺寸');
    return {schema:'cinevista.grade/1',algorithm:VERSION,id:meta.id,name:meta.name,size:meta.size,
      input:{encoding:'sRGB',range:'full',stage:'jpeg-before-software-look',camera_baseline:meta.baseline||''},
      output:{encoding:'sRGB',range:'full'},interpolation:'trilinear',parameters:JSON.parse(JSON.stringify(p)),
      camera_status:'unverified'};
  }
  function parseProject(text){
    if(typeof text!=='string'||new TextEncoder().encode(text).length>65536)throw Error('工程文件过大');
    const v=JSON.parse(text);
    if(!v||v.schema!=='cinevista.grade/1'||v.algorithm!==VERSION)throw Error('工程版本或调色算法不兼容');
    const allowed=['schema','algorithm','id','name','size','input','output','interpolation','parameters','camera_status'];
    if(Object.keys(v).some(k=>!allowed.includes(k)))throw Error('工程包含未知字段');
    if(v.camera_status!=='unverified'||v.interpolation!=='trilinear'||v.input?.encoding!=='sRGB'||v.input?.range!=='full'||v.input?.stage!=='jpeg-before-software-look'||v.output?.encoding!=='sRGB'||v.output?.range!=='full')throw Error('此原型只支持未认证的 sRGB 全范围软件颜色工程');
    return project(v.parameters,{id:v.id,name:v.name,size:v.size,baseline:v.input.camera_baseline});
  }
  function makePackage(p,meta,lut){
    const v=project(p,meta);if(!v.input.camera_baseline.trim())throw Error('先记录样张的相机颜色设置，避免机内重复上色');
    if(lut.size!==v.size)throw Error('LUT 分辨率不一致');
    return {schema:'cinevista.lut-package/1',status:'draft-camera-importer-not-implemented',project:v,
      payload:{kind:'iridas-cube',text:cube(lut,v.id)},notes:'离线软件调色数据；不是 Sony 原生 Picture Profile；原片应保留。'};
  }
  const api={VERSION,fields,parameters,validate,transform,buildLut,checkLut,sample,apply,cube,project,parseProject,makePackage};
  if(typeof module==='object'&&module.exports)module.exports=api;root.CineVistaGrade=api;
}(typeof globalThis==='undefined'?this:globalThis));
