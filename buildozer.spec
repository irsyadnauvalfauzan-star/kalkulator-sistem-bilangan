[app]
title = Kalkulator Sistem Bilangan
package.name = kalkulatorsistembilangan
package.domain = org.nauval
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.minapi = 23
android.api = 35
android.arch = arm64-v8a
android.entrypoint = org.kivy.android.PythonActivity
