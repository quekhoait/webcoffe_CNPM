from eapp.models.WarehouseSlip import SlipType
from eapp.services.ExportStrategy import ExportStrategy
from eapp.services.ImportStrategy import ImportStrategy
from eapp.services.SlipStrategy import SlipStrategy
from eapp.services.TransferStrategy import TransferStrategy
from eapp.services.UpdateStrategy import UpdateStrategy


class SlipStrategyFactory:
    SLIP_TYPE_DICT = {
        SlipType.EXPORT : ExportStrategy,
        SlipType.IMPORT : ImportStrategy,
        SlipType.TRANSFER : TransferStrategy,
        SlipType.UPDATE : UpdateStrategy 
    }

    @staticmethod
    def get_strategy(slip_type: SlipType) -> SlipStrategy:
        return SlipStrategyFactory.SLIP_TYPE_DICT.get(slip_type)()