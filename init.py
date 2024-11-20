from nex_logger import logger
from result_codes import init_result_codes
from nex_types import variant
from nex_types.datetime import DateTime
from nex_types.bool import Bool

nexlogger = logger.NewLogger()

def init():
    init_result_codes()
    
    variant.register_variant_type(1, Bool(False))
    variant.register_variant_type(2, DateTime(0))