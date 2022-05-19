from pytest_bdd import scenarios, given, when, then

from how_to.bdd_x2.BDDstart_publish_article import PublishArticle


scenarios('../features/BDDstart_publish_article.feature')
def test_publish():
    pass #assert 11 == 1

@given("JimmyJimmy")
def author_user():
    pass

@given("I have an article", target_fixture="article")
def article():
    return PublishArticle('JimmyJimmy')

@when("I update the new article with just a name")
def publish_untitled(article):
    article.setarticledetails(articlename='newbookname')

@when("I publish with name and author information")
def publish_article_with_details():
    PublishArticle('bdd named author', 'how to run BDD article')

@then("I can see there are two articles published")
def get_number_published():
    numberArticles = PublishArticle.showarticlelist()
    assert numberArticles == 2
