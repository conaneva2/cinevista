package org.cinevista.probe;
import org.cinevista.io.*;
import android.os.*;
import android.graphics.*;
import android.view.View;
import android.widget.*;
import java.io.*;
import org.cinevista.core.*;

/** Small, app-generated test only. No user photographs or Sony native filters.
 * This tests Android Bitmap/Canvas/JPEG. It does not establish full-res Sony output.
 */
public final class ImageProbeActivity extends BaseProbeActivity {
    private TextView status;private ImageView view;private Button run,save;
    private final Handler handler=new Handler();private volatile boolean cancelled;private File resultDir;
    protected void onCreate(Bundle b){super.onCreate(b);LinearLayout root=new LinearLayout(this);root.setOrientation(LinearLayout.VERTICAL);setContentView(root);
        status=new TextView(this);status.setText(R.string.image_notice);root.addView(status);
        run=new Button(this);run.setText(R.string.image_run);root.addView(run);
        save=new Button(this);save.setText(R.string.image_export);save.setEnabled(false);root.addView(save);
        view=new ImageView(this);root.addView(view,new LinearLayout.LayoutParams(-1,0,1));
        run.setOnClickListener(new View.OnClickListener(){public void onClick(View v){run.setEnabled(false);cancelled=false;new Thread(new Runnable(){public void run(){test();}},"cinevista-small-image-test").start();}});
        save.setOnClickListener(new View.OnClickListener(){public void onClick(View v){try{File dir=Filesafe.reserveJob(new File(Environment.getExternalStorageDirectory(),"CINEVISTA_PROBE"));
            for(String name:new String[]{"source.jpg","image.jpg","manifest.json"})copy(new File(resultDir,name),new File(dir,name));
            status.setText(getString(R.string.image_exported,dir.getAbsolutePath()));
        }catch(Exception e){status.setText(getString(R.string.image_export_error,ProbeLog.error(e)));}}});
    }
    protected void onPause(){cancelled=true;super.onPause();}
    private void test(){Bitmap source=null,input=null,output=null;try{
        long estimated=600L*800*4*2+600L*400*4+4L*1024*1024;
        if(estimated>Runtime.getRuntime().maxMemory()/2)throw new IOException("Insufficient reference buffer budget");
        File job=Filesafe.reserveJob(new File(getFilesDir(),"image-tests"));
        source=Bitmap.createBitmap(600,800,Bitmap.Config.ARGB_8888);Canvas c=new Canvas(source);c.drawColor(Color.WHITE);Paint p=new Paint();
        p.setColor(Color.BLACK);p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(6);c.drawOval(new RectF(250,300,350,500),p);c.drawRect(10,10,590,790,p);
        p.setStyle(Paint.Style.FILL);p.setTextSize(19);c.drawText("SYNTHETIC 2x SQUEEZED TARGET",25,100,p);c.drawText("TOP",20,30,p);c.drawText("BOTTOM",450,775,p);
        File raw=new File(job,"source.jpg");write(source,raw);source.recycle();source=null;
        String original=Filesafe.sha256(raw);JpegGuard.Info info=JpegGuard.read(raw);info.requireSupported(true);
        input=BitmapFactory.decodeFile(raw.getAbsolutePath());if(input==null)throw new IOException("Source decode returned null");
        Geometry.Plan plan=Geometry.plan(info.width,info.height,2,null,0,0,false,null,1);
        output=Bitmap.createBitmap(plan.outputWidth,plan.outputHeight,Bitmap.Config.ARGB_8888);Canvas out=new Canvas(output);
        Matrix m=new Matrix();float sx=(float)(plan.outputWidth/plan.crop.width()),sy=(float)(plan.outputHeight/plan.crop.height());
        m.setValues(new float[]{sx,0,(float)(-plan.crop.left*sx),0,sy,(float)(-plan.crop.top*sy),0,0,1});
        Paint filter=new Paint(Paint.FILTER_BITMAP_FLAG);out.drawBitmap(input,m,filter);
        File temp=new File(job,"image.jpg.part");write(output,temp);
        JpegGuard.Info check=JpegGuard.read(temp);if(check.width!=600||check.height!=400)throw new IOException("Encoded size mismatch");
        Bitmap decoded=BitmapFactory.decodeFile(temp.getAbsolutePath());if(decoded==null)throw new IOException("Output failed to decode");decoded.recycle();
        if(!original.equals(Filesafe.sha256(raw)))throw new IOException("Source changed");
        if(cancelled)throw new IOException("Activity paused; no final file published");
        Filesafe.publish(temp,new File(job,"image.jpg"));
        Filesafe.writeUtf8New(new File(job,"manifest.json"),"{\"synthetic\":true,\"backend\":\"android-bitmap-canvas\",\"source_sha256\":\""+original+"\",\"source_unchanged\":true,\"visual_geometry_verified\":false,\"plan\":"+plan.toJson()+"}\n");
        final File done=job;handler.post(new Runnable(){public void run(){if(cancelled)return;resultDir=done;view.setImageBitmap(BitmapFactory.decodeFile(new File(done,"image.jpg").getAbsolutePath()));save.setEnabled(true);status.setText(R.string.image_done);}});
        ProbeLog.event("synthetic_image","small JPEG call completed; dimensions and source hash checked; visual result unverified");
    }catch(final Throwable e){handler.post(new Runnable(){public void run(){if(!cancelled){status.setText(getString(R.string.image_error,ProbeLog.error(e)));run.setEnabled(true);}}});ProbeLog.event("synthetic_image",ProbeLog.error(e));}
    finally{if(source!=null)source.recycle();if(input!=null)input.recycle();if(output!=null)output.recycle();}}
    private static void write(Bitmap b,File file)throws IOException{FileOutputStream o=Filesafe.createNew(file);try{if(!b.compress(Bitmap.CompressFormat.JPEG,95,o))throw new IOException("JPEG compress returned false");o.flush();o.getFD().sync();}finally{o.close();}}
    private static void copy(File a,File b)throws IOException{InputStream in=new FileInputStream(a);try{FileOutputStream out=Filesafe.createNew(b);try{byte[] bytes=new byte[32768];int n;while((n=in.read(bytes))!=-1)out.write(bytes,0,n);out.getFD().sync();}finally{out.close();}}finally{in.close();}}
}
