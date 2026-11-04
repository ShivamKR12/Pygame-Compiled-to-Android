# Pygame Compiled to Android (Ludo Realms)

An Android APK compilation setup for a Pygame/Python game using Buildozer, Docker (`kivy/buildozer:latest`), and GitHub Actions.

## Project Structure
- `main.py`: Interactive Pygame application designed for Android touch and desktop screen resolutions.
- `buildozer.spec`: Buildozer configuration specifying package details, Python/Pygame requirements, Android SDK/NDK APIs, and permissions.
- `.github/workflows/build.yml`: GitHub Actions workflow that executes Buildozer with dependency caching to build an `arm64-v8a` debug APK.
- `build.yml`: Local copy of the build specification.
- `p4a-recipes/`: Directory for custom python-for-android recipes if needed.

## Build Caching
The workflow uses `actions/cache@v4` caching:
- `.buildozer`: Local project builds, compiled recipes, and python-for-android distribution.
- `~/.buildozer`: Global Android SDK, Android NDK, and download cache.
- `~/.gradle`: Gradle distributions and wrapper cache.

Cache key is tied to `buildozer.spec` hash (`buildozer-v1-${{ runner.os }}-${{ hashFiles('buildozer.spec') }}`). Subsequent builds restore existing toolchains and distributions, drastically reducing build times from ~12+ minutes to under 2 minutes.

## Building the APK
The GitHub Actions workflow triggers automatically on push to `main` or manually via `workflow_dispatch`. 
Once the build job finishes, the compiled `.apk` is uploaded as an artifact (`LudoRealms-APK`).
