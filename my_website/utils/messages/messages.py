import sweetify

class Message:
    def __init__(self):
        self.colors = {'info': "rgba(17, 176, 234, 0.4)",
                       'success': "rgba(33, 180, 7, 0.4)",
                       'error': "rgba(180, 7, 7, 0.4)",
                       'warning': "rgba(199, 212, 21, 0.4)"}
        
    def info(self, request, text):
        sweetify.info(request, text, backdrop=self.colors['info'])
    
    def success(self, request, text):
        sweetify.success(request, text, backdrop=self.colors['success'])
    
    def error(self, request, text):
        sweetify.error(request, text, backdrop=self.colors['error'])

    def warning(self, request, text):
        sweetify.warning(request, text, backdrop=self.colors['warning'])