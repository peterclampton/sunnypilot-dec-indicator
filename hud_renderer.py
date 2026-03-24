"""
Copyright (c) 2021-, Haibin Wen, sunnypilot, and a number of other contributors.

This file is part of sunnypilot and is licensed under the MIT License.
See the LICENSE.md file in the root directory for more details.
"""
import pyray as rl
from openpilot.system.ui.lib.application import gui_app

from openpilot.selfdrive.ui.mici.onroad.hud_renderer import HudRenderer
from openpilot.selfdrive.ui.sunnypilot.onroad.blind_spot_indicators import BlindSpotIndicators


class HudRendererSP(HudRenderer):
  def __init__(self):
    super().__init__()
    self.blind_spot_indicators = BlindSpotIndicators()
    self._txt_exp_mode = gui_app.texture('icons_mici/experimental_mode.png', 28, 28)

  def _update_state(self) -> None:
    super()._update_state()
    self.blind_spot_indicators.update()

  def _render(self, rect: rl.Rectangle) -> None:
    super()._render(rect)
    self.blind_spot_indicators.render(rect)
    self._draw_dec_indicator(rect)

  def _draw_dec_indicator(self, rect: rl.Rectangle) -> None:
    """Draw small experimental mode icon in top-right corner when active."""
    try:
      from openpilot.selfdrive.ui.ui_state import ui_state
      exp_mode = ui_state.sm["selfdriveState"].experimentalMode
      dec_blended = False
      try:
        lp_sp = ui_state.sm["longitudinalPlanSP"]
        dec = lp_sp.dec
        dec_blended = dec.active and dec.state.raw == 1
      except Exception:
        pass
      if exp_mode or dec_blended:
        x = int(rect.x + rect.width - 46)
        y = int(rect.y + 14)
        rl.draw_texture(self._txt_exp_mode, x, y, rl.WHITE)
    except Exception:
      pass

  def _has_blind_spot_detected(self) -> bool:
    return self.blind_spot_indicators.detected
