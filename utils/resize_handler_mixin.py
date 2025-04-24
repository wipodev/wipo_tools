from tkinter import TclError

class ResizeHandlerMixin:
    def setup_resize_listener(self, callback, threshold=10, delay=300):
        self._resize_job = None
        self._last_width = 0
        self._resize_threshold = threshold
        self._resize_delay = delay
        self._resize_callback = callback

        root = self.winfo_toplevel()
        self._bind_id = root.bind("<Configure>", self._handle_resize_event)

    def _handle_resize_event(self, event):
        # Ignoramos Configure de cualquier widget que no sea el root
        try:
            root = self.winfo_toplevel()
        except TclError:
            return

        if event.widget is not root:
            return

        # Cancelar cualquier job pendiente
        if self._resize_job:
            self.after_cancel(self._resize_job)

        new_width = event.width  # ancho del root
        # Si el cambio es muy pequeño, no hacemos nada
        if abs(new_width - self._last_width) < self._resize_threshold:
            return

        self._last_width = new_width
        # Programamos el callback (ej. refresh_all) tras `delay` ms
        self._resize_job = self.after(self._resize_delay, self._resize_callback)

    def destroy(self):
        try:
            root = self.winfo_toplevel()
            root.unbind("<Configure>", self._bind_id)
        except (AttributeError, TclError):
            pass
        super().destroy()
