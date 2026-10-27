from .users import User
from .conversations import Message
from .runtime import Metronome


def main():

    metronome1 = Metronome(1, 400)
    metronome2 = Metronome(0.5, 800)
    metronome3 = Metronome(0.25, 1200)
    
    try:
        metronome1.start()
        metronome2.start()
        metronome3.start()
    except KeyboardInterrupt:
        metronome1.terminate()
        metronome2.terminate()
        metronome3.terminate()

if (__name__ == "__main__"):
    main()
    