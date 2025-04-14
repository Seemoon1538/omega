from core.database.models import News, db

class NewsRepository:
    def create(self, title, text):
        new_news = News(title=title, text=text, timestamp=db.func.now())
        db.session.add(new_news)
        db.session.commit()
        return new_news

    def get_by_id(self, news_id):
        return News.query.get(news_id)

    def get_all(self):
        return News.query.order_by(News.timestamp.desc()).all()

    def update(self, news_id, title, text):
        news = self.get_by_id(news_id)
        if news:
            news.title = title
            news.text = text
            db.session.commit()
            return news
        return None

    def delete(self, news_id):
        news = self.get_by_id(news_id)
        if news:
            db.session.delete(news)
            db.session.commit()