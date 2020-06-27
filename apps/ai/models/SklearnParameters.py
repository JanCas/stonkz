from django.db import models


class SklearnParameters(models.Model):

    INT = 0
    FLOAT = 1
    STRING = 2
    DATA_TYPE_CHOICES = [
        (INT, 'int'),
        (FLOAT, 'float'),
        (STRING, 'string'),
    ]

    model_training = models.ForeignKey('ai.ModelTraining', on_delete=models.CASCADE)
    parameter = models.CharField(max_length=50, default=None)
    data_type = models.SmallIntegerField(default=INT, choices=DATA_TYPE_CHOICES, null=True, blank=True)
    value = models.CharField(max_length=50, default=None, null=True, blank=True)

    def get_value(self):
        if self.data_type == self.INT:
            return int(self.data_type)
        elif self.data_type == self.FLOAT:
            return float(self.data_type)
        elif self.data_type == self.STRING:
            return self.data_type
