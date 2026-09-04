"""The contracts are the platform. If these break, something important changed."""

import yaml

from core.contracts import PackManifest


def test_template_pack_validates() -> None:
    with open("packs/_template/pack.yaml", encoding="utf-8") as fh:
        PackManifest.model_validate(yaml.safe_load(fh))


def test_a_pack_cannot_opt_out_of_never_acts() -> None:
    with open("packs/_template/pack.yaml", encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)
    raw["guardrails"]["never_acts"] = False
    try:
        PackManifest.model_validate(raw)
    except Exception:
        return
    raise AssertionError("never_acts=False must be rejected by the type, not by review")


def test_generated_files_are_in_sync() -> None:
    """The register headers and the extraction models are generated from pack.yaml.

    If this fails, someone edited a pack and did not run `python -m packs.build`. That is
    exactly the drift this whole mechanism exists to prevent, so it is a hard failure.
    """
    import subprocess
    import sys

    r = subprocess.run(
        [sys.executable, "-m", "packs.build", "--check"], capture_output=True, text=True
    )
    assert r.returncode == 0, r.stdout + r.stderr
