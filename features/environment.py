"""Behave environment hooks for running feature files directly from PyCharm."""

import html
import json
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from core.appium_manager import AppiumDriverManager
from core.logger import logger
from core.screenshot_manager import ScreenshotManager, evidence_href
from config.settings import settings
from mobile_pages.login.actions import MobileLoginActions
from mobile_pages.login.assertions import MobileLoginAssertions
from mobile_pages.login.page import MobileLoginPage
from mobile_pages.login.full_advisory import FullAdvisoryActions, FullAdvisoryPage
from mobile_pages.login.short_advisory import ShortAdvisoryActions, ShortAdvisoryPage

try:
    import allure

    ALLURE_AVAILABLE = settings.reporting.enable_allure
except ImportError:
    allure = None
    ALLURE_AVAILABLE = False


def before_all(context):
    """Prepare Behave report folders and in-memory result collection."""
    context.report_started_at = datetime.now()
    context.behave_report_dir = settings.reporting.html_dir / "behave"
    context.behave_json_dir = settings.reporting.allure_dir / "behave-json"
    context.behave_report_dir.mkdir(parents=True, exist_ok=True)
    context.behave_json_dir.mkdir(parents=True, exist_ok=True)
    settings.reporting.screenshot_dir.mkdir(parents=True, exist_ok=True)
    settings.reporting.video_dir.mkdir(parents=True, exist_ok=True)
    settings.reporting.logs_dir.mkdir(parents=True, exist_ok=True)
    context.behave_results = []
    logger.info(f"Behave HTML report directory: {context.behave_report_dir}")
    logger.info(f"Behave JSON report directory: {context.behave_json_dir}")
    if ALLURE_AVAILABLE:
        logger.info(f"Allure results directory: {settings.reporting.allure_dir}")


def _reset_mobile_app(manager: AppiumDriverManager) -> None:
    """Relaunch the app so language-screen scenarios start from a clean state."""
    driver = getattr(manager, "driver", None)
    if not driver:
        return

    app_package = settings.appium.app_package
    try:
        driver.terminate_app(app_package)
        driver.activate_app(app_package)
        logger.info(f"Mobile app relaunched: {app_package}")
    except Exception as exc:
        logger.warning(f"Could not relaunch mobile app '{app_package}': {exc}")


def before_scenario(context, scenario):
    """Create mobile page objects for scenarios tagged with @mobile."""
    if "mobile" not in scenario.effective_tags:
        return

    scenario.started_at = datetime.now()
    scenario.step_results = []
    scenario.video = ""

    context.mobile_driver_manager = AppiumDriverManager.get_instance("behave")
    context.mobile_driver_manager.initialize_driver()
    _reset_mobile_app(context.mobile_driver_manager)

    context.mobile_login_page = MobileLoginPage(context.mobile_driver_manager.driver)
    context.mobile_login_actions = MobileLoginActions(context.mobile_login_page)
    context.mobile_login_assertions = MobileLoginAssertions(context.mobile_login_page)
    context.short_advisory_actions = ShortAdvisoryActions(
        ShortAdvisoryPage(context.mobile_driver_manager.driver)
    )
    context.full_advisory_actions = FullAdvisoryActions(
        FullAdvisoryPage(context.mobile_driver_manager.driver)
    )

    if context.mobile_driver_manager.start_screen_recording():
        scenario.video_recording = True

    logger.info("Behave mobile driver initialized")


def after_step(context, step):
    """Collect step status and capture evidence for each step."""
    result = {
        "keyword": step.keyword.strip(),
        "name": step.name,
        "status": str(step.status),
        "duration": getattr(step, "duration", 0),
        "error": str(step.exception) if getattr(step, "exception", None) else "",
        "screenshot": "",
        "page_source": "",
    }

    manager = getattr(context, "mobile_driver_manager", None)
    driver = getattr(manager, "driver", None)
    is_failed = str(step.status) == "Status.failed"
    should_capture_screenshot = driver and (
        settings.capture_screenshot_each_step
        or (is_failed and settings.capture_screenshot_on_failure)
    )

    if should_capture_screenshot:
        screenshot_manager = ScreenshotManager()
        safe_step_name = _safe_filename(step.name)
        status_prefix = "failure" if is_failed else "step"
        screenshot = screenshot_manager.capture_screenshot(
            driver,
            name=f"{status_prefix}_{safe_step_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
            test_name=step.name,
        )
        result["screenshot"] = str(screenshot) if screenshot else ""

        if is_failed:
            page_source = screenshot_manager.capture_page_source(driver, safe_step_name)
            result["page_source"] = str(page_source) if page_source else ""

        if screenshot and ALLURE_AVAILABLE:
            allure.attach.file(
                str(screenshot),
                name=f"{step.keyword.strip()} {step.name}",
                attachment_type=allure.attachment_type.PNG,
            )

    scenario_step_results = getattr(context.scenario, "step_results", None)
    if scenario_step_results is not None:
        scenario_step_results.append(result)


