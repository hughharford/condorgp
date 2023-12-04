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
#        config = self.get_config_strategy()
        config = self.get_config_strategy_without_full_declaration()
        strategy = EMACross(config=config)
        return strategy

    def get_config_strategy(self):
        config = EMACrossConfig(
            instrument_id=str(self.instrument.id),
            bar_type=self.bar_type,
            trade_size=Decimal(1_000_000),
            fast_ema_period=100,
            slow_ema_period=200,
            )
        return config

    def get_config_strategy_without_full_declaration(self):
        config = EMACrossConfig(
            str(self.instrument.id),
            self.bar_type,
            Decimal(1_000_000),
            100,
            200,
            )
        return config

if __name__ == "__main__":
    from nautilus_trader.model.identifiers import Venue
    from nautilus_trader.test_kit.providers import TestInstrumentProvider

    SIM = Venue("SIM")
    AUDUSD_SIM = TestInstrumentProvider.default_fx_ccy("AUD/USD", SIM)

    ns = CGPNautilusStrategies(instrument = AUDUSD_SIM)
    config = ns.get_config_strategy_without_full_declaration()
    print(type(config))
