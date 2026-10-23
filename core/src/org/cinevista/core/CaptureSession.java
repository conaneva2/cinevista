package org.cinevista.core;

/** A deliberately single-capture probe session. A callback is NOT proof of a file.
 * No timeout, key release or app restart is allowed to fabricate SOURCE_CONFIRMED.
 */
public final class CaptureSession {
    public enum State { READY, CAPTURING, CALLBACK_RECEIVED, SOURCE_CONFIRMED, INTERRUPTED_UNKNOWN, FAILED }
    public static final class Intent {
        public final String id;
        public final long requestedAt;
        public final double squeeze;
        public final Double aspect;
        public Intent(String i,long time,double s,Double a) {
            if(i==null||i.length()==0||Double.isNaN(s)||Double.isInfinite(s)||s<1)
                throw new IllegalArgumentException("invalid capture intent");
            if(a!=null&&(Double.isNaN(a.doubleValue())||Double.isInfinite(a.doubleValue())||a.doubleValue()<=0))
                throw new IllegalArgumentException("invalid aspect");
            id=i; requestedAt=time; squeeze=s; aspect=a;
        }
    }
    private State state=State.READY;
    private Intent intent;
    private boolean shutterDown;
    private Integer rawCallbackCode;
    private String sourceToken;
    public synchronized boolean press(boolean repeat,Intent request) {
        if(repeat||shutterDown||state!=State.READY) return false;
        if(request==null) throw new IllegalArgumentException("intent required");
        shutterDown=true; intent=request; state=State.CAPTURING; return true;
    }
    public synchronized void releaseKey() { shutterDown=false; }
    public synchronized void callback(int rawCode) {
        if(state!=State.CAPTURING&&state!=State.CALLBACK_RECEIVED) return;
        rawCallbackCode=Integer.valueOf(rawCode); state=State.CALLBACK_RECEIVED;
    }
    /** For a future validated media adapter only, never called by the probe UI. */
    public synchronized void confirmSource(String captureId,String verifiedToken) {
        if(state!=State.CALLBACK_RECEIVED||intent==null||!intent.id.equals(captureId)
                ||verifiedToken==null||verifiedToken.length()==0)
            throw new IllegalStateException("unmatched/unverified capture");
        sourceToken=verifiedToken; state=State.SOURCE_CONFIRMED;
    }
    public synchronized void fail() { if(state!=State.SOURCE_CONFIRMED) state=State.FAILED; }
    public synchronized void interrupt() {
        shutterDown=false;
        if(state==State.CAPTURING||state==State.CALLBACK_RECEIVED) state=State.INTERRUPTED_UNKNOWN;
    }
    public synchronized State state() { return state; }
    public synchronized Intent intent() { return intent; }
    public synchronized Integer callbackCode() { return rawCallbackCode; }
    public synchronized String sourceToken() { return sourceToken; }
}
