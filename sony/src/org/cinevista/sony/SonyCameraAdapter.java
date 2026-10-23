package org.cinevista.sony;
import org.cinevista.camera.CameraSession;
import org.cinevista.core.Diagnostics;
import org.cinevista.io.Errors;
import android.hardware.Camera;
import android.view.SurfaceHolder;
import java.lang.reflect.*;

/** Compile without Sony stubs; use only source-checked reflection signatures.
 * No direct Backup writes are issued; native runtime side effects remain unverified. No fallback to another camera is hidden.
 */
public final class SonyCameraAdapter implements CameraSession {
    private final Diagnostics log;
    public SonyCameraAdapter(Diagnostics log) { if(log == null) throw new IllegalArgumentException("diagnostics required"); this.log = log; }
    private Object ex,proxy;
    private Camera camera;
    private volatile boolean active;
    private volatile int generation;
    public void open(final Observer observer)throws Exception {
        final int token=++generation;
        try{
            Class<?> cx=Class.forName("com.sony.scalar.hardware.CameraEx");
            ex=cx.getMethod("open",Integer.TYPE,Class.forName("com.sony.scalar.hardware.CameraEx$OpenOptions")).invoke(null,Integer.valueOf(0),null);
            camera=(Camera)cx.getMethod("getNormalCamera").invoke(ex);active=true;
            try{
                Class<?> listener=Class.forName("com.sony.scalar.hardware.CameraEx$StoreImageCompleteListener");
                proxy=Proxy.newProxyInstance(listener.getClassLoader(),new Class<?>[]{listener},new InvocationHandler(){
                    public Object invoke(Object p,Method m,Object[] a)throws Throwable{
                        if(m.getDeclaringClass()==Object.class){if(m.getName().equals("hashCode"))return Integer.valueOf(System.identityHashCode(p));if(m.getName().equals("equals"))return Boolean.valueOf(a!=null&&a[0]==p);return "CineVistaStoreObserver";}
                        if(active&&generation==token&&m.getName().equals("onDone")&&a!=null&&a.length==3){
                            int code=((Integer)a[0]).intValue();Object info=a[1];
                            observer.callback(code,number(info,"DirectoryNo"),number(info,"FileNo"),number(info,"MediaId"));
                        }return null;
                    }
                });
                cx.getMethod("setStoreImageCompleteListener",listener).invoke(ex,proxy);
                log.event("capture_listener","registered; callback meanings NOT VERIFIED");
            }catch(Throwable e){log.event("capture_listener","unavailable "+Errors.describe(e));}
        }catch(Exception e){close();throw e;}
    }
    private static int number(Object info,String name){try{return info.getClass().getField(name).getInt(info);}catch(Throwable e){return -1;}}
    public PreviewSize previewSize(){if(camera==null)return null; Camera.Size size=camera.getParameters().getPreviewSize(); return size==null?null:new PreviewSize(size.width,size.height);}
    public void preview(SurfaceHolder holder)throws Exception { if(camera==null)throw new IllegalStateException("camera closed");camera.setPreviewDisplay(holder);camera.startPreview(); }
    public void focus(boolean down){if(camera!=null){if(down)camera.autoFocus(null);else camera.cancelAutoFocus();}}
    public void pressShutter(){if(camera==null)throw new IllegalStateException("camera closed");camera.takePicture(null,null,null);}
    public void releaseShutter()throws Exception{if(ex!=null)ex.getClass().getMethod("cancelTakePicture").invoke(ex);}
    public void close(){active=false;generation++; if(camera!=null)try{camera.stopPreview();}catch(Throwable ignored){}
        if(ex!=null)try{ex.getClass().getMethod("release").invoke(ex);}catch(Throwable e){log.event("camera_release",Errors.describe(e));}
        camera=null;ex=null;proxy=null;
    }
}
