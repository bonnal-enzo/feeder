import time
import sys
import logging
from common.common import Coords, ClicPoint, DragAndDropsRecorder

class ForgeStrategy:
    def __init__(self, first_runes: ClicPoint, second_runes: ClicPoint, n_first_runes: int, n_second_runes: int, dry_run: bool):
        self.first_runes: ClicPoint = first_runes
        self.second_runes: ClicPoint = second_runes
        self.n_first_runes = n_first_runes
        self.n_second_runes = n_second_runes
        self.dry_run = dry_run

    def use_runes(self, runes: ClicPoint, times: int):
        if self.dry_run:
            runes.point_at()
        else:
            for _ in range(times):
                runes.clic()

    def forge(self):
        while True:
            self.use_runes(self.first_runes, self.n_first_runes)
            self.use_runes(self.second_runes, self.n_second_runes)


if __name__ == "__main__":
    n_first_runes: int = int(sys.argv[1])
    n_second_runes: int = int(sys.argv[2])
    dry_run = "--dry-run" in sys.argv

    ClicPoint.actions_delay_seconds = 0.3
    dd_recorder = DragAndDropsRecorder()
    dd_recorder.start()
    time.sleep(6)
    dd_recorder.stop()


    forge_strat = ForgeStrategy(
        ClicPoint(Coords(*dd_recorder.clicks[-2])),
        ClicPoint(Coords(*dd_recorder.clicks[-1])),
        n_first_runes,
        n_second_runes,
        dry_run
    )

    logging.getLogger().setLevel("INFO")
    logging.info(f"Entering forge with last vector={dd_recorder.last_vector().tuple}, dry_run= {dry_run}")
    forge_strat.forge()
