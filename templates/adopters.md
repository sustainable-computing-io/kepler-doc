---
title: Kepler Adopters
type: adopters
description: >
  On this page you can see a selection of organisations who self-identified as using Kepler.
---

## Kepler Adopters

Organizations below all are using Kepler.

To join this list, please follow [these instructions](https://sustainable-computing.io/project/contributing/).

{{- range (datasource "adopters").adopters.companies }}
{{ if has . "logo" }}
![{{.name}}](../fig/{{ .logo }})
{{ else }}
![{{.name}}](../fig/logos/default.svg)
{{ end }}
[{{.name}}]({{.url}})
{{ end }}
