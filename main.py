"""
Ludo Realms - Mobile Android Pygame Test Application
Compatible with Android (via python-for-android/Buildozer) and Desktop.
"""

from game import LudoRealmsGame

def main():
    game = LudoRealmsGame()
    game.run()

if __name__ == '__main__':
    main()
