@echo off
echo Building hybrid_game_v2...
mkdir build
cd build
cmake ..
cmake --build .
echo Done building!
cd ..
echo Running game...
python main.py
pause