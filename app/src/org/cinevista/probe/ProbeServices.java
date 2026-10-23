package org.cinevista.probe;
import android.content.Context;
import org.cinevista.core.Diagnostics;
import org.cinevista.camera.CameraSession;
import org.cinevista.camera.DisplayInfo;
import org.cinevista.sony.SonyCameraAdapter;
import org.cinevista.sony.DeviceProbe;
import org.cinevista.sony.KeyResolver;
import java.util.Map;
/** The only UI composition root allowed to select a Sony implementation. */
final class ProbeServices {
    private ProbeServices() {}
    static CameraSession camera() {
        return new SonyCameraAdapter(new Diagnostics() {
            public void event(String category, String value) { ProbeLog.event(category, value); }
        });
    }
    static String snapshot(Context c) { return DeviceProbe.snapshot(c); }
    static DisplayInfo display(Context c) { return DeviceProbe.display(c); }
    static Map<Integer,String> keys() { return KeyResolver.resolve(); }
}
