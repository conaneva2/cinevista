package org.cinevista.camera;
import android.view.SurfaceHolder;
/** Android-side camera port. Domain never depends on this interface.
 * Closing a session invalidates earlier callbacks. A receipt is not source verification.
 */
public interface CameraSession {
    interface Observer { void callback(int rawCode, int directoryNo, int fileNo, int mediaId); }
    final class PreviewSize {
        public final int width, height;
        public PreviewSize(int width, int height) { this.width = width; this.height = height; }
    }
    void open(Observer observer) throws Exception;
    PreviewSize previewSize();
    void preview(SurfaceHolder holder) throws Exception;
    void focus(boolean down);
    void pressShutter();
    void releaseShutter() throws Exception;
    void close();
}
