import logging
from decimal import Decimal

from nautilus_trader.examples.strategies.ema_cross import EMACross
from nautilus_trader.examples.strategies.ema_cross import EMACrossConfig

from condorgp.evaluation.gp_run_strat_base import GpRunStrategyBase
from condorgp.evaluation.gp_run_strat_base import GpRunStrategyBaseConfig
from condorgp.evaluation.gp_run_strat_inject import GpRunStrategyInject

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

    def get_std_config_for_evolved_strategy(self):
        config = GpRunStrategyBaseConfig(
            str(self.instrument.id),
            self.bar_type,
            trade_size=Decimal(1_000_000),
            fast_ema_period=40, # 10
            slow_ema_period=82, # 20
            )
        return config

    def get_evolved_strategy(self, ev_strategy=""):
        config = self.get_std_config_for_evolved_strategy()
        if ev_strategy:
            # i.e. run inherited strategy with adjusted check_triggers method
            self.ev_strategy = GpRunStrategyInject(
                                            config=config,
                                            ev_strategy=ev_strategy)
        else:
            # i.e. run standard strategy, but with check_triggers method
            self.ev_strategy = GpRunStrategyBase(config=config)
        return self.ev_strategy

if __name__ == "__main__":
    from nautilus_trader.model.identifiers import Venue
    from nautilus_trader.test_kit.providers import TestInstrumentProvider

    SIM = Venue("SIM")
    AUDUSD_SIM = TestInstrumentProvider.default_fx_ccy("AUD/USD", SIM)

    ns = GetStrategies(instrument = AUDUSD_SIM)
    config = ns.get_config_strategy_without_full_declaration()
    print(type(config))
