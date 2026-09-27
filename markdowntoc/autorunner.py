import os.path
import sublime_plugin

from .base import Base


class AutoRunner(sublime_plugin.EventListener, Base):
    def on_pre_save(self, view):
        # limit scope
        root, ext = os.path.splitext(view.file_name())
        ext = ext.lower()
        extensions = [e.lower() for e in self.settings("autorun_extensions")]
        if ext in extensions:
            view.run_command("markdowntoc_update")
