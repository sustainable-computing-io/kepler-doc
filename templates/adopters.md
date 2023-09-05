---
title: Kepler Adopters
type: adopters
description: >
  On this page you can see a selection of organisations who self-identified as using Kepler.
---

# Kepler Adopters

Organisations below all are using Kepler.

To join this list, please follow [these instructions](https://sustainable-computing.io/project/contributing/).

{{- range (datasource "adopters").adopters.companies }}
{{ if has . "logo" }}
<img src="../../data/{{ .logo }}" alt="{{.name}}" width="300px"/>
{{ else }}
<img src="../../data/logos/default.svg" alt="{{.name}}" width="300px"/>
{{ end }}
[{{.name}}]({{.url}})
{{ end }}