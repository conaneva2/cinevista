package org.cinevista.camera;
/** Runtime report, NOT optical calibration evidence. Mutable probe DTO only. */
public final class DisplayInfo {
    public double pixelAspect = 1;
    public boolean known;
    public String text = "Display pixel aspect ASSUMED 1; uncalibrated\n";
}