def after_scenario(context, scenario):
    """Persist scenario evidence and keep the mobile driver open."""
    finished_at = datetime.now()
    started_at = getattr(scenario, "started_at", finished_at)
    video_path = ""

    if "mobile" in scenario.effective_tags:
        manager = getattr(context, "mobile_driver_manager", None)
        if manager and getattr(scenario, "video_recording", False):
            safe_scenario_name = _safe_filename(scenario.name)
            saved_video = manager.stop_screen_recording(
                name=f"{safe_scenario_name}_{finished_at.strftime('%Y%m%d_%H%M%S')}.mp4"
            )
            if saved_video:
                video_path = str(saved_video)
                if ALLURE_AVAILABLE:
                    allure.attach.file(
                        str(saved_video),
                        name=f"{scenario.name} video",
                        attachment_type=allure.attachment_type.MP4,
                    )

    context.behave_results.append(
        {
            "feature": scenario.feature.name,
            "scenario": scenario.name,
            "tags": list(scenario.effective_tags),
            "status": str(scenario.status),
            "started_at": started_at.isoformat(timespec="seconds"),
            "finished_at": finished_at.isoformat(timespec="seconds"),
            "duration_seconds": round((finished_at - started_at).total_seconds(), 3),
            "video": video_path,
            "steps": getattr(scenario, "step_results", []),
        }
    )

    if "mobile" not in scenario.effective_tags:
        return

    manager = getattr(context, "mobile_driver_manager", None)
    if manager:
        logger.info("Behave mobile driver kept open")


def after_all(context):
    """Write lightweight HTML and JSON reports for Behave runs."""
    finished_at = datetime.now()
    results = getattr(context, "behave_results", [])
    summary = {
        "started_at": getattr(context, "report_started_at", finished_at).isoformat(timespec="seconds"),
        "finished_at": finished_at.isoformat(timespec="seconds"),
        "total": len(results),
        "passed": sum(1 for result in results if result["status"] == "Status.passed"),
        "failed": sum(1 for result in results if result["status"] == "Status.failed"),
        "skipped": sum(1 for result in results if result["status"] == "Status.skipped"),
        "results": results,
    }

    timestamp = finished_at.strftime("%Y%m%d_%H%M%S")
    json_path = context.behave_json_dir / f"behave_report_{timestamp}.json"
    html_path = context.behave_report_dir / f"behave_report_{timestamp}.html"
    latest_html_path = context.behave_report_dir / "latest.html"

    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    report_html = _build_html_report(summary, context.behave_report_dir)
    html_path.write_text(report_html, encoding="utf-8")
    latest_html_path.write_text(report_html, encoding="utf-8")

    logger.info(f"Behave JSON report created: {json_path}")
    logger.info(f"Behave HTML report created: {html_path}")
    logger.info(f"Latest Behave HTML report: {latest_html_path}")
    if not os.getenv("CI"):
        _generate_and_open_allure_report()
    if ALLURE_AVAILABLE:
        logger.info(
            "Allure results are available. Generate the report with: "
            f"allure serve {settings.reporting.allure_dir}"
        )


