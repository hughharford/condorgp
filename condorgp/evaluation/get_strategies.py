import logging
from decimal import Decimal

from nautilus_trader.examples.strategies.ema_cross import EMACross
from nautilus_trader.examples.strategies.ema_cross import EMACrossConfig

class GetStrategies():

    def __init__(self, instrument, bar_type = ""):
        self.instrument = instrument
        if bar_type == "":
            bar_type = "AUD/USD.SIM-1-MINUTE-MID-INTERNAL"
        self.bar_type = bar_type
        # logging.info(f"{__name__} init: INSTR: {self.instrument} BAR: {self.bar_type}")

    def get_strategy(self, config_ev=""):
        if config_ev:
            config = self.get_injected_config(injected_config=config_ev)
        else:
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
            400, # 10
            820, # 20
            )
        return config

    def get_injected_config(self, injected_config):
        if injected_config:
            config = injected_config
        else:
            config = self.get_config_strategy_without_full_declaration()
        return config

if __name__ == "__main__":
    from nautilus_trader.model.identifiers import Venue
    from nautilus_trader.test_kit.providers import TestInstrumentProvider

    SIM = Venue("SIM")
    AUDUSD_SIM = TestInstrumentProvider.default_fx_ccy("AUD/USD", SIM)

    ns = GetStrategies(instrument = AUDUSD_SIM)
    config = ns.get_config_strategy_without_full_declaration()
    print(type(config))
