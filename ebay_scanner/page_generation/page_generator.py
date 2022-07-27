from utils.environment import Environment 

class GenerateHTML:
    def __init__(self, name, title = 'Python: Ebay Scraper', footer = 'Zoom Devices 2021'):
        self.name = name
        self.title = title
        self.footer = footer

    def setup_page(self):
        header = '<html>\
                    <header>\
                    </header>'
        body = '    <body>\
                    </body>'
        footer = '  <footer>\
                    </footer>\
                </html>'
                
        self.path_to_file = Environment().environment_default_web_directory() + self.name
        # TODO: check if page exists, if it doesn't create it if it does import it and clear document
        print(self.path_to_file)

    # TODO: def append_page(self):#    
    # TODO: def replace_page(self): 

    def export_page(self):
        # TODO: move content of page to desired pages
        # for ebay scrapper need current items and history
        print()