def _generate_and_open_allure_report() -> None:
    """Generate a persistent Allure report and open it in the default browser."""
    allure_cli = _find_allure_command()
    report_dir = settings.reporting.allure_dir.parent / "allure-report"

    if not allure_cli:
        logger.warning(
            "Allure CLI and npx were not found. Install the Allure command-line tool to "
            "generate and open the permanent Allure report. No fallback HTML report will be opened."
        )
        return

    try:
        report_dir.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [
                *allure_cli,
                "generate",
                str(settings.reporting.allure_dir),
                "-o",
                str(report_dir),
                "--clean",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        logger.info(f"Permanent Allure report generated: {report_dir}")

        # `allure open` serves the report correctly and opens the default browser.
        subprocess.Popen(
            [*allure_cli, "open", str(report_dir)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
        )
        logger.info("Permanent Allure report opened in the default browser")
    except (OSError, subprocess.CalledProcessError) as exc:
        logger.warning(f"Could not generate or open the Allure report: {exc}")


def _find_allure_command() -> list[str] | None:
    """Find the standalone Allure CLI or an npx-based Allure CLI command."""
    allure_cli = shutil.which("allure")
    if allure_cli:
        return [allure_cli]

    npx_cli = shutil.which("npx.cmd") or shutil.which("npx")
    if npx_cli:
        return [npx_cli, "--yes", "allure-commandline"]

    return None


def _safe_filename(value: str) -> str:
    """Return a filesystem-safe filename fragment."""
    safe = "".join(char if char.isalnum() else "_" for char in value.lower())
    return "_".join(part for part in safe.split("_") if part)[:80]


def _build_html_report(summary: dict, report_dir: Path) -> str:
    """Build a simple self-contained Behave HTML report."""
    rows = []
    for result in summary["results"]:
        step_rows = "".join(
            f"""
            <tr>
              <td>{html.escape(step["keyword"])}</td>
              <td>{html.escape(step["name"])}</td>
              <td class="{_status_class(step["status"])}">{html.escape(step["status"].replace("Status.", ""))}</td>
              <td>{step["duration"]:.3f}s</td>
              <td>{_evidence_links(report_dir, step)}</td>
            </tr>
            """
            for step in result["steps"]
        )
        scenario_video = _video_link(report_dir, result.get("video", ""))
        rows.append(
            f"""
            <section class="scenario">
              <h2>{html.escape(result["scenario"])}</h2>
              <p>
                <span class="{_status_class(result["status"])}">{html.escape(result["status"].replace("Status.", ""))}</span>
                · {html.escape(result["feature"])}
                · {result["duration_seconds"]:.3f}s
              </p>
              {scenario_video}
              <table>
                <thead>
                  <tr><th>Keyword</th><th>Step</th><th>Status</th><th>Duration</th><th>Evidence</th></tr>
                </thead>
                <tbody>{step_rows}</tbody>
              </table>
            </section>
            """
        )

    total = summary["total"]
    passed = summary["passed"]
    failed = summary["failed"]
    skipped = summary["skipped"]
    summary_cards = f"""
  <div class="summary">
    <div class="card">Total<br><strong>{total}</strong></div>
    <div class="card passed">Passed<br><strong>{passed}</strong></div>
    <div class="card failed">Failed<br><strong>{failed}</strong></div>
    <div class="card skipped">Skipped<br><strong>{skipped}</strong></div>
  </div>
"""

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Behave Mobile Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; color: #1f2937; }}
    .summary {{ display: flex; gap: 12px; margin: 16px 0 24px; }}
    .card {{ border: 1px solid #d1d5db; border-radius: 8px; padding: 12px 16px; min-width: 100px; }}
    .passed {{ color: #047857; font-weight: 700; }}
    .failed {{ color: #b91c1c; font-weight: 700; }}
    .skipped {{ color: #92400e; font-weight: 700; }}
    .scenario {{ border-top: 1px solid #e5e7eb; padding-top: 16px; margin-top: 16px; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #e5e7eb; padding: 8px; text-align: left; vertical-align: top; }}
    th {{ background: #f9fafb; }}
    a {{ color: #2563eb; }}
    .thumb {{ display: block; margin-top: 6px; max-width: 220px; border: 1px solid #e5e7eb; border-radius: 4px; }}
  </style>
</head>
<body>
  <h1>Behave Mobile Report</h1>
  <p>Started: {html.escape(summary["started_at"])} · Finished: {html.escape(summary["finished_at"])}</p>
  {summary_cards}
  {"".join(rows)}
</body>
</html>
"""


def _status_class(status: str) -> str:
    """Map Behave status strings to CSS classes."""
    return status.replace("Status.", "")


def _video_link(report_dir: Path, video_path: str) -> str:
    """Build scenario video link for the HTML report."""
    if not video_path:
        return ""
    href = evidence_href(report_dir, Path(video_path))
    return f'<p><a href="{html.escape(href)}">scenario video</a></p>'


def _evidence_links(report_dir: Path, step: dict) -> str:
    """Build screenshot/page-source links for a step."""
    links = []
    if step["screenshot"]:
        screenshot_path = Path(step["screenshot"])
        href = evidence_href(report_dir, screenshot_path)
        links.append(f'<a href="{html.escape(href)}">screenshot</a>')
        if screenshot_path.exists():
            links.append(
                f'<a href="{html.escape(href)}"><img class="thumb" src="{html.escape(href)}" alt="screenshot"></a>'
            )
    if step["page_source"]:
        href = evidence_href(report_dir, Path(step["page_source"]))
        links.append(f'<a href="{html.escape(href)}">page source</a>')
    return "<br>".join(links)
