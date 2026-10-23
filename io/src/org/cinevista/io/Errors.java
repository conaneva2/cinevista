package org.cinevista.io;
/** Intentionally omits messages and paths from diagnostics. */
public final class Errors {
    private Errors() {}
    public static String describe(Throwable error) {
        if (error == null) return "UnknownError";
        if (error instanceof java.lang.reflect.InvocationTargetException) {
            Throwable target = ((java.lang.reflect.InvocationTargetException) error).getTargetException();
            if (target != null) error = target;
        }
        return error.getClass().getSimpleName();
    }
}
