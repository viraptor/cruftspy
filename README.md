# Cruftspy

To check for unnecessary files in a Docker image:

```
$ docker save -o image.tar image_name
$ ./cruftspy.py image.tar

layer 12fa932d.../layer.tar: Bundler cache in root/.bundle/cache (19.6 MB)
layer 12fa932d.../layer.tar: Git repository in usr/local/bundle/ruby/2.7.0/bundler/gems/cypress-rails-54d1c9abe82e/.git/ (0.7 MB)
layer 12fa932d.../layer.tar: Bundle cached gems in usr/local/bundle (132.8 MB)
layer 24735ca3.../layer.tar: Tmp files in tmp/ (0 B)
layer 24735ca3.../layer.tar: Log files in var/log/ (383.0 KB)
layer 2d886302.../layer.tar: Log files in var/log/ (273.6 KB)
layer 496a49c5.../layer.tar: Log files in var/log/ (207.9 KB)
layer 7a94aec5.../layer.tar: Tmp files in tmp/ (2.1 MB)
layer 7a94aec5.../layer.tar: APT lists cache in var/lib/apt/lists/ (0 B)
layer 7a94aec5.../layer.tar: Log files in var/log/ (446.1 KB)
layer 93324a7b.../layer.tar: Tmp files in tmp/ (79.7 KB)
layer 93324a7b.../layer.tar: Log files in var/log/ (322.0 KB)
layer adc9602b.../layer.tar: Tmp files in tmp/ (0.8 KB)
layer adc9602b.../layer.tar: Yarn cache in usr/local/share/.cache/yarn (155.3 MB)
layer ce3cc836.../layer.tar: Log files in var/log/ (0.6 MB)
layer f2d2743e.../layer.tar: Log files in var/log/ (224.0 KB)
Total: 313.0 MB
```

Detected classes of files:
- logs
- temporary files
- git repositories
- package manager caches (apt, apk, dnf, bundle, ...)
