from django.db import models

from datetime import datetime

# Create your models here.
class TestClass(models.Model):
    test_int = models.IntegerField()
    test_double = models.DecimalField(max_digits=12, decimal_places=8)
    test_string = models.CharField(max_length=100) # use TextField if large string
    test_bool = models.BooleanField()
    test_date = models.DateField()

    def set_values(self, test_int, test_double, test_string, test_bool, test_date_string):
    	self.test_int = test_int
    	self.test_double = test_double
    	self.test_string = test_string
    	self.test_bool = test_bool
    	self.date = datetime.strptime(test_date_string, '%m %d %Y')

    def __str__(self):
        return str(self.test_int) + ' ' + str(self.test_double) + ' ' + self.test_string + ' ' + str(self.test_bool) + ' ' + str(self.test_date)
