class Feedback:
    def __init__(self):
        self.__fb_name = ''
        self.__fb_email = ''
        self.__fb_subject = ''
        self.__fb_desc = ''
        self.__fb_id = ''
    
    def set_fb_name(self, name):
        self.__fb_name = name
    def set_fb_email(self, email):
        self.__fb_email = email
    def set_fb_subject(self, subject):
        self.__fb_subject = subject
    def set_fb_desc(self, desc):
        self.__fb_desc = desc
    def set_fb_id(self, id):
        self.__fb_id = id

    def get_fb_name(self):
        return self.__fb_name
    def get_fb_email(self):
        return self.__fb_email
    def get_fb_subject(self):
        return self.__fb_subject
    def get_fb_desc(self):
        return self.__fb_desc
    def get_fb_id(self):
        return self.__fb_id