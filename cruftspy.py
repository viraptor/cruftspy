#!/usr/bin/env python3

# Copyright 2022 Stanislaw Pitucha
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import tarfile
import sys
import os
import re
from typing import List, Optional, Tuple

already_seen = set()

def classify_logs(layer: str, fname: str) -> Optional[Tuple[str, str]]:
  for path in ('var/log/',):
    if fname.startswith(path):
      seen_key = (layer, 'classify_logs', path)
      if seen_key not in already_seen:
        already_seen.add(seen_key)
        return ("Log files", path)
  return None

def classify_tmp(layer: str, fname: str) -> Optional[Tuple[str, str]]:
  for path in ('tmp/', 'var/tmp/'):
    if fname.startswith(path):
      seen_key = (layer, 'classify_tmp', path)
      if seen_key not in already_seen:
        already_seen.add(seen_key)
        return ("Tmp files", path)
  return None

def classify_apk_cache(layer: str, fname: str) -> Optional[Tuple[str, str]]:
  for path in ('var/cache/apk/',):
    if fname.startswith(path):
      seen_key = (layer, 'classify_apk_cache', path)
      if seen_key not in already_seen:
        already_seen.add(seen_key)
        return ("APK cache", path)
  return None

def classify_apt_cache(layer: str, fname: str) -> Optional[Tuple[str, str]]:
  for path in ('var/lib/apt/lists/',):
    if fname.startswith(path):
      seen_key = (layer, 'classify_apt_cache', path)
      if seen_key not in already_seen:
        already_seen.add(seen_key)
        return ("APT lists cache", path)
  return None

def classify_dnf_cache(layer: str, fname: str) -> Optional[Tuple[str, str]]:
  for path in ('var/cache/dnf/', 'var/lib/dnf/repos/'):
    if fname.startswith(path):
      seen_key = (layer, 'classify_dnf_cache', path)
      if seen_key not in already_seen:
        already_seen.add(seen_key)
        return ("DNF cache", path)
  return None

def classify_bundler_cache(layer: str, fname: str) -> Optional[Tuple[str, str]]:
  if '.bundle/cache' in fname:
    base_path = fname[:(fname.index('.bundle/cache'))] or '(root)'
    base_path += '.bundle/cache'
    seen_key = (layer, 'classify_bundler_cache', base_path)
    if seen_key not in already_seen:
      already_seen.add(seen_key)
      return ("Bundler cache", base_path)
  return None

def classify_sprockets_cache(layer: str, fname: str) -> Optional[Tuple[str, str]]:
  if 'cache/assets/sprockets/' in fname:
    base_path = fname[:(fname.index('cache/assets/sprockets/'))] or '(root)'
    base_path += 'cache/assets/sprockets/'
    seen_key = (layer, 'classify_sprockets_cache', base_path)
    if seen_key not in already_seen:
      already_seen.add(seen_key)
      return ("Sprockets cache", base_path)
  return None

def classify_yarn_cache(layer: str, fname: str) -> Optional[Tuple[str, str]]:
  if '.cache/yarn' in fname:
    base_path = fname[:(fname.index('.cache/yarn'))] or '(root)'
    base_path += '.cache/yarn'
    seen_key = (layer, 'classify_yarn_cache', base_path)
    if seen_key not in already_seen:
      already_seen.add(seen_key)
      return ("Yarn cache", base_path)
  return None

def classify_pip_cache(layer: str, fname: str) -> Optional[Tuple[str, str]]:
  if '.cache/pip' in fname:
    base_path = fname[:(fname.index('.cache/pip'))] or '(root)'
    base_path += '.cache/pip'
    seen_key = (layer, 'classify_pip_cache', base_path)
    if seen_key not in already_seen:
      already_seen.add(seen_key)
      return ("Pip cache", base_path)
  return None

def classify_bundle_cache(layer: str, fname: str) -> Optional[Tuple[str, str]]:
  m = re.search('/ruby/[^/]*/cache/[^/]*\.gem', fname)
  if m:
    base_path = fname[:m.start(0)] or '(root)'
    seen_key = (layer, 'classify_bundle_cache', base_path)
    if seen_key not in already_seen:
      already_seen.add(seen_key)
      return ("Bundle cached gems", base_path)
  return None

def classify_git_repo(layer: str, fname: str) -> Optional[Tuple[str, str]]:
  if '.git/objects/' in fname:
    base_path = fname[:(fname.index('.git/objects/'))] or '(root)'
    base_path += '.git/'
    seen_key = (layer, 'classify_git_repo', base_path)
    if seen_key not in already_seen:
      already_seen.add(seen_key)
      return ("Git repository", base_path)
  return None

def classify(layer: str, fname: str) -> Optional[Tuple[str, str]]:
  for f in (
      classify_logs,
      classify_tmp,
      classify_bundler_cache,
      classify_bundle_cache,
      classify_yarn_cache,
      classify_pip_cache,
      classify_git_repo,
      classify_apk_cache,
      classify_apt_cache,
      classify_dnf_cache,
      classify_sprockets_cache):
    r = f(layer, fname)
    if r:
      return r
  return None

mags = ['B', 'KB', 'MB', 'GB', 'TB']
def calc_size(tf: tarfile.TarFile, path: str) -> int:
  total = 0
  for ti_entry in tf.getmembers():
    if ti_entry.name.startswith(path):
      total += ti_entry.size
  return total

def format_size(size: float) -> str:
  mag = 0
  while size > 512:
    mag += 1
    size /= 1024
  if mag == 0:
    return f"{size} {mags[mag]}"
  else:
    return f"{size:.1f} {mags[mag]}"

def main(args: List[str]) -> None:
  if len(args) < 2:
    print(f"usage: {args[0]} docker-image.tar")
    return

  total_cruft = 0
  with tarfile.open(args[1]) as tf:
    layer_tars = [x for x in tf.getnames() if x.endswith('/layer.tar')]

    for layer in layer_tars:
      if 'TEST' in os.environ:
        print(f"layer: {layer}")

      with tarfile.TarFile(fileobj=tf.extractfile(layer)) as layer_tf:
        if 'TEST' in os.environ:
          for fname in layer_tf.getnames():
            print(fname)
        issues = [x for x in (classify(layer, fname) for fname in layer_tf.getnames()) if x]
        for (issue_type, path) in issues:
          size = calc_size(layer_tf, path)
          total_cruft += size
          print(f"layer {layer}: {issue_type} in {path} ({format_size(size)})")

  print(f"Total: {format_size(total_cruft)}")

if __name__ == "__main__":
  main(sys.argv)
