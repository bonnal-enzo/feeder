import time
import sys
import logging
from common.common import Coords, ClicPoint, DragAndDropsRecorder

class ClicPointFactory:
    ref_origin = Coords(209.46170043945312, 55.83537292480469)

    ref_fami_slot_relative_coords = Coords(945.1976318359375, 284.1272888183594).minus(ref_origin)
    ref_equip_tab_relative_coords = Coords(1058.3575439453125, 184).minus(ref_origin)
    ref_resou_tab_relative_coords = Coords(1118.3980712890625, 184).minus(ref_origin)
    ref_first_inv_slot_relative_coords = Coords(1031.5552978515625, 278.10980224609375).minus(ref_origin)

    ref_tabs_x_diff = ref_resou_tab_relative_coords.x - ref_equip_tab_relative_coords.x

    ref_inv_slot_width = 1097.438720703125 - 1055.46826171875
    ref_inv_slot_height = 340.6443786621094 - 299.8241271972656

    def __init__(self, equip_tab_coords: Coords, equip_to_resources_vector_coords: Coords):
        if equip_tab_coords is None or equip_to_resources_vector_coords is None:
            self.coef = 1  # TODO remove, dev only
            self.origin = self.ref_origin
        else:
            self.coef = equip_to_resources_vector_coords.x / self.ref_tabs_x_diff
            self.origin = equip_tab_coords.minus(self.ref_equip_tab_relative_coords.times(self.coef))
        print("using coef=", self.coef)

    def _true_coords_from_ref(self, coords):
        return coords.times(self.coef).plus(self.origin)

    def create_fami_inv_slots(self, n_famis):
        return [
            ClicPoint(
                self._true_coords_from_ref(self.ref_first_inv_slot_relative_coords)
                .plus(
                    Coords(
                        self.ref_inv_slot_width * self.coef * (i % 4),
                        self.ref_inv_slot_height * self.coef * (i // 4)
                    )
                )
            )
            for i in range(n_famis)
        ]
    
    def create_equipment_tab(self):
        return ClicPoint(self._true_coords_from_ref(self.ref_equip_tab_relative_coords))

    def create_resources_tab(self):
        return ClicPoint(self._true_coords_from_ref(self.ref_resou_tab_relative_coords))
    
    def create_fami_slot(self):
        return ClicPoint(self._true_coords_from_ref(self.ref_fami_slot_relative_coords))

    def create_food_inv_slot(self):
        return ClicPoint(self._true_coords_from_ref(self.ref_first_inv_slot_relative_coords))

class FeedStrategy:
    def __init__(self, clic_point_factory: ClicPointFactory, n_famis: int, dry_run: bool):
        self.fami_inv_slots: iter[ClicPoint] = clic_point_factory.create_fami_inv_slots(n_famis)
        self.equip_tab: ClicPoint = clic_point_factory.create_equipment_tab()
        self.res_tab: ClicPoint = clic_point_factory.create_resources_tab()
        self.fami_slot: ClicPoint = clic_point_factory.create_fami_slot()
        self.food_inv_slot: ClicPoint = clic_point_factory.create_food_inv_slot()
        self.dry_run = dry_run

    def give_food(self):
        if self.dry_run:
            self.food_inv_slot.point_at()
            self.fami_slot.point_at()
        else:
            self.food_inv_slot.drag_and_drop(self.fami_slot)

    def feed(self):
        self.equip_tab.clic()
        self.fami_inv_slots[0].double_clic()
        self.res_tab.clic()
        self.give_food()
        for fami_inv_slot in self.fami_inv_slots[:-1]:
            self.equip_tab.clic()
            fami_inv_slot.double_clic()
            self.res_tab.clic()
            self.give_food()


if __name__ == "__main__":
    n_famis: int = int(sys.argv[1])
    dry_run = "--dry-run" in sys.argv

    ClicPoint.actions_delay_seconds = 0.3
    dd_recorder = DragAndDropsRecorder()
    dd_recorder.start()
    time.sleep(6)
    dd_recorder.stop()

    clic_point_factory = ClicPointFactory(
        dd_recorder.last_origin(),
        dd_recorder.last_vector()
    )
    feed_strat = FeedStrategy(clic_point_factory, n_famis, dry_run)
    logging.getLogger().setLevel("INFO")
    logging.info(f"Entering feed with n_famis={n_famis}, dry_run= {dry_run}, last vector={dd_recorder.last_vector().tuple}")
    feed_strat.feed()
