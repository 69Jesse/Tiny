from pyhtsl import trigger_function
from constants import MACHINE_EFFECT_INDEX
from functions import maybe_apply_machine_effect


MACHINE_EFFECT_INDEX.value = 0
trigger_function(maybe_apply_machine_effect)
