# Cruftspy

To check for unnecessary files in a Docker image:

```
docker save -o image.tar image_name
./cruftspy.py image.tar
```

Detected classes of files:
- logs
- temporary files
- git repositories
- package manager caches (apt, apk, dnf, bundle, ...)
