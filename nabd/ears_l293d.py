import asyncio
import logging
import 1293d.driver as 1293d
from concurrent.futures import ThreadPoolExecutor
from .ears import Ears

#https://www.instructables.com/DC-Motor-Control-With-Raspberry-Pi-and-L293D/
#https://keithweaverca.medium.com/controlling-dc-motors-using-python-with-a-raspberry-pi-40-pin-f6fa891dc3d
class EarsCustom(Ears):  # pragma: no cover
    """
    Implementation for ears based on /dev/ear*.
    Relying on tagtagtag-ears driver.
    """

    def __init__(self):
        self.motor = [None, None]
        self.callback = None
        self.positions = [None, None]
        self.motorPosition = [0, 0]
                
        try:
            self.motor[0] = 1293d.motor(22,18,16)
            asyncio.get_event_loop().add_reader(ear, self._do_read, 0)
            
            self.motor[1] = 1293d.motor(15,13,12)
            asyncio.get_event_loop().add_reader(ear, self._do_read, 1)

        except Exception:
            logging.error(f"ear {i} is apparently broken")
            1239d.cleanup()
        self.executor = ThreadPoolExecutor(max_workers=1)
        # Lock preventing detection and move operations happening
        # simultaneously
        self.lock = asyncio.Lock()

    def _do_read(self, ear):
        self.positions[ear] = self.motorPosition[ear]

    def on_move(self, loop, callback):
        """
        Define the callback for ears events.
        callback is cb(ear) with ear being LEFT_EAR or RIGHT_EAR.
        The callback is called on the provided event loop, with
        loop.call_soon_threadsafe
        """
        self.callback = (loop, callback)

    async def reset_ears(self, target_left, target_right):
        """ Reset the ears to a known position """
        async with self.lock:
            await asyncio.get_event_loop().run_in_executor(
                self.executor, self._do_reset_ears, target_left, target_right
            )

    def _do_reset_ears(self, target_left, target_right):
        """
        Reset ears by running a detection and ignoring the result.
        Thread: executor
        Lock: acquired
        """
        1239d.cleanup();

    async def move(self, motor, delta, direction):
        """
        Move an ear by a delta (position) in a direction.
        May run a complete turn.
        Returns before ear reached requested position.
        """
        async with self.lock:
            await asyncio.get_event_loop().run_in_executor(
                self.executor, self._do_move, motor, delta, direction
            )

    def _do_move(self, motor, delta, direction):
        """
        Move a given ear by a delta in a given direction.
        Thread: executor
        Lock: acquired
        """
        if direction:
            cmd = b"-"
        else:
            cmd = b"+"
        if self.fds[motor] is not None:
            os.write(self.fds[motor], cmd + bytes([delta]))

    async def wait_while_running(self):
        """
        Wait until both ears stopped.
        """
        async with self.lock:
            await asyncio.get_event_loop().run_in_executor(
                self.executor, self._do_wait_while_running
            )

    def _do_wait_while_running(self):
        """
        Wait until motors are no longer running, sending a blocking NOP to ears.
        Thread: executor
        Lock: acquired
        """        
        if self.fds[0] is not None:
            os.write(self.fds[0], b".")
        if self.fds[1] is not None:
            os.write(self.fds[1], b".")

    async def get_positions(self):
        """
        Get the position of the ears, without running any detection.
        """
        async with self.lock:
            await asyncio.get_event_loop().run_in_executor(
                self.executor, lambda: self._do_detect_positions(False)
            )
            return (self.positions[0], self.positions[1])

    async def detect_positions(self):
        """
        Get the position of the ears, running a detection if required.
        """
        async with self.lock:
            await asyncio.get_event_loop().run_in_executor(
                self.executor, lambda: self._do_detect_positions(True)
            )
            return (self.positions[0], self.positions[1])

    def _do_detect_positions(self, run_detection):
        """
        Get the position of the ears, running a detection if requested.
        Thread: executor
        Lock: acquired
        """
        self._do_wait_while_running()

    async def go(self, ear, position, direction):
        """
        Go to a specific position.
        If direction is 0, turn forward, otherwise, turn backward
        If position is not within 0-16, it represents additional turns.
        For example, 17 means to position the ear at 0 after at least a
        complete turn.
        Returns before ear reached requested position.
        """
        async with self.lock:
            await asyncio.get_event_loop().run_in_executor(
                self.executor, self._do_go, ear, position, direction
            )

    def _do_go(self, ear, position, direction):
        """
        Actually go to a specific position.
        Lock: acquired.
        """        
        if direction:
           for i in range(ear, position):
             motor1.clockwise()
           self.motorPosition[ear] = self.motorPosition[ear] + position
        else:
           for i in range(ear, position):
             motor1.anticlockwise()
           self.motorPosition[ear] = self.motorPosition[ear] - position


    def is_broken(self, ear):
        """
        Determine if ear is apparently broken
        """
        return self.motor[ear] is None
