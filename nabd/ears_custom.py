import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from .ears_custom_driver import EarsCustomDrivers
from .ears import Ears


class EarsCustom(Ears):  # pragma: no cover
    """
    Implementation for ears based on /dev/ear*.
    Relying on tagtagtag-ears driver.
    """

    def __init__(self):
        logging.debug("EAR INIT")
        self.fds = [None, None]
        self.callback = None
        self.positions = [None, None]
        self.cpt = [1, 1]
        self.os = EarsCustomDrivers()
        self.os.attach(self)
        for i in range(0, 2):
            ear = self.os.open("/dev/ear" + str(i))
            #try:
            self.os.write(ear, "?")
            logging.debug("EAR    {a} write cmd=?".format(a=ear))
                #asyncio.get_event_loop().add_reader(ear, self._do_read, i)
            #except Exception:
            #    logging.error(f"ear {i} is apparently broken")
            #    self.os.close(ear)
            #    logging.debug("EAR    {a} close".format(a=ear))
        self.executor = ThreadPoolExecutor(max_workers=1)
        # Lock preventing detection and move operations happening
        # simultaneously
        self.lock = asyncio.Lock()

    def update(self, ear):
        logging.debug('EAR UPDATE {a}'.format(a=ear))
        self._do_read(ear)

    def _do_read(self, ear):
        logging.debug("EAR READ")
        #byte = self.os.read(self.fds[ear])
        byte = b"\xf0"#self.os.read(ear)
        logging.debug("EAR {a} read".format(a=ear))
        ###
        #if len(byte) == "0":
        #    # EOF, ear is broken.
        #    logging.error(f"ear {ear} has been declared broken")
        #    fd = self.fds[ear]
        #    asyncio.get_event_loop().remove_reader(fd)
        #    self.os.close(fd)
        #    logging.debug("EAR {a} close".format(a=fd))
        #    self.positions[ear] = None
        #    self.fds[ear] = None
        #else:
        #    if byte == b"m":
        #        if self.callback:
        ##            (loop, callback) = self.callback
        #            loop.call_soon_threadsafe(lambda ear=ear: callback(ear))
        #    elif byte == b"\xff":
        #        self.positions[ear] = None
        #    else:
        #        self.positions[ear] = byte[0]

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
        logging.debug("EAR RESET {a} {b}".format(a=target_left, b=target_right))
        """
        Reset ears by running a detection and ignoring the result.
        Thread: executor
        Lock: acquired
        """
        if self.fds[0] is not None:
            self.os.write(self.fds[0], ">",target_left)
            #logging.debug("EAR    {a} write cmd=> target={b}".format(a=self.fds[0], b=target_left))
        if self.fds[1] is not None:
            self.os.write(self.fds[1], ">", target_right)
            #logging.debug("EAR    {a} write cmd=> target={b}".format(a=self.fds[1], b=target_right))

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
        logging.debug("EAR MOVE {a} {b} {c}".format(a=motor, b=delta, c=direction))
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
            #logging.debug("EAR    {a} write cmd={b} delta={c}".format(a=self.fds[motor], b=cmd, c=delta))
            os.write(self.fds[motor], cmd ,delta)
    async def wait_while_running(self):
        """
        Wait until both ears stopped.
        """
        async with self.lock:
            await asyncio.get_event_loop().run_in_executor(
                self.executor, self._do_wait_while_running
            )

    def _do_wait_while_running(self):
        logging.debug("EAR WAIT")
        """
        Wait until motors are no longer running, sending a blocking NOP to ears.
        Thread: executor
        Lock: acquired
        """
        if self.fds[0] is not None:
            self.os.write(self.fds[0], b".")
            #logging.debug("EAR    {a} write cmd=.".format(a=self.fds[0]))
        if self.fds[1] is not None:
            self.os.write(self.fds[1], b".")
            #logging.debug("EAR    {a} write cmd=.".format(a=self.fds[1]))

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
        if run_detection:
            logging.debug("EAR DETECT True")
            command = b"!"
        else:
            logging.debug("EAR DETECT False")
            command = b"?"
        if self.fds[0] is not None:
            self.os.write(self.fds[0], command)
            #logging.debug("EAR    {a} write cmd={b}".format(a=self.fds[0], b=command))
        if self.fds[1] is not None:
            self.os.write(self.fds[1], command)
            #logging.debug("EAR    {a} write cmd={b}".format(a=self.fds[1], b=command))
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
        logging.debug("EAR GO {a} {b} {c}".format(a=ear, b=position, c=direction))
        """
        Actually go to a specific position.
        Lock: acquired.
        """
        if direction:
            cmd = b"<"
        else:
            cmd = b">"
        if self.fds[ear] is not None:
            self.os.write(self.fds[ear], cmd, position)
            #logging.debug("EAR    {a} write cmd={b} pos={c}".format(a=ear, b=cmd, c=position))

    def is_broken(self, ear):
        logging.debug("EAR BROKEN? {a}".format(a=self.fds[ear]))
        """
        Determine if ear is apparently broken
        """
        return self.fds[ear] is None
