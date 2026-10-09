---
title: Linux workstation management
hide:
  - navigation
  - toc
---

<div class="pd-hero" markdown>

<h1 class="pd-hero__title" markdown>
![Paddock](assets/logo/paddock-horizontal-light.svg#only-light){ .pd-hero__logo width="420" height="145" }
![Paddock](assets/logo/paddock-horizontal-dark.svg#only-dark){ .pd-hero__logo width="420" height="145" }
</h1>

<p class="pd-hero__pitch">Open-source management for Linux workstations that keeps local administrator rights with
their users.</p>

[Get started](getting-started.md){ .md-button .md-button--primary }
[Install Paddock](operations/install.md){ .md-button }
[:fontawesome-brands-github: GitHub](https://github.com/phischl/paddock-mdm){ .md-button }

</div>

Paddock distributes signed configuration to Linux laptops and desktops. It manages identity and device login
(Authentik and Himmelblau), sudo rights from permission profiles, a managed local administrator, and disk encryption
with TPM2, a boot PIN and escrowed recovery keys. It handles updates and inventory (Fleet), detects tampering and
keeps a tamper-evident audit trail for ISO 27001. The portal ships in English and German.

<div class="grid cards pd-features" markdown>

-   :material-account-key:{ .lg .middle } **Central management, local admin rights stay**

    ---

    Users keep the administrator rights their organization grants them. Paddock makes those rights explicit,
    reviewable and audited: sudo rights come from permission profiles, and a managed local administrator with a
    rotated, escrowed password lets an organization administrator sign in at any device.

    [Managed local administrator](operations/local-admin.md) ·
    [Device login](operations/device-login.md)

-   :material-file-sign:{ .lg .middle } **Signed configuration, pull-only devices**

    ---

    Devices only ever talk to the server on their own initiative and keep working when it is unreachable. They
    apply only configuration bundles signed by the server. Agent updates are signed and roll out in stages, with
    a self-test and an automatic rollback.

    [Architecture](architecture.md) ·
    [Agent releases](operations/agent-releases.md)

-   :material-shield-check:{ .lg .middle } **Tamper detection and a WORM audit trail**

    ---

    Changes to protected areas on the device are reported as tamper events. Every privileged action is audited
    into WORM storage with Object Lock and a signed daily hash chain. The compliance pack maps Paddock to
    ISO/IEC 27001:2022 Annex A controls.

    [Compliance pack](compliance/README.md) ·
    [ISO 27001 mapping](compliance/iso27001-mapping.md)

-   :material-laptop:{ .lg .middle } **Inventory, vulnerabilities, updates, revocation**

    ---

    Software inventory and vulnerability matching come from Fleet, with Ubuntu's priorities and fixed versions.
    Devices get daily security updates and scheduled regular updates. Revocation (Lock, Destroy, dead man's
    switch) is behind a feature flag pending second-person review and hardware acceptance.

    [Inventory and vulnerabilities](operations/fleet.md) ·
    [Revocation](operations/revocation.md)

</div>

## The portal

<div class="pd-shots" markdown>

<figure markdown>
![The device list of the Paddock portal](assets/screenshots/devices-light.png){ loading=lazy }
<figcaption>Devices: state, last contact, bundle and agent version and disk encryption per device.</figcaption>
</figure>

<figure markdown>
![The audit log of the Paddock portal](assets/screenshots/audit-light.png){ loading=lazy }
<figcaption>Audit log: every privileged action with its outcome and actor.</figcaption>
</figure>

<figure markdown>
![The vulnerability list of the Paddock portal](assets/screenshots/vulnerabilities-light.png){ loading=lazy }
<figcaption>Vulnerabilities: CVEs with Ubuntu's priority, CVSS, affected devices and the fixed version.</figcaption>
</figure>

</div>

## Status and license

Release 0.1.0 is in preparation; see the [changelog](changelog.md). Paddock is open source under the
[MIT license](https://github.com/phischl/paddock-mdm/blob/main/LICENSE). Source code, issues and releases live on
[GitHub](https://github.com/phischl/paddock-mdm).
