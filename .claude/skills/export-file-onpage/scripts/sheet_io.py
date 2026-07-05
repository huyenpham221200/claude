#!/usr/bin/env python3
"""
sheet_io.py - Doc/ghi Google Sheets qua Sheets API v4. Day la lop I/O mong:
logic "hang nao khop checklist nao" do Claude tu doc du lieu va suy luan,
script chi lo phan goi API thuc.

Usage:
    python sheet_io.py resolve-tab <sheet_url_or_id> --gid <gid>
    python sheet_io.py read <sheet_url_or_id> --range "A1:Z100" [--gid <gid>]
    python sheet_io.py write <sheet_url_or_id> --range "L7" --values '[["Check lan 2"]]' [--gid <gid>]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).parent))
from auth import get_credentials  # noqa: E402

from googleapiclient.discovery import build  # noqa: E402


def extract_spreadsheet_id(raw: str) -> str:
    m = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", raw)
    return m.group(1) if m else raw.strip()


def extract_gid(raw: str) -> str | None:
    m = re.search(r"[?#&]gid=(\d+)", raw)
    return m.group(1) if m else None


def get_service():
    creds = get_credentials()
    return build("sheets", "v4", credentials=creds)


def resolve_sheet_name(service, spreadsheet_id: str, gid: str) -> str:
    meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    for sheet in meta["sheets"]:
        props = sheet["properties"]
        if str(props["sheetId"]) == str(gid):
            return props["title"]
    raise ValueError(f"Khong tim thay tab voi gid={gid} trong spreadsheet {spreadsheet_id}")


def build_range(service, spreadsheet_id: str, a1_range: str, gid: str | None) -> str:
    if gid:
        sheet_name = resolve_sheet_name(service, spreadsheet_id, gid)
        return f"'{sheet_name}'!{a1_range}"
    return a1_range


def cmd_resolve_tab(args):
    ssid = extract_spreadsheet_id(args.sheet)
    gid = args.gid or extract_gid(args.sheet)
    if not gid:
        print("ERROR: khong tim thay gid (truyen --gid hoac url co #gid=...)", file=sys.stderr)
        sys.exit(1)
    service = get_service()
    name = resolve_sheet_name(service, ssid, gid)
    print(json.dumps({"spreadsheet_id": ssid, "gid": gid, "sheet_name": name}, ensure_ascii=False))


def cmd_read(args):
    ssid = extract_spreadsheet_id(args.sheet)
    gid = args.gid or extract_gid(args.sheet)
    service = get_service()
    full_range = build_range(service, ssid, args.range, gid)
    result = service.spreadsheets().values().get(
        spreadsheetId=ssid, range=full_range
    ).execute()
    values = result.get("values", [])
    print(json.dumps(values, ensure_ascii=False))


def cmd_write(args):
    ssid = extract_spreadsheet_id(args.sheet)
    gid = args.gid or extract_gid(args.sheet)
    values = json.loads(args.values)
    service = get_service()
    full_range = build_range(service, ssid, args.range, gid)
    body = {"values": values}
    result = service.spreadsheets().values().update(
        spreadsheetId=ssid,
        range=full_range,
        valueInputOption="USER_ENTERED",
        body=body,
    ).execute()
    print(json.dumps({
        "updatedRange": result.get("updatedRange"),
        "updatedCells": result.get("updatedCells"),
    }, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="sheet_io - doc/ghi Google Sheets")
    sub = parser.add_subparsers(dest="command", required=True)

    p_resolve = sub.add_parser("resolve-tab")
    p_resolve.add_argument("sheet")
    p_resolve.add_argument("--gid")

    p_read = sub.add_parser("read")
    p_read.add_argument("sheet")
    p_read.add_argument("--range", required=True)
    p_read.add_argument("--gid")

    p_write = sub.add_parser("write")
    p_write.add_argument("sheet")
    p_write.add_argument("--range", required=True)
    p_write.add_argument("--values", required=True, help="JSON 2D array, vd: '[[\"a\",\"b\"]]'")
    p_write.add_argument("--gid")

    args = parser.parse_args()
    {
        "resolve-tab": cmd_resolve_tab,
        "read": cmd_read,
        "write": cmd_write,
    }[args.command](args)


if __name__ == "__main__":
    main()
