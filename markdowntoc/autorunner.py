import os.path
import sublime_plugin

class AutoRunner(sublime_plugin.EventListener):

    def on_pre_save(self, view):
        # limit scope
        root, ext = os.path.splitext(view.file_name())
        ext = ext.lower()
        if ext in ['.md',
                   '.markdown',
                   '.mdown',
                   '.mdwn',
                   '.mkdn',
                   '.mkd',
                   '.mark']:
            view.run_command('markdowntoc_update')