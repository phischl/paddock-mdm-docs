# Getting started

Paddock consists of a control plane, which runs the portal, the admin API and the device API, an audit domain on a
separate host that keeps the WORM audit trail, and an agent on every managed device. The
[architecture](architecture.md) describes how these parts fit together. The portal ships in English and German.

Pick the path that fits what you want to do.

<div class="grid cards" markdown>

-   :material-server-network:{ .lg .middle } **Run Paddock in production**

    ---

    Install the control plane and the audit domain on two Linux hosts with Docker Compose, public TLS, secrets,
    backups and monitoring, then check the installation with `make prod-check`.

    [Production installation](operations/install.md)

-   :material-laptop:{ .lg .middle } **Try it locally**

    ---

    Start the whole stack on one machine with `make up`, seed two test organizations and open the portal at
    `https://admin.paddock.localhost:8443`. For evaluation and development only, never for production.

    [Local development stack](operations/local-dev.md)

-   :material-disc:{ .lg .middle } **Install and enroll devices**

    ---

    Install Ubuntu Desktop 24.04 or 26.04 with full-disk encryption and the Paddock agent; the device enrolls
    itself and escrows its recovery key and LUKS header in Paddock.

    [Installing devices with the Paddock autoinstall](operations/autoinstall.md)

</div>

## Next steps

- Day-to-day operation is covered by the [operations guide](operations/install.md): identity and login, disk
  encryption and recovery, updates and inventory, backup and restore, monitoring, agent releases, and configuration
  as code with [paddockctl](operations/paddockctl.md).
- Auditors start with the [compliance pack](compliance/README.md): the ISO/IEC 27001:2022 mapping, residual risks,
  audit event codes and privacy.
- Revocation (Lock, Destroy, dead man's switch) is behind a feature flag pending second-person review and hardware
  acceptance; see [revocation acceptance](operations/revocation-acceptance.md).
