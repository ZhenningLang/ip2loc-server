# -*- coding: utf-8 -*-

from .log import logger
from .util import is_good_file, unzip


class DataModel:

    def __init__(self, *, csv_loc: str, zip_loc: str = None):
        self._csv_loc = csv_loc
        self._zip_loc = zip_loc
        is_csv_good = is_good_file(csv_loc)
        is_zip_good = is_good_file(zip_loc)
        if not self._is_data_ready():
            if not is_csv_good and not is_zip_good:
                logger.critical(f'No available data in {self.__class__}, '
                                f'neither csv(zip) nor any other types of data!')
                exit(11)
            if not is_csv_good and is_zip_good:
                self._unzip_to_csv()
            assert is_good_file(csv_loc)
            self._build_data()
        assert self._is_data_ready()

    def _unzip_to_csv(self):
        logger.info(f"Unzip '{self._zip_loc}' \nto '{self._csv_loc}'")
        unzip(self._zip_loc, self._csv_loc)

    def _is_data_ready(self) -> bool:
        raise NotImplementedError()

    def _build_data(self):
        raise NotImplementedError()

    def select_data(self, idx: int):
        """ Select data by index
        :return {
            'id': 'id',
            'ip_from': 'ip_from',
            'ip_to': 'ip_to',
            'country_code': 'country_code',
            'country_name': 'country_name',
            'region_name': 'region_name',
            'city_name': 'city_name',
            'latitude': 'latitude',
            'longitude': 'longitude'
        }
        """
        raise NotImplementedError()


class MemoryDataModel(DataModel):
    HEADER = ('id', 'ip_from', 'ip_to',
              'country_code', 'country_name', 'region_name', 'city_name',
              'latitude', 'longitude')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.data is a list of dict
        # the data structure of dict is
        # {
        #     'id': 'id',
        #     'ip_from': 'ip_from',
        #     'ip_to': 'ip_to',
        #     'country_code': 'country_code',
        #     'country_name': 'country_name',
        #     'region_name': 'region_name',
        #     'city_name': 'city_name',
        #     'latitude': 'latitude',
        #     'longitude': 'longitude'
        # }
        # In addition, the index of a dict equals its 'id'
        self.data = []

    def _build_data(self):
        with open(self._csv_loc, 'r') as csv:
            idx = 0
            while True:
                line = csv.readline()
                if not line:
                    break
                item = line.strip('\n').strip('"')
                if not item:
                    break
                # noinspection PyTypeChecker
                data_list = [idx] + item.split('","')
                self.data.append(dict(zip(MemoryDataModel.HEADER, data_list)))

    def select_data(self, idx: int):
        return self.data[idx]

    def _is_data_ready(self) -> bool:
        return bool(self.data)


class SQLMemoryDataModel(DataModel):
    TABLE_NAME = 'ip2location'

    def __init__(self, db_conn_url, *args, **kwargs):
        self.db_conn_url = db_conn_url
        self.conn = None  # TODO
        super().__init__(*args, **kwargs)

    def _build_data(self):
        pass

    def select_data(self, idx: int):
        pass

    def _is_data_ready(self) -> bool:
        pass
