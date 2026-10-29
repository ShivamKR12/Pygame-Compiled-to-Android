# Pygame Compiled to Android (Ludo Realms)

An Android APK compilation setup for a Pygame/Python game using Buildozer and GitHub Actions.

## Project Structure
- `main.py`: Interactive Pygame application designed for Android touch and desktop screen resolutions.
- `.github/workflows/build.yml`: GitHub Actions workflow that executes Buildozer (`kivy/buildozer:latest`) to build an `arm64-v8a` debug APK.
- `build.yml`: Local copy of the build specification.
- `p4a-recipes/`: Directory for custom python-for-android recipes if needed.

## Building the APK
The GitHub Actions workflow triggers automatically on push to `main` or manually via `workflow_dispatch`. 
Once the build job finishes, the compiled `.apk` is uploaded as an artifact (`LudoRealms-APK`).
