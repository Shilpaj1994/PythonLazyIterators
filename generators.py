"""
Module to read to data from the csv file
Author: Shilpaj Bhalerao
Date: Aug 01, 2021
"""
# Standard Library Import
from collections import namedtuple, Counter


class LazyIterator:
    """
    LazyIterator class to read from *.csv file and return namedtuple of data in each row
    """
    def __init__(self, filename):
        """
        Constructor
        """
        # To check if all the rows are read from the file
        self.exhausted = False

        # Namedtuple to store the date information
        self.Date = namedtuple('Date', "month day year")
        self.Date.__doc__ = 'Date on which the traffic violation was issued'
        self.Date.month.__doc__ = 'Month of the year'
        self.Date.day.__doc__ = 'Day of the month'
        self.Date.year.__doc__ = 'Year'

        # Data type of each field in the namedtuple
        self.data_types = ['INT', 'STRING', 'STRING', 'STRING', 'DATE', 'INT', 'STRING', 'STRING', 'STRING']

        self.file = open(filename, 'r')

        # Create an iterator for iterating over rows of a file
        self.file_iter = iter(self.file)

        # Format the 1st line to extract the headers from the file
        headers = next(self.file_iter).replace(' ', '').strip('\n').split(',')

        # Create a namedtuple for the violation data
        self.Data = namedtuple('Data', headers, defaults=[None] * len(headers))
        self.Data.__doc__ = "Traffic violation data"
        self.Data.SummonsNumber.__doc__ = "Record number associated with the violations"
        self.Data.PlateID.__doc__ = "Plate Number of the vehicle"
        self.Data.RegistrationState.__doc__ = "State in which the vehicle is registered"
        self.Data.PlateType.__doc__ = "Type of number plate on the vehicle"
        self.Data.IssueDate.__doc__ = "Date on which the violation was issued"
        self.Data.ViolationCode.__doc__ = "Traffic violation code"
        self.Data.VehicleBodyType.__doc__ = "Type of the vehicle body"
        self.Data.VehicleMake.__doc__ = "Manufacturing Company of the vehicle"
        self.Data.ViolationDescription.__doc__ = "Description of Violation"

    def __iter__(self):
        """
        Method to create an iterator
        """
        return self

    def __next__(self):
        """
        Method to access next row from the file
        """
        row_data = self.cast_row(self.data_types, next(self.file_iter).replace(' ', '').strip('\n').split(','))
        if row_data is not None:
            return row_data
        raise StopIteration

    def cast_row(self, data_type, data_row):
        """
        Function to return the casted value of the data row
        :param data_type: Expected data type
        :param data_row: Input data row
        :return: Data row in the converted format
        """
        casted_data = (self.cast(data_type, value) for data_type, value in zip(data_type, data_row))

        _data = self.Data(*casted_data)
        return _data

    def cast(self, data_type, value):
        """
        Function to cast appropriate data type for the input value
        :param data_type: Expected data type
        :param value: Input value
        :return: Converted value in the data_type
        """
        if data_type == 'STRING':
            return str(value)
        elif data_type == 'INT':
            return int(value)
        elif data_type == 'DATE':
            value = value.split('/')
            return self.Date(*value)


if __name__ == '__main__':
    # Create an Iterator Object
    _object = LazyIterator('nyc_parking_tickets_extract-1.csv')
    iterator_object = iter(_object)

    # List to store the data
    parking_data = []

    # Access row data from the iterator
    for row in iterator_object:
        print(row)
        parking_data.append(row)

    # Print the number of violations for Car Make
    violation_data = Counter(data.VehicleMake for data in parking_data if data is not None)
    print(violation_data)
