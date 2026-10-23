package org.cinevista.sony;
import org.cinevista.camera.DisplayInfo;
import org.cinevista.io.Errors;
import android.content.Context;
import android.os.Build;
import android.util.DisplayMetrics;
import java.lang.reflect.*;

public final class DeviceProbe {
    static final String[] TYPES={"com.sony.scalar.hardware.CameraEx","com.sony.scalar.hardware.CameraEx$StoreImageCompleteListener",
        "com.sony.scalar.hardware.CameraSequence","com.sony.scalar.hardware.DeviceMemory",
        "com.sony.scalar.graphics.OptimizedImageFactory","com.sony.scalar.graphics.imagefilter.CropImageFilter",
        "com.sony.scalar.graphics.imagefilter.ScaleImageFilter","com.sony.scalar.graphics.JpegExporter",
        "com.sony.scalar.hardware.avio.DisplayManager","android.graphics.SurfaceTexture","android.view.TextureView"};
    public static String snapshot(Context c){
        StringBuilder b=new StringBuilder("CineVista Probe 0.4\nDECLARED != WORKING != VERIFIED\n");
        b.append("Android model: ").append(Build.MODEL).append("\nAndroid release: ").append(Build.VERSION.RELEASE)
            .append("\nAPI: ").append(Build.VERSION.SDK_INT).append("\nCamera firmware: NOT READ; fill manually\n");
        b.append("Java heap max bytes: ").append(Runtime.getRuntime().maxMemory()).append('\n');
        DisplayMetrics dm=c.getResources().getDisplayMetrics(); b.append("UI metrics: ").append(dm.widthPixels).append('x').append(dm.heightPixels).append('\n');
        for(String name:TYPES){try{Class.forName(name);b.append("runtime_declared ").append(name).append('\n');}
            catch(Throwable e){b.append("not_available ").append(name).append(' ').append(Errors.describe(e)).append('\n');}}
        for(String name:new String[]{"com.sony.scalar.hardware.CameraSequence","com.sony.scalar.graphics.imagefilter.ScaleImageFilter","com.sony.scalar.graphics.JpegExporter"}){
            try{for(Method m:Class.forName(name).getDeclaredMethods()){
                String method=m.getName();
                if(method.equals("getPreviewSequenceFrames")||method.equals("setDestSize")||method.equals("encode")||method.equals("storeImage"))
                    b.append("signature ").append(m.toGenericString()).append('\n');
            }}catch(Throwable e){b.append("signature_read_failed ").append(name).append('\n');}
        }
        b.append(display(c).text);return b.toString();
    }
    public static DisplayInfo display(Context c){
        DisplayInfo out=new DisplayInfo();Object manager=null;
        try{
            Class<?> type=Class.forName("com.sony.scalar.hardware.avio.DisplayManager");manager=type.getConstructor().newInstance();
            String active=(String)type.getMethod("getActiveDevice").invoke(manager);
            Object device=type.getMethod("getDeviceInfo",String.class).invoke(manager,active);
            int a=device.getClass().getField("aspect").getInt(device);
            String[] names={"ASPECT_RATIO_3_2","ASPECT_RATIO_4_3","ASPECT_RATIO_5_3","ASPECT_RATIO_11_9","ASPECT_RATIO_16_9"};
            double[] values={1.5,4.0/3,5.0/3,11.0/9,16.0/9};double physical=0;
            for(int i=0;i<names.length;i++)if(type.getField(names[i]).getInt(null)==a)physical=values[i];
            DisplayMetrics dm=c.getResources().getDisplayMetrics();
            if(physical>0&&dm.widthPixels>0&&dm.heightPixels>0){out.pixelAspect=physical/((double)dm.widthPixels/dm.heightPixels);out.known=true;}
            out.text="Active display: "+active+"; physical aspect="+physical+"; pixel aspect="+out.pixelAspect
                +(out.known?" (runtime reported; NOT optically calibrated)":" (ASSUMED)")+"\n";
        }catch(Throwable e){out.text+="Display read: "+Errors.describe(e)+"\n";}
        finally{if(manager!=null)try{manager.getClass().getMethod("finish").invoke(manager);}catch(Throwable ignored){}}
        return out;
    }
}
