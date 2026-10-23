package org.cinevista.probe;
import android.app.Activity;
import android.os.Bundle;
import android.view.KeyEvent;
import java.util.*;

/** Resolve ScalarInput constants from the actual runtime instead of A6000 numbers. */
abstract class BaseProbeActivity extends Activity {
    private final Map<Integer,String> keys=new HashMap<Integer,String>();
    protected void onCreate(Bundle b){super.onCreate(b);ProbeLog.init(this);
        keys.putAll(ProbeServices.keys());
        if(keys.isEmpty())ProbeLog.event("keys","Sony constants unavailable; Android navigation only");
    }
    protected boolean shutter(boolean down,boolean repeat){return true;}
    protected boolean focus(boolean down){return true;}
    /** Dialogs have their own Window; reuse the same runtime mapping there. */
    protected int navigationKey(KeyEvent e){
        String n=keys.get(Integer.valueOf(e.getScanCode()));
        if("UP".equals(n))return KeyEvent.KEYCODE_DPAD_UP;
        if("DOWN".equals(n))return KeyEvent.KEYCODE_DPAD_DOWN;
        if("LEFT".equals(n))return KeyEvent.KEYCODE_DPAD_LEFT;
        if("RIGHT".equals(n))return KeyEvent.KEYCODE_DPAD_RIGHT;
        if("ENTER".equals(n))return KeyEvent.KEYCODE_DPAD_CENTER;
        if("MENU".equals(n)||"DELETE".equals(n)||"SK1".equals(n)||"SK2".equals(n))return KeyEvent.KEYCODE_BACK;
        return 0;
    }
    public boolean dispatchKeyEvent(KeyEvent e){
        if(e.getAction()!=KeyEvent.ACTION_DOWN&&e.getAction()!=KeyEvent.ACTION_UP)return super.dispatchKeyEvent(e);
        ProbeLog.event("key","scan="+e.getScanCode()+" key="+e.getKeyCode()+" action="+e.getAction()+" repeat="+e.getRepeatCount());
        String n=keys.get(Integer.valueOf(e.getScanCode()));boolean down=e.getAction()==KeyEvent.ACTION_DOWN;
        if("S1_1".equals(n)){if(down&&e.getRepeatCount()>0)return true;return focus(down);} if("S1_2".equals(n))return true;
        if("S2".equals(n))return shutter(down,e.getRepeatCount()>0);
        int translated=navigationKey(e);
        if(translated==KeyEvent.KEYCODE_BACK){
            if(!down)onBackPressed();return true; // Back ONLY. Never delete media.
        }
        if(translated!=0)return super.dispatchKeyEvent(new KeyEvent(e.getDownTime(),e.getEventTime(),e.getAction(),translated,e.getRepeatCount()));
        return super.dispatchKeyEvent(e);
    }
}
