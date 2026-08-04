# Risk Register

- R-001 `HIGH`: no pristine predictive test exists in the frozen corpus. Mitigation: require a later locked panel or classify outcome work blocked.
- R-002 `HIGH`: licensed article and price rights do not permit public raw data. Mitigation: hashes, aggregate metrics, schemas, and synthetic fixtures only.
- R-003 `HIGH`: human gold does not yet exist. Mitigation: outcome-blinded packet, explicit pending status, no AI labels presented as human.
- R-004 `MEDIUM`: prior event clusters are one article per cluster and do not validate multi-source clustering. Mitigation: synthetic and later-corpus clustering tests before predictive use.
- R-005 `MEDIUM`: model outputs may contain unsupported interpretation. Mitigation: evidence offsets, field mapping, abstention, and unsupported-field warnings.
- R-006 `MEDIUM`: a public branch can leak local paths or licensed excerpts. Mitigation: automated public-boundary tests before every push.
- R-007 `MEDIUM`: GPU inference can duplicate expensive work. Mitigation: no inference until cache and blob checks pass; one worker; atomic checkpoints.
- R-008 `LOW`: existing unreachable Git blobs may confuse recovery. Mitigation: record them; they are not object corruption and require no destructive cleanup.
