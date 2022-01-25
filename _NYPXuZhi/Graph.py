class Graph:
    count_id = 0

    def __init__(self, DATE1, DATE2, DATE3, DATE4, DATE5, COVID1, COVID2, COVID3, COVID4, COVID5):
        Graph.count_id += 1
        self.__graph_id = Graph.count_id
        self.__DATE1 = DATE1
        self.__DATE2 = DATE2
        self.__DATE3 = DATE3
        self.__DATE4 = DATE4
        self.__DATE5 = DATE5
        self.__COVID1 = COVID1
        self.__COVID2 = COVID2
        self.__COVID3 = COVID3
        self.__COVID4 = COVID4
        self.__COVID5 = COVID5
    def set_graph_id(self, graph_id):
        self.__graph_id=graph_id
    def get_graph_id(self):
        return self.__graph_id

    def get_DATE1(self):
        return self.__DATE1

    def get_DATE2(self):
        return self.__DATE2

    def get_DATE3(self):
        return self.__DATE3

    def get_DATE4(self):
        return self.__DATE4

    def get_DATE5(self):
        return self.__DATE5

    def get_COVID1(self):
        return self.__COVID1

    def get_COVID2(self):
        return self.__COVID2

    def get_COVID3(self):
        return self.__COVID3

    def get_COVID4(self):
        return self.__COVID4

    def get_COVID5(self):
        return self.__COVID5

    def set_DATE1(self, DATE1):
        self.__DATE2 = DATE1

    def set_DATE2(self, DATE2):
        self.__DATE2 = DATE2

    def set_DATE3(self, DATE3):
        self.__DATE3 = DATE3

    def set_DATE4(self, DATE4):
        self.__DATE4 = DATE4

    def set_DATE5(self, DATE5):
        self.__DATE5 = DATE5


    def set_COVID1(self, COVID1):
        self.__DATE2 = COVID1

    def set_COVID2(self, COVID2):
        self.__COVID2 = COVID2

    def set_COVID3(self, COVID3):
        self.__COVID3 = COVID3

    def set_COVID4(self, COVID4):
        self.__COVID4 = COVID4

    def set_COVID5(self, COVID5):
        self.__COVID5 = COVID5

