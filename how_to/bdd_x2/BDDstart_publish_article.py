

class PublishArticle():
    
    __articlelist = None
    __numberArticles = 0
    
    # static methods do not receive class or instance arguments
    # and usually operate on data that is not instance- or
    # class-specific
    @staticmethod
    def getarticlelist():
        if PublishArticle.__articlelist == None:
            PublishArticle.__articlelist = []
        return PublishArticle.__articlelist

    # instance methods receive a specific object instance as an argument
    # and operate on data specific to that object instance
    #     def create_test_article(self, author, name='unsure yet'):

    def __init__(self, author='tbc identity', name='unsure yet'):
  
        self.author = author
        self.articlename = name
        
        internalarticlelist = PublishArticle.getarticlelist()

        if (not internalarticlelist == None):
            internalarticlelist.append(self)
        else:
            print("internal __articlelist not working")
        
    @staticmethod
    def showarticlelist():
        #reset articles counter:
        PublishArticle.__numberArticles = 0
        # see the cells
        if (not PublishArticle.__articlelist):
            print('no articles published yet')
            return PublishArticle.__numberArticles
            # raise AttributeError('no cells found')
        else:
            for a in PublishArticle.__articlelist:
                print(f'Article ref: {a.articlename}, {a.author}, {a}')
                PublishArticle.__numberArticles += 1
            return PublishArticle.__numberArticles

    # instance methods
    def setarticledetails(self, articlename, author=None):
        self.author = author
        self.articlename = articlename

def main():
    # demonstrate start
    print("Published articles: ", PublishArticle.showarticlelist())

    # declare cells
    a1 = PublishArticle()
    a2 = PublishArticle('tired old author', 'last epic')
    a3 = PublishArticle(name='newbookname')


    # demonstrate published so far
    print("Published articles: ", PublishArticle.showarticlelist())

    a1.setarticledetails('new great writer', 'fancy book')
    print("Published articles: ", PublishArticle.showarticlelist())


if __name__ == '__main__': main()