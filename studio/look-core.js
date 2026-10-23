/* SPDX-License-Identifier: MIT
 * CineVista Studio authoring contract. NOT a Sony emulator or a camera driver.
 * No vendor numeric IDs, addresses or writable firmware slots are accepted.
 */
(function (root) {
  'use strict';
  const field = (key, label, value, min, max) => ({key,label,default:value,min,max,type:'integer'});
  const choice = (key,label,value,values) => ({key,label,default:value,values,type:'enum'});
  const WB = [choice('wb_mode','白平衡模式','auto',['auto','kelvin']),
    field('wb_kelvin','色温 K（仅 Kelvin 模式）',5500,2500,9900),
    field('wb_amber_blue','白平衡 A/B：正值为 Amber',0,-7,7),
    field('wb_green_magenta','白平衡 G/M：正值为 Green',0,-7,7)];
  const CS = [choice('style','Creative Style','neutral',['standard','vivid','neutral','clear','deep','light','portrait','landscape','sunset','night','autumn','monochrome','sepia']),
    field('contrast','对比度（标准菜单范围）',0,-3,3),field('saturation','饱和度（标准菜单范围）',0,-3,3),
    field('sharpness','锐度（标准菜单范围）',0,-3,3),choice('dro','DRO','off',['off','auto','1','2','3','4','5'])];
  const PP = [choice('gamma','Gamma','Still',['Movie','Still','Cine1','Cine2','Cine3','Cine4','ITU709','ITU709(800%)','S-Log2']),
    choice('color_mode','Color Mode','Still',['Movie','Still','Cinema','Pro','ITU709 Matrix','Black & White','S-Gamut']),
    field('black_level','Black Level',0,-15,15),choice('black_gamma_range','Black Gamma Range','Middle',['Wide','Middle','Narrow']),
    field('black_gamma_level','Black Gamma Level',0,-7,7),choice('knee_mode','Knee Mode','Auto',['Auto','Manual']),
    field('knee_auto_max','Auto Knee Max Point %',100,90,100),choice('knee_auto_sensitivity','Auto Knee Sensitivity','Mid',['High','Mid','Low']),
    field('knee_manual_point','Manual Knee Point %',90,75,105),field('knee_manual_slope','Manual Knee Slope',0,-5,5),
    field('saturation','Saturation（PP 独立范围）',0,-32,32),field('color_phase','Color Phase',0,-7,7),
    ...['R','G','B','C','M','Y'].map(k=>field('depth_'+k,'Color Depth '+k,0,-7,7)),
    field('detail_level','Detail Level',0,-7,7),choice('detail_mode','Detail Adjust Mode','Auto',['Auto','Manual']),
    field('detail_vh_balance','Detail V/H Balance',0,-2,2),choice('detail_bw_balance','Detail B/W Balance','Type3',['Type1','Type2','Type3','Type4','Type5']),
    field('detail_limit','Detail Limit',7,0,7),field('detail_crispning','Detail Crispning',0,0,7),field('detail_highlight','Hi-Light Detail',0,0,4)];
  const engines = {'sony-creative-style':CS.concat(WB), 'sony-picture-profile':PP.concat(WB)};
  const maxBytes = 65536;
  function make(engine) {
    if (!engines[engine]) throw Error('Unknown engine');
    let params={};engines[engine].forEach(f=>{params[f.key]=f.default;});
    return {schema:'cinevista.look/1',id:'MYLOOK01',name:'我的胶片配方',revision:1,
      target:{model:'ILCE-7RM2',firmware:null},engine,parameters:params,
      exposure:{policy:'manual',suggested_ev_thirds:0},
      provenance:{kind:'user-created',author:'',license:'UNSPECIFIED',upstream:null},
      validation:{status:'unverified'},notes:''};
  }
  function object(o) { return o!==null && typeof o==='object' && !Array.isArray(o); }
  function keys(o, allowed, path, errors) {
    if (!object(o)) {errors.push(path+' must be an object');return false;}
    const actual=Object.keys(o);
    actual.forEach(k=>{if(!allowed.includes(k))errors.push(path+': unknown field '+k);});
    allowed.forEach(k=>{if(!Object.prototype.hasOwnProperty.call(o,k))errors.push(path+': missing '+k);});
    return true;
  }
  function text(v,n) {return typeof v==='string' && v.length<=n && !/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/.test(v);}
  function validate(v) {
    const e=[];
    if(!keys(v,['schema','id','name','revision','target','engine','parameters','exposure','provenance','validation','notes'],'look',e))return e;
    if(v.schema!=='cinevista.look/1')e.push('schema version unsupported');
    if(typeof v.id!=='string'|| !/^[A-Z0-9_]{1,8}$/.test(v.id))e.push('id: use 1–8 uppercase letters, digits or underscore');
    if(!text(v.name,64)||!v.name.trim())e.push('name required (maximum 64 characters)');
    if(!Number.isInteger(v.revision)||v.revision<1||v.revision>2147483647)e.push('invalid revision');
    if(!text(v.notes,2000))e.push('notes too long or invalid');
    if(keys(v.target,['model','firmware'],'target',e)) {
      if(v.target.model!=='ILCE-7RM2')e.push('target model not supported by this editor');
      if(v.target.firmware!==null&&(!text(v.target.firmware,32)||!v.target.firmware.trim()))e.push('firmware must be null or a short string');
    }
    const fs=engines[v.engine];
    if(!fs)e.push('engine unsupported (software LUT is a separate future format)');
    else if(keys(v.parameters,fs.map(f=>f.key),'parameters',e)) {
      fs.forEach(f=>{const n=v.parameters[f.key];
        if(f.type==='enum'?!f.values.includes(n):(!Number.isInteger(n)||n<f.min||n>f.max))e.push(f.key+': invalid value');});
      if(v.parameters.wb_kelvin%100!==0)e.push('wb_kelvin: prototype uses 100 K steps');
      if(v.engine==='sony-creative-style'&&['monochrome','sepia'].includes(v.parameters.style)&&v.parameters.saturation!==0)e.push('monochrome/sepia: saturation must be 0 (not adjustable)');
    }
    if(keys(v.exposure,['policy','suggested_ev_thirds'],'exposure',e)){
      if(v.exposure.policy!=='manual')e.push('this version must not silently apply exposure compensation');
      if(!Number.isInteger(v.exposure.suggested_ev_thirds)||Math.abs(v.exposure.suggested_ev_thirds)>15)e.push('EV suggestion out of bounds');
    }
    if(keys(v.provenance,['kind','author','license','upstream'],'provenance',e)) {
      if(!['user-created','adapted'].includes(v.provenance.kind))e.push('provenance kind invalid');
      if(!text(v.provenance.author,120)||!text(v.provenance.license,80))e.push('provenance text invalid');
      if(v.provenance.kind==='adapted'&&v.provenance.upstream===null)e.push('adapted look needs upstream attribution');
      if(v.provenance.upstream!==null) {
        if(keys(v.provenance.upstream,['project','commit','recipe','license'],'upstream',e)){
          for(const k of ['project','recipe','license'])if(!text(v.provenance.upstream[k],200)||!v.provenance.upstream[k])e.push('upstream '+k+' invalid');
          if(!/^[0-9a-f]{40}$/.test(v.provenance.upstream.commit))e.push('upstream commit must be 40 hex');
        }
      }
    }
    if(keys(v.validation,['status'],'validation',e)&&v.validation.status!=='unverified')e.push('authors cannot self-certify device compatibility; use external evidence');
    return e;
  }
  function serialize(v) {const e=validate(v);if(e.length)throw Error(e.join('\n'));return JSON.stringify(v,null,2)+'\n';}
  function parse(s) {
    if(typeof s!=='string'||s.length>maxBytes||new TextEncoder().encode(s).length>maxBytes)throw Error('file exceeds 64 KiB');
    // Authoring tool only; camera importer must additionally reject duplicate JSON keys.
    const v=JSON.parse(s);const e=validate(v);if(e.length)throw Error(e.join('\n'));return v;
  }
  function warnings(v) {
    const out=['相机端 .CVL 导入器尚未接入。这个文件不是 Sony 原生预设或 LUT，也不能交给 Recipe Lab 直接导入。',
      '本页不模拟 Sony 成像。参考照片不会随参数改变；真实颜色需要相机样片验证。',
      '白平衡轴采用语义坐标：正 A、正 G；接入 Sony 时要按机型验证符号，不能照搬整数。'];
    if(v.engine==='sony-picture-profile') {
      out.push('PP 菜单参数有官方依据，但 App 自动写入尚未验证。当前可导出手工设置单；数值默认是工作起点，不是索尼出厂预设。');
      if(['ITU709(800%)','S-Log2'].includes(v.parameters.gamma))out.push('Log/800% 不是直接分享外观；Black Level 可能无效，Gamma 会改变可用 ISO 范围。');
      if(v.parameters.knee_mode==='Auto'&&['Still','Cine1','Cine2','Cine3','Cine4','ITU709(800%)','S-Log2'].includes(v.parameters.gamma))out.push('此 Gamma + Auto Knee 组合下 Knee 不生效；不是一个遗漏的曲线功能。');
      if(v.parameters.knee_mode==='Manual'&&v.parameters.knee_manual_slope===5)out.push('Manual Knee Slope +5 会关闭 Knee。');
      out.push('PP 与 Creative Style 是替代后端，不是可叠加的两套滤镜；Color Depth 不等于任意六轴 HSL。');
    }
    return out;
  }
  function manual(v) {
    serialize(v);
    const intro=v.engine==='sony-picture-profile'?
      '菜单 → Camera Settings → Picture Profile → 选择由你确认可修改的 PP 槽。先记录原参数；本工具不指定或覆盖任何槽。':
      '菜单 → Camera Settings → Creative Style。使用前确认 Picture Profile / Picture Effect 不覆盖 Creative Style；记录原参数。';
    const lines=['幕野 Studio｜手工设置单',v.name+' / '+v.id+' / revision '+v.revision,
      '目标 ILCE-7RM2；固件 '+(v.target.firmware||'未记录'),'状态：未实机验证',intro,'',
      ...engines[v.engine].map(f=>f.label+': '+String(v.parameters[f.key])),
      '', '建议曝光补偿 EV: '+(v.exposure.suggested_ev_thirds/3).toFixed(2)+'（建议，不自动应用）',
      '白平衡 Kelvin 只在相应模式有效；自动/手动 Knee 与 Detail 只应用当前模式子项。',
      'DRO、拍摄模式和曝光应记录，且须确认相机未因互斥关系忽略相关设置。',
      '', ...warnings(v),'', '注释：'+v.notes];
    return lines.join('\n')+'\n';
  }
  const api={engines,make,validate,parse,serialize,manual,warnings,maxBytes};
  if(typeof module==='object'&&module.exports)module.exports=api;
  root.CineVistaLook=api;
}(typeof globalThis!=='undefined'?globalThis:this));
