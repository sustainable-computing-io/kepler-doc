---
title: Kepler Adopters
type: adopters
description: >
  On this page you can see a selection of organisations who self-identified as using Kepler.
---

## Kepler Adopters

Organizations below all are using [Kepler](https://sustainable-computing.io/).

We are happy and proud to have you all as part of our community! 💚

To join this list, please follow [these instructions](contributing.md#kepler-adopters).

### {{ (datasource "adopters").adopters.project }}

{{ strings.TrimSpace (datasource "adopters").adopters.description }}

<!-- markdownlint-disable MD033 -->
<div class="adopters" markdown>
{{ range (coll.Sort "name" (datasource "adopters").adopters.companies) }}
[![{{ .name }}](../fig/{{ if has . "logo" }}{{ .logo }}{{ else }}logos/default.svg{{ end }})<span>{{ .name }}</span>]({{ .url }})
{{- end }}

</div>
<!-- markdownlint-enable MD033 -->
