
class StockPrice:
    open: float
    close: float
    high: float
    low: float
    average: float
    ceiling: float
    floor: float
    volume: int

class ConnectionError(Exception):
    pass

class ParsingError(Exception):
    pass
