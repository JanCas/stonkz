from django.db import models


class ModelTraining(models.Model):
    REGRESSION = 0
    CLASSIFICATION = 1
    MODEL_TYPE_CHOICES = [
        (REGRESSION, 'regression'),
        (CLASSIFICATION, 'classification')
    ]

    sklearn_model = models.CharField(max_length=50, default=None, null=False)
    ticker = models.ForeignKey('base.Tickers', on_delete=models.CASCADE, null=False)
    portfolio = models.ForeignKey('trading.Portfolio', on_delete=models.SET_NULL, null=True, blank=True)
    accuracy = models.IntegerField(default=None, null=True, blank=True)
    model_type = models.SmallIntegerField(default=CLASSIFICATION, choices=MODEL_TYPE_CHOICES, null=False)

    def __str__(self):
        return ' '.join([str(self.ticker), self.sklearn_model])

    class Meta:
        verbose_name = 'Model Training'
        verbose_name_plural = 'Model Trainings'

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
        y_label = ticker_data_normalized['close'] > 0 # stock went up during that period

        # splitting data into train/test set
        print('splitting data in test/train')
        rows, _ = ticker_data_normalized.size()
        training_size_num = rows * train_size
        ticker_data_train = ticker_data_normalized[:training_size_num]
        ticker_data_test = ticker_data_normalized[training_size_num+1:]
        y_label_train = y_label[:training_size_num]
        y_label_test = y_label[training_size_num+1:]

        #training and testing model
        print('training model')
        model = import_sklearn_module(self.sklearn_model)
        model.fit(ticker_data_train, y_label_train)

        self.accuracy = model.score(ticker_data_test, y_label_test)
        print('model accuracy {}'.format(self.accuracy))
        self.save()

        print()
