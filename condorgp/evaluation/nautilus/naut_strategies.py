import logging
from decimal import Decimal

from nautilus_trader.examples.strategies.ema_cross import EMACross
from nautilus_trader.examples.strategies.ema_cross import EMACrossConfig

class CGPNautilusStrategies():

    def __init__(self, instrument, bar_type = ""):
        self.instrument = instrument
        if bar_type == "":
            bar_type = "AUD/USD.SIM-1-MINUTE-MID-INTERNAL"
        self.bar_type = bar_type
        logging.info(f"{__name__} init: {self.instrument} {self.bar_type}")

    def get_strategy(self):
        config = self.get_config_strategy()
        strategy = EMACross(config=config)
        return strategy

    def get_config_strategy(self):
        config = EMACrossConfig(
            instrument_id=str(self.instrument.id),
            bar_type=self.bar_type,
            fast_ema_period=100,
            slow_ema_period=200,
            trade_size=Decimal(1_000_000),
            )
        return config
