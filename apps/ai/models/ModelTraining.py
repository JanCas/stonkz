from django.db import models


class ModelTraining(models.Model):
    REGRESSION = 0
    CLASSIFICATION = 1
    MODEL_TYPE_CHOICES = [
        (REGRESSION, 'regression'),
        (CLASSIFICATION, 'classification')
    ]

    name = models.CharField(max_length=50, default=None, null=True, blank=True)
    sklearn_model = models.CharField(max_length=50, default=None, null=True)
    accuracy = models.IntegerField(default=None, null=True, blank=True)
    model_type = models.SmallIntegerField(default=CLASSIFICATION, choices=MODEL_TYPE_CHOICES, null=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Model Training'
        verbose_name_plural = 'Model Trainings'

    def preprocess_data(self, test_size = .3, random_state=42):
        """
        :param test_size:
        :param random_state:
        :return: x_train, x_test, y_train, y_test
        """
        from yahooquery import Ticker
        from sklearn.model_selection import train_test_split
        from API.Help import pct_change
        from apps.trading.models.PortfolioItems import PortfolioItems

        portfolio_item = PortfolioItems.objects.get(ai_model=self)
        ticker_history = Ticker(str(portfolio_item)).history(interval=portfolio_item.portfolio.get_trading_frequency(),
                                                             period=portfolio_item.portfolio.get_max_period())

        #cleaning the data
        if all(elem in list(ticker_history) for elem in ['dividends', 'splits']):
            ticker_history = ticker_history.drop(['dividends', 'splits'], axis=1)

        #applying pct_change and dropping NA values
        ticker_history = pct_change(ticker_history).dropna()

        # predicting next period movement based on last period numbers
        y_label = (ticker_history['close'] > 0).shift(-1).dropna() == True
        ticker_history = ticker_history[:-1]

        assert(ticker_history.size()[0] == y_label.size()[0])
        return train_test_split(ticker_history, y_label, test_size=test_size, random_state=random_state)




    def initialize_model(self):
        pass

    def train(self, train_size=.8):
        from API.Help import import_sklearn_module, pct_change
        from yahooquery import Ticker

        print('training data for {}---------------------------'.format(str(self.ticker)))
        # retrieving data
        print('retrieving data')
        period = self.portfolio.get_max_period()
        interval = self.portfolio.get_trading_frequency()
        ticker_data = Ticker(str(self.ticker)).history(period=period, interval=interval)
        ticker_data_normalized = pct_change(ticker_data).dropna()
        y_label = ticker_data_normalized['close'] > 0  # stock went up during that period

        # splitting data into train/test set
        print('splitting data in test/train')
        rows, _ = ticker_data_normalized.size()
        training_size_num = rows * train_size
        ticker_data_train = ticker_data_normalized[:training_size_num]
        ticker_data_test = ticker_data_normalized[training_size_num + 1:]
        y_label_train = y_label[:training_size_num]
        y_label_test = y_label[training_size_num + 1:]

        # training and testing model
        print('training model')
        model = import_sklearn_module(self.sklearn_model)
        model.fit(ticker_data_train, y_label_train)

        self.accuracy = model.score(ticker_data_test, y_label_test)
        print('model accuracy {}'.format(self.accuracy))
        self.save()
        print()
