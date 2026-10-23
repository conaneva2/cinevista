package org.cinevista.core;
/** Injected diagnostic destination; no Android, filesystem or UI dependency. */
public interface Diagnostics {
    void event(String category, String value);
}
