@echo off
echo Cleaning previous builds...
rmdir /s /q build
echo Building hybrid_game_v2 fresh...
mkdir build
cd build
cmake ..
cmake --build .
cd ..
echo Done rebuilding!
pause