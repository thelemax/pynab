import logging

class EarsCustomDrivers():

    def __init__(self):
        self.ears = {"/dev/ear0": "Motor0", "/dev/ear1": "Motor1"}
        self.position = {"Motor0": None, "Motor1": None}
        self._observers = []
        logging.debug("EAR    init")
    
    def open(self, ear):
        logging.debug("EAR    {a} open".format(a=ear))
        self.position[self.ears[ear]] = 0
        return self.ears[ear]
    
    def write(self, ear, cmd, value = None):
        logging.debug("EAR    {a} write cmd={b} value={c}".format(a=ear, b=cmd, c=value))
        if cmd == "+":
            self.__move_forward(ear, value)
        elif cmd == "-":
            self.__move_backward(ear, value)
        elif cmd == ">":
            self.__goto_forward(ear, value)
        elif cmd == "<":
            self.__goto_backward(ear, value)
        elif cmd == "?":
            self.__get_position(ear, 0)
        elif cmd == "!":
            self.__get_position(ear, 1)
        else:
            logging.debug("       -  UNKNOWN")
    
    def close(self, ear):
        logging.debug("EAR    {a} close".format(a=ear))
       
    def __move_forward(self, ear, count):
        self.position[ear] += count
        logging.debug("       -  move_forward")
      
    def __move_backward(self, ear, count):
        self.position[ear] -= count
        logging.debug("       -  move_backward")

    def __goto_forward(self, ear, count):
        self.position[ear] += count
        logging.debug("       -  goto_forward")

    def __goto_backward(self, ear, count):
        self.position[ear] -= count
        logging.debug("       -  goto_backward")
    
    def __get_position(self, ear, run_detection):
        logging.debug("       -  get_position")
        self.__notify(ear)
        
    def read(self, ear):
        logging.debug("EAR    {a} read".format(a=ear))
        return self.position[ear]

    def __notify(self, ear, modifier = None):
        """Alert the observers"""
        for observer in self._observers:
            if modifier != observer:
                observer.update(ear)
                
    def attach(self, observer):
        """If the observer is not in the list,append it into the list"""
        if observer not in self._observers:
            self._observers.append(observer)
  
    def detach(self, observer):
        """Remove the observer from the observer list"""
        try:
            self._observers.remove(observer)
        except ValueError:
            pass
                
                
                
                
                
                