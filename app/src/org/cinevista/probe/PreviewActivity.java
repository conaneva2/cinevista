package org.cinevista.probe;
import android.os.*;
import android.app.AlertDialog;
import android.content.DialogInterface;
import java.util.Locale;
import org.cinevista.camera.CameraSession;
import org.cinevista.camera.DisplayInfo;
import android.graphics.*;
import android.view.*;
import android.widget.*;
import org.cinevista.core.*;
import java.util.UUID;

public final class PreviewActivity extends BaseProbeActivity implements SurfaceHolder.Callback {
    private final Handler handler=new Handler();
    private final CameraSession adapter=ProbeServices.camera();
    private final CaptureSession capture=new CaptureSession();
    private SurfaceView surface;private FrameLayout stage;private TextView status;private Guide guide;
    private boolean surfaceReady,foreground,opened,shutterAccepted;
    private int epoch,index;private double squeeze=1,pixelAspect=1;private Double aspect=Geometry.XPAN;
    private String display="";private boolean resizeExperiment;
    private Button lensControl,frameControl;private int notice;
    protected void onCreate(Bundle b){super.onCreate(b);
        setContentView(R.layout.probe_viewfinder);
        status=(TextView)findViewById(R.id.viewfinder_status);
        stage=(FrameLayout)findViewById(R.id.viewfinder_stage);
        surface=(SurfaceView)findViewById(R.id.viewfinder_surface);
        surface.getHolder().setType(SurfaceHolder.SURFACE_TYPE_PUSH_BUFFERS);surface.getHolder().addCallback(this);
        guide=new Guide();stage.addView(guide,new FrameLayout.LayoutParams(-1,-1));
        lensControl=(Button)findViewById(R.id.lens_control);
        frameControl=(Button)findViewById(R.id.frame_control);
        lensControl.setOnClickListener(new View.OnClickListener(){public void onClick(View v){
            double[] ratios={1,1.33,1.5,1.6,1.8,2};index=(index+1)%ratios.length;squeeze=ratios[index];layoutExperiment();
        }});
        frameControl.setOnClickListener(new View.OnClickListener(){public void onClick(View v){
            aspect=aspect==null?Double.valueOf(Geometry.XPAN):(aspect.doubleValue()==Geometry.XPAN?Double.valueOf(Geometry.SCOPE):null);refresh();
        }});
        findViewById(R.id.settings_control).setOnClickListener(new View.OnClickListener(){public void onClick(View v){showSettings();}});
        frameControl.requestFocus();refresh();
    }
    private void showSettings(){
        String[] items={getString(resizeExperiment?R.string.surface_disable:R.string.surface_enable),
            getString(R.string.retry_preview),getString(R.string.show_diagnostics),getString(R.string.back_home)};
        showDialog(new AlertDialog.Builder(this).setTitle(R.string.probe_settings).setItems(items,new DialogInterface.OnClickListener(){
            public void onClick(DialogInterface dialog,int which){
                if(which==0){resizeExperiment=!resizeExperiment;layoutExperiment();}
                else if(which==1)startPreview();
                else if(which==2)showDiagnostics();
                else finish();
            }
        }).setNegativeButton(R.string.close,null).create());
    }
    private void showDiagnostics(){
        ScrollView scroll=new ScrollView(this);TextView text=new TextView(this);text.setTextSize(16);
        text.setText(getString(R.string.diagnostics_body,getString(R.string.preview_limit),display,capture.state().name(),ProbeLog.recent()));
        scroll.addView(text);
        showDialog(new AlertDialog.Builder(this).setTitle(R.string.diagnostics_title).setView(scroll).setPositiveButton(R.string.close,null).create());
    }
    private void showDialog(final AlertDialog dialog){
        dialog.setOnKeyListener(new DialogInterface.OnKeyListener(){
            private boolean forwarding;
            public boolean onKey(DialogInterface ignored,int keyCode,KeyEvent event){
                if(forwarding)return false;
                int key=navigationKey(event);if(key==0)return false;
                forwarding=true;
                try{dialog.dispatchKeyEvent(new KeyEvent(event.getDownTime(),event.getEventTime(),event.getAction(),key,event.getRepeatCount()));}
                finally{forwarding=false;}
                return true;
            }
        });
        dialog.show();
    }
    protected void onResume(){super.onResume();foreground=true;final int token=++epoch;
        DisplayInfo d=ProbeServices.display(this);pixelAspect=d.pixelAspect;display=d.text;
        try{adapter.open(new CameraSession.Observer(){public void callback(final int code,final int dir,final int file,final int media){
            handler.post(new Runnable(){public void run(){if(!foreground||token!=epoch)return;
                capture.callback(code);ProbeLog.event("store_callback","rawCode="+code+" DirectoryNo="+dir+" FileNo="+file+" MediaId="+media+"; NOT file verification");refresh();
            }});
        }});opened=true;ProbeLog.event("camera_open","invocation returned; optical/capture correctness unverified");startPreview();}
        catch(Throwable e){opened=false;adapter.close();notice=R.string.camera_open_error;refresh();ProbeLog.event("camera_open",ProbeLog.error(e));}
    }
    protected void onPause(){foreground=false;epoch++;capture.interrupt();
        if(shutterAccepted)try{adapter.releaseShutter();}catch(Throwable ignored){}
        shutterAccepted=false;adapter.close();opened=false;ProbeLog.event("session_state",capture.state().name());super.onPause();}
    protected void onDestroy(){surface.getHolder().removeCallback(this);handler.removeCallbacksAndMessages(null);super.onDestroy();}
    public void surfaceCreated(SurfaceHolder h){surfaceReady=true;startPreview();}
    public void surfaceChanged(SurfaceHolder h,int format,int w,int height){ProbeLog.event("surface_changed",w+"x"+height+"; requested geometry is not proof of image stretch");guide.invalidate();}
    public void surfaceDestroyed(SurfaceHolder h){surfaceReady=false;}
    private void startPreview(){if(!foreground||!opened||!surfaceReady)return;
        try{adapter.preview(surface.getHolder());notice=0;refresh();}
        catch(Throwable e){ProbeLog.event("preview",ProbeLog.error(e));notice=R.string.preview_error;refresh();}
    }
    protected boolean focus(boolean down){if(opened)try{adapter.focus(down);}catch(Throwable e){ProbeLog.event("focus",ProbeLog.error(e));}return true;}
    protected boolean shutter(boolean down,boolean repeat){
        if(!down){capture.releaseKey();if(shutterAccepted){shutterAccepted=false;try{adapter.releaseShutter();}catch(Throwable e){ProbeLog.event("shutter_release",ProbeLog.error(e));}}return true;}
        if(!opened||!surfaceReady)return true;
        CaptureSession.Intent intent=new CaptureSession.Intent(UUID.randomUUID().toString(),System.currentTimeMillis(),squeeze,aspect);
        if(capture.press(repeat,intent)){shutterAccepted=true;
            ProbeLog.event("capture_intent",intent.id+" squeeze="+intent.squeeze+" aspect="+intent.aspect+"; capture source unconfirmed");
            try{adapter.pressShutter();}catch(Throwable e){capture.fail();ProbeLog.event("shutter",ProbeLog.error(e));}refresh();
        }return true;
    }
    private CameraSession.PreviewSize size(){try{return adapter.previewSize();}catch(Throwable e){return null;}}
    private void layoutExperiment(){
        if(notice==R.string.geometry_error)notice=0;
        if(resizeExperiment){CameraSession.PreviewSize z=size();int w=stage.getWidth(),h=stage.getHeight();
            if(z==null||z.width<2||z.height<2||w<2||h<2){notice=R.string.geometry_error;refresh();return;}
            Geometry.Rect r=Geometry.fit((double)z.width*squeeze/z.height,w,h,pixelAspect);
            surface.setLayoutParams(new FrameLayout.LayoutParams(Math.max(2,(int)Math.round(r.width())),Math.max(2,(int)Math.round(r.height())),Gravity.CENTER));
            ProbeLog.event("surface_request","ratio="+squeeze+" view="+r.width()+"x"+r.height()+"; actual content transform UNVERIFIED");
        }else surface.setLayoutParams(new FrameLayout.LayoutParams(-1,-1,Gravity.CENTER));refresh();
    }
    private void refresh(){
        if(status==null)return;
        lensControl.setText(getString(R.string.lens_value,String.format(Locale.US,"%s",Double.valueOf(squeeze))));
        frameControl.setText(getString(R.string.frame_value,aspect==null?getString(R.string.frame_auto):aspect.doubleValue()==Geometry.XPAN?"65:24":"2.39"));
        int stateText=R.string.preview_ready;
        switch(capture.state()){
            case CAPTURING:stateText=R.string.preview_capturing;break;
            case CALLBACK_RECEIVED:stateText=R.string.preview_callback;break;
            case SOURCE_CONFIRMED:stateText=R.string.preview_confirmed;break;
            case INTERRUPTED_UNKNOWN:stateText=R.string.preview_interrupted;break;
            case FAILED:stateText=R.string.preview_failed;break;
            default:break;
        }
        status.setText(getString(notice!=0?notice:stateText)+"\n"+getString(resizeExperiment?R.string.surface_active:R.string.preview_limit));
        if(guide!=null)guide.invalidate();
    }
    private final class Guide extends View{
        private final Paint paint=new Paint();Guide(){super(PreviewActivity.this);setFocusable(false);}
        protected void onDraw(Canvas canvas){super.onDraw(canvas);CameraSession.PreviewSize z=size();if(z==null||z.width<2||z.height<2||aspect==null)return;
            try{
                Geometry.Plan p=Geometry.plan(z.width,z.height,squeeze,aspect,0,0,false,null,1);
                Geometry.Rect displayRect=Geometry.fit((double)z.width*squeeze/z.height,surface.getWidth(),surface.getHeight(),pixelAspect);
                // Assumed content fit only. Calibration remains a separate hardware gate.
                Geometry.Rect target=new Geometry.Rect(displayRect.left+surface.getLeft(),displayRect.top+surface.getTop(),displayRect.right+surface.getLeft(),displayRect.bottom+surface.getTop());
                Geometry.Rect full=new Geometry.Rect(0,0,z.width,z.height);
                double[] tl=Geometry.sourceToDisplay(full,target,p.crop.left,p.crop.top),br=Geometry.sourceToDisplay(full,target,p.crop.right,p.crop.bottom);
                paint.setColor(Color.WHITE);paint.setStyle(Paint.Style.STROKE);paint.setStrokeWidth(1.5f);
                canvas.drawRect((float)tl[0],(float)tl[1],(float)br[0],(float)br[1],paint);
            }catch(Throwable e){/* Unknown geometry is not drawn. */}
        }
    }
}
