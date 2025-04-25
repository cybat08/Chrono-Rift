@echo off
echo Cleaning previous builds...
rmdir /s /q build
rmdir /s /q release
mkdir build
cd build
cmake ..
cmake --build .
cd ..
echo Preparing release folder...
mkdir release
copy main.py release\
copy build\*.pyd release\
xcopy assets release\assets\ /E /I /Y
echo Release ready in /release folder!
pause