"""Read-only file preflight. Does not open SF, deserialize or prove crawl validity."""
import argparse
import hashlib
import json
from pathlib import Path
import sys


def inspect_file(path):
    source = Path(path).expanduser()
    result = {"schema_version": 1, "route": "saved_crawl", "preflight_state": "failed",
              "load_state": "not_attempted", "source": {"path": str(source.absolute())},
              "error": None, "next_action": None}

    def fail(code, message, action):
        result.update(error={"code": code, "message": message}, next_action=action)
        return result

    try:
        source = source.resolve(strict=True)
        result["source"]["path"] = str(source)
        if not source.is_file():
            return fail("not_a_file", "Input is not a regular saved file", "Provide a portable .seospider file or readable exports")
        if source.suffix.lower() != ".seospider":
            code = "configuration_not_crawl" if source.suffix.lower() == ".seospiderconfig" else "unsupported_file_type"
            return fail(code, "Expected a saved .seospider crawl", "Provide the saved crawl; do not rename configuration or database files")
        before = source.stat()
        if before.st_size == 0:
            return fail("empty_file", "Saved file is empty", "Provide a completed portable save or exports")
        digest = hashlib.sha256()
        with source.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        after = source.stat()
        if (before.st_size, before.st_mtime_ns, before.st_ino) != (after.st_size, after.st_mtime_ns, after.st_ino):
            return fail("file_changed", "Input changed during reading", "Wait for a completed save and supply the stable file")
        result["source"].update(size_bytes=after.st_size, mtime_ns=after.st_mtime_ns, sha256=digest.hexdigest())
        result.update(preflight_state="file_ready_unverified", next_action="Reuse matching exports or open once through a supported SF saved-crawl reader; validate site and fields")
        return result
    except FileNotFoundError as exc:
        return fail("file_not_found", str(exc), "Correct the file path on the executing host")
    except PermissionError as exc:
        return fail("file_unreadable", str(exc), "Provide read access or an accessible copy")
    except (OSError, RuntimeError) as exc:
        return fail("file_read_error", str(exc), "Resolve the file error or provide readable exports")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--output", type=Path, help="Optional new JSON record; existing files are never overwritten")
    args = parser.parse_args()
    result = inspect_file(args.file)
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        try:
            with args.output.open("x", encoding="utf-8") as stream:
                stream.write(payload + "\n")
        except OSError as exc:
            print(json.dumps({"error": {"code": "output_write_error", "message": str(exc)}}, ensure_ascii=False), file=sys.stderr)
            return 2
    print(payload)
    return 0 if result["error"] is None else 1


if __name__ == "__main__":
    raise SystemExit(main())
