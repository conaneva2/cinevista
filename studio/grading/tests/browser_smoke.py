from playwright.sync_api import sync_playwright
from pathlib import Path
import json,os,shutil
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'build'/'studio-browser';OUT.mkdir(parents=True,exist_ok=True)
html=(ROOT/'studio'/'grading'/'index.html').read_text()
report={'mode':'Chromium in-memory document.set_content; file navigation blocked by environment policy','checks':[],'browser':None}
with sync_playwright() as p:
 executable=os.environ.get('CINEVISTA_CHROMIUM') or shutil.which('chromium')
 b=p.chromium.launch(executable_path=executable,headless=True,args=['--no-sandbox'] if hasattr(os,'geteuid') and os.geteuid()==0 else [])
 report['browser']=b.version
 page=b.new_page(viewport={'width':1440,'height':1200},accept_downloads=True)
 errors=[];console=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('console',lambda e:console.append(e.type+': '+e.text))
 page.set_content(html,wait_until='load')
 page.wait_for_function("() => document.body.dataset.renderId === '1'",timeout=12000)
 report['checks'].append('initial_worker_LUT_ready')
 page.locator('#photos').set_input_files(str(ROOT/'studio/grading/tests/fixtures/srgb-grid.png'))
 page.wait_for_function("() => document.body.dataset.renderId === '3'",timeout=12000)
 before=page.evaluate("Array.from(document.getElementById('preview').getContext('2d').getImageData(150,120,1,1).data)")
 report['before']=before
 page.locator('#p_temperature').evaluate("e=>{e.value='80';e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}));}")
 page.wait_for_function("() => document.body.dataset.renderId === '4'",timeout=12000)
 after=page.evaluate("Array.from(document.getElementById('preview').getContext('2d').getImageData(150,120,1,1).data)")
 assert after!=before,(before,after)
 report['after']=after;report['checks'].append('imported_pixels_really_change_on_input_event')
 page.locator('#compare').select_option('before')
 now=page.evaluate("Array.from(document.getElementById('preview').getContext('2d').getImageData(150,120,1,1).data)")
 assert now==before,(before,now);report['checks'].append('original_view_restores_ungraded_pixels')
 page.locator('#compare').select_option('after')
 page.locator('#undo').click();page.wait_for_function("() => document.body.dataset.renderId === '5'")
 now=page.evaluate("Array.from(document.getElementById('preview').getContext('2d').getImageData(150,120,1,1).data)")
 assert now==before;report['checks'].append('undo_restores_original_pixels')
 page.locator('#redo').click();page.wait_for_function("() => document.body.dataset.renderId === '6'")
 with page.expect_download() as di: page.locator('#exportCube').click()
 download=di.value;download.save_as(str(OUT/'browser_test_export.CUBE'))
 assert 'LUT_3D_SIZE 33' in Path(str(OUT/'browser_test_export.CUBE')).read_text();report['checks'].append('visible_33_cube_download')
 with page.expect_download() as di:page.locator('#saveProject').click()
 di.value.save_as(str(OUT/'browser_test_export.CVG'));assert json.loads(Path(str(OUT/'browser_test_export.CVG')).read_text())['parameters']['temperature']==80
 report['checks'].append('editable_project_download')
 assert page.locator('#exportPackage').is_disabled();report['checks'].append('camera_package_requires_user_input_contract_confirmation')
 page.locator('#baseline').fill('sRGB; PP off; same capture pipeline; test fixture only');page.locator('#confirmInput').check()
 with page.expect_download() as di:page.locator('#exportPackage').click()
 di.value.save_as(str(OUT/'browser_test_export.CVP'));pack=json.loads(Path(str(OUT/'browser_test_export.CVP')).read_text());assert pack['payload']['text']==Path(str(OUT/'browser_test_export.CUBE')).read_text()
 report['checks'].append('camera_package_contains_exact_exported_cube')
 with page.expect_download() as di:page.locator('#exportImage').click()
 di.value.save_as(str(OUT/'browser_test_preview.png'));report['checks'].append('preview_png_export')
 page.locator('#compare').select_option('after')
 previous=int(page.locator('body').get_attribute('data-render-id'))
 page.locator('#p_temperature').evaluate("e=>{for(const n of [10,20,30,40,50]){e.value=String(n);e.dispatchEvent(new Event('input',{bubbles:true}));}e.dispatchEvent(new Event('change',{bubbles:true}));}")
 page.wait_for_function("id=>Number(document.body.dataset.renderId)===id",arg=previous+5)
 current=page.evaluate("Array.from(document.getElementById('preview').getContext('2d').getImageData(150,120,1,1).data)")
 expected=page.evaluate("p=>{const s=CineVistaGrade.parameters();s.temperature=50;return Array.from(CineVistaGrade.apply(CineVistaGrade.buildLut(s),new Uint8ClampedArray(p)));}", before)
 assert current==expected,(current,expected)
 report['checks'].append('rapid_slider_updates_do_not_publish_stale_effect')
 page.locator('#compare').select_option('split')
 page.screenshot(path=str(OUT/'studio_realtime_browser.png'),full_page=True)
 report['status']=page.locator('#status').inner_text();report['errors']=errors;report['console']=console
 assert not errors,errors
 b.close()
Path(str(OUT/'grade_browser_report.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